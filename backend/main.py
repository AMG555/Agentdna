"""AgentDNA local API.

The service is intentionally local-first: observation is disabled by default,
applications must be explicitly allowed, and the API is meant for loopback use.
"""
from contextlib import asynccontextmanager
from pathlib import Path
import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from .observer.privacy_guard import PrivacyGuard
from .observer.activity_monitor import ActivityMonitor
from .evolution.evolution_engine import EvolutionEngine
from .storage import store
from .agents import population
from .patterns import pattern_summary
from .automation import automations, Permission
from .settings import settings
from .ai.providers import llm
from .ai.model_router import router
from .retrieval.vector_store import vector_store
from .ai.context import grounded_suggestion
from .reasoning.react_loop import react
from .nursery import nursery
from .events import event_bus
from .automation_executor import executor

ROOT=Path(__file__).resolve().parents[1]
privacy=PrivacyGuard(); monitor=ActivityMonitor(privacy); evolution=EvolutionEngine(); clients=set()

async def evolution_loop():
    while True:
        await asyncio.sleep(86400)
        evolution.run_cycle()

@asynccontextmanager
async def lifespan(app):
    tasks=[asyncio.create_task(monitor.run()), asyncio.create_task(evolution_loop())]
    try: yield
    finally:
        for task in tasks: task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

app=FastAPI(title='AgentDNA Local API', version='1.0.0', lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=['http://127.0.0.1:8000'], allow_methods=['GET','POST','PUT','DELETE'], allow_headers=['Content-Type'])

class AppPermission(BaseModel):
    app_name:str=Field(min_length=1,max_length=120)
    @field_validator('app_name')
    @classmethod
    def clean_name(cls,v): return ' '.join(v.split())
class Feedback(BaseModel):
    agent_id:str=Field(min_length=1,max_length=120)
    response:str=Field(min_length=1,max_length=30)
    response_time_ms:int|None=Field(default=None,ge=0,le=86_400_000)
class AutomationRequest(BaseModel):
    name:str=Field(min_length=1,max_length=120); trigger:str=Field(min_length=1,max_length=500); action:str=Field(min_length=1,max_length=500); permission:str='confirm'
class SettingRequest(BaseModel): key:str=Field(min_length=1,max_length=80); value:str|int|bool
class NurseryRequest(BaseModel): agent_id:str=Field(min_length=1,max_length=120)
class NurseryObservation(BaseModel): agent_id:str=Field(min_length=1,max_length=120); correct:bool
class ToolRequest(BaseModel): tool:str=Field(min_length=1,max_length=80); argument:str=Field(min_length=1,max_length=1000); confirmed:bool=False

@app.get('/api/health')
def health(): return {'status':'ok','monitoring':privacy.monitoring_enabled,'version':'1.0.0'}
@app.get('/api/privacy')
def get_privacy(): return privacy.to_dict()
@app.post('/api/privacy/pause')
def pause(): privacy.pause(); store.audit('monitoring_paused'); return privacy.to_dict()
@app.post('/api/privacy/resume')
def resume(): privacy.resume(); store.audit('monitoring_resumed'); return privacy.to_dict()
@app.post('/api/privacy/allow')
def allow(p:AppPermission): privacy.allow(p.app_name); store.audit('app_allowed',p.app_name); return privacy.to_dict()
@app.delete('/api/privacy/data')
def delete_data():
    monitor.clear(); store.clear()
    return {'deleted':True}
@app.get('/api/activity')
def activity(): return [x.to_dict() for x in monitor.snapshots[-100:]]
@app.get('/api/patterns')
def patterns(): return pattern_summary(monitor.snapshots)
@app.get('/api/agents')
def agents(): return population.to_dict()
@app.get('/api/nursery')
def nursery_state(): return nursery.list()
@app.post('/api/nursery/start')
def nursery_start(r:NurseryRequest): return nursery.start(r.agent_id)
@app.post('/api/nursery/observe')
def nursery_observe(r:NurseryObservation):
    result=nursery.observe(r.agent_id,r.correct)
    if result is None: raise HTTPException(status_code=404,detail='nursery_trial_not_found')
    return result
@app.post('/api/agents/feedback')
def feedback(f:Feedback):
    result=population.feedback(f.agent_id,f.response)
    if result is None: raise HTTPException(status_code=404, detail='agent_not_found')
    store.feedback(f.agent_id,f.response,f.response_time_ms); return result
@app.get('/api/feedback')
def feedback_log(): return store.list_feedback()
@app.get('/api/evolution')
def evolution_state(): return evolution.to_dict()
@app.post('/api/evolution/run')
def run_evolution(): store.audit('evolution_cycle'); return evolution.run_cycle()
@app.get('/api/automations')
def list_automations(): return automations.list()
@app.post('/api/automations')
def create_automation(r:AutomationRequest):
    if r.permission not in [p.value for p in Permission]: raise HTTPException(status_code=422, detail='invalid_permission')
    item=automations.create(r.name,r.trigger,r.action,r.permission); store.audit('automation_created',r.name); return item
class SuggestionRequest(BaseModel): context:str=Field(min_length=1,max_length=1000); goal:str=Field(min_length=1,max_length=500)
class RetrievalItem(BaseModel): id:str=Field(min_length=1,max_length=120); text:str=Field(min_length=1,max_length=1000); metadata:dict={}
@app.get('/api/ai/status')
def ai_status(): return {**llm.status(), 'router':router.status()}
@app.post('/api/retrieval/index')
def index_retrieval(item:RetrievalItem):
    vector_store.add(item.id,item.text,item.metadata); return {'indexed':True,'count':len(vector_store.items)}
@app.get('/api/retrieval/search')
def search_retrieval(q:str,limit:int=5): return vector_store.search(q,max(1,min(limit,20)))
@app.post('/api/ai/suggestion')
def suggestion(r:SuggestionRequest): return grounded_suggestion(r.context,r.goal)
@app.post('/api/reasoning/plan')
def reasoning_plan(r:SuggestionRequest): return react.plan(r.goal,r.context)
@app.post('/api/automation/preview')
def automation_preview(r:ToolRequest): return executor.preview(r.tool,r.argument)
@app.post('/api/automation/execute')
def automation_execute(r:ToolRequest): return executor.execute(r.tool,r.argument,r.confirmed)
@app.get('/api/events')
def events(): return event_bus.history[-100:]
@app.get('/api/settings')
def get_settings(): return settings.values
@app.put('/api/settings')
def update_setting(r:SettingRequest): settings.values[r.key]=r.value; store.audit('setting_updated',r.key); return settings.values
@app.websocket('/ws')
async def websocket(ws:WebSocket):
    await ws.accept(); clients.add(ws)
    try:
        while True: await ws.receive_text()
    except WebSocketDisconnect: clients.discard(ws)
app.mount('/assets',StaticFiles(directory=ROOT),name='assets')
@app.get('/')
def ui(): return FileResponse(ROOT/'index.html')
