from pydantic import BaseModel, Field
from typing import List, Optional

class AskRequest(BaseModel):
    query: str = Field(..., description="Customer support question or query")

class AskResponse(BaseModel):
    answer: str
    sources: List[str]
    intent: str
    confidence: float