from .tools import post
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


class VkApiError(Exception):
    def __init__(self, code: int, text_error: str) -> None:
        self.code = code
        self.text_error = str(text_error)

    def __str__(self) -> str:
        return self.text_error


class User:
    def __init__(self, user_token: str) -> None:
        self._to_handle: List[dict] = []
        self._events_to_handle: List[dict] = []
        self.handle_errors: Dict[str, Callable] = {}
        self.server = "https://api.vk.com"
        self.token = user_token
        self.event = None
        self.last_message = None
        self._base_params: Dict[str, str] = {
            "access_token": self.token,
            "v": "5.131"
        }

    async def method(
        self,
        name: str,
        params: Dict[str, Union[str, int]] = {}
    ) -> Optional[Dict[str, Any]]:
        params.update(self._base_params)
        answer = await post(self.server + "/method/" + name, params)
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
    ) -> dict:
        type_to = "user_id" if user_id is not None else "peer_id"
        type_to_v = user_id if user_id is not None else peer_id
        return await self.method(
            "messages.send",
            {
                type_to: type_to_v,
                "random_id": randint(-555555, 555555),
                "message": message,
                "attachment": attachment,
            },
        )

    async def reply(
        self,
        peer_id: int,
        mes_id: int,
        message: str,
        attachment: Optional[str] = None
    ) -> dict:
        return await self.method(
            "messages.send",
            {
                "peer_id": peer_id,
                "reply_to": mes_id,
                "random_id": randint(-555555, 555555),
                "message": message,
                "attachment": attachment,
            },
        )

    async def get_messages(self, count: int = 10) -> list:
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
        cmd: Optional[str] = None,
        event: Optional[int] = None,
        from_where: str = "*"
    ) -> Callable:
        def get_func(func: Callable) -> Callable:
            async def wrapper() -> None:
                return None
            to_handle_dict: Dict[str, Any] = {"func": func, "from": from_where}
            if event is not None:
                to_handle_dict["event"] = event
                self._events_to_handle.append(to_handle_dict)
                return wrapper
            elif cmd is not None:
                to_handle_dict["cmd"] = cmd
            else:
                to_handle_dict["text"] = text
            self._to_handle.append(to_handle_dict)
            return wrapper
        return get_func

    async def __check_handle(self, handle: Dict[str, Any]) -> None:
        mes = Message(self)
        last_text: str = self.last_message["text"]
        func = handle["func"]
        if handle["from"] != "*":
            if handle["from"] != mes.from_where:
                return
        if "text" in handle:
            text = handle["text"]
            if text is None or last_text in text:
                await func(mes)
        elif "cmd" in handle:
            cmd_args = last_text.split()
            if cmd_args[0] == handle["cmd"]:
                await func(mes, cmd_args[1:])
        elif "event" in handle:
            if handle["event"] == self.event:
                await func(self._longpoll_result["updates"])

    async def __main_loop(self) -> None:
        my_info = await self.method("users.get")
        self._longpoll = await self.method("messages.getLongPollServer")
        self.my_id = my_info[0]["id"]
        longpoll_url = "https://" + self._longpoll["server"]
        self.ts = self._longpoll["ts"]
        while True:
            try:
                await self.loopfunc()
                self._longpoll_result = await post(longpoll_url, {
                    "act": "a_check",
                    "key": self._longpoll["key"],
                    "ts": self.ts,
                    "wait": 1,
                    "mode": 2,
                    "version": 3
                })
                self.ts = self._longpoll_result["ts"]
                if "updates" not in self._longpoll_result:
                    continue
                for update in self._longpoll_result["updates"]:
                    self.event = update[0]
                    for handle in self._events_to_handle:
                        await self.__check_handle(handle)
                    if self.event != 4:
                        continue
                    vk_event = await self.method(
                        "messages.getById", {"message_ids": update[1]}
                    )
                    self.last_message = vk_event["items"][0]
                    for handle in self._to_handle:
                        await self.__check_handle(handle)
            except Exception:
                print_exc()

    def run(self) -> None:
        asyncio.run(self.__main_loop())

    async def loopfunc(self) -> None:
        pass


from .message import _Message
Message = _Message
