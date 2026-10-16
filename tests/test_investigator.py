import asyncio, time, uuid
import pytest
from fastapi.testclient import TestClient
from backend.app import main, investigator, domain, ai
from test_core import HEAD, action

@pytest.fixture
def setup(monkeypatch):
    monkeypatch.setattr(ai,'mode',lambda:'gemini')
    monkeypatch.setenv('MODEL_ID','test-model')
    client=TestClient(main.app)
    c=client.post('/api/investigations',headers=HEAD).json()
    return client,c

def test_agent_tools_cannot_approve_and_citations_require_reads(setup,monkeypatch):
    client,c=setup
    async def fake_extract(key,path):return {**ai.DEMO[key],'artifact_id':key,'provider':'test','label':'Test reading'}
    monkeypatch.setattr(ai,'extract',fake_extract)
    async def run(self):
        with pytest.raises(ValueError):await self.execute('confirm_baseline',{})
        with pytest.raises(ValueError):await self.execute('read_document',{'artifact_id':'E7'})
        await self.execute('search_archive',{'query':'S4 packing slip'})
        for key in ['E2','E3','E6','E7']:await self.execute('read_document',{'artifact_id':key})
        report={'summary':'Test draft','findings':[{'finding':'S4 candidate B104','sources':['E5'],'proposed_check':'Review original ledger'}],'unresolved':[]}
        with pytest.raises(ValueError):await self.execute('submit_findings',report)
        await self.execute('read_document',{'artifact_id':'E5'})
        await self.execute('submit_findings',report)
        assert action(client,client.get('/api/investigations/'+c['id']).json(),'confirm_baseline').status_code==409
    monkeypatch.setattr(investigator.Runner,'run',run)
    body={'request_id':str(uuid.uuid4())};url=f"/api/investigations/{c['id']}/investigator"
    result=client.post(url,headers=HEAD,json=body);assert result.status_code==200
    after=result.json();assert after['investigator']['status']=='awaiting_review'
    assert not after['baseline'] and after['resolved_batch'] is None and after['proposals']==[]
    assert after['scope']['totals']['unreviewed']==2000
    assert after['candidates']['E7']['status']=='pending' and after['added_clear_slip']
    assert client.post(url,headers=HEAD,json=body).json()==after
    approved=action(client,after,'confirm_baseline').json();assert approved['scope']['totals']['unresolved']==500
    assert TestClient(main.app).post(url,headers=HEAD,json=body).status_code==404

def test_failure_is_partial_and_no_authored_agent_fallback(setup,monkeypatch):
    client,c=setup
    async def fail(self):
        self.log('evidence_index',{}, {'sources':['E1']})
        raise RuntimeError('provider error secret')
    monkeypatch.setattr(investigator.Runner,'run',fail)
    url=f"/api/investigations/{c['id']}/investigator"
    for _ in range(2):
        result=client.post(url,headers=HEAD,json={'request_id':str(uuid.uuid4())})
        assert result.json()['investigator']['status']=='incomplete'
        assert 'provider error secret' not in result.text
    assert client.post(url,headers=HEAD,json={'request_id':str(uuid.uuid4())}).status_code==429
    monkeypatch.setattr(ai,'mode',lambda:'demo')
    assert client.post(url,headers=HEAD,json={'request_id':str(uuid.uuid4())}).status_code==503

def test_manual_tool_loop_preserves_signatures_and_call_ids(setup,monkeypatch):
    from google import genai
    from google.genai import types
    client,c=setup;seen=[]
    responses=[types.GenerateContentResponse(candidates=[types.Candidate(content=types.Content(role='model',parts=[types.Part(function_call=types.FunctionCall(name='read_document',args={'artifact_id':'E1'},id='call-a'),thought_signature=b'signature')]))]),types.GenerateContentResponse(candidates=[types.Candidate(content=types.Content(role='model',parts=[types.Part(function_call=types.FunctionCall(name='submit_findings',id='call-b',args={'summary':'Complaint review draft','findings':[{'finding':'Customer reports leaking cap','sources':['E1'],'proposed_check':'Inspect returned cap seal'}],'unresolved':['Physical inspection pending']}))]))])]
    class Models:
        async def generate_content(self,**kwargs):
            seen.append(list(kwargs['contents']));return responses[len(seen)-1]
    class Aio:
        models=Models()
        async def __aenter__(self):return self
        async def __aexit__(self,*args):pass
    class Client:
        aio=Aio()
        def __init__(self,**kwargs):pass
    monkeypatch.setattr(genai,'Client',Client);monkeypatch.setenv('GOOGLE_CLOUD_PROJECT','test')
    result=client.post(f"/api/investigations/{c['id']}/investigator",headers=HEAD,json={'request_id':str(uuid.uuid4())}).json()
    assert result['investigator']['status']=='awaiting_review'
    assert seen[1][1].parts[0].thought_signature==b'signature'
    assert seen[1][2].parts[0].function_response.id=='call-a'
    assert result['agent_model_attempts']==2

def test_model_budget_and_saved_ai_draft_are_bounded(setup,monkeypatch):
    client,c=setup
    async def run(self):
        self.mutate(lambda case:case.update(agent_model_attempts=12))
        with pytest.raises(ValueError,match='budget'):self.budget()
        self.read_ids.add('E1')
        await self.execute('submit_findings',{'summary':'<script>draft</script>','findings':[{'finding':'Draft','sources':['E1'],'proposed_check':'Review'}],'unresolved':[]})
    monkeypatch.setattr(investigator.Runner,'run',run)
    after=client.post(f"/api/investigations/{c['id']}/investigator",headers=HEAD,json={'request_id':str(uuid.uuid4())}).json()
    def baseline(case):
        case['baseline']=True;case['suspect_lot']='CAP-17'
    main.store.mutate(c['id'],baseline)
    saved=action(client,after,'create_proposal',note='Reviewed scope, draft still advisory').json()
    proposal=saved['proposals'][0]
    assert proposal['investigator_report']['summary']=='<script>draft</script>'
    html=client.get(f"/api/investigations/{c['id']}/proposals/{proposal['id']}/export").text
    assert '&lt;script&gt;draft&lt;/script&gt;' in html and '<script>' not in html
    assert proposal['scope']['totals']['unresolved']==500
