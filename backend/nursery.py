"""Shadow-mode nursery lifecycle."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
@dataclass
class NurseryTrial:
    agent_id:str; started_at:str; predictions:int=0; correct:int=0; extension_used:bool=False; state:str='OBSERVING'
    @property
    def accuracy(self): return self.correct/self.predictions if self.predictions else 0.0
    def evaluate(self):
        if self.predictions < 10: return self.state
        if self.accuracy >= .60: self.state='GRADUATE'
        elif self.accuracy < .30 or self.extension_used: self.state='DEAD'
        else: self.extension_used=True
        return self.state
    def to_dict(self): return {**asdict(self),'accuracy':round(self.accuracy,3)}
class Nursery:
    def __init__(self): self.trials={}
    def start(self,agent_id):
        trial=NurseryTrial(agent_id,datetime.now(timezone.utc).isoformat()); self.trials[agent_id]=trial; return trial.to_dict()
    def observe(self,agent_id,correct):
        trial=self.trials.get(agent_id)
        if not trial: return None
        trial.predictions+=1; trial.correct+=int(bool(correct)); trial.evaluate(); return trial.to_dict()
    def list(self): return [t.to_dict() for t in self.trials.values()]
nursery=Nursery()
