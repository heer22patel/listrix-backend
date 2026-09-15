from typing import List, Literal

from pydantic import BaseModel, Field, field_validator


class ChatMessage(BaseModel):
    """One turn of prior conversation, supplied by the client from its
    in-memory history. The backend never stores this."""

    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1, max_length=2000)


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    # Capped so a client can't balloon the prompt sent to OpenAI.
    history: List[ChatMessage] = Field(default_factory=list, max_length=20)

    @field_validator("message")
    @classmethod
    def message_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty.")
        return v


class ChatResponse(BaseModel):
    reply: str
    suggested_questions: List[str] = Field(default_factory=list)
