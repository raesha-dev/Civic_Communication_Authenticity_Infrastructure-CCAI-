from pydantic import BaseModel, Field

class TranslationRequest(BaseModel):
    analysis_id: str = Field(..., description="ID from a previous successful analysis")
    original_text: str = Field(..., min_length=1)
    target_lang: str = Field(..., min_length=2, max_length=5)
    
class AppealRequest(BaseModel):
    analysis_id: str = Field(...)
    reason: str = Field(..., min_length=10, max_length=1000)
    contact_email: str = Field(..., pattern=r"^\S+@\S+\.\S+$")
