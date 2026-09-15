from typing import Optional

from pydantic import BaseModel, Field


class KnowledgeCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    category: Optional[str] = Field(default=None, max_length=100)


class KnowledgeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, max_length=100)


class KnowledgeResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]

    model_config = {"from_attributes": True}
