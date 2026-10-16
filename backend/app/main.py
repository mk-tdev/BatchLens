import asyncio, csv, hashlib, hmac, html, io, json, os, secrets, time, uuid
from pathlib import Path
from typing import Literal
from urllib.parse import urlparse
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict, Field
from . import domain, ai, investigator, operations, copilot
from .storage import make_store

ROOT=Path(__file__).resolve().parents[2]
ASSETS=ROOT/'backend/scenarios/bottles_v1/assets'
ai.mode()  # Fail closed on Cloud Run when live inference is not configured.
store=make_store()
app=FastAPI(title='BatchLens API', version='0.1.0')

class Command(BaseModel):
    model_config=ConfigDict(extra='forbid')
    request_id: str = Field(min_length=8,max_length=80)
    expected_revision: int = Field(ge=0)
    action: Literal['confirm_baseline','add_evidence','review_slip','select_lot','create_proposal','reject_candidate','correct_candidate']
    value: str | None = Field(default=None,max_length=50)
    note: str = Field(default='',max_length=1000)

class ExtractionRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    artifact_id: Literal['E2','E3','E6','E7']
    request_id: str=Field(min_length=8,max_length=80)

@app.middleware('http')
async def protections(request: Request, call_next):
    if request.method in {'POST','PUT','DELETE','PATCH'}:
        origin=request.headers.get('origin')
        allowed = set(os.getenv('ALLOWED_ORIGINS', 'http://127.0.0.1:5173,http://127.0.0.1:5174' if not os.getenv('K_SERVICE') else '').split(','))
        if origin and urlparse(origin).netloc!=request.headers.get('host') and origin not in allowed:
            return Response('Cross-origin mutations are not allowed.',status_code=403)
        if request.headers.get('x-batchlens-client')!='workspace':
            return Response('Missing request verification header.',status_code=403)
        if int(request.headers.get('content-length','0'))>32768:
            return Response('Request is too large.',status_code=413)
    response=await call_next(request)
    response.headers['X-Content-Type-Options']='nosniff'
    response.headers['Referrer-Policy']='same-origin'
    if request.url.path.startswith('/api'): response.headers['Cache-Control']='no-store'
    return response

def check(case,request):
    token=request.cookies.get('batchlens_owner','')
    if not case or not hmac.compare_digest(case['owner_hash'],hashlib.sha256(token.encode()).hexdigest()): raise HTTPException(404,'Investigation not found.')
    if case['expires_at']<time.time(): raise HTTPException(410,'This investigation has expired. Start a new case.')
    return case

def read(id,request): return check(store.get(id),request)

@app.get('/api/health')
def health(): return {'status':'ok','storage':os.getenv('STORAGE_BACKEND','sqlite'),'ai_mode':ai.mode(),'model':os.getenv('MODEL_ID')}

@app.post('/api/investigations')
def create(request:Request,response:Response):
    token=request.cookies.get('batchlens_owner') or secrets.token_urlsafe(32)
    case=domain.new_case(hashlib.sha256(token.encode()).hexdigest())
    domain.event(case,'Investigation opened','Original synthetic case · Northstar Bottles')
    store.create(case)
    response.set_cookie('batchlens_owner',token,httponly=True,secure=os.getenv('COOKIE_SECURE','false')=='true',samesite='strict',max_age=86400)
    return domain.public(case,ai.mode())

@app.get('/api/investigations/{id}')
def get_case(id:str,request:Request): return domain.public(read(id,request),ai.mode())

@app.get('/api/investigations/{id}/artifacts/{artifact_id}')
def source(id:str,artifact_id:str,request:Request):
    case=read(id,request)
    artifact=next((a for a in domain.ARTIFACTS if a['id']==artifact_id),None)
    if not artifact or (artifact_id=='E7' and not case['added_clear_slip']): raise HTTPException(404,'Artifact not found.')
    return FileResponse(ASSETS/artifact['file'],headers={'Cache-Control':'no-store'})

@app.post('/api/investigations/{id}/commands')
def command(id:str,body:Command,request:Request):
    fingerprint=hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    def apply(case):
        check(case,request)
        prior=case['requests'].get(body.request_id)
        if prior:
            if prior['hash']!=fingerprint: raise HTTPException(409,'Request ID already used with a different body.')
            return prior['result']
        if investigator.active(case): raise HTTPException(409,'Pip is investigating. Wait for the journal to finish before reviewing decisions.')
        if body.expected_revision!=case['revision']: raise HTTPException(409,{'message':'The case changed in another tab. Your view has been refreshed.','state':domain.public(case,ai.mode())})
        if len(case['requests'])>=24: raise HTTPException(429,'Case action limit reached. Start a new case.')
        if body.action=='confirm_baseline':
            if case['baseline']: raise HTTPException(422,'Baseline already confirmed.')
            if not all(case['candidates'].get(k,{}).get('value') and case['candidates'][k].get('status')!='rejected' for k in ['E2','E3']): raise HTTPException(422,'Extract and review the label and supplier report first.')
            if case['candidates']['E2']['value']!='B101' or case['candidates']['E3']['value']!='CAP-17': raise HTTPException(422,'Extracted values conflict with this case. Inspect the sources before proceeding.')
            case['baseline']=True; case['suspect_lot']='CAP-17'
            for key in ['E2','E3']: case['candidates'][key]['status']='confirmed'
            domain.event(case,'Baseline evidence confirmed','Label B101, suspect CAP-17, production and shipment records reviewed. '+body.note)
        elif body.action=='add_evidence':
            if not case['baseline']: raise HTTPException(422,'Review baseline evidence first.')
            if not case['added_clear_slip']:
                case['added_clear_slip']=True
                domain.event(case,'New source added','E7 · Recovered packing slip. Extraction and review still required.')
        elif body.action=='review_slip':
            if not case['baseline']: raise HTTPException(422,'Review baseline evidence before confirming shipment mappings.')
            candidate=case['candidates'].get('E7')
            if not case['added_clear_slip'] or not candidate or candidate.get('status')=='rejected': raise HTTPException(422,'Extract the recovered slip first.')
            if body.value not in domain.BATCHES: raise HTTPException(422,'Choose a known batch identifier.')
            if body.value!=candidate['value'] and not body.note.strip(): raise HTTPException(422,'Explain the correction before confirming.')
            case['resolved_batch']=body.value; candidate['status']='confirmed'; candidate['reviewed_value']=body.value
            domain.event(case,'Shipment S4 relationship confirmed',f'S4 → {body.value} · E7. '+body.note)
        elif body.action=='select_lot':
            if not case['baseline'] or body.value not in {'CAP-17','CAP-18'}: raise HTTPException(422,'Review baseline and choose a known component lot.')
            if not body.note.strip(): raise HTTPException(422,'Record a reason for changing the investigation hypothesis.')
            case['suspect_lot']=body.value
            domain.event(case,'Investigation hypothesis changed',body.value+' · '+body.note)
        elif body.action=='correct_candidate':
            artifact_id,_,value=(body.value or '').partition(':')
            candidate=case['candidates'].get(artifact_id)
            if not candidate or candidate.get('status')=='confirmed': raise HTTPException(422,'Only unconfirmed candidates can be corrected.')
            allowed={'CAP-17','CAP-18'} if artifact_id=='E3' else set(domain.BATCHES)
            if value not in allowed or not body.note.strip(): raise HTTPException(422,'Choose a valid identifier and explain the source-backed correction.')
            candidate['original_value']=candidate.get('original_value',candidate['value'])
            candidate['value']=value; candidate['review_note']=body.note; candidate['status']='pending'
            candidate['label']='Reviewer-corrected candidate · '+candidate['provider']+' extraction'
            domain.event(case,'Candidate corrected',artifact_id+' → '+value+' · '+body.note)
        elif body.action=='reject_candidate':
            candidate=case['candidates'].get(body.value)
            if not candidate: raise HTTPException(422,'Candidate not found.')
            if candidate.get('status')=='confirmed': raise HTTPException(422,'A confirmed relationship cannot be discarded by rejecting a candidate.')
            candidate['status']='rejected'
            domain.event(case,'Candidate rejected',f'{body.value} · '+body.note)
        elif body.action=='create_proposal':
            if not case['baseline']: raise HTTPException(422,'Review baseline evidence before preparing a proposal.')
            if len(case['proposals'])>=3: raise HTTPException(429,'Three proposal snapshots are available per demo case.')
            snap=domain.scope(case)
            proposal={'id':str(uuid.uuid4()),'created_at':domain.now(),'revision':case['revision'],'scope':snap,'note':body.note,'suspect_lot':case['suspect_lot'],'sources':[a for a in domain.ARTIFACTS if a['id']!='E7' or case['added_clear_slip']],'candidate_snapshot':json.loads(json.dumps(case['candidates'])),'missions_snapshot':json.loads(json.dumps(case.get('missions',[]))),'actions_approval':case.get('actions_approval'),'comparison':(case.get('investigator') or {}).get('comparison'),'investigator_report':json.loads(json.dumps((case.get('investigator') or {}).get('report')))}
            case['proposals'].append(proposal)
            domain.event(case,'Inspection proposal saved',f"{snap['totals']['inspection']:,} units · reviewed revision {case['revision']}")
        case['revision']+=1
        result=domain.public(case,ai.mode())
        case['requests'][body.request_id]={'hash':fingerprint,'result':result}
        return result
    return store.mutate(id,apply)

@app.post('/api/investigations/{id}/extractions')
async def extract(id:str,body:ExtractionRequest,request:Request):
    job_id=body.request_id
    def reserve(case):
        check(case,request)
        if investigator.active(case): raise HTTPException(409,'Pip is reading the evidence. Wait for the investigation to finish.')
        if body.artifact_id=='E7' and not case['added_clear_slip']: raise HTTPException(422,'Add the recovered slip first.')
        prior=case['jobs'].get(job_id)
        if prior:
            if prior['artifact_id']!=body.artifact_id: raise HTTPException(409,'Request ID is already used for another artifact.')
            if prior['status']=='complete': return prior['result']
            if prior['lease']>time.time() and prior['status']=='running': raise HTTPException(409,'This extraction is already running.')
        if any(j['status']=='running' and j['lease']>time.time() for j in case['jobs'].values()): raise HTTPException(409,'Another extraction is running. Try again shortly.')
        if case['candidates'].get(body.artifact_id,{}).get('status')=='confirmed': raise HTTPException(422,'This source has already been confirmed.')
        if case['model_attempts']>=8: raise HTTPException(429,'The eight-attempt case limit has been reached.')
        case['model_attempts']+=1
        case['jobs'][job_id]={'artifact_id':body.artifact_id,'status':'running','lease':time.time()+90}
        return None
    previous=store.mutate(id,reserve)
    if previous: return previous
    artifact=next(a for a in domain.ARTIFACTS if a['id']==body.artifact_id)
    try:
        if ai.mode()=='gemini': store.reserve_model_budget()
        candidate=await asyncio.wait_for(ai.extract(body.artifact_id,ASSETS/artifact['file']),timeout=60)
    except Exception as exc:
        def fail(case):
            case['jobs'][job_id]['status']='failed'
        store.mutate(id,fail)
        raise HTTPException(502,'Extraction could not finish. Check model configuration or try again. No graph facts were changed.') from exc
    def commit(case):
        check(case,request)
        job=case['jobs'][job_id]
        if job['status']!='running' or job['lease']<time.time(): raise HTTPException(409,'Extraction lease expired. Retry extraction.')
        existing=case['candidates'].get(body.artifact_id)
        if existing and existing.get('status')=='confirmed': raise HTTPException(409,'This evidence is already confirmed; the result was not overwritten.')
        case['candidates'][body.artifact_id]={**candidate,'status':'pending'}
        domain.event(case,'Source extracted',body.artifact_id+' · '+candidate['label']+' · review required')
        case['revision']+=1
        job['status']='complete'
        result=domain.public(case,ai.mode()); job['result']=result
        return result
    return store.mutate(id,commit)

class InvestigatorRequest(BaseModel):
    model_config=ConfigDict(extra='forbid')
    request_id: str=Field(min_length=8,max_length=80)

@app.post('/api/investigations/{id}/investigator')
async def investigate(id:str,body:InvestigatorRequest,request:Request):
    read(id,request)
    if ai.mode()!='gemini': raise HTTPException(503,'Pip requires real Gemini. Configure Vertex AI to run an investigation; no authored agent fallback is used.')
    def reserve(case):
        check(case,request)
        if body.request_id in case.get('agent_run_ids',[]):
            return False
        if investigator.active(case): raise HTTPException(409,'Pip is already investigating this case.')
        if any(j['status']=='running' and j['lease']>time.time() for j in case['jobs'].values()): raise HTTPException(409,'Wait for the current source scan.')
        if len(case.get('agent_run_ids',[]))>=2: raise HTTPException(429,'Two investigator runs are available per case.')
        if case.get('investigator'): case.setdefault('past_investigations',[]).append(case['investigator'])
        case.setdefault('agent_run_ids',[]).append(body.request_id)
        case['investigator']={'id':body.request_id,'status':'running','lease':time.time()+110,'started_at':domain.now(),'journal':[],'report':None,'model':os.environ.get('MODEL_ID'),'provider':'gemini'}
        case['revision']+=1
        return True
    if not store.mutate(id,reserve): return domain.public(read(id,request),ai.mode())
    runner=investigator.Runner(store,id,body.request_id,lambda c:check(c,request))
    status,message='awaiting_review','Findings ready for human review.'
    try:
        await asyncio.wait_for(runner.run(),timeout=95)
    except Exception as exc:
        status='incomplete';message='Investigation stopped before completion. Partial tool results remain available; no decisions were approved.'
        # Do not expose provider exception bodies or credentials in client responses.
        import logging
        logging.getLogger(__name__).warning('Investigator stopped: %s',type(exc).__name__)
    def finish(case):
        check(case,request)
        if case.get('investigator',{}).get('id')==body.request_id:
            case['investigator'].update(status=status,message=message,finished_at=domain.now(),lease=0)
            case['revision']+=1
            domain.event(case,'Pip investigation '+status.replace('_',' '),message)
        return domain.public(case,ai.mode())
    return store.mutate(id,finish)

@app.post('/api/investigations/{id}/missions')
def mission_command(id:str,body:operations.MissionCommand,request:Request):
    fingerprint=hashlib.sha256(body.model_dump_json().encode()).hexdigest()
    def apply(case):
        check(case,request)
        prior=case['requests'].get(body.request_id)
        if prior:
            if prior['hash']!=fingerprint:raise HTTPException(409,'Request ID reused with different input.')
            return prior['result']
        if investigator.active(case):raise HTTPException(409,'Wait for Pip to finish before changing reviewed state.')
        if body.expected_revision!=case['revision']:raise HTTPException(409,'Case changed. Reload before reviewing.')
        if len(case['requests'])>=24:raise HTTPException(429,'Case action limit reached.')
        if body.action=='approve_actions':
            run=case.get('investigator') or {}
            if not case['baseline'] or not (run.get('report') or {}).get('corrective_actions'):raise HTTPException(422,'Review baseline and generate action drafts first.')
            if any(m.get('result') and m['result']['recorded_at']>run.get('started_at','') for m in case.get('missions',[])):raise HTTPException(422,'Reassess the new operator results before approving action drafts.')
            case['actions_approval']={'run_id':run['id'],'at':domain.now(),'note':body.note,'status':'approved_for_handover'}
            domain.event(case,'Corrective-action draft reviewed',body.note+' · No work order dispatched.')
        else:
            mission=next((m for m in case.get('missions',[]) if m['id']==body.mission_id),None)
            if not mission:raise HTTPException(404,'Mission not found.')
            if body.action=='approve_mission':
                if mission['status']!='proposed':raise HTTPException(422,'Only proposed missions can be approved.')
                mission.update(status='approved',approved_at=domain.now(),approval_note=body.note)
                domain.event(case,'Operator approved demo mission',mission['title'])
            else:
                if mission['status']!='approved':raise HTTPException(422,'Approve the mission before recording a result. Completed records cannot be overwritten.')
                mission['result']={'id':'R'+str(len([m for m in case.get('missions',[]) if m.get('result')])+1),'recorded_at':domain.now(),'origin':'operator-entered synthetic demo result','procedure_id':mission['procedure_id'],'lot':mission['lot'],'sample_ids':body.sample_ids,'tested':body.tested,'failed':body.failed,'outcome':body.outcome,'observation':body.note}
                mission['status']='completed'
                case['actions_approval']=None
                domain.event(case,'Operator recorded synthetic result',mission['result']['id']+' · '+body.note)
        case['revision']+=1
        result=domain.public(case,ai.mode());case['requests'][body.request_id]={'hash':fingerprint,'result':result}
        return result
    return store.mutate(id,apply)

@app.post('/api/investigations/{id}/chat')
async def operational_chat(id:str,body:copilot.ChatRequest,request:Request):
    read(id,request)
    if ai.mode()!='gemini':raise HTTPException(503,'Operational chat requires real Gemini.')
    def reserve(case):
        check(case,request)
        prior=next((m for m in case.get('chat',[]) if m['id']==body.request_id),None)
        if prior:
            if prior['question']!=body.question:raise HTTPException(409,'Request ID reused.')
            return prior
        if investigator.active(case):raise HTTPException(409,'Wait for the current AI task to finish.')
        if any(j['status']=='running' and j['lease']>time.time() for j in case['jobs'].values()):raise HTTPException(409,'Wait for the current source scan.')
        if case.get('chat_attempts',0)>=6:raise HTTPException(429,'Six operational questions are available per case.')
        case['chat_attempts']=case.get('chat_attempts',0)+1
        case['chat_job']={'id':body.request_id,'lease':time.time()+70}
    previous=store.mutate(id,reserve)
    if previous:return domain.public(read(id,request),ai.mode())
    def budget():
        def charge(case):
            check(case,request)
            if case.get('chat_job',{}).get('id')!=body.request_id or case['chat_job']['lease']<time.time():raise ValueError('Chat lease expired')
            if case.get('chat_model_attempts',0)>=12:raise ValueError('Chat model budget reached')
            case['chat_model_attempts']=case.get('chat_model_attempts',0)+1
        store.mutate(id,charge);store.reserve_model_budget()
    try:
        answer=await asyncio.wait_for(copilot.respond(read(id,request),body.question,budget),timeout=55)
    except Exception as exc:
        import logging
        logging.getLogger(__name__).warning('Operational chat stopped: %s',type(exc).__name__)
        answer={'answer':'Pip could not verify an answer. Try again within the remaining case budget or inspect the original evidence. No decisions changed.','sources':[],'status':'failed'}
    def finish(case):
        check(case,request)
        if case.get('chat_job',{}).get('id')==body.request_id:
            case.setdefault('chat',[]).append({'id':body.request_id,'question':body.question,**answer,'at':domain.now()})
            case['chat_job']['lease']=0
        return domain.public(case,ai.mode())
    return store.mutate(id,finish)

@app.get('/api/investigations/{id}/proposals/{proposal_id}/export')
def export(id:str,proposal_id:str,request:Request,format:Literal['html','csv']='html'):
    case=read(id,request); proposal=next((p for p in case['proposals'] if p['id']==proposal_id),None)
    if not proposal: raise HTTPException(404,'Proposal not found.')
    rows=proposal['scope']['rows']
    if format=='csv':
        output=io.StringIO(); writer=csv.writer(output); writer.writerow(['Shipment','Units','Batch','Category','Reason','Evidence'])
        def safe(v):
            v=str(v)
            return "'"+v if v.lstrip().startswith(('=','+','-','@')) else v
        for row in rows: writer.writerow([safe(row[k] or '') for k in ['id','units','batch','category','reason']]+['; '.join(row['evidence'])])
        return Response(output.getvalue(),media_type='text/csv',headers={'Content-Disposition':'attachment; filename="batchlens-inspection.csv"'})
    e=html.escape
    trs=''.join(f"<tr><td>{e(r['id'])}</td><td>{r['units']}</td><td>{e(r['batch'] or 'Unresolved')}</td><td>{e(r['category'])}</td><td>{e(r['reason'])}</td><td>{e(', '.join(r['evidence']))}</td></tr>" for r in rows)
    sources=''.join(f"<li>{e(a['id'])} · {e(a['name'])}</li>" for a in proposal['sources'])
    quotes=''.join(f"<li>{e(k)}: {e(v.get('quote',''))} — {e(v['label'])}</li>" for k,v in proposal['candidate_snapshot'].items())
    report=proposal.get('investigator_report')
    agent_html=''
    if report:
        items=''.join('<li><strong>'+e(f['finding'])+'</strong><p>Proposed check: '+e(f['proposed_check'])+'</p><p>Sources: '+e(', '.join(f['sources']))+'</p></li>' for f in report['findings'])
        agent_html='<h2>Pip’s AI draft at handover</h2><p>AI recommendations, not approved physical actions. Reviewer approval applies to the saved scope.</p><p>'+e(report['summary'])+'</p><ul>'+items+'</ul><h3>Open questions</h3><ul>'+''.join('<li>'+e(q)+'</li>' for q in report['unresolved'])+'</ul>'
    if report:
        agent_html+='<h3>Cause comparison</h3><pre>'+e(json.dumps(report.get('hypotheses',[]),indent=2))+'</pre><h3>Changes after operator results</h3><p>'+e(report.get('changed_since_previous',''))+'</p><h3>Corrective-action drafts</h3><pre>'+e(json.dumps(report.get('corrective_actions',[]),indent=2))+'</pre>'
    agent_html+='<h3>Mission records (synthetic)</h3><pre>'+e(json.dumps(proposal.get('missions_snapshot',[]),indent=2))+'</pre><h3>Action review</h3><pre>'+e(json.dumps(proposal.get('actions_approval') or {'status':'not approved'},indent=2))+'</pre><h3>Illustrative scope comparison</h3><pre>'+e(json.dumps(proposal.get('comparison'),indent=2))+'</pre>'
    content=f'''<!doctype html><html lang="en"><meta charset="utf-8"><title>BatchLens inspection proposal</title><style>body{{font:15px system-ui;color:#233b32;max-width:1050px;margin:60px auto;padding:30px}}h1{{font-size:36px}}table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:14px;text-align:left}}.notice{{padding:18px;background:#f2f4ec}}@media print{{body{{margin:0}}}}</style><h1>BatchLens inspection proposal</h1><p class="notice">Synthetic case · Requires quality review. Shared exposure does not prove a defect. No recorded connection does not certify safety.</p><p>Frozen revision {proposal['revision']} · Engine 1.0.0 · {e(proposal['created_at'])}</p><h2>{proposal['scope']['totals']['inspection']:,} units proposed for inspection</h2><p>Includes connected and unresolved shipment lines. Suspect lot: {e(proposal['suspect_lot'])}.</p><table><tr><th>Shipment</th><th>Units</th><th>Batch</th><th>Status</th><th>Reason</th><th>Sources</th></tr>{trs}</table><h2>Reviewer note</h2><p>{e(proposal['note'] or 'No additional note.')}</p>{agent_html}<h2>Source manifest</h2><ul>{sources}</ul><h2>Extraction excerpts</h2><ul>{quotes}</ul><p>Source images are available in the investigation until its 24-hour expiry. This file preserves the reviewed scope and excerpts.</p></html>'''
    return HTMLResponse(content,headers={'Content-Disposition':'attachment; filename="batchlens-inspection.html"'})

DIST=ROOT/'dist'
if DIST.exists():
    app.mount('/',StaticFiles(directory=DIST,html=True),name='frontend')
