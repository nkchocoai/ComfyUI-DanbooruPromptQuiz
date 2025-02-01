from server import PromptServer
from aiohttp import web
import time


class MessageHolder:
    messages = {}

    @classmethod
    def addMessage(cls, id, message):
        cls.messages[str(id)] = message

    @classmethod
    def waitForMessage(cls, id, period=0.1):
        sid = str(id)
        while not (sid in cls.messages):
            time.sleep(period)
        message = cls.messages.pop(str(id), "")
        return message


routes = PromptServer.instance.routes


@routes.post("/dpq_submit")
async def submit_answer(request):
    post = await request.post()
    MessageHolder.addMessage(post.get("id"), post.get("input"))
    return web.json_response({})
