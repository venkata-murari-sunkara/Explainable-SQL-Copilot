from pydantic import BaseModel
from typing import List, Dict, Any

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    sql: str
    explanation: str

class ExecuteRequest(BaseModel):
    sql: str

class ExecuteResponse(BaseModel):
    rows: List[Dict[str, Any]]