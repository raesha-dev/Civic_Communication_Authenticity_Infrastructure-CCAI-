import re
from dataclasses import dataclass

try:
    from pydantic import BaseModel, Field, ValidationError  # type: ignore

    class TranslationRequest(BaseModel):
        analysis_id: str = Field(..., min_length=1, max_length=128, description="ID from a previous successful analysis")
        original_text: str = Field(..., min_length=1, max_length=5000)
        target_lang: str = Field(..., min_length=2, max_length=5, pattern=r"^[A-Za-z-]+$")

        class Config:
            extra = "forbid"


    class AppealRequest(BaseModel):
        analysis_id: str = Field(..., min_length=1, max_length=128)
        reason: str = Field(..., min_length=10, max_length=1000)
        contact_email: str = Field(..., min_length=3, max_length=254, pattern=r"^\S+@\S+\.\S+$")

        class Config:
            extra = "forbid"
except ModuleNotFoundError:
    class ValidationError(Exception):
        def __init__(self, errors):
            super().__init__("validation error")
            self._errors = errors

        def errors(self):
            return self._errors


    def _validation_error(field: str, message: str, value=None):
        raise ValidationError([{
            "loc": [field],
            "msg": message,
            "input": value,
            "type": "value_error",
        }])


    def _contains_control_chars(value: str) -> bool:
        return any(ord(char) < 32 and char not in "\t\n\r" for char in value)


    @dataclass
    class TranslationRequest:
        analysis_id: str
        original_text: str
        target_lang: str

        def __init__(self, **data):
            analysis_id = data.get("analysis_id")
            original_text = data.get("original_text")
            target_lang = data.get("target_lang")

            if not isinstance(analysis_id, str) or not analysis_id.strip():
                _validation_error("analysis_id", "analysis_id must be a non-empty string", analysis_id)
            if len(analysis_id) > 128:
                _validation_error("analysis_id", "analysis_id must be at most 128 characters", analysis_id)
            if not isinstance(original_text, str) or not original_text.strip():
                _validation_error("original_text", "original_text must be a non-empty string", original_text)
            if len(original_text) > 5000:
                _validation_error("original_text", "original_text must be at most 5000 characters", original_text)
            if _contains_control_chars(original_text):
                _validation_error("original_text", "original_text contains unsupported control characters", original_text)
            if not isinstance(target_lang, str) or not (2 <= len(target_lang) <= 5):
                _validation_error("target_lang", "target_lang must be between 2 and 5 characters", target_lang)
            if not re.match(r"^[A-Za-z-]+$", target_lang):
                _validation_error("target_lang", "target_lang must contain only letters or hyphens", target_lang)

            self.analysis_id = analysis_id
            self.original_text = original_text
            self.target_lang = target_lang


    @dataclass
    class AppealRequest:
        analysis_id: str
        reason: str
        contact_email: str

        def __init__(self, **data):
            analysis_id = data.get("analysis_id")
            reason = data.get("reason")
            contact_email = data.get("contact_email")

            if not isinstance(analysis_id, str) or not analysis_id.strip():
                _validation_error("analysis_id", "analysis_id must be a non-empty string", analysis_id)
            if len(analysis_id) > 128:
                _validation_error("analysis_id", "analysis_id must be at most 128 characters", analysis_id)
            if not isinstance(reason, str) or not (10 <= len(reason.strip()) <= 1000):
                _validation_error("reason", "reason must be between 10 and 1000 characters", reason)
            if _contains_control_chars(reason):
                _validation_error("reason", "reason contains unsupported control characters", reason)
            if not isinstance(contact_email, str) or not re.match(r"^\S+@\S+\.\S+$", contact_email):
                _validation_error("contact_email", "contact_email must be a valid email", contact_email)
            if len(contact_email) > 254:
                _validation_error("contact_email", "contact_email must be at most 254 characters", contact_email)

            self.analysis_id = analysis_id
            self.reason = reason
            self.contact_email = contact_email
