"""
One-time helper to populate the knowledge_base table with a starting
set of entries about Listora Digital Media.

IMPORTANT: the content below is placeholder copy based on the general
shape of the site (real estate-focused digital marketing + CRM,
Local SEO, case studies, packages). Review and replace each entry
with the exact, current copy from the live site before going live —
Listrix will only ever be as accurate as this table.

Run with:  python seed_knowledge.py
"""

from database import Base, SessionLocal, engine
from models.knowledge import KnowledgeBase

ENTRIES = [
    {
        "title": "What Listora Digital Media does",
        "content": (
            "Listora Digital Media is a digital marketing and CRM agency focused "
            "on the real estate industry. It helps real estate businesses attract "
            "more leads, stay organized with client relationships, and grow "
            "predictably through a combination of marketing and technology "
            "services."
        ),
        "category": "Company",
    },
    {
        "title": "Services overview",
        "content": (
            "Listora offers real estate-focused digital marketing and CRM "
            "solutions, including local SEO, broader digital marketing/lead "
            "generation, and CRM setup to help agencies manage and convert "
            "their leads."
        ),
        "category": "Services",
    },
    {
        "title": "Local SEO service",
        "content": (
            "Listora's Local SEO service helps real estate businesses rank "
            "higher in local search results (such as Google's local map pack) "
            "so nearby buyers and sellers can find them more easily."
        ),
        "category": "Services",
    },
    {
        "title": "CRM solutions",
        "content": (
            "Listora sets up and configures CRM systems for real estate "
            "businesses so leads, client communication, and follow-ups are "
            "organized in one place instead of scattered across spreadsheets "
            "and inboxes."
        ),
        "category": "Services",
    },
    {
        "title": "Case studies and results",
        "content": (
            "Listora publishes case studies on its site showing results it has "
            "delivered for real estate clients. Ask Listrix to point you to the "
            "case studies page, or a member of the team can walk through "
            "relevant examples on a strategy call."
        ),
        "category": "Proof",
    },
    {
        "title": "Packages and pricing",
        "content": (
            "Listora offers tiered packages rather than one-size-fits-all "
            "pricing, since needs vary by business size and goals. The best "
            "way to get exact pricing for your situation is to book a "
            "strategy call with the team."
        ),
        "category": "Pricing",
    },
    {
        "title": "Who Listora works with",
        "content": (
            "Listora works specifically with real estate businesses — agents, "
            "teams, and agencies — rather than general small businesses across "
            "every industry."
        ),
        "category": "Company",
    },
    {
        "title": "How to book a strategy call",
        "content": (
            "Visitors can request a strategy call directly through the site, "
            "or by sharing their name, email, and a short message with Listrix, "
            "which the team will follow up on."
        ),
        "category": "Contact",
    },
]


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_titles = {row.title for row in db.query(KnowledgeBase.title).all()}
        added = 0
        for entry in ENTRIES:
            if entry["title"] in existing_titles:
                continue
            db.add(KnowledgeBase(**entry))
            added += 1
        db.commit()
        print(f"Seed complete: {added} new entries added, {len(ENTRIES) - added} already existed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
