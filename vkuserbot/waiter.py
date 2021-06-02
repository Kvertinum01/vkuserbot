from typing import Dict, Callable


class Waiter:
    def __init__(self) -> None:
        self._in_wait_ids: Dict[str, str] = {}
        self._to_handle: Dict[str, Callable] = {}

    def new(self, func_id: int) -> Callable:
        def get_func(func: Callable) -> Callable:
            async def wrapper() -> None:
                pass
            self._to_handle[str(func_id)] = func
            return wrapper
        return get_func

    def add(self, peer_id: int, func_id: int):
        self._in_wait_ids[str(peer_id)] = str(func_id)

    def exit_waiter(self, peer_id: int):
        del self._in_wait_ids[str(peer_id)]
