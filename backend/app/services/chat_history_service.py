from app.models.chat_session import ChatSession
from app.models.chat_message import ChatMessage

def get_recent_messages(
    db,
    session_id,
    limit=10
):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at.desc()
        )
        .limit(limit)
        .all()
    )

    return list(reversed(messages))





def get_messages(
    db,
    session_id
):

    messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.session_id == session_id
        )
        .order_by(
            ChatMessage.created_at.asc()
        )
        .all()
    )

    return messages


def create_session(db):

    session = ChatSession()

    db.add(session)
    db.commit()
    db.refresh(session)

    return session


def save_message(
    db,
    session_id,
    role,
    content
):

    message = ChatMessage(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)
    db.commit()

    return message