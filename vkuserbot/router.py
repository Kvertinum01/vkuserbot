from typing import Dict, Any, List, Optional, Callable
from .message import Message
import vkuserbot.user as user

class Router:
    def __init__(self, bot: "user.User") -> None:
        self._bot = bot
        self._to_handle: Dict[dict] = {}
        self._events_to_handle: Dict[dict] = {}

    def _new_handle(
        self,
        func: Optional[Callable],
        from_where: Optional[str],
        event: Optional[int],
        cmds: Optional[List[str]],
        texts: Optional[List[str]]
    ) -> None:
        to_handle_dict: Dict[str, Any] = {
            "func": func,
            "from": from_where,
            "is_text": False,
            "is_cmd": False,
            "is_event": False
        }
        if event is not None:
            to_handle_dict["is_event"] = True
            self._events_to_handle.update(
                {event: to_handle_dict}
            )
        elif cmds is not None:
            to_handle_dict["is_cmd"] = True
            for command in cmds:
               self._to_handle.update(
                   {command: to_handle_dict}
               )
        else:
            to_handle_dict["is_text"] = True
            for text in texts:
                self._to_handle.update(
                   {text: to_handle_dict}
               )

    async def _check_handle(self, handle_text: Dict[str, Any]) -> None:
        mes = Message(self._bot)
        last_text: str = self._bot.last_message["text"]
        handle = self._to_handle[handle_text]
        func = handle["func"]
        if handle["from"] != "*":
            if handle["from"] != mes.from_where:
                return
        if handle["is_text"]:
            if handle_text is None or last_text == handle_text:
                await func(mes)
        elif handle["is_cmd"]:
            cmd_args = last_text.split(" ")
            if cmd_args[0] in handle["cmd"]:
                await func(
                    mes, tuple(cmd_args[1:])
                )
        elif handle["is_event"]:
            if handle["event"] == self._bot.longpoll.event:
                await func(
                    self._bot.longpoll._longpoll_result["updates"]
                )