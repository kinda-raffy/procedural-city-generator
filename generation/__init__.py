from typing import NoReturn
from mcpi.vec3 import Vec3


class DummyConnection:
    def set_block(self, *args) -> NoReturn: ...
    def set_blocks(self, *args) -> NoReturn: ...
    def get_block(self, *args) -> int: ...


try:
    from mcpi.minecraft import Minecraft

    connection: Minecraft = Minecraft.create()
except ConnectionRefusedError:
    print("Failed to connect to Minecraft. Using dummy connection.")

    class Minecraft(DummyConnection):
        pass

    connection: Minecraft = Minecraft()
