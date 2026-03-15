import re
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

try:
    from pydantic import BaseModel, Field, ValidationError  # type: ignore

    class AnalysisRequest(BaseModel):
        communication_text: str = Field(..., min_length=1, max_length=5000)
        channel_type: str = Field(..., pattern="^(sms|email|url|website|whatsapp|text|SMS|WhatsApp)$")
        metadata: Dict[str, Any] = Field(default_factory=dict)
        language_preference: Optional[str] = "en"

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
    class AnalysisRequest:
        communication_text: str
        channel_type: str
        metadata: Dict[str, Any] = field(default_factory=dict)
        language_preference: Optional[str] = "en"

        def __init__(self, **data):
            communication_text = data.get("communication_text")
            channel_type = data.get("channel_type")
            metadata = data.get("metadata", {})
            language_preference = data.get("language_preference", "en")

            if not isinstance(communication_text, str) or not communication_text.strip():
                _validation_error("communication_text", "communication_text must be a non-empty string", communication_text)
            if len(communication_text) > 5000:
                _validation_error("communication_text", "communication_text must be at most 5000 characters", communication_text)
            if _contains_control_chars(communication_text):
                _validation_error("communication_text", "communication_text contains unsupported control characters", communication_text)
            if not isinstance(channel_type, str) or not re.match(r"^(sms|email|url|website|whatsapp|text|SMS|WhatsApp)$", channel_type):
                _validation_error("channel_type", "channel_type is invalid", channel_type)
            if metadata is None:
                metadata = {}
            if not isinstance(metadata, dict):
                _validation_error("metadata", "metadata must be an object", metadata)
            if len(metadata) > 20:
                _validation_error("metadata", "metadata must not contain more than 20 keys", metadata)
            for key, value in metadata.items():
                if not isinstance(key, str) or not key.strip():
                    _validation_error("metadata", "metadata keys must be non-empty strings", metadata)
                if len(key) > 64:
                    _validation_error("metadata", "metadata keys must be at most 64 characters", metadata)
                if isinstance(value, str) and len(value) > 512:
                    _validation_error("metadata", "metadata string values must be at most 512 characters", metadata)
                if isinstance(value, str) and _contains_control_chars(value):
                    _validation_error("metadata", "metadata contains unsupported control characters", metadata)
            if language_preference is not None and not isinstance(language_preference, str):
                _validation_error("language_preference", "language_preference must be a string", language_preference)
            if isinstance(language_preference, str) and len(language_preference) > 16:
                _validation_error("language_preference", "language_preference must be at most 16 characters", language_preference)

            self.communication_text = communication_text
            self.channel_type = channel_type
            self.metadata = metadata
            self.language_preference = language_preference
