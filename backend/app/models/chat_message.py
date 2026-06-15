from sqlalchemy import Column, Text, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from app.db.database import Base
import uuid


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id")
    )

    role = Column(
        String,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )