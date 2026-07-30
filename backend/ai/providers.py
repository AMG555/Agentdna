"""LLM and embedding adapters. Cloud use is explicit; local-only is the default."""
import os, json, urllib.request
from hashlib import sha256
class ProviderError(RuntimeError): pass
class EmbeddingProvider:
    def embed(self,text):
        # Deterministic local fallback: dependency-free and never sends data away.
        vec=[0.0]*64
        for token in text.lower().split(): vec[int(sha256(token.encode()).hexdigest(),16)%64]+=1.0
        norm=sum(x*x for x in vec)**0.5 or 1.0
        return [x/norm for x in vec]
class LLMProvider:
    def __init__(self):
        self.mode=os.getenv('AGENTDNA_LLM_MODE','mock')
        self.base=os.getenv('AGENTDNA_LLM_BASE_URL','http://127.0.0.1:11434')
        self.model=os.getenv('AGENTDNA_LLM_MODEL','llama3.2')
        self.api_key=os.getenv('AGENTDNA_LLM_API_KEY','')
        self.app_url=os.getenv('AGENTDNA_APP_URL','http://127.0.0.1:8000')
        self.app_name=os.getenv('AGENTDNA_APP_NAME','AgentDNA')
    def status(self):
        return {'mode':self.mode,'base_url':self.base,'model':self.model,'enabled':self.mode not in ('disabled','mock'),'api_key_configured':bool(self.api_key)}
    def generate(self,prompt):
        if self.mode in ('disabled','mock'): return 'A low-risk suggestion based on the approved local context.'
        if self.mode not in ('ollama','openai_compatible','openrouter'): raise ProviderError('Unsupported or disabled LLM mode')
        if self.mode=='ollama':
            url=self.base.rstrip('/')+'/api/generate'; payload={'model':self.model,'prompt':prompt,'stream':False}; headers={'Content-Type':'application/json'}
        else:
            base=self.base.rstrip('/')
            url=base+'/chat/completions' if not base.endswith('/chat/completions') else base
            payload={'model':self.model,'messages':[{'role':'user','content':prompt}]}; headers={'Content-Type':'application/json','Authorization':f'Bearer {self.api_key}'}
            if self.mode=='openrouter': headers.update({'HTTP-Referer':self.app_url,'X-Title':self.app_name})
        if self.mode in ('openai_compatible','openrouter') and not self.api_key: raise ProviderError('API key is not configured')
        req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers=headers)
        try:
            with urllib.request.urlopen(req,timeout=60) as r: data=json.loads(r.read())
            return data.get('response') or data.get('choices',[{}])[0].get('message',{}).get('content','')
        except Exception as exc: raise ProviderError(str(exc)) from exc
llm=LLMProvider(); embeddings=EmbeddingProvider()
