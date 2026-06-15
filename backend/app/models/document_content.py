from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base

import uuid


class DocumentContent(Base):
    __tablename__ = "document_contents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id")
    )

    content = Column(
        Text,
        nullable=False
    )