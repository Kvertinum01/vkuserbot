from .tools import VkuserbotClass
from typing import Dict, Any, Union
import vkuserbot.user as user
import json

UPDATE_T = Dict[Union[int, str], Union[int, str, dict]]

def parse_longpoll(update: UPDATE_T, my_id: int):
    message_info = {
        "message_id": update[1],
        "peer_id": update[3],
        "date": update[4],
        "text": update[5],
        "attachments": [],
        "from_id": my_id
    }
    for inf in update:
        if not isinstance(inf, dict):
            continue
        for name, value in inf.items():
            if isinstance(value, dict):
                message_info.update(
                    {name: value}
                )
                continue
            if name == "reply":
                value: Dict[str, int] = json.loads(value)
                message_info.update(
                    {"conversation_message_id": value["conversation_message_id"]}
                )
                continue
            if name == "attachments":
                value: Dict[str, int] = json.loads(value)
                message_info.update(
                    {"attachments": value}
                )
                continue
            if name == "from":
                message_info["from_id"] = value
                continue
            message_info.update(
                {name: value}
            )
    return message_info


class Longpoll(VkuserbotClass):
    def __init__(self, bot: "user.User") -> None:
        self._bot = bot
        bot.loop.run_until_complete(
            self._init_longpoll()
        )

    async def _init_longpoll(self) -> None:
        self._longpoll = await self._bot.method("messages.getLongPollServer")
        self._longpoll_url = "https://" + self._longpoll["server"]
        self.ts = self._longpoll["ts"]

    async def listener(self) -> Dict[str, Any]:
        while True:
            self._longpoll_result = await self._bot.post(self._longpoll_url, {
                "act": "a_check",
                "key": self._longpoll["key"],
                "ts": self.ts,
                "wait": 1,
                "mode": 234,
                "version": 3
            })
            self.ts = self._longpoll_result["ts"]
            if "updates" not in self._longpoll_result:
                continue
            for update in self._longpoll_result["updates"]:
                self.event = update[0]
                for handle in self._bot._events_to_handle:
                    await self._bot._check_handle(handle)
                if self.event != 4:
                    continue
                message = parse_longpoll(update, self._bot.my_id)
                yield message
