"""Pure trace engine. No model output changes scope until a reviewer accepts it."""
from datetime import datetime, timezone
import uuid

import csv
from pathlib import Path

ASSET_ROOT=Path(__file__).resolve().parents[1]/'scenarios/bottles_v1/assets'
def import_records():
    with (ASSET_ROOT/'production.csv').open() as f:
        production=list(csv.DictReader(f))
    with (ASSET_ROOT/'shipments.csv').open() as f:
        shipments=list(csv.DictReader(f))
    if len({r['finished_batch'] for r in production})!=len(production): raise ValueError('Duplicate batch record')
    batches={r['finished_batch']:r['component_lot'] for r in production}
    if len({r['shipment_id'] for r in shipments})!=len(shipments): raise ValueError('Duplicate shipment line')
    rows=[]
    for r in shipments:
        units=int(r['units'])
        if units<=0: raise ValueError('Shipment units must be positive')
        batch=r['finished_batch'] or None
        if batch and batch not in batches: raise ValueError('Unknown batch in shipment records')
        rows.append({'id':r['shipment_id'],'destination':r['destination'],'units':units,'batch':batch})
    return batches,rows

BATCHES,SHIPMENTS=import_records()
ARTIFACTS = [
    {'id':'E1','name':'Customer complaint','file':'complaint.txt','kind':'text','label':'CUSTOMER SUPPORT','description':'A customer reports water escaping around the bottle cap.','size':'1 KB'},
    {'id':'E2','name':'Product label','file':'label.png','kind':'image','label':'PRODUCT IDENTIFICATION','description':'The returned bottle’s production label.','size':'Image'},
    {'id':'E3','name':'Supplier inspection','file':'supplier-report.png','kind':'image','label':'QUALITY CONTROL','description':'Dimensional checks for the cap delivery.','size':'Image'},
    {'id':'E4','name':'Production records','file':'production.csv','kind':'csv','label':'BATCH GENEALOGY','description':'Component lots assigned to finished batches.','size':'4 rows'},
    {'id':'E5','name':'Shipment ledger','file':'shipments.csv','kind':'csv','label':'DISTRIBUTION','description':'Four shipment lines. One batch reference is missing.','size':'4 rows'},
    {'id':'E6','name':'Original packing slip','file':'packing-slip-obscured.png','kind':'image','label':'INCOMPLETE RECORD','description':'Shipment S4 is readable. Its batch identifier is obscured.','size':'Image'},
    {'id':'E7','name':'Recovered packing slip','file':'packing-slip-clear.png','kind':'image','label':'SUPPLEMENTARY EVIDENCE','description':'A legible replacement for the S4 packing slip.','size':'Image'},
]

def now(): return datetime.now(timezone.utc).isoformat()

def new_case(owner_hash):
    return {'id': str(uuid.uuid4()), 'owner_hash': owner_hash, 'revision': 0, 'created_at': now(),
            'expires_at': datetime.now(timezone.utc).timestamp()+86400, 'baseline': False,
            'suspect_lot': None, 'resolved_batch': None, 'added_clear_slip': False,
            'candidates': {}, 'jobs': {}, 'model_attempts': 0, 'history': [], 'proposals': [], 'requests': {}}

def scope(case):
    rows=[]
    for record in SHIPMENTS:
        row=dict(record)
        if row['id']=='S4': row['batch']=case['resolved_batch']
        batch=row['batch']
        if not case['baseline']:
            category='unreviewed'; reason='Confirm the baseline evidence before computing inspection scope.'; path=[]
        elif not batch or batch not in BATCHES:
            category='unresolved'; reason='No confirmed batch identifier. Keep this shipment in the conservative inspection proposal.'; path=[]
        elif BATCHES[batch]==case['suspect_lot']:
            category='included'; reason=f"{row['id']} → {batch} → {BATCHES[batch]}. Confirmed shared component exposure; not proof of a defect."; path=['E3','E4','E7' if row['id']=='S4' else 'E5']
        else:
            category='outside'; reason=f"{batch} uses {BATCHES[batch]}. No recorded connection to {case['suspect_lot']} within this case; this is not a safety determination."; path=['E4','E7' if row['id']=='S4' else 'E5']
        rows.append({**row,'category':category,'reason':reason,'evidence':path})
    totals={key:sum(r['units'] for r in rows if r['category']==key) for key in ['included','unresolved','outside','unreviewed']}
    totals['total']=sum(r['units'] for r in rows)
    totals['inspection']=totals['included']+totals['unresolved']
    return {'engine_version':'1.0.0','revision':case['revision'],'rows':rows,'totals':totals}

def event(case,title,detail):
    case['history'].append({'id':str(uuid.uuid4()),'at':now(),'title':title,'detail':detail,'revision':case['revision']+1})

def public(case, mode):
    return {k:case[k] for k in ['id','revision','created_at','baseline','suspect_lot','resolved_batch','added_clear_slip','candidates','history','proposals','model_attempts']} | {
        'scope':scope(case), 'artifacts':[a for a in ARTIFACTS if a['id']!='E7' or case['added_clear_slip']],
        'batches':BATCHES,'mode':mode,'scenario_version':'bottles_v1',
    }
