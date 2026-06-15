from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(
    question,
    context,
    chat_history
):

    prompt = f"""
You are a helpful AI support assistant.

Previous Conversation:
{chat_history}

Knowledge Base Context:
{context}

Current Question:
{question}

Answer using the knowledge base context.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content