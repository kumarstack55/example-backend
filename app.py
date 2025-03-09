from aiohttp import web
import json
import random
import os
import logging

DEFAULT_ERROR_SUCCESS_COUNT = 90
DEFAULT_ERROR_FAILURE_COUNT = 10
DEFAULT_PORT = 8080

logging.basicConfig(level=logging.INFO)

_message_factory = None


class Message:
    def __init__(self, message: str, success: bool = True):
        self._message = message
        self._success = success

    @property
    def success(self) -> bool:
        return self._success

    def to_json(self) -> str:
        return json.dumps({"message": self._message})


class MessageFactory:
    def __init__(self, success_count: int, error_count: int):
        self._success_rate: float = success_count / (success_count + error_count)

    def create_message(self) -> Message:
        if random.random() < self._success_rate:
            return Message("ok")
        else:
            return Message("bad", success=False)


async def index_handler(request: web.Request) -> web.Response:
    message = _message_factory.create_message()
    if message.success:
        return web.Response(text=message.to_json(), content_type="application/json")
    else:
        return web.Response(text=message.to_json(), content_type="application/json", status=500)


def main():
    global _message_factory

    ERROR_SUCCESS_COUNT = int(os.getenv("ERROR_SUCCESS_COUNT", DEFAULT_ERROR_SUCCESS_COUNT))
    ERROR_FAILURE_COUNT = int(os.getenv("ERROR_FAILURE_COUNT", DEFAULT_ERROR_FAILURE_COUNT))
    _message_factory = MessageFactory(ERROR_SUCCESS_COUNT, ERROR_FAILURE_COUNT)

    port = int(os.getenv("PORT", DEFAULT_PORT))

    app = web.Application()
    app.router.add_get("/", index_handler)
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
