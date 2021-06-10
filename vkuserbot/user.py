from .waiter import Waiter
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


class VkApiError(Exception):
    def __init__(self, code: int, text_error: dict) -> None:
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
        self.waiter: Optional[Waiter] = None
        self._base_params: Dict[str, str] = {
            "access_token": self.token,
            "v": "5.131"
        }
        self.SETTINGS = {
            "print_full_exc": True,
            "print_exc": False
        }
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            self.__init_settings()
        )

    def __repr__(self) -> str:
        res_class_info = "User("
        class_vars = []
        for name, value in self.__dict__.items():
            if name[0] == "_":
                continue
            class_vars.append(name + "=" + str(value))
        str_class_vars = ", ".join(class_vars)
        res_class_info += str_class_vars + ")"
        return res_class_info

    async def method(
        self,
        name: str,
        params: Dict[str, Union[str, int]] = {}
    ) -> Optional[Dict[str, Any]]:
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
        params = {
            type_to_name: type_to_value,
            "random_id": randint(-555555, 555555),
            "message": message,
            "attachment": attachment,
            "expire_ttl": None
        }
        if expire_ttl is not None:
            params["expire_ttl"] = expire_ttl
        return await self.method(
            "messages.send", params
        )

    async def reply(
        self, peer_id: int, mes_id: int, message: str,
        attachment: Optional[str] = None,
        expire_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        params = {
            "peer_id": peer_id,
            "reply_to": mes_id,
            "random_id": randint(-555555, 555555),
            "message": message,
            "attachment": attachment,
        }
        if expire_ttl is not None:
            params["expire_ttl"] = expire_ttl
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
            to_handle_dict: Dict[str, Any] = {"func": func, "from": from_where}
            if event is not None:
                to_handle_dict.update({"event": event})
                self._events_to_handle.append(to_handle_dict)
                return wrapper
            elif cmd is not None:
                to_handle_dict["cmd"] = cmd
            else:
                to_handle_dict["text"] = text
            self._to_handle.append(to_handle_dict)
            return wrapper
        return get_func

    async def post(self, link: str, data: Dict[str, Union[str, int]]) -> dict:
        async with self.session.post(link, data=data) as response:
            return await response.json(content_type=None)

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
            cmd_args = last_text.split(" ")
            if cmd_args[0] in handle["cmd"]:
                await func(mes, " ".join(cmd_args[1:]))
        elif "event" in handle:
            if handle["event"] == self.event:
                await func(self._longpoll_result["updates"])

    async def __init_settings(self):
        self.session = aiohttp.ClientSession()
        my_info = await self.method("users.get")
        self._longpoll = await self.method("messages.getLongPollServer")
        self.my_id = my_info[0]["id"]
        self._longpoll_url = "https://" + self._longpoll["server"]
        self.ts = self._longpoll["ts"]

    async def __main_loop(self) -> None:
        while True:
            try:
                await self.loop_func()
                self._longpoll_result = await self.post(self._longpoll_url, {
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
                    from_id = self.last_message["from_id"]
                    if (
                        self.waiter is not None and from_id != self.my_id
                    ):
                        str_peer_id = str(self.last_message["peer_id"])
                        if str_peer_id in self.waiter._in_wait_ids:
                            func_id = self.waiter._in_wait_ids[str_peer_id]
                            func_to_call = self.waiter._to_handle[func_id]
                            await func_to_call(Message(self))
                    for handle in self._to_handle:
                        await self.__check_handle(handle)
            except KeyboardInterrupt:
                break
            except Exception as error:
                if self.SETTINGS["print_full_exc"]:
                    print_exc()
                if self.SETTINGS["print_exc"]:
                    print(error)

    def run(self) -> None:
        try:
            self.loop.run_until_complete(
                self.__main_loop()
            )
        except KeyboardInterrupt:
            pass

    async def async_run(self) -> None:
        await self.__main_loop()

    async def loop_func(self) -> None:
        pass


from .message import Message
