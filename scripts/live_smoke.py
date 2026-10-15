"""Run the real hosted API workflow. Prints non-secret verification results only."""
import json, sys, uuid, time
import httpx
base=sys.argv[1].rstrip('/')
results={'url':base,'started_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'extractions':[]}
with httpx.Client(base_url=base,headers={'X-BatchLens-Client':'workspace'},timeout=90,follow_redirects=True) as client:
    health=client.get('/api/health');health.raise_for_status();results['health']=health.json()
    assert results['health']['ai_mode']=='gemini'
    r=client.post('/api/investigations');r.raise_for_status();case=r.json()
    def extract(artifact,expected):
        global case
        before=case['scope']
        r=client.post(f"/api/investigations/{case['id']}/extractions",json={'artifact_id':artifact,'request_id':str(uuid.uuid4())})
        r.raise_for_status();case=r.json();c=case['candidates'][artifact]
        assert c['provider']=='gemini' and c['value']==expected,(artifact,c)
        assert case['scope']['totals']==before['totals']
        results['extractions'].append({k:c.get(k) for k in ['artifact_id','provider','model','value','quote','latency_ms','response_id','usage']})
    def command(action,value=None):
        global case
        r=client.post(f"/api/investigations/{case['id']}/commands",json={'action':action,'value':value,'note':'Live deployment verification with synthetic source records.','expected_revision':case['revision'],'request_id':str(uuid.uuid4())})
        r.raise_for_status();case=r.json()
    extract('E2','B101');extract('E3','CAP-17');command('confirm_baseline')
    assert case['scope']['totals']['inspection']==1500 and case['scope']['totals']['unresolved']==500
    extract('E6',None);command('add_evidence');extract('E7','B104');command('review_slip','B104');command('create_proposal')
    assert case['scope']['totals']['included']==1500 and case['scope']['totals']['unresolved']==0
    proposal=case['proposals'][-1]
    for fmt in ['html','csv']:
        r=client.get(f"/api/investigations/{case['id']}/proposals/{proposal['id']}/export",params={'format':fmt});r.raise_for_status();assert 'S4' in r.text and 'B104' in r.text
    restored=client.get('/api/investigations/'+case['id']);restored.raise_for_status();assert restored.json()['resolved_batch']=='B104'
    results.update(totals=case['scope']['totals'],exports=['html','csv'],reload='passed',result='passed')
print(json.dumps(results,indent=2))
