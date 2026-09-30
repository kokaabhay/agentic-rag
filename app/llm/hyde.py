

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


def generate_hypothetical_answer(query: str) -> str:
    """
    Generate a hypothetical answer to the user's question into a concise search reference 
    optimized for semantic based knowledge-base retrieval.
    """

    response = client.chat.completions.create(
        model=AZURE_CHAT_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    "Generate a concise hypothetical answer that represents "
                    "the information likely to be found in a customer-support "
                    "knowledge base. Include important technical terms and "
                    "concepts from the user's question. "
                    "Do not mention that the answer is hypothetical. "
                    "Do not add unrelated information. "
                    "Return only the hypothetical answer."
                    
                ),
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        temperature=0,
    )

    hypothetical_answer = response.choices[0].message.content.strip()

    return hypothetical_answer