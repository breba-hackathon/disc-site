import uuid
import httpx
from common.model import SendTaskRequest, SendTaskResponse, JSONRPCMessage, TaskSendParams


class A2AClient:
    def __init__(self, agent_url: str):
        self.url = agent_url.rstrip("/") + "/"

    async def _send_request(self, request: JSONRPCMessage) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.post(self.url, json=request.model_dump(exclude_none=True))
            response.raise_for_status()
            return response.json()

    async def send_task(self, payload: TaskSendParams) -> SendTaskResponse:
        request = SendTaskRequest(
            params=payload,
            id=str(uuid.uuid4())  # or pass your own
        )
        response_data = await self._send_request(request)
        return SendTaskResponse(**response_data)
