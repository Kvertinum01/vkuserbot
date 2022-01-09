from .tools import VkuserbotClass
from typing import Optional, Dict, Any, List
from copy import copy
import vkuserbot.user as user
import aiofiles


class Message(VkuserbotClass):
    def __init__(self, bot: "user.User") -> None:
        self.__init_none_vars()
        self._bot = bot
        self.data: dict = copy(bot.last_message)
        for name, value in self.data.items():
            self.__dict__[name] = value
        self.session = self._bot.session
        self.attachments_in_message = (
            False if not len(self.attachments) else True
        )
        plan_self = bot.middleware.after(self)
        self = (
            plan_self if plan_self is not None else self
        )

    def __init_none_vars(self) -> None:
        self.text: Optional[str] = None
        self.from_id: Optional[int] = None
        self.peer_id: Optional[int] = None
        self.message_id: Optional[int] = None
        self.conversation_message_id: Optional[int] = None
        self.attachments: Optional[
            List[Dict[str, Any]]
        ] = None

    async def answer(
        self,
        text: str,
        attachment: Optional[str] = None,
        expire_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        return await self._bot.send(
            peer_id=self.peer_id,
            message=text,
            attachment=attachment,
            expire_ttl=expire_ttl
        )

    async def reply(
        self, text: str,
        attachment: Optional[str] = None,
        expire_ttl: Optional[int] = None
    ) -> Dict[str, Any]:
        return await self._bot.reply(
            peer_id=self.peer_id,
            mes_id=self.message_id,
            message=text,
            attachment=attachment,
            expire_ttl=expire_ttl
        )

    async def get_photo_bytes(self, img_index: int = 0) -> None:
        assert self.attachments_in_message, "В сообщении нет файлов."
        img_data = self.attachments
        if "photo" in img_data[img_index]:
            img_link = img_data[img_index]["photo"]["sizes"][-1]["url"]
            async with self.session.get(img_link) as response:
                return await response.read()

    async def get_photo(self, file_to_save: str, img_index: int = 0) -> None:
        img_p = await self.get_photo_bytes(img_index)
        async with aiofiles.open(file_to_save, mode="wb") as file:
            await file.write(img_p)

    @property
    def from_where(self) -> str:
        return (
            "user" if self.from_id == self.peer_id else "chat"
        )
