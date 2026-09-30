from openai import OpenAI

from config import (
    AZURE_CHAT_DEPLOYMENT,
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
   
)


client = OpenAI(
    base_url=f"{AZURE_OPENAI_ENDPOINT.rstrip('/')}/openai/v1/",
    api_key=AZURE_OPENAI_API_KEY,
)


def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=AZURE_CHAT_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a customer support assistant "
                    "that answers using a provided knowledge base."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
   
        temperature=0,
    )

    return response.choices[0].message.content.strip()