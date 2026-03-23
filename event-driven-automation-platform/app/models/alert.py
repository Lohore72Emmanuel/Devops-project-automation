from pydantic import BaseModel, Field
from typing import Optional, Dict, Any


class Alert(BaseModel):
    name: str = Field(..., min_length=1)
    severity: str = Field(..., min_length=1)
    source: str = Field(..., min_length=1)
    details: Optional[str] = ""
    metadata: Dict[str, Any] = {}
