from openai import AsyncOpenAI
from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
    api_key=OPENAI_API_KEY
)


async def generate_embedding(text: str):

    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    return response.data[0].embedding