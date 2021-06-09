from .user import User
from typing import Optional, Dict, Any, List
from copy import copy
import aiofiles


class Message:
    def __init__(self, bot: User) -> None:
        self.init_none_vars()
        self._bot = bot
        self.data: dict = copy(bot.last_message)
        for name, value in self.data.items():
            self.__dict__[name] = value
        self.session = self._bot.session
        self.mes_id: int = self.data["id"]
        self.attachments_in_message = (
            False if not len(self.attachments) else True
        )

    def init_none_vars(self) -> None:
        self.text: Optional[str] = None
        self.from_id: Optional[int] = None
        self.peer_id: Optional[int] = None
        self.attachments: Optional[List[Dict[str, Any]]] = None

    async def answer(
        self,
        text: str,
        attachment: Optional[str] = None
    ) -> Dict[str, Any]:
        return await self._bot.send(
            peer_id=self.peer_id, message=text, attachment=attachment
        )

    async def reply(
        self, text: str,
        attachment: Optional[str] = None
    ) -> Dict[str, Any]:
        return await self._bot.reply(
            peer_id=self.peer_id,
            mes_id=self.mes_id,
            message=text,
            attachment=attachment
        )

    async def get_photo(self, file_to_save: str, img_index: int = 0) -> None:
        assert self.attachments_in_message, "В сообщении нет файлов."
        img_data = self.attachments
        if "photo" in img_data[img_index]:
            img_link = img_data[img_index]["photo"]["sizes"][-1]["url"]
            async with self.session.get(img_link) as response:
                img_p = await response.read()
            async with aiofiles.open(file_to_save, mode="wb") as file:
                await file.write(img_p)

    @property
    def from_where(self) -> str:
        return (
            "user" if self.from_id == self.peer_id else "chat"
        )
