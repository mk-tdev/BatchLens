import json, uuid
import pytest
from fastapi.testclient import TestClient
from backend.app import main, investigator, operations, copilot, ai
from test_core import HEAD, action
from test_investigator import setup

def mission_post(client,c,action_name,**kw):
 return client.post(f"/api/investigations/{c['id']}/missions",headers=HEAD,json={'request_id':str(uuid.uuid4()),'expected_revision':c['revision'],'action':action_name,'note':'Operator synthetic test review.',**kw})

def test_missions_require_human_approval_and_results_change_context(setup,monkeypatch):
 client,c=setup
 async def run(self):
  await self.execute('read_procedure',{'procedure_id':'seal_check'})
  await self.execute('propose_mission',{'procedure_id':'seal_check','lot':'CAP-17','reason':'Compare cap seals against the complaint.'})
  with pytest.raises(ValueError):await self.execute('approve_mission',{})
  await self.execute('read_document',{'artifact_id':'E1'})
  context=await self.execute('read_operating_context',{})
  sources=['E1']+([context['operator_results'][0]['id']] if context['operator_results'] else [])
  await self.execute('submit_findings',{'summary':'Draft based on current records','findings':[{'finding':'Complaint and result reviewed','sources':sources,'proposed_check':'Review sample limits'}],'unresolved':['Causation unproven'],'hypotheses':[{'cause':'Cap variation','assessment':'unresolved','supporting_sources':sources,'contradicting_sources':[],'explanation':'Limited records','next_evidence':'More representative testing'}],'corrective_actions':[{'task':'Review supplier check','owner_role':'Quality lead','verification':'Supplier response','sources':sources}]})
 monkeypatch.setattr(investigator.Runner,'run',run)
 url=f"/api/investigations/{c['id']}/investigator"
 c=client.post(url,headers=HEAD,json={'request_id':str(uuid.uuid4())}).json();m=c['missions'][0]
 assert m['status']=='proposed' and not c['baseline']
 assert mission_post(client,c,'record_result',mission_id=m['id'],sample_ids='DEMO-1',tested=2,failed=1).status_code==422
 assert mission_post(TestClient(main.app),c,'approve_mission',mission_id=m['id']).status_code==404
 c=mission_post(client,c,'approve_mission',mission_id=m['id']).json()
 assert mission_post(client,c,'record_result',mission_id=m['id'],sample_ids='DEMO-1',tested=2,failed=3).status_code==422
 c=mission_post(client,c,'record_result',mission_id=m['id'],sample_ids='DEMO-1, DEMO-2',tested=2,failed=1).json()
 assert c['missions'][0]['result']['id']=='R1'
 assert mission_post(client,c,'record_result',mission_id=m['id'],sample_ids='X',tested=1).status_code==422
 assert c['scope']['totals']['unreviewed']==2000
 c=client.post(url,headers=HEAD,json={'request_id':str(uuid.uuid4())}).json()
 assert 'R1' in c['investigator']['report']['findings'][0]['sources']
 assert len(c['missions'])==1
 assert mission_post(client,c,'approve_actions').status_code==422
 main.store.mutate(c['id'],lambda x:x.update(baseline=True,suspect_lot='CAP-17'))
 c=mission_post(client,c,'approve_actions').json();assert c['actions_approval']['status']=='approved_for_handover'
 c=action(client,c,'create_proposal',note='Reviewed synthetic results').json();p=c['proposals'][0]
 assert p['missions_snapshot'][0]['result']['failed']==1
 assert p['actions_approval'] and p['investigator_report']['hypotheses']

def test_comparison_is_conservative_and_illustrative():
 c=main.domain.new_case('x')
 r=operations.compare(c,'CAP-17',0.5)
 assert [o['units'] for o in r['options']]==[1000,1500,2000]
 assert r['options'][0]['unresolved_excluded']==500
 assert r['options'][1]['minutes']==750
 assert not c['baseline']

@pytest.mark.parametrize('allow,citations,expected',[(False,[],'out_of_scope'),(True,['E1'],'answered'),(True,['E404'],'failed')])
def test_chat_scope_guard_citations_and_read_only(setup,monkeypatch,allow,citations,expected):
 from google import genai
 client,c=setup;calls=[]
 class Models:
  async def generate_content(self,**kw):
   calls.append(kw)
   class Response:pass
   r=Response();r.text=json.dumps({'operational':allow} if len(calls)==1 else {'operational':True,'answer':'The complaint reports a leaking cap.','sources':citations})
   return r
 class Aio:
  models=Models()
  async def __aenter__(self):return self
  async def __aexit__(self,*args):pass
 class Client:
  aio=Aio()
  def __init__(self,**kw):pass
 monkeypatch.setattr(genai,'Client',Client);monkeypatch.setenv('GOOGLE_CLOUD_PROJECT','test')
 body={'request_id':str(uuid.uuid4()),'question':'What does the complaint say?' if allow else 'Write a poem about space'}
 url=f"/api/investigations/{c['id']}/chat"
 after=client.post(url,headers=HEAD,json=body).json()
 assert after['chat'][-1]['status']==expected
 assert not after['baseline'] and after['missions']==[] and after['scope']==c['scope']
 assert len(calls)==(2 if allow else 1)
 assert client.post(url,headers=HEAD,json=body).json()==after
 assert TestClient(main.app).post(url,headers=HEAD,json=body).status_code==404
 assert client.post(url,headers=HEAD,json={**body,'question':'Different query'}).status_code==409
