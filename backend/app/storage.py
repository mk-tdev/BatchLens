"""SQLite for durable local development; Firestore for the packaged Cloud Run app."""
import json, os, sqlite3
from datetime import datetime, timezone
from pathlib import Path

class SQLiteStore:
    def __init__(self):
        self.path=os.environ.get('DATABASE_PATH','.data/batchlens.db')
        Path(self.path).parent.mkdir(parents=True,exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS cases (id TEXT PRIMARY KEY, body TEXT NOT NULL)')
            db.execute('CREATE TABLE IF NOT EXISTS usage (day TEXT PRIMARY KEY, count INTEGER NOT NULL)')
    def reserve_model_budget(self):
        day=datetime.now(timezone.utc).date().isoformat()
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT count FROM usage WHERE day=?',(day,)).fetchone()
            count=row[0] if row else 0
            if count>=int(os.getenv('DAILY_MODEL_CALL_LIMIT','100')): raise ValueError('Daily model call limit reached')
            db.execute('INSERT OR REPLACE INTO usage VALUES (?,?)',(day,count+1))
    def connect(self): return sqlite3.connect(self.path, timeout=15)
    def create(self, case):
        with self.connect() as db: db.execute('INSERT INTO cases VALUES (?,?)',(case['id'],json.dumps(case)))
    def get(self, id):
        with self.connect() as db: row=db.execute('SELECT body FROM cases WHERE id=?',(id,)).fetchone()
        return json.loads(row[0]) if row else None
    def mutate(self,id,fn):
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT body FROM cases WHERE id=?',(id,)).fetchone()
            case=json.loads(row[0]) if row else None
            result=fn(case)
            if case is not None: db.execute('UPDATE cases SET body=? WHERE id=?',(json.dumps(case),id))
            return result

class FirestoreStore:
    def __init__(self):
        from google.cloud import firestore
        self.fs=firestore
        self.db=firestore.Client(project=os.environ.get('GOOGLE_CLOUD_PROJECT'),database=os.getenv('FIRESTORE_DATABASE','(default)'))
        self.collection=self.db.collection('batchlens_cases')
    def reserve_model_budget(self):
        day=datetime.now(timezone.utc).date().isoformat()
        ref=self.db.collection('batchlens_usage').document(day)
        @self.fs.transactional
        def reserve(transaction):
            snap=ref.get(transaction=transaction)
            count=snap.to_dict()['count'] if snap.exists else 0
            if count>=int(os.getenv('DAILY_MODEL_CALL_LIMIT','100')): raise ValueError('Daily model call limit reached')
            transaction.set(ref,{'count':count+1})
        reserve(self.db.transaction())
    def create(self,case): self.collection.document(case['id']).create({'body':json.dumps(case),'expires_at':datetime.fromtimestamp(case['expires_at'],timezone.utc)})
    def get(self,id):
        snap=self.collection.document(id).get()
        return json.loads(snap.to_dict()['body']) if snap.exists else None
    def mutate(self,id,fn):
        ref=self.collection.document(id)
        @self.fs.transactional
        def run(transaction):
            snap=ref.get(transaction=transaction)
            case=json.loads(snap.to_dict()['body']) if snap.exists else None
            result=fn(case)
            if case is not None:
                payload=json.dumps(case)
                if len(payload.encode())>850000: raise ValueError('Investigation storage limit reached')
                transaction.set(ref,{'body':payload,'expires_at':datetime.fromtimestamp(case['expires_at'],timezone.utc)})
            return result
        return run(self.db.transaction())

def make_store():
    if os.getenv('K_SERVICE') and os.getenv('STORAGE_BACKEND')!='firestore':
        raise RuntimeError('Cloud Run requires STORAGE_BACKEND=firestore; container storage is not durable.')
    return FirestoreStore() if os.getenv('STORAGE_BACKEND')=='firestore' else SQLiteStore()
