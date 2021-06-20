from typing import Dict, Any


class VkuserbotClass:
    def __repr__(self) -> str:
        res_class_info = self.__class__.__name__ + "("
        class_vars = []
        for name, value in self.__dict__.items():
            if name[0] == "_":
                continue
            class_vars.append(name + "=" + str(value))
        str_class_vars = ", ".join(class_vars)
        res_class_info += str_class_vars + ")"
        return res_class_info


class VkApiError(Exception):
    def __init__(self, code: int, text_error: dict) -> None:
        self.code = code
        self.text_error = str(text_error)

    def __str__(self) -> str:
        return self.text_error


class EmptyMiddleware:
    from .message import Message

    async def before(
        message: Dict[str, Any]
    ) -> Dict[str, Any]:
        return message

    def after(message: Message) -> Message:
        return message
