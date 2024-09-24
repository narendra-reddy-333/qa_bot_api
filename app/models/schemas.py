
from pydantic import BaseModel
from typing import List, Dict

class QAResponse(BaseModel):
    results: Dict[str, str]