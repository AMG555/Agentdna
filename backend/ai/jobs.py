"""Small in-process async job registry for the modular monolith."""
import asyncio, uuid
class JobRegistry:
    def __init__(self): self.jobs={}
    async def submit(self,coro):
        jid=str(uuid.uuid4()); self.jobs[jid]={'id':jid,'state':'queued'}
        async def run():
            self.jobs[jid]['state']='running'
            try: self.jobs[jid].update({'state':'completed','result':await coro})
            except Exception as exc: self.jobs[jid].update({'state':'failed','error':str(exc)})
        asyncio.create_task(run()); return self.jobs[jid]
    def get(self,jid): return self.jobs.get(jid)
jobs=JobRegistry()
