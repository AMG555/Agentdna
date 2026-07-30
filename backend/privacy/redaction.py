"""Conservative metadata redaction before persistence, retrieval or model use."""
import re
EMAIL=re.compile(r'\b[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}\b')
CARD=re.compile(r'(?<!\d)(?:\d[ -]?){13,19}(?!\d)')
SECRET=re.compile(r'\b(?:sk|pk|api|token|secret)[_-]?[A-Za-z0-9_-]{8,}\b',re.I)
def redact(value):
    text=str(value or '')
    text=EMAIL.sub('[REDACTED_EMAIL]',text)
    text=CARD.sub('[REDACTED_NUMBER]',text)
    text=SECRET.sub('[REDACTED_SECRET]',text)
    return text[:500]
