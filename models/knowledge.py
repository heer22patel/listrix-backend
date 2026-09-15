from sqlalchemy import Column, Integer, String, Text

from database import Base


class KnowledgeBase(Base):
    """A single verified fact/answer about Listora Digital Media that Listrix may cite."""

    __tablename__ = "knowledge_base"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(100), nullable=True, index=True)
