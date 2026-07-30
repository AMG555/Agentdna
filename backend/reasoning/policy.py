ALLOWED_TOOLS={'show_suggestion','open_url','open_application','create_draft'}
RISKY_WORDS={'send','delete','purchase','submit','password','payment','share'}
def authorize(tool, argument, confirmed=False):
    if tool not in ALLOWED_TOOLS: return False,'tool_not_allowed'
    if any(word in argument.lower() for word in RISKY_WORDS) and not confirmed: return False,'confirmation_required'
    return True,'ok'
