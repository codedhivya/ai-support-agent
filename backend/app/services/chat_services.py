from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from typing import AsyncGenerator
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2,
    api_key=OPENAI_API_KEY
)


async def generate_answer(
    question: str,
    context: str,
    chat_history: list[dict]
) -> str:
    system_instruction = (
        "You are an expert AI support assistant.\n"
        "Your task is to answer the user's question accurately, relying strictly on the provided Knowledge Base Context.\n\n"
        "Rules:\n"
        "1. Base your answer ONLY on the provided Knowledge Base Context. Do not use external information or make up facts.\n"
        "2. If the answer cannot be found in the context, politely state: 'I am sorry, but I do not have enough information in the knowledge base to answer that.'\n"
        "3. You MUST cite the source document name (e.g., [document_name.pdf]) for any facts you extract. If multiple documents are referenced, cite them appropriately.\n"
        "4. Keep your responses clear, helpful, and concise."
    )

    messages = [
        SystemMessage(content=system_instruction)
    ]

    for msg in chat_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=f"Knowledge Base Context:\n{context}\n\nCurrent Question: {question}"))

    response = await model.ainvoke(messages)
    return response.content


async def generate_answer_stream(
    question: str,
    context: str,
    chat_history: list[dict]
) -> AsyncGenerator[str, None]:
    system_instruction = (
        "You are an expert AI support assistant.\n"
        "Your task is to answer the user's question accurately, relying strictly on the provided Knowledge Base Context.\n\n"
        "Rules:\n"
        "1. Base your answer ONLY on the provided Knowledge Base Context. Do not use external information or make up facts.\n"
        "2. If the answer cannot be found in the context, politely state: 'I am sorry, but I do not have enough information in the knowledge base to answer that.'\n"
        "3. You MUST cite the source document name (e.g., [document_name.pdf]) for any facts you extract. If multiple documents are referenced, cite them appropriately.\n"
        "4. Keep your responses clear, helpful, and concise."
    )

    messages = [
        SystemMessage(content=system_instruction)
    ]

    for msg in chat_history:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "user":
            messages.append(HumanMessage(content=content))
        else:
            messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=f"Knowledge Base Context:\n{context}\n\nCurrent Question: {question}"))

    async for chunk in model.astream(messages):
        if chunk.content:
            yield chunk.content