from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class AnalysisRequest(BaseModel):
    communication_text: str = Field(..., min_length=1, max_length=5000)
    channel_type: str = Field(..., pattern="^(sms|email|url|website|whatsapp|text|SMS|WhatsApp)$")
    metadata: Dict[str, Any] = Field(default_factory=dict)
    language_preference: Optional[str] = "en"
