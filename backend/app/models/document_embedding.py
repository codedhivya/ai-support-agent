from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector

from app.db.database import Base

import uuid


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"

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

    embedding = Column(
        Vector(1536)
    )