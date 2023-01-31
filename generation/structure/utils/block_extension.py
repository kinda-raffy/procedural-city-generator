from __future__ import annotations
from enum import ReprEnum, unique

__all__ = [
    "BlockExt",
]


@unique
class BlockExt(tuple, ReprEnum):
    """
    Extended blocks under
    @kinda_raffy/procedural_city_generator.generator.structure.utils.Block_Ext
    See original by @martinohanlon/mcpi.block.Block
    BlockExt supports block sub-states.
    """

    AIR = 0
    SANDSTONE = 24
    RED_SANDSTONE = 179
    CHISELED_SANDSTONE = 24, 1
    RED_CHISELED_SANDSTONE = 179, 1
    SMOOTH_SANDSTONE = 24, 2
    RED_SMOOTH_SANDSTONE = 179, 2
    SANDSTONE_SLAB = 44, 1
    RED_SANDSTONE_SLAB = 182, 0
    OAK_PLANK = 5, 0
    SPRUCE_PLANK = 5, 1
    BIRCH_PLANK = 5, 2
    JUNGLE_PLANK = 5, 3
    ACACIA_PLANK = 5, 4
    DARK_PLANK = 5, 5
    OAK_LOG = 17, 0
    SPRUCE_LOG = 17, 1
    BIRCH_LOG = 17, 2
    JUNGLE_LOG = 17, 3
    ACACIA_LOG = 162
    DARK_LOG = 162, 1
    OAK_SLAB = 126, 0
    SPRUCE_SLAB = 126, 1
    BIRCH_SLAB = 126, 2
    JUNGLE_SLAB = 126, 3
    ACACIA_SLAB = 126, 4
    DARK_SLAB = 126, 5
    STONE_SLAB = 44
    COBBLESTONE_SLAB = 44, 3
    GLASS = 20
    BLACK_GLASS = 95, 15
    RED_GLASS = 95, 14
    WHITE_GLASS = 95, 0
    ORANGE_GLASS = 95, 1
    MAGENTA_GLASS = 95, 2
    LIGHT_BLUE_GLASS = 95, 3
    YELLOW_GLASS = 95, 4
    LIME_GLASS = 95, 5
    PINK_GLASS = 95, 6
    GRAY_GLASS = 95, 7
    LIGHT_GRAY_GLASS = 95, 8
    CYAN_GLASS = 95, 9
    PURPLE_GLASS = 95, 10
    BLUE_GLASS = 95, 11
    BROWN_GLASS = 95, 12
    GREEN_GLASS = 95, 13
    WHITE = 35, 0
    ORANGE = 35, 1
    MAGENTA = 35, 2
    LIGHT_BLUE = 35, 3
    YELLOW = 35, 4
    LIME = 35, 5
    PINK = 35, 6
    GRAY = 35, 7
    LIGHT_GRAY = 35, 8
    CYAN = 35, 9
    PURPLE = 35, 10
    BLUE = 35, 11
    BROWN = 35, 12
    GREEN = 35, 13
    RED = 35, 14
    BLACK = 35, 15
    RED_CARPET = 171, 14
    WHITE_CONCRETE = (251,)
    ORANGE_CONCRETE = 251, 1
    MAGENTA_CONCRETE = 251, 2
    LIGHT_BLUE_CONCRETE = 251, 3
    YELLOW_CONCRETE = 251, 4
    LIME_CONCRETE = 251, 5
    PINK_CONCRETE = 251, 6
    GRAY_CONCRETE = 251, 7
    LIGHT_GRAY_CONCRETE = 251, 8
    CYAN_CONCRETE = 251, 9
    PURPLE_CONCRETE = 251, 10
    BLUE_CONCRETE = 251, 11
    BROWN_CONCRETE = 251, 12
    GREEN_CONCRETE = 251, 13
    RED_CONCRETE = 251, 14
    BLACK_CONCRETE = 251, 15
    OAK_DOOR = 64
    IRON_DOOR = 71
    SPRUCE_DOOR = 193
    BIRCH_DOOR = 194
    JUNGLE_DOOR = 195
    ACACIA_DOOR = 196
    DARK_DOOR = 197
    COBBLESTONE = 4
    MOSSY_STONE = 48
    MOSSY_STONE_BRICK = 98, 1
    STONE_BRICK = 98
    CRACKED_STONE_BRICK = 98, 2
    CHISELED_STONE_BRICK = 98, 3
    IRON = 42
    COAL = 173
    OAK_FENCE = 85
    SPRUCE_FENCE = 188
    BIRCH_FENCE = 189
    JUNGLE_FENCE = 190
    DARK_FENCE = 191
    ACACIA_FENCE = 192
    OAK_FENCE_GATE = 107
    SPRUCE_FENCE_GATE = 183
    BIRCH_FENCE_GATE = 184
    JUNGLE_FENCE_GATE = 185
    DARK_FENCE_GATE = 186
    ACACIA_FENCE_GATE = 187
    ACACIA_LEAVES = 161
    DARK_LEAVES = 161, 1
    BED = 26
    FURNACE_LEFT = 62
    FURNACE_TOWARDS = 62, 4
    CRAFTING_TABLE = 58
    ENDER_CHEST = 130
    CHEST = 54
    JUKEBOX = 84
    CAKE = 92
    LAVA = 11
    WATER = 9
    TORCH = 50
    TORCH_AWAY = 50, 0
    TORCH_TOWARDS = 50, 2
    TORCH_RIGHT = 50, 3
    TORCH_LEFT = 50, 4
    TORCH_STANDING = 50, 5
    GLOWSTONE = 89
    JACK_O_LANTERN = 91
    REDSTONE_LAMP = 124
    REDSTONE_BLOCK = 152
    ENCHANTMENT_TABLE = 116
    NOTE_BLOCK = 25
    BREWING_STAND = 117
    CAULDRON = 118, 3
    ANVIL = 145
    BEACON = 138
    MELON = 103
    COBWEB = 30
    DEAD_SHRUB = 31
    FIRE = 51
    STICKY_PISTON = 29
    MONSTER_SPAWNER = 52
    BOOKSHELF = 47
    PUMPKIN = 86
    WOOD_BUTTON = 143
    WOOD_BUTTON_TOWARDS = 143, 1
    WOOD_BUTTON_AWAY = 143, 2
    WOOD_BUTTON_LEFT = 143, 3
    WOOD_BUTTON_RIGHT = 143, 4
    END_PORTAL_FRAME = 120
    STANDING_BANNER = 176, 4
    COMMAND_BLOCK = 137
    OBSERVER = 218
    GOLD = 41
    DIAMOND = 57
    TNT = 46
    IRON_PRESSURE_PLATE = 148
    WOOD_PRESSURE_PLATE = 72
    LEVER = 69
    FLOWER_POT = 140
    OAK_STAIRS = 53
    COBBLESTONE_STAIRS = 67
    SANDSTONE_STAIRS = 128
    SPRUCE_STAIRS = 134
    BIRCH_STAIRS = 135
    BIRCH_STAIRS_RIGHT = 135, 2
    JUNGLE_STAIRS = 136
    ACACIA_STAIRS = 163
    DARK_STAIRS = 164
    DARK_STAIRS_RIGHT = 164, 2
    RED_SANDSTONE_STAIRS = 180
    STONE_BRICK_STAIRS = 109
    WHITE_TERRACOTTA = 235
    ORANGE_TERRACOTTA = 236
    MAGENTA_TERRACOTTA = 237
    LIGHTBLUE_TERRACOTTA = 238
    YELLOW_TERRACOTTA = 239
    LIME_TERRACOTTA = 240
    PINK_TERRACOTTA = 241
    GRAY_TERRACOTTA = 242
    LIGHTGRAY_TERRACOTTA = 243
    CYAN_TERRACOTTA = 244
    PURPLE_TERRACOTTA = 245
    BLUE_TERRACOTTA = 246
    BROWN_TERRACOTTA = 247
    GREEN_TERRACOTTA = 248
    RED_TERRACOTTA = 249
    BLACK_TERRACOTTA = 250
