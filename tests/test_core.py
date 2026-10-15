import os
import tempfile
os.environ['DATABASE_PATH']=tempfile.mktemp(suffix='.db')
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.domain import new_case,scope
from backend.app import ai
import uuid
HEAD={'X-BatchLens-Client':'workspace'}

def action(client,case,name,value=None,note=''):
    return client.post('/api/investigations/'+case['id']+'/commands',headers=HEAD,json={'action':name,'value':value,'note':note,'expected_revision':case['revision'],'request_id':str(uuid.uuid4())})
def extract(client,case,id):
    return client.post('/api/investigations/'+case['id']+'/extractions',headers=HEAD,json={'artifact_id':id,'request_id':str(uuid.uuid4())})
def test_scope_boundaries():
    c=new_case('owner');assert scope(c)['totals']['unreviewed']==2000
    c.update(baseline=True,suspect_lot='CAP-17')
    assert scope(c)['totals']=={'included':1000,'unresolved':500,'outside':500,'unreviewed':0,'total':2000,'inspection':1500}
    c['resolved_batch']='B104';assert scope(c)['totals']['included']==1500;assert scope(c)['totals']['inspection']==1500
    c['suspect_lot']='CAP-18';assert scope(c)['totals']['included']==500
    c['resolved_batch']='NOT-A-BATCH';assert scope(c)['rows'][3]['category']=='unresolved'
def test_complete_flow_and_snapshot(monkeypatch):
    monkeypatch.delenv('MODEL_ID',raising=False)
    client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
    assert action(client,c,'confirm_baseline').status_code==422
    for id in ['E2','E3']: c=extract(client,c,id).json()
    c=action(client,c,'confirm_baseline').json();assert c['scope']['totals']['included']==1000
    stale=dict(c)
    c=action(client,c,'create_proposal',note='<script>alert(1)</script>').json();pid=c['proposals'][0]['id']
    assert action(client,stale,'add_evidence').status_code==409
    c=action(client,c,'add_evidence').json()
    c=extract(client,c,'E6').json();assert c['candidates']['E6']['value'] is None
    c=extract(client,c,'E7').json();assert c['scope']['totals']['unresolved']==500
    c=action(client,c,'review_slip','B104').json();assert c['scope']['totals']['included']==1500
    export=client.get(f"/api/investigations/{c['id']}/proposals/{pid}/export").text
    assert '&lt;script&gt;' in export and '<script>' not in export
    assert c['proposals'][0]['scope']['totals']['unresolved']==500
    assert client.get('/api/investigations/'+c['id']).json()['resolved_batch']=='B104'
    other=TestClient(app)
    assert other.get('/api/investigations/'+c['id']).status_code==404
    assert other.get(f"/api/investigations/{c['id']}/artifacts/E2").status_code==404
    assert other.get(f"/api/investigations/{c['id']}/proposals/{pid}/export").status_code==404

def test_dedup_and_csrf(monkeypatch):
    monkeypatch.delenv('MODEL_ID',raising=False)
    client=TestClient(app)
    assert client.post('/api/investigations').status_code==403
    assert client.post('/api/investigations',headers={**HEAD,'Origin':'https://evil.example'}).status_code==403
    c=client.post('/api/investigations',headers=HEAD).json()
    for id in ['E2','E3']:c=extract(client,c,id).json()
    body={'action':'confirm_baseline','request_id':str(uuid.uuid4()),'expected_revision':c['revision']}
    url='/api/investigations/'+c['id']+'/commands'
    a=client.post(url,headers=HEAD,json=body);b=client.post(url,headers=HEAD,json=body)
    assert a.json()==b.json()
    body['note']='different';assert client.post(url,headers=HEAD,json=body).status_code==409

def test_model_failure_does_not_change_graph(monkeypatch):
    async def fail(*args):raise ValueError('invalid schema')
    monkeypatch.setattr(ai,'extract',fail)
    client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
    assert extract(client,c,'E2').status_code==502
    after=client.get('/api/investigations/'+c['id']).json()
    assert not after['baseline'] and after['candidates']=={} and after['scope']==c['scope']

def test_rejected_candidate_cannot_be_confirmed(monkeypatch):
    monkeypatch.delenv('MODEL_ID',raising=False)
    client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
    for id in ['E2','E3']:c=extract(client,c,id).json()
    c=action(client,c,'reject_candidate','E3').json()
    assert action(client,c,'confirm_baseline').status_code==422
    c=extract(client,c,'E3').json();c=action(client,c,'confirm_baseline').json()
    assert extract(client,c,'E2').status_code==422
    c=action(client,c,'add_evidence').json();c=extract(client,c,'E7').json()
    c=action(client,c,'reject_candidate','E7').json()
    assert action(client,c,'review_slip','B104').status_code==422

def test_expiry_and_request_validation(monkeypatch):
    from backend.app.main import store
    client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
    bad={'action':'not-an-action','request_id':'abcdefgh','expected_revision':0,'extra':'bad'}
    assert client.post('/api/investigations/'+c['id']+'/commands',headers=HEAD,json=bad).status_code==422
    store.mutate(c['id'],lambda record:record.update(expires_at=0))
    assert client.get('/api/investigations/'+c['id']).status_code==410
    assert client.get('/api/investigations/'+c['id']+'/artifacts/E2').status_code==410

def test_daily_budget_is_shared(monkeypatch):
    from backend.app.storage import SQLiteStore
    monkeypatch.setenv('DATABASE_PATH',tempfile.mktemp(suffix='.db'))
    monkeypatch.setenv('DAILY_MODEL_CALL_LIMIT','2')
    store=SQLiteStore();store.reserve_model_budget();store.reserve_model_budget()
    import pytest
    with pytest.raises(ValueError,match='Daily model'):store.reserve_model_budget()

def test_ten_fresh_case_runs(monkeypatch):
    monkeypatch.delenv('MODEL_ID',raising=False)
    for _ in range(10):
        client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
        for id in ['E2','E3']:c=extract(client,c,id).json()
        c=action(client,c,'confirm_baseline').json();c=action(client,c,'add_evidence').json()
        c=extract(client,c,'E7').json();c=action(client,c,'review_slip','B104').json()
        c=action(client,c,'create_proposal').json()
        assert c['scope']['totals']['inspection']==1500 and c['scope']['totals']['unresolved']==0

def test_manual_correction_keeps_review_boundary(monkeypatch):
    monkeypatch.delenv('MODEL_ID',raising=False)
    client=TestClient(app);c=client.post('/api/investigations',headers=HEAD).json()
    c=extract(client,c,'E2').json()
    assert action(client,c,'correct_candidate','E2:B101','').status_code==422
    c=action(client,c,'correct_candidate','E2:B101','The source label reads B101.').json()
    assert c['candidates']['E2']['status']=='pending'
    assert c['candidates']['E2']['original_value']=='B101'
    assert c['scope']['totals']['unreviewed']==2000

def test_cloud_run_never_silently_uses_demo(monkeypatch):
    import pytest
    monkeypatch.setenv('K_SERVICE','batchlens')
    monkeypatch.delenv('MODEL_ID',raising=False)
    with pytest.raises(RuntimeError,match='live Gemini'): ai.mode()
    monkeypatch.setenv('MODEL_ID','configured-model')
    monkeypatch.setenv('GOOGLE_CLOUD_PROJECT','test-project')
    assert ai.mode()=='gemini'
