from pydantic import BaseModel
from typing import Dict


class GetNoteInfoResponse(BaseModel):
    created_at: str
    updated_at: str


class GetNoteTextResponse(BaseModel):
    id: int
    text: str


class CreateNoteResponse(BaseModel):
    id: int


class GetNoteListResponse(BaseModel):
    notes: Dict[int, str]