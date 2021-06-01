from .user import User
from .tools import post
from typing import Optional
import aiofiles


class MesPhotoUploader:
    def __init__(self, bot: User) -> None:
        self._bot = bot

    async def upload(self, filename: str) -> str:
        server = await self._bot.method("photos.getMessagesUploadServer")
        server_url = server["upload_url"]
        async with aiofiles.open(filename, mode="rb") as file:
            file = await post(server_url, {"file": file})
        doc = await self._bot.method(
            "photos.save",
            {
                "album_id": server["album_id"],
                "server": file["server"],
                "photos_list": file["photo"],
                "hash": file["hash"],
            },
        )
        doc = doc[0]
        return "photo{}_{}".format(doc["owner_id"], doc["id"])


class MesDocUploader:
    def __init__(self, bot: User) -> None:
        self._bot = bot

    async def upload(
        self,
        filename: str,
        docname: str = "document",
        peer_id: Optional[int] = None,
        doctype: str = "doc",
    ) -> str:
        last_peer_id = self._bot.last_message["peer_id"]
        peer_id = (
            peer_id if peer_id is not None else last_peer_id
        )
        server = await self._bot.method(
            "docs.getMessagesUploadServer",
            {"type": doctype, "peer_id": peer_id},
        )
        server_url = server["upload_url"]
        async with aiofiles.open(filename, mode="rb") as doc_file:
            file = await post(server_url, {"file": doc_file})
        file = file["file"]
        doc = await self._bot.method(
            "docs.save", {"file": file, "title": docname}
        )
        doc = doc[doctype]
        return "doc{}_{}".format(doc["owner_id"], doc["id"])
