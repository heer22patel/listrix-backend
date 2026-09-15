"""
Naive keyword search over the KnowledgeBase table.

This is intentionally simple (no vector DB / embeddings) to match the
project's scope: it scores rows by how many query keywords appear in
their title/content and returns the top matches. It's adequate for a
knowledge base of tens to low hundreds of entries. If the knowledge
base grows much larger, swap this for a vector-embedding search
(e.g. pgvector, a hosted vector store, or OpenAI embeddings) behind
the same `search_knowledge` signature.
"""

import re
from typing import List

from sqlalchemy.orm import Session

from models.knowledge import KnowledgeBase

_STOPWORDS = {
    "the", "a", "an", "is", "are", "do", "does", "what", "how", "can",
    "you", "your", "i", "to", "of", "for", "in", "on", "and", "or",
    "about", "with", "me", "my", "it", "this", "that", "be", "have",
}


def _keywords(text: str) -> List[str]:
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return [w for w in words if w not in _STOPWORDS and len(w) > 2]


def search_knowledge(db: Session, query: str, limit: int = 4) -> List[KnowledgeBase]:
    keywords = _keywords(query)
    if not keywords:
        return []

    entries = db.query(KnowledgeBase).all()
    scored: List[tuple[int, KnowledgeBase]] = []
    for entry in entries:
        haystack = f"{entry.title} {entry.content}".lower()
        score = sum(haystack.count(kw) for kw in keywords)
        if score > 0:
            scored.append((score, entry))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [entry for _, entry in scored[:limit]]
