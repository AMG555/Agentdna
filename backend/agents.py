from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
@dataclass
class Agent:
    id:str; name:str; agent_type:str; trigger:str; action:str; fitness:int=50; state:str='NURSERY'; generation:int=1; suggestions:int=0; accepted:int=0; dismissed:int=0; cooldown_minutes:int=30
    def feedback(self, response):
        self.suggestions += 1
        if response in ('ACCEPTED','THUMBS_UP'): self.accepted+=1; self.fitness=min(100,self.fitness+(25 if response=='THUMBS_UP' else 15))
        elif response=='DISMISSED': self.dismissed+=1; self.fitness=max(0,self.fitness-3)
        elif response in ('STOP','NEVER'): self.fitness=max(0,self.fitness-30); self.state='DORMANT' if response=='STOP' else 'DEAD'
        return asdict(self)
    def to_dict(self): return asdict(self)
class Population:
    def __init__(self): self.agents=[Agent('scout-7','Scout-7','shortcut','Repeated menu sequence','Suggest a keyboard shortcut',92,'ACTIVE',8),Agent('muse-12','Muse-12','focus','Long coding session','Offer a five-minute break',84,'ACTIVE',8),Agent('link-4','Link-4','research','Work app → browser','Suggest relevant documentation',78,'ACTIVE',8)]
    def get(self, aid): return next((a for a in self.agents if a.id==aid),None)
    def feedback(self,aid,response):
        a=self.get(aid)
        if not a: return None
        return a.feedback(response)
    def to_dict(self): return {'agents':[a.to_dict() for a in self.agents], 'population':len(self.agents), 'generation':8}
population=Population()
