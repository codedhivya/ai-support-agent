from sqlalchemy import Column, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

import uuid


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id")
    )

    chunk_index = Column(
        Integer,
        nullable=False
    )

    content = Column(
        Text,
        nullable=False
    )