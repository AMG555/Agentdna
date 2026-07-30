"""Local SQLite persistence with a small, migration-friendly schema."""
import sqlite3, json
from pathlib import Path
from datetime import datetime, timezone
DB_PATH = Path(__file__).resolve().parent / "agentdna.db"
class Store:
    def __init__(self, path=DB_PATH):
        self.path=path; self.init()
    def conn(self):
        c=sqlite3.connect(self.path); c.row_factory=sqlite3.Row; return c
    def init(self):
        with self.conn() as c:
            c.executescript('''CREATE TABLE IF NOT EXISTS feedback(id INTEGER PRIMARY KEY, agent_id TEXT NOT NULL, response TEXT NOT NULL, response_time_ms INTEGER, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS patterns(id INTEGER PRIMARY KEY, kind TEXT, description TEXT, confidence REAL, created_at TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, event TEXT NOT NULL, detail TEXT, created_at TEXT NOT NULL);''')
    def feedback(self, agent_id, response, response_time_ms=None):
        with self.conn() as c: c.execute('INSERT INTO feedback(agent_id,response,response_time_ms,created_at) VALUES(?,?,?,?)',(agent_id,response,response_time_ms,datetime.now(timezone.utc).isoformat()))
    def list_feedback(self, limit=100):
        with self.conn() as c: return [dict(r) for r in c.execute('SELECT * FROM feedback ORDER BY id DESC LIMIT ?', (limit,))]
    def audit(self,event,detail=''):
        with self.conn() as c: c.execute('INSERT INTO audit(event,detail,created_at) VALUES(?,?,?)',(event,detail,datetime.now(timezone.utc).isoformat()))
    def clear(self):
        with self.conn() as c: c.execute('DELETE FROM feedback'); c.execute('DELETE FROM patterns'); c.execute('DELETE FROM audit')
store=Store()
