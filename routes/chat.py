from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from config import limiter, settings
from database import get_db
from schemas.chat import ChatRequest, ChatResponse
from services.knowledge_service import search_knowledge
from services.openai_service import generate_reply

router = APIRouter()

DEFAULT_SUGGESTED_QUESTIONS = [
    "What services does Listora offer?",
    "Do you work with real estate businesses specifically?",
    "How do I book a strategy call?",
]


@router.post("/chat", response_model=ChatResponse)
@limiter.limit(settings.CHAT_RATE_LIMIT)
def chat(request: Request, payload: ChatRequest, db: Session = Depends(get_db)) -> ChatResponse:
    """
    Stateless chat turn: the client sends the current message plus its
    own in-memory history, we search the knowledge base, ask OpenAI,
    and return a reply. Nothing about this exchange is written to disk.
    """
    knowledge_entries = search_knowledge(db, payload.message)
    history = [turn.model_dump() for turn in payload.history]
    reply = generate_reply(payload.message, history, knowledge_entries)

    return ChatResponse(reply=reply, suggested_questions=DEFAULT_SUGGESTED_QUESTIONS)
