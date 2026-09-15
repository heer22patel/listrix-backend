"""
Wraps calls to OpenAI's Responses API. This is the only place the
OpenAI API key is touched — it lives in `config.settings`, loaded from
an environment variable, and is never returned to the client.
"""

import logging
from typing import List

from openai import OpenAI, OpenAIError

from config import settings
from models.knowledge import KnowledgeBase

logger = logging.getLogger("listrix.openai_service")

_client = OpenAI(api_key=settings.OPENAI_API_KEY)

FALLBACK_REPLY = (
    "I couldn't find a verified answer to that question. "
    "Please contact our team for more information."
)

SYSTEM_PROMPT = """You are Listrix, the official AI assistant for Listora Digital Media,
a digital marketing and CRM agency focused on the real estate industry.

Your job is to help website visitors:
- understand Listora's services and how they work
- figure out which solution fits their situation
- get comfortable enough to book a strategy call
- get routed to a human when that's what they need

Tone: professional, helpful, friendly, and consultative. Write like a
knowledgeable team member having a real conversation — never robotic,
never stiff, no corporate filler.

Ground rules:
- Only answer using the verified context provided below. Do not use
  outside knowledge about Listora, and do not guess at pricing,
  timelines, or claims that aren't in the context.
- If the context does not contain the answer, reply with exactly:
  "I couldn't find a verified answer to that question. Please contact our team for more information."
- When it's a natural fit, invite the visitor to book a strategy call
  — but don't force it into every reply.
- Keep replies concise and easy to read in a chat widget (short
  paragraphs, no long essays).
"""


def _build_context_block(entries: List[KnowledgeBase]) -> str:
    if not entries:
        return "No verified context was found for this question."
    return "\n\n".join(
        f"[{entry.category or 'General'}] {entry.title}\n{entry.content}"
        for entry in entries
    )


def generate_reply(user_message: str, history: List[dict], knowledge_entries: List[KnowledgeBase]) -> str:
    """Call the Responses API and return the assistant's reply text.

    `history` is the client-supplied, in-memory conversation (never
    persisted server-side). `knowledge_entries` are the top matches
    from `knowledge_service.search_knowledge`.
    """
    context_block = _build_context_block(knowledge_entries)
    instructions = f"{SYSTEM_PROMPT}\n\nVerified context for this question:\n{context_block}"

    input_messages = [{"role": h["role"], "content": h["content"]} for h in history[-10:]]
    input_messages.append({"role": "user", "content": user_message})

    try:
        response = _client.responses.create(
            model=settings.OPENAI_MODEL,
            instructions=instructions,
            input=input_messages,
            max_output_tokens=500,
            temperature=0.6,
            # The Responses API stores conversation state server-side by
            # default. This project's requirement is "no saved chat
            # history" anywhere in the stack, so that's turned off here.
            store=False,
        )
        text = (response.output_text or "").strip()
        return text or FALLBACK_REPLY
    except OpenAIError:
        logger.exception("OpenAI Responses API call failed")
        return "I'm having trouble connecting right now. Please try again shortly, or contact our team directly."
