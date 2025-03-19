from aiohttp import web
import json
import random
import os
import logging
import aiohttp_cors

DEFAULT_OK_RATIO = 0.6
DEFAULT_PORT = 8080

_message_factory = None

logging.basicConfig(level=logging.INFO)


class Message:
    def __init__(self, message: str, ok: bool):
        self._message = message
        self._ok = ok

    @property
    def ok(self) -> bool:
        return self._ok

    def to_json(self) -> str:
        return json.dumps({"message": self._message})


class MessageFactory:
    def __init__(self, ok_ratio: float):
        self._ok_ratio: float = ok_ratio

    def create_message(self) -> Message:
        if random.random() < self._ok_ratio:
            return Message("good", ok=True)
        else:
            return Message("bad", ok=False)


async def index_handler(request: web.Request) -> web.Response:
    message = _message_factory.create_message()
    args = {"text": message.to_json()}
    if not message.ok:
        args["status"] = 500
    return web.json_response(**args)


def main():
    global _message_factory

    ok_ratio = float(os.getenv("OK_RATIO", DEFAULT_OK_RATIO))
    if not (0 <= ok_ratio <= 1):
        raise ValueError("OK_RATIO should be between 0 and 1: {ok_ratio=}")
    logging.info(f"{ok_ratio=}")
    _message_factory = MessageFactory(ok_ratio)

    port = int(os.getenv("PORT", DEFAULT_PORT))
    logging.info(f"{port=}")

    app = web.Application()
    cors = aiohttp_cors.setup(app)
    resource = cors.add(app.router.add_resource("/"))
    cors.add(
        resource.add_route("GET", index_handler),
        {"*": aiohttp_cors.ResourceOptions(allow_credentials=False)},
    )

    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
