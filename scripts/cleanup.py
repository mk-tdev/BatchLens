"""Manually remove expired local demo sessions. No active sessions are removed."""
import os, sqlite3, json, time
path=os.getenv('DATABASE_PATH','.data/batchlens.db')
with sqlite3.connect(path) as db:
    expired=[(id,) for id,body in db.execute('SELECT id, body FROM cases') if json.loads(body)['expires_at']<time.time()]
    db.executemany('DELETE FROM cases WHERE id=?',expired)
print(f'Removed {len(expired)} expired local investigations.')
