from app.db.database import engine, Base
from app.models.user import User
from app.models.document import Document
from app.models.document_content import DocumentContent
from app.models.document_chunk import DocumentChunk
from app.models.document_embedding import DocumentEmbedding
from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage

Base.metadata.create_all(bind=engine)

print("Tables Created")