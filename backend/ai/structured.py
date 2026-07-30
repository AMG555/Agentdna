"""Validation for model output before it reaches the UI or tool policy."""
import json
ALLOWED_ACTIONS={'suggest_text','suggest_link','suggest_shortcut','suggest_break','open_url','open_application','create_draft'}
def safe_suggestion(text, evidence=None):
    text=' '.join(str(text).split())[:500]
    return {'suggestion':text or 'No suggestion available.','confidence':0.0,'action_type':'suggest_text','requires_confirmation':True,'reason':f'{len(evidence or [])} approved evidence items retrieved.'}
def parse_model_json(raw, evidence=None):
    try:
        data=json.loads(raw)
        if not isinstance(data,dict): raise ValueError('object_required')
        action=data.get('action_type','suggest_text')
        if action not in ALLOWED_ACTIONS: action='suggest_text'
        return {'suggestion':' '.join(str(data.get('suggestion','')).split())[:500] or 'No suggestion available.','confidence':max(0.0,min(1.0,float(data.get('confidence',0.0)))),'action_type':action,'requires_confirmation':bool(data.get('requires_confirmation',True)),'reason':' '.join(str(data.get('reason','')).split())[:500]}
    except (ValueError,TypeError,json.JSONDecodeError): return safe_suggestion(raw,evidence)
