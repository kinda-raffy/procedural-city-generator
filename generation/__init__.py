from mcpi.minecraft import Minecraft

try:
    connection: Minecraft = Minecraft.create()
except ConnectionRefusedError:
    print("Failed to connect to Minecraft")
