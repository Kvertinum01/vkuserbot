from .message import Message
from typing import Dict, Any


class EmptyMiddleware:
    async def before(
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        return message

    def after(message: Message) -> Message:
        return message