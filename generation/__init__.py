from mcpi.minecraft import Minecraft
from typing import NoReturn, Final
import logging
import inspect


class DummyConnection(Minecraft):
    def postToChat(self, msg) -> NoReturn: ...
    def setBlock(self, *args) -> NoReturn: ...
    def setBlocks(self, *args) -> NoReturn: ...
    def getBlock(self, *args) -> int: ...


class ProxiedConnection(Minecraft):
    def postToChat(self, msg: str) -> NoReturn:
        caller: Final[int] = 1
        module = inspect.getmodule(inspect.stack()[caller][0])
        logging.info(f'BROADCAST by {module} : {msg}')
        super(ProxiedConnection, self).postToChat(msg)


try:
    connection: Minecraft = ProxiedConnection.create()
except ConnectionRefusedError:
    logging.critical(
        'Server connection failed. Using dummy connection.'
    )
    connection: Minecraft = DummyConnection.create()
