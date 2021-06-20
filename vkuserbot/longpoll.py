from .tools import VkuserbotClass
from .user import *

class Longpoll(VkuserbotClass):
    def __init__(self, bot: "User") -> None:
        self._bot = bot
        bot.loop.run_until_complete(
            self._init_longpoll()
        )

    async def _init_longpoll(self):
        self._longpoll = await self._bot.method("messages.getLongPollServer")
        self._longpoll_url = "https://" + self._longpoll["server"]
        self.ts = self._longpoll["ts"]

    async def listener(self):
        while True:
            self._longpoll_result = await self._bot.post(self._longpoll_url, {
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
                for handle in self._bot._events_to_handle:
                    await self._bot._check_handle(handle)
                if self.event != 4:
                    continue
                vk_event = await self._bot.method(
                    "messages.getById", {"message_ids": update[1]}
                )
                yield vk_event["items"][0]