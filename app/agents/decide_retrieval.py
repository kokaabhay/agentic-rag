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


def decide_retrieve(prompt: str) -> bool:
    response = client.chat.completions.create(
        model=AZURE_CHAT_DEPLOYMENT,
        messages=[
            {
                "role": "system",
                "content": (
                    """
                    The user will ask a query and it will be forwarded to the customer support agent bot
                    The usecase is to answer from policy documents of our product and our product is smarthome hub                                        
                    You are given a user prompt and you need to decide whether retrieval is actually needed or if the question can be answered without retrieval
                    product intro(keep in mind):SmartHome Hub is a home automation device that allows customers to connect 
                    and control compatible smart lights, thermostats, security devices, and other smart-home 
                    products from a single application
                    for example:-
                    user:Good morning,Hello-> not needed
                    user:what is your product?-> the bot needs to get context from documents to answer the question correctly
                    Remember the question is supposed to be relevant to our product
                    Return False if retrieval is not needed and True if it is needed based on the user query"""
                                                    ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
   
        temperature=0,
    )

    result= response.choices[0].message.content.strip()
    return result=="True"

#print(type(bool(decide_retrieve("I need a product...ans also calcium is not healthy for body...i want to buy calicum"))))
