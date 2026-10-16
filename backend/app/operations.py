"""Case-bound operating procedures and deterministic comparisons; no AI approval authority."""
from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing import Literal
import uuid
from . import domain

PROCEDURES={
 'seal_check': {'title':'Compare cap seals at Mira’s bench','station':'evidence','source':'E8','steps':['Use the labelled synthetic inspection record or a supervisor-authorized real procedure outside this demo.','Record sample identifiers, tested count and leaking count for one component lot.','Record the method and observations. A sample result does not certify an entire lot.'],'max_samples':20},
 'settings_review': {'title':'Review assembly settings with Sol','station':'assembly','source':'E8','steps':['Compare the E9 assembly record with the fictional setup reference in E8.','Record which setting or time window was checked and whether the record agrees.','Escalate missing calibration or measurements. A setpoint is not a measured cap torque.'],'max_samples':20},
}
class Strict(BaseModel):
 model_config=ConfigDict(extra='forbid')
class ProcedureArgs(Strict):
 procedure_id: Literal['seal_check','settings_review']
class MissionArgs(ProcedureArgs):
 reason: str=Field(min_length=10,max_length=600)
 lot: Literal['CAP-17','CAP-18']
class CompareArgs(Strict):
 lot: Literal['CAP-17','CAP-18']
 minutes_per_unit: float=Field(ge=0.01,le=60)
class Hypothesis(Strict):
 cause: str=Field(min_length=1,max_length=160)
 assessment: Literal['supported','weakened','unresolved']
 supporting_sources: list[str]=Field(max_length=10)
 contradicting_sources: list[str]=Field(max_length=10)
 explanation: str=Field(min_length=1,max_length=600)
 next_evidence: str=Field(min_length=1,max_length=400)
class CorrectiveAction(Strict):
 task: str=Field(min_length=1,max_length=400)
 owner_role: str=Field(min_length=1,max_length=80)
 verification: str=Field(min_length=1,max_length=400)
 sources: list[str]=Field(min_length=1,max_length=10)

def compare(case,lot,minutes):
 s=domain.scope(dict(case,baseline=True,suspect_lot=lot))
 total=s['totals'];connected=total['included'];unknown=total['unresolved']
 return {'hypothetical':True,'lot':lot,'source_ids':['E4','E5'],'assumption':f'{minutes} minutes per unit, illustrative operator/model input; not measured productivity.', 'options':[
 {'name':'Connected units only','units':connected,'unresolved_excluded':unknown,'minutes':round(connected*minutes,2),'notice':'Incomplete while unresolved units remain. This cannot be selected as the conservative proposal.'},
 {'name':'Connected plus unresolved','units':connected+unknown,'unresolved_excluded':0,'minutes':round((connected+unknown)*minutes,2),'notice':'Existing conservative inspection policy; requires human review.'},
 {'name':'All case shipments','units':total['total'],'unresolved_excluded':0,'minutes':round(total['total']*minutes,2),'notice':'Broader workload comparison only. No release or containment order is executed.'}], 'scope':s}

async def tool(runner,name,args):
 c=runner.case()
 if name=='read_operating_context':
  if args:raise ValueError('Unexpected arguments')
  result={'procedures':PROCEDURES,'missions':c.get('missions',[]),'previous_report':(c.get('past_investigations') or [{}])[-1].get('report'),'operator_results':[m['result'] for m in c.get('missions',[]) if m.get('result')],'notice':'Results are operator-entered synthetic demo records, not AI observations or verified real measurements.'}
  runner.read_ids.update(m['result']['id'] for m in c.get('missions',[]) if m.get('result'))
  return result
 if name=='read_procedure':
  p=ProcedureArgs.model_validate(args);runner.read_ids.add('E8')
  return {'id':p.procedure_id,**PROCEDURES[p.procedure_id],'notice':'Fictional demo procedure only. Mission approval is required before entering results. No real machine control.'}
 if name=='propose_mission':
  p=MissionArgs.model_validate(args)
  if 'E8' not in runner.read_ids:raise ValueError('Read the procedure before proposing a mission')
  if any(m['procedure_id']==p.procedure_id and m['lot']==p.lot for m in c.get('missions',[])):return {'existing':next(m for m in c['missions'] if m['procedure_id']==p.procedure_id and m['lot']==p.lot)}
  if len(c.get('missions',[]))>=3:raise ValueError('Three missions maximum')
  m={'id':str(uuid.uuid4()),**p.model_dump(),**PROCEDURES[p.procedure_id],'status':'proposed','created_at':domain.now(),'result':None}
  def save(case):
   case.setdefault('missions',[]).append(m);case['revision']+=1
   domain.event(case,'Pip proposed an inspection mission',m['title']+' · human approval required')
  runner.mutate(save);return m
 if name=='compare_containment':
  p=CompareArgs.model_validate(args);result=compare(c,p.lot,p.minutes_per_unit)
  runner.mutate(lambda case:case['investigator'].update(comparison=result));return result
 raise ValueError('Unknown operating tool')

class MissionCommand(Strict):
 request_id: str=Field(min_length=8,max_length=80)
 expected_revision: int=Field(ge=0)
 action: Literal['approve_mission','record_result','approve_actions']
 mission_id: str=Field(default='',max_length=80)
 sample_ids: str=Field(default='',max_length=200)
 tested: int=Field(default=0,ge=0,le=20)
 failed: int=Field(default=0,ge=0,le=20)
 outcome: Literal['supports','contradicts','inconclusive']='inconclusive'
 note: str=Field(min_length=10,max_length=1000)
 @model_validator(mode='after')
 def validate_counts(self):
  if self.failed>self.tested:raise ValueError('Failed count cannot exceed tested count')
  if self.action=='record_result' and (not self.sample_ids.strip() or self.tested<1):raise ValueError('Record sample or record identifiers and count')
  return self
