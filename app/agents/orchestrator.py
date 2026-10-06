from openai import AzureOpenAI
import json

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

AGENTS = {
    "rag_agent": {
        "description": "Answers questions using the company's knowledge base."
    # },
    # "order_agent": {
    #     "description": "Checks order status and order information."
    # },
    # "support_agent": {
    #     "description": "Handles general customer support conversations."
    # }
    }
}


class Orchestrator:

    def __init__(self):
        pass
        

    def orchestrate(user_query: str):
        tools=[]
        system_prompt = f"""
        You are the orchestrator of a customer-support agentic AI system.
        Your job is NOT to answer the user's question directly.
        Your job is to decide which knowledge base should be used
        to retrieve information for answering the user's question.
        There are two knowledge bases.

        DOCUMENT 1:
        This document provides customer support representatives with
        information and standard responses for common customer questions
        and issues.

        It primarily covers:
        - hardware
        - Wi-Fi
        - device pairing
        - common troubleshooting
        - standard customer support issues

        DOCUMENT 2:
        This document focuses on:
        - account management
        - household access
        - service configuration
        - device ownership
        - notifications
        - customer data requests

        It is intended for situations that are different from
        hardware, Wi-Fi, and device-pairing troubleshooting.

        Your task is to determine whether the user's question requires
        information from document 1, document 2, or both.

        Return ONLY valid JSON.

        The JSON format must be:

        {{
            "documents": "1",
            "reason": "Explain why this document was selected."
        }}

        The "documents" field MUST contain exactly one of:

        "1"
        "2"
        "both"

        Do not answer the user's question.

        Re-Written user query:
        {user_query}
        """

        response = client.chat.completions.create(
            model=AZURE_CHAT_DEPLOYMENT,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            temperature=0,
            tools=tools
        )
        decision = json.loads(response.choices[0].message.content)
        return decision










# """ from openai import AzureOpenAI
# import json

# client = AzureOpenAI(
#     api_key="AZURE_API_KEY",
#     api_version="2024-10-21",
#     azure_endpoint="AZURE_ENDPOINT"
# )

# DEPLOYMENT = "gpt-4.1"


# AGENTS = {
#     "rag_agent": {
#         "description": "Answers questions using the company's knowledge base."
#     },
#     "order_agent": {
#         "description": "Checks order status and order information."
#     },
#     "support_agent": {
#         "description": "Handles general customer support conversations."
#     }
# }


# def orchestrate(user_query: str):

#     system_prompt = f"""
# You are the orchestrator of a customer-support agentic AI system.

# Your job is NOT to answer the user's question directly.

# Your job is to decide which agent should handle the request.

# Available agents:

# {json.dumps(AGENTS, indent=2)}

# Return ONLY valid JSON in this format:

# {{
#     "agent": "rag_agent",
#     "reason": "The user is asking about information contained in the knowledge base."
# }}

# Choose exactly one agent.

# User query:
# {user_query}
# """

#     response = client.chat.completions.create(
#         model=DEPLOYMENT,
#         messages=[
#             {
#                 "role": "system",
#                 "content": system_prompt
#             }
#         ],
#         temperature=0
#     )

#     decision = json.loads(response.choices[0].message.content)

#     return decision """