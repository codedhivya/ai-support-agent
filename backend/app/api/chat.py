from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.schemas.chat import QuestionRequest
from app.services.embedding_service import generate_embedding
from app.services.search_service import search_similar_chunks
from app.services.chat_services import generate_answer
from app.services.chat_history_service import create_session, save_message

from app.services.chat_history_service import get_messages
from app.services.chat_history_service import get_recent_messages

router = APIRouter()

@router.get("/{session_id}/messages")
def get_chat_messages(
    session_id: str,
    db: Session = Depends(get_db)
):

    messages = get_messages(
        db,
        session_id
    )

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at
            }
            for msg in messages
        ]
    }


@router.post("/ask")
def ask_question(
    request: QuestionRequest,
    db: Session = Depends(get_db)
):

  # Save user's question
    save_message(
        db,
        request.session_id,
        "user",
        request.question
    )
    
    query_embedding = generate_embedding(
        request.question
    )

    chunks = search_similar_chunks(
        db,
        query_embedding
    )

    context = "\n\n".join(
    [row[2] for row in chunks])

    sources = []

    for row in chunks:
        sources.append(
        {
            "document": row[0],
            "chunk_index": row[1],
            "content": row[2]
        }
    )
        
    history = get_recent_messages(
    db,
    request.session_id
    )
    chat_history = "\n".join(
    [
        f"{msg.role}: {msg.content}"
        for msg in history
    ]
)


    answer = generate_answer(
    request.question,
    context,
    chat_history
)

    save_message(
    db,
    request.session_id,
    "assistant",
    answer
)

    return {
        "question": request.question,
        "answer": answer,
        "sources": sources
    }

@router.post("/session")
def create_chat_session(
    db: Session = Depends(get_db)
):

    session = create_session(db)

    return {
        "session_id": str(session.id)
    }