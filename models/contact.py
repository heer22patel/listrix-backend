from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func

from database import Base


class Contact(Base):
    """A visitor's submitted contact request."""

    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    phone = Column(String(50), nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)
