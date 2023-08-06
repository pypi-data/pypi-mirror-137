import asyncio
import subprocess
from asyncio.transports import BaseTransport
from typing import Optional

from .mixins import IOMixin
from .protocol import HaruProtocol

__all__ = ("Communicator", "PIPE", "DEVNULL", "STDOUT")

PIPE = subprocess.PIPE
DEVNULL = subprocess.DEVNULL
STDOUT = subprocess.STDOUT


class Communicator(IOMixin):
    __slots__ = ("transport",)

    def __init__(self) -> None:
        self.transport: Optional[BaseTransport] = None
        super().__init__()

    async def run(self, program: str, args: str, stdin=None, stdout=None) -> str:
        loop = asyncio.get_running_loop()

        self.transport, _ = await loop.subprocess_exec(
            lambda: HaruProtocol(self), program, args, stdin, stdout=stdout
        )
        await self.disconnect_event.wait()

        self.transport.close()
        data = bytes(self.process_output)
        return data.decode()
