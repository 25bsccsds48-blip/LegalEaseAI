from pydantic import BaseModel

class DocumentRequest(BaseModel):
    document_type: str
    details: str

class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str
    mock: bool