import os
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.core.current_user import get_current_user
from app.models.user import User

from app.services.document_services import create_document
from app.services.document_processor import extract_text
from app.models.document_content import DocumentContent
from app.services.chunking_service import chunk_text
from app.models.document_chunk import DocumentChunk
from app.services.embedding_service import generate_embedding
from app.models.document_embedding import DocumentEmbedding
from app.models.document import Document

router = APIRouter()

UPLOAD_DIR = "uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True
)

@router.get("")
def get_documents(
    db: Session = Depends(get_db)
):

    documents = db.query(Document).all()

    return [
        {
            "id": str(doc.id),
            "file_name": doc.file_name,
            "created_at": doc.created_at
        }
        for doc in documents
    ]



@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    document = create_document(
        db=db,
        file_name=file.filename,
        file_path=file_path,
        uploaded_by=current_user.id
    )

    text = extract_text(file_path)
    content = DocumentContent(
    document_id=document.id,
    content=text
)
    chunks = chunk_text(text)

    for index, chunk in enumerate(chunks):

         # Skip empty chunks
        if not chunk.strip():
            continue

        chunk_record = DocumentChunk(
        document_id=document.id,
        chunk_index=index,
        content=chunk
    )

        db.add(chunk_record)

        embedding = await generate_embedding(chunk)
        embedding_record = DocumentEmbedding(
        document_id=document.id,
        chunk_index=index,
        embedding=embedding
    )

        db.add(embedding_record)

    db.add(content)
    db.commit()
    return {
        "document_id": str(document.id),
        "file_name": document.file_name,
        "uploaded_by": str(current_user.id)
    }