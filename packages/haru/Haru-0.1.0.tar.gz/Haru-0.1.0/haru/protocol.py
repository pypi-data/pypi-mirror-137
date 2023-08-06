from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .communicator import Communicator

__all__ = ("HaruProtocol",)


class HaruProtocol(asyncio.SubprocessProtocol):
    __slots__ = ("communicator",)

    def __init__(self, communicator: Communicator) -> None:
        self.communicator = communicator

    def pipe_data_received(self, _, data: bytes) -> None:
        self.communicator.process_output.extend(data)

    def process_exited(self) -> None:
        self.communicator.disconnect_event.set()
