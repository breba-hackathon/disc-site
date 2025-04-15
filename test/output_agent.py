import asyncio
import os
from uuid import uuid4

import httpx

from common.client import A2AClient
from common.model import TaskSendParams, TextPart, Message

PUBSUB_URL: str = "http://127.0.0.1:8000"
PUSH_ENDPOINT: str = "http://my-localhost:7999/echo"
OUTPUT_AGENT_TOPIC: str = "output_agent_topic"

url = f"{PUBSUB_URL}/subscribe"


async def send_task_to_agent_direct(session_id: str):
    client = A2AClient("http://localhost:8001")

    # Build structured message
    message = Message(
        role="user",
        parts=[
            TextPart(text="Generate a site for my birthday. I'm turning 18. My birthday is on June 11 and the theme is 1990s.")
        ]
    )

    # Wrap in TaskSendParams
    task_params = TaskSendParams(
        id=f"task-{uuid4().hex}",
        sessionId=session_id,
        message=message
    )

    # Send the task
    response = await client.send_task(task_params.model_dump(exclude_none=True))

    # Print the structured response
    print(response.model_dump())


def subscribe_to_agent():
    payload = {
        "topic": OUTPUT_AGENT_TOPIC,
        "endpoint": PUSH_ENDPOINT
    }

    headers = {"Content-Type": "application/json"}

    response = httpx.post(url, json=payload, headers=headers)

    print(response.status_code)
    print(response.json())


session_id = os.environ.get("SESSION_ID")
asyncio.run(send_task_to_agent_direct(session_id))
