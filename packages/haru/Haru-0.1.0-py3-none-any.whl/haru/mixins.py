import asyncio

__all__ = ("IOMixin",)


class IOMixin:
    __slots__ = ("process_output", "futures", "disconnect_event")

    def __init__(self) -> None:
        self.process_output: bytearray = bytearray()
        self.futures: asyncio.Queue = asyncio.Queue()

        self.disconnect_event: asyncio.Event = asyncio.Event()

    def enqueue_future(self, fut: asyncio.Future) -> None:
        self.futures.put_nowait(fut)
