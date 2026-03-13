import re

EMAIL_REGEX = r'[\w\.-]+@[\w\.-]+\.\w+'
PHONE_REGEX = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
SSN_REGEX = r'\b\d{3}-\d{2}-\d{4}\b'

def redact_pii_regex(text: str) -> str:
    redacted_text = re.sub(EMAIL_REGEX, '[EMAIL]', text)
    redacted_text = re.sub(PHONE_REGEX, '[PHONE]', redacted_text)
    redacted_text = re.sub(SSN_REGEX, '[SSN]', redacted_text)
    return redacted_text
