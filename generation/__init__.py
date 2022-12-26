from mcpi.minecraft import Minecraft
from typing import NoReturn, Final
import logging
import inspect


class ServerConnection:
    """Type-safe wrapper for a Minecraft connection."""
    def postToChat(self, msg) -> NoReturn: ...
    def setBlock(self, *args) -> NoReturn: ...
    def setBlocks(self, *args) -> NoReturn: ...
    def getBlock(self, *args) -> int: ...


class DummyConnection(ServerConnection):
    """Dummy connection for testing."""


class ProxiedConnection(Minecraft, ServerConnection):
    def postToChat(self, msg: str) -> NoReturn:
        caller: Final[int] = 1
        module = inspect.getmodule(inspect.stack()[caller][0])
        logging.info(f'BROADCAST by {module} : {msg}')
        super(ProxiedConnection, self).postToChat(msg)


try:
    connection: ServerConnection = ProxiedConnection.create()
except ConnectionRefusedError:
    logging.critical(
        'Server connection failed. Using dummy connection.'
    )
    connection: ServerConnection = DummyConnection()
