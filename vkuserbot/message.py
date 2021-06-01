from .user import User
from typing import Optional
from copy import copy
import aiohttp
import aiofiles


class _Message:
    def __init__(self, bot: User) -> None:
        self._bot = bot
        self.data = copy(bot.last_message)
        self.peer_id = self.data["peer_id"]
        self.mes_id = self.data["id"]
        attachments = self.data["attachments"]
        self.attachments = False if not len(attachments) else True

    async def answer(
        self,
        text: str,
        attachment: Optional[str] = None
    ) -> dict:
        return await self._bot.send(
            peer_id=self.peer_id, message=text, attachment=attachment
        )

    async def reply(
        self,
        text: str,
        attachment: Optional[str] = None
    ) -> dict:
        return await self._bot.reply(
            peer_id=self.peer_id,
            mes_id=self.mes_id,
            message=text,
            attachment=attachment
        )

    async def get_photo(self, file_to_save: str, img_index: int = 0) -> None:
        img_data = self.data["attachments"]
        assert self.attachments, "В сообщении нет файлов."
        if "photo" in img_data[img_index]:
            img_link = img_data[img_index]["photo"]["sizes"][-1]["url"]
            async with aiohttp.ClientSession() as session:
                async with session.get(img_link) as response:
                    img_p = await response.read()
            async with aiofiles.open(file_to_save, mode="wb") as file:
                await file.write(img_p)

    @property
    def from_where(self) -> str:
        return (
            "user" if self.data["from_id"] == self.data["peer_id"] else "chat"
        )
