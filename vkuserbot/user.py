from .longpoll import Longpoll
from .waiter import Waiter
from .middleware import EmptyMiddleware
from .tools import (
    VkuserbotClass,
    VkApiError
)
from .router import Router
from .message import Message
from random import randint
from traceback import print_exc
from typing import (
    Any,
    List,
    Dict,
    Optional,
    Union,
    Callable
)
import asyncio
import aiohttp


class User(VkuserbotClass):
    def __init__(
        self,
        user_token: str,
        version: Optional[str] = None,
        server: Optional[str] = None,
        waiter: Optional[Waiter] = None,
        middleware: EmptyMiddleware = None
    ) -> None:
        # Base variables
        self.stop = False
        self.handle_errors: Dict[str, Callable] = {}
        self.server = server or "https://api.vk.com"
        self.event = None
        self.last_message = None

        # Settings
        self._base_params: Dict[str, str] = {
            "access_token": user_token,
            "v": version or "5.131"
        }
        self.SETTINGS = {
            "print_full_exc": True,
            "print_exc": False
        }

        # Init loop and settings
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            self.__init_settings()
        )

        # Tools
        self.waiter = waiter
        self.longpoll = Longpoll(self)
        self.router = Router(self)
        self.middleware = middleware or EmptyMiddleware

    async def method(
        self,
        name: str,
        params: Dict[str, Union[str, int]] = {}
    ) -> Dict[str, Any]:
        params.update(self._base_params)
        answer = await self.post(self.server + "/method/" + name, params)
        if "error" not in answer:
            return answer["response"]
        answer = answer["error"]
        errcode = str(answer["error_code"])
        if errcode in self.handle_errors:
            await self.handle_errors[errcode](answer)
        else:
            raise VkApiError(int(errcode), answer)

    async def send(
        self,
        user_id: Optional[int] = None,
        peer_id: Optional[int] = None,
        message: Optional[str] = None,
        attachment: Optional[str] = None,
        expire_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        type_to_name, type_to_value = (
            ("user_id", user_id)
            if user_id is not None else
            ("peer_id", peer_id)
        )
        plan_params = {
            type_to_name: type_to_value,
            "random_id": randint(-555555, 555555),
            "message": message,
            "attachment": attachment,
            "expire_ttl": expire_ttl
        }
        params = {}
        params.update(
            (k, v) for k, v in plan_params.items() if v is not None
        )
        return await self.method(
            "messages.send", params
        )

    async def reply(
        self, peer_id: int, mes_id: int, message: str,
        attachment: Optional[str] = None,
        expire_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        plan_params = {
            "peer_id": peer_id,
            "reply_to": mes_id,
            "random_id": randint(-555555, 555555),
            "message": message,
            "attachment": attachment,
            "expire_ttl": expire_ttl
        }
        params = {}
        params.update(
            (k, v) for k, v in plan_params.items() if v is not None
        )
        return await self.method(
            "messages.send", params
        )

    async def messages_get(self, count: int = 10) -> List[dict]:
        chats = await self.method("messages.getConversations")
        chats = chats["items"]
        chat_id = chats[0]["conversation"]["peer"]["id"]
        mes = await self.method(
            "messages.getHistory", {"peer_id": chat_id, "count": count}
        )
        return mes["items"]

    def handle(
        self,
        text: Optional[List[str]] = None,
        cmd: Optional[List[str]] = None,
        event: Optional[int] = None,
        from_where: str = "*"
    ) -> Callable:
        def get_func(func: Callable) -> Callable:
            async def wrapper() -> None:
                return None
            self.router._new_handle(
                func, from_where, event, cmd, text
            )
            return wrapper
        return get_func

    async def post(self, link: str, data: Dict[str, Any]) -> dict:
        async with self.session.post(link, data=data) as response:
            return await response.json(content_type=None)

    async def __init_settings(self):
        self.session = aiohttp.ClientSession()
        my_info = await self.method("users.get")
        self.my_id = my_info[0]["id"]

    async def __main_loop(self) -> None:
        while True:
            try:
                await self.loop_func()
                if self.stop:
                    continue
                async for message in self.longpoll.listener():
                    message = await self.middleware.before(message)
                    self.last_message = message
                    from_id = message["from_id"]
                    if (
                        self.waiter is not None and from_id != self.my_id
                    ):
                        str_peer_id = str(message["peer_id"])
                        if str_peer_id in self.waiter._in_wait_ids:
                            func_id = self.waiter._in_wait_ids[str_peer_id]
                            func_to_call = self.waiter._to_handle[func_id]
                            await func_to_call(Message(self))
                    for handle in self.router._to_handle:
                        await self.router._check_handle(handle)
            except KeyboardInterrupt:
                break
            except Exception as error:
                if self.SETTINGS["print_full_exc"]:
                    print_exc()
                if self.SETTINGS["print_exc"]:
                    print(error)

    def run(self) -> None:
        self.loop.run_until_complete(
            self.async_run()
        )

    async def async_run(self) -> None:
        await self.__main_loop()
        await self.session.close()

    async def loop_func(self) -> None:
        pass
