"""Small local vector index. SQLite remains the source of truth; this index is rebuildable."""
import math
from ..ai.providers import embeddings
class LocalVectorStore:
    def __init__(self): self.items=[]
    def add(self, item_id, text, metadata=None): self.items=[x for x in self.items if x['id']!=item_id]; self.items.append({'id':item_id,'text':text,'metadata':metadata or {},'vector':embeddings.embed(text)})
    def search(self, query, limit=5):
        q=embeddings.embed(query); terms=set(query.lower().split())
        def score(x):
            semantic=sum(a*b for a,b in zip(q,x['vector']))
            lexical=sum(1 for t in terms if t in x['text'].lower()) / max(1,len(terms))
            return 0.7*semantic+0.3*lexical
        return [{k:v for k,v in x.items() if k!='vector'}|{'score':round(score(x),4)} for x in sorted(self.items,key=score,reverse=True)[:limit]]
    def clear(self): self.items.clear()
vector_store=LocalVectorStore()
