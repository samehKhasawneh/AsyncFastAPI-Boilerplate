import httpx
from app.core.logging import logger


async def log_request(request):
    logger.info(
        f"Request event hook: {request.method} {request.url} - Waiting for response"
    )


async def log_response(response):
    request = response.request
    logger.info(
        f"Response event hook: {request.method} {request.url} - Status {response.status_code}"
    )


class HTTPService:
    @staticmethod
    async def request(method: str, url: str, headers: dict = None, data: dict = None):
        client = httpx.AsyncClient(
            headers=headers,
            event_hooks={"request": [log_request], "response": [log_response]},
        )

        try:
            response = await client.request(method, url, json=data)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}"
            )

            return None
        finally:
            await client.aclose()