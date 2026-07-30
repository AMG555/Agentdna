"""Task-aware model routing with safe fallback and no secret exposure."""
from .providers import llm
class ModelRouter:
    def choose(self, task, sensitive=False):
        if sensitive or task in {'classify','embed','redact'}: return 'local'
        return llm.mode
    def status(self): return {'active_provider':llm.mode,'policy':'sensitive_tasks_local','fallback':'mock'}
    def generate(self, task, prompt, sensitive=False):
        provider=self.choose(task,sensitive)
        if provider=='local' and llm.mode not in ('ollama','mock','disabled'):
            return 'A local-safe suggestion based on approved metadata.',provider
        return llm.generate(prompt),provider
router=ModelRouter()
