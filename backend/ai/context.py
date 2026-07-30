from ..retrieval.vector_store import vector_store
from .model_router import router
from .structured import parse_model_json

def grounded_suggestion(context, goal):
    related=vector_store.search(context,5)
    evidence='\n'.join(x['text'] for x in related)
    prompt=('Return JSON only with keys suggestion, confidence, action_type, '
            'requires_confirmation, reason. Use only approved metadata evidence.\n'
            f'Evidence:\n{evidence}\nCurrent context: {context}\nGoal: {goal}')
    # Context is already metadata-only and passed through the privacy gate; cloud use remains opt-in via LLM_MODE.
    raw,provider=router.generate('suggestion',prompt,sensitive=False)
    result=parse_model_json(raw,related); result['provider']=provider; result['evidence']=related
    return result
