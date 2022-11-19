from mcpi import block
air = 0
blocks = {
    'air': [0],

    # sand
    'sandstone': [24],
    'red_sandstone': [179],

    'chiseled_sandstone': [24, 1],
    'red_chiseled_sandstone': [179, 1],

    'smooth_sandstone': [24, 2],
    'red_smooth_sandstone': [179, 2],

    'sandstone_slab': [44, 1],
    'red_sandstone_slab': [182, 0],

    # wood
    'oak_plank': [5, 0],
    'spruce_plank': [5, 1],
    'birch_plank': [5, 2],
    'jungle_plank': [5, 3],
    'acacia_plank': [5, 4],
    'dark_plank': [5, 5],

    'oak_log': [17, 0],
    'spruce_log': [17, 1],
    'birch_log': [17, 2],
    'jungle_log': [17, 3],
    'acacia_log': [162],
    'dark_log': [162, 1],

    'oak_slab': [126, 0],
    'spruce_slab': [126, 1],
    'birch_slab': [126, 2],
    'jungle_slab': [126, 3],
    'acacia_slab': [126, 4],
    'dark_slab': [126, 5],
    'stone_slab': [44],
    'cobblestone_slab': [44, 3],

    # glass
    'glass': [20],
    'black_glass': [95, 15],
    'red_glass': [95, 14],
    'white_glass': [95, 0],
    'orange_glass': [95, 1],
    'magenta_glass': [95, 2],
    'light_blue_glass': [95, 3],
    'yellow_glass': [95, 4],
    'lime_glass': [95, 5],
    'pink_glass': [95, 6],
    'gray_glass': [95, 7],
    'light_gray_glass': [95, 8],
    'cyan_glass': [95, 9],
    'purple_glass': [95, 10],
    'blue_glass': [95, 11],
    'brown_glass': [95, 12],
    'green_glass': [95, 13],

    # wools
    'white': [35, 0],
    'orange': [35, 1],
    'magenta': [35, 2],
    'light_blue': [35, 3],
    'yellow': [35, 4],
    'lime': [35, 5],
    'pink': [35, 6],
    'gray': [35, 7],
    'light_gray': [35, 8],
    'cyan': [35, 9],
    'purple': [35, 10],
    'blue': [35, 11],
    'brown': [35, 12],
    'green': [35, 13],
    'red': [35, 14],
    'black': [35, 15],
    'red_carpet': [171, 14],

    # concrete
    'white concrete': 251,
    'orange concrete': [251, 1],
    'magenta concrete': [251, 2],
    'light blue concrete': [251, 3],
    'yellow concrete': [251, 4],
    'lime concrete': [251, 5],
    'pink concrete': [251, 6],
    'gray concrete': [251, 7],
    'light gray concrete': [251, 8],
    'cyan concrete': [251, 9],
    'purple concrete': [251, 10],
    'blue concrete': [251, 11],
    'brown concrete': [251, 12],
    'green concrete': [251, 13],
    'red concrete': [251, 14],
    'black concrete': [251, 15],

    # doors
    'oak_door': [64],
    'iron_door': [71],
    'spruce_door': [193],
    'birch_door': [194],
    'jungle_door': [195],
    'acacia_door': [196],
    'dark_door': [197],

    # stone
    'cobblestone': [4],
    'mossy_stone': [48],
    'mossy_stone_brick': [98, 1],
    'stone_brick': [98],
    'cracked_stone_brick': [98, 2],
    'chiseled_stone_brick': [98, 3],
    'iron': [42],
    'coal': [173],

    # fences
    'oak_fence': [85],
    'spruce_fence': [188],
    'birch_fence': [189],
    'jungle_fence': [190],
    'dark_fence': [191],
    'acacia_fence': [192],

    # fence gates
    'oak_fence_gate': [107],
    'spruce_fence_gate': [183],
    'birch_fence_gate': [184],
    'jungle_fence_gate': [185],
    'dark_fence_gate': [186],
    'acacia_fence_gate': [187],

    # leaves
    'acacia_leaves': [161],
    'dark_leaves': [161, 1],

    # misc (used for furnishing)
    'bed': [26],
    'furnace_left': [62],
    'furnace_towards': [62, 4],
    'crafting_table': [58],
    'ender_chest': [130],
    'chest': [54],
    'jukebox': [84],
    'cake': [92],
    'lava': [11],
    'water': [9],

    'torch': [50],
    'torch_away': [50, 0],
    'torch_towards': [50, 2],
    'torch_right': [50, 3],
    'torch_left': [50, 4],
    'torch_standing': [50, 5],
    'glowstone': [89],
    'jack_o_lantern': [91],
    'redstone_lamp': [124],
    'redstone_block': [152],

    'enchantment_table': [116],
    'note_block': [25],
    'brewing_stand': [117],
    'cauldron': [118, 3],
    'anvil': [145],
    'beacon': [138],
    'melon': [103],
    'cobweb': [30],
    'dead_shrub': [31],
    'fire': [51],
    'sticky_piston': [29],
    'monster_spawner': [52],
    'bookshelf': [47],
    'pumpkin': [86],
    'wood_button': [143],
    'wood_button_towards': [143, 1],
    'wood_button_away': [143, 2],
    'wood_button_left': [143, 3],
    'wood_button_right': [143, 4],
    'end_portal_frame': [120],
    'standing_banner': [176, 4],
    'command_block': [137],
    'observer': [218],
    'gold': [41],
    'diamond': [57],
    'tnt': [46],
    'iron_pressure_plate': [148],
    'wood_pressure_plate': [72],
    'lever': [69],
    'flower_pot': [140],


    # stairs
    'oak_stairs': [53],
    'cobblestone_stairs': [67],
    'sandstone_stairs': [128],
    'spruce_stairs': [134],
    'birch_stairs': [135],
    'birch_stairs_right': [135, 2],
    'jungle_stairs': [136],
    'acacia_stairs': [163],
    'dark_stairs': [164],
    'dark_stairs_right': [164, 2],
    'red_sandstone_stairs': [180],
    'stone_brick_stairs': [109],

    # terracotta
    'white_terracotta': [235],
    'orange_terracotta': [236],
    'magenta_terracotta': [237],
    'lightblue_terracotta': [238],
    'yellow_terracotta': [239],
    'lime_terracotta': [240],
    'pink_terracotta': [241],
    'gray_terracotta': [242],
    'lightgray_terracotta': [243],
    'cyan_terracotta': [244],
    'purple_terracotta': [245],
    'blue_terracotta': [246],
    'brown_terracotta': [247],
    'green_terracotta': [248],
    'red_terracotta': [249],
    'black_terracotta': [250],
}

"""
BIOME TEMPLATE:
        'foundation': blocks['sandstone'],
        'stone': blocks['sandstone'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['chiseled_sandstone'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['dark_fence'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        
        'pool_wall': blocks['birch_plank'],
        'pool_container': blocks['cobblestone'],
        'pool_liquid': blocks['water'],
        
        'sunroof': blocks['dark_fence'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['chiseled_sandstone'],
"""
apartment_biome = [
    {
        # Iron with black windows
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['iron'],

        'walls': blocks['black_glass'],
        'pillars': blocks['iron'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['iron'],
        'roof_corner': blocks['beacon'],
    },
    {
        # Iron with blue windows
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['iron'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['iron'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['iron'],
        'roof_corner': blocks['beacon'],
    },
    {
        # Coal with black windows
        'foundation': blocks['iron'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['coal'],

        'walls': blocks['black_glass'],
        'pillars': blocks['coal'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['dark_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['coal'],
        'roof_corner': blocks['beacon'],
    },
    {
        # coal with blue windows
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['coal'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['coal'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['coal'],
        'roof_corner': blocks['beacon'],
    },
    {
        # coal with white accents (black windows)
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['iron'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['coal'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['iron'],
        'roof_corner': blocks['beacon'],
    },
    {
        # blue wool with blue windows
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['white_terracotta'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['blue'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['white_terracotta'],
        'roof_corner': blocks['beacon'],
    },
    {
        # blue glass with white floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['white'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['blue_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['blue_terracotta'],
        'roof_corner': blocks['beacon'],
    },
    {
        # black glass with white floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['white'],

        'walls': blocks['black_glass'],
        'pillars': blocks['black_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['coal'],
        'roof_corner': blocks['beacon'],
    },
    {
        # white glass with white floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['white'],

        'walls': blocks['white_glass'],
        'pillars': blocks['white_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['white_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['iron'],
        'roof_corner': blocks['beacon'],
    },
    {
        # blue glass with blue floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['blue'],

        'walls': blocks['blue_glass'],
        'pillars': blocks['blue_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['blue_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['blue'],
        'roof_corner': blocks['beacon'],
    },
    {
        # black glass with black floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['black'],

        'walls': blocks['black_glass'],
        'pillars': blocks['black_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['coal'],
        'roof_corner': blocks['beacon'],
    },
    # Golden Tower
    {
        # yellow glass with gold floors
        'foundation': blocks['stone_brick'],
        'stone': blocks['yellow_terracotta'],
        'upstairs_floor': blocks['gold'],

        'walls': blocks['yellow_glass'],
        'pillars': blocks['yellow_glass'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['yellow_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['yellow_glass'],
        'roof_outer': blocks['gold'],
        'roof_corner': blocks['beacon'],
    },
]
sand_biome = [
    {
        # Desert birch
        'foundation': blocks['sandstone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['birch_log'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['birch_slab'],
    },
    {
        # Normal Sandstone
        'foundation': blocks['sandstone'],
        'stone': blocks['sandstone'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['chiseled_sandstone'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['sandstone'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['chiseled_sandstone'],
    },
    {
        # Sandstone with birch windows
        'foundation': blocks['sandstone'],
        'stone': blocks['sandstone'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['chiseled_sandstone'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['birch_fence'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['birch_plank'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['chiseled_sandstone'],
    },
    {
        # Sandstone with dark fences
        'foundation': blocks['sandstone'],
        'stone': blocks['sandstone'],
        'upstairs_floor': blocks['red_chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['chiseled_sandstone'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['dark_fence'],
        'door': blocks['birch_door'],

        'fence': blocks['dark_fence'],
        'fence_gate': blocks['birch_fence_gate'],
        # pool
        'pool_wall': blocks['birch_plank'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['chiseled_sandstone'],
    },
    {
        # Red Sandstone
        'foundation': blocks['red_sandstone'],
        'stone': blocks['red_sandstone'],
        'upstairs_floor': blocks['red_chiseled_sandstone'],

        'walls': blocks['red_smooth_sandstone'],
        'pillars': blocks['red_chiseled_sandstone'],
        'slab': blocks['red_sandstone_slab'],

        'stairs': blocks['red_sandstone_stairs'],
        'windows': blocks['red_glass'],
        'door': blocks['acacia_door'],

        'fence': blocks['acacia_fence'],
        'fence_gate': blocks['acacia_fence_gate'],
        # pool
        'pool_wall': blocks['orange_glass'],
        'pool_container': blocks['red_chiseled_sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['red_glass'],
        'roof_outer': blocks['acacia_plank'],
        'roof_corner': blocks['red_chiseled_sandstone'],
    },
    {
        # Red Sandstone
        'foundation': blocks['red_sandstone'],
        'stone': blocks['red_sandstone'],
        'upstairs_floor': blocks['gold'],

        'walls': blocks['red_smooth_sandstone'],
        'pillars': blocks['gold'],
        'slab': blocks['red_sandstone_slab'],

        'stairs': blocks['red_sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['dark_fence'],
        'fence_gate': blocks['acacia_fence_gate'],
        # pool
        'pool_wall': blocks['red_glass'],
        'pool_container': blocks['red_chiseled_sandstone'],
        'pool_liquid': blocks['water'],
        # roof
        'sunroof': blocks['yellow_glass'],
        'roof_outer': blocks['gold'],
        'roof_corner': blocks['glowstone'],
    },
]

grass_biome = [
    # Plain configs
    {
        # Birch with birch pillars
        'foundation': blocks['cobblestone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['birch_log'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_plank'],
        'pool_container': blocks['birch_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['dark_slab'],
    },
    {
        # oak with oak pillars
        'foundation': blocks['mossy_stone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['oak_log'],

        'walls': blocks['oak_plank'],
        'pillars': blocks['oak_log'],
        'slab': blocks['oak_slab'],

        'stairs': blocks['oak_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['oak_door'],

        'fence': blocks['oak_fence'],
        'fence_gate': blocks['oak_fence_gate'],

        'pool_wall': blocks['oak_plank'],
        'pool_container': blocks['oak_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['oak_plank'],
        'roof_corner': blocks['oak_slab'],
    },
    {
        # spruce with spruce pillars
        'foundation': blocks['cobblestone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['spruce_log'],

        'walls': blocks['spruce_plank'],
        'pillars': blocks['spruce_log'],
        'slab': blocks['spruce_slab'],

        'stairs': blocks['spruce_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['spruce_fence'],
        'fence_gate': blocks['spruce_fence_gate'],

        'pool_wall': blocks['spruce_plank'],
        'pool_container': blocks['spruce_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['spruce_plank'],
        'roof_corner': blocks['dark_slab'],
    },
    {
        # jungle with jungle pillars
        'foundation': blocks['mossy_stone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['jungle_log'],

        'walls': blocks['jungle_plank'],
        'pillars': blocks['jungle_log'],
        'slab': blocks['jungle_slab'],

        'stairs': blocks['jungle_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['jungle_door'],

        'fence': blocks['jungle_fence'],
        'fence_gate': blocks['jungle_fence_gate'],

        'pool_wall': blocks['jungle_plank'],
        'pool_container': blocks['jungle_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['jungle_plank'],
        'roof_corner': blocks['jungle_slab'],
    },
    {
        # acacia with acacia pillars
        'foundation': blocks['cobblestone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['acacia_log'],

        'walls': blocks['acacia_plank'],
        'pillars': blocks['acacia_log'],
        'slab': blocks['acacia_slab'],

        'stairs': blocks['acacia_stairs'],
        'windows': blocks['gray_glass'],
        'door': blocks['acacia_door'],

        'fence': blocks['acacia_fence'],
        'fence_gate': blocks['acacia_fence_gate'],

        'pool_wall': blocks['orange_glass'],
        'pool_container': blocks['acacia_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['orange_glass'],
        'roof_outer': blocks['acacia_plank'],
        'roof_corner': blocks['stone_slab'],
    },
    {
        # dark with dark pillars and brown glass
        'foundation': blocks['mossy_stone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['dark_log'],

        'walls': blocks['dark_plank'],
        'pillars': blocks['dark_log'],
        'slab': blocks['dark_slab'],

        'stairs': blocks['dark_stairs'],
        'windows': blocks['brown_glass'],
        'door': blocks['dark_door'],

        'fence': blocks['dark_fence'],
        'fence_gate': blocks['dark_fence_gate'],

        'pool_wall': blocks['brown_glass'],
        'pool_container': blocks['dark_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['dark_plank'],
        'roof_corner': blocks['birch_slab'],
    },

    # Multi configs
    {
        # Spruce with dark pillars
        'foundation': blocks['cobblestone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['dark_log'],

        'walls': blocks['spruce_plank'],
        'pillars': blocks['dark_log'],
        'slab': blocks['dark_slab'],

        'stairs': blocks['spruce_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['dark_door'],

        'fence': blocks['spruce_fence'],
        'fence_gate': blocks['spruce_fence_gate'],

        'pool_wall': blocks['spruce_plank'],
        'pool_container': blocks['spruce_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['dark_log'],
        'roof_corner': blocks['spruce_slab'],
    },
    {
        # Dark with spruce pillars
        'foundation': blocks['cobblestone'],
        'stone': blocks['cobblestone'],
        'upstairs_floor': blocks['spruce_log'],

        'walls': blocks['dark_plank'],
        'pillars': blocks['spruce_log'],
        'slab': blocks['dark_slab'],

        'stairs': blocks['dark_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['spruce_door'],

        'fence': blocks['dark_fence'],
        'fence_gate': blocks['dark_fence_gate'],

        'pool_wall': blocks['dark_plank'],
        'pool_container': blocks['dark_plank'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['spruce_log'],
        'roof_corner': blocks['spruce_slab'],
    },
]

water_biome = [
    # Coloured Concrete
    {
        # Birch with Red Concrete
        'foundation': blocks['mossy_stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['red concrete'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['acacia_stairs'],
        'windows': blocks['red_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['acacia_fence'],
        'fence_gate': blocks['acacia_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['red_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['light_blue_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['birch_slab'],
    },
    {
        # Birch with Blue Concrete
        'foundation': blocks['stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['blue concrete'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['light_blue_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['light_blue_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['blue_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['gold'],
    },
    {
        # Birch with Orange Concrete
        'foundation': blocks['mossy_stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['orange concrete'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['orange_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['orange_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['orange_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['acacia_slab'],
    },
    {
        # Birch with Purple Concrete
        'foundation': blocks['stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['purple concrete'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['purple_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['purple_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['purple_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['gold'],
    },
    {
        # Birch with Green Concrete
        'foundation': blocks['mossy_stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_log'],

        'walls': blocks['birch_plank'],
        'pillars': blocks['green concrete'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['lime_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['lime_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['green_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['green concrete'],
    },
    {
        # White Concrete with birch
        'foundation': blocks['stone_brick'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['birch_plank'],

        'walls': blocks['white concrete'],
        'pillars': blocks['birch_log'],
        'slab': blocks['birch_slab'],

        'stairs': blocks['birch_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['birch_log'],
        'pool_container': blocks['white_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['white_glass'],
        'roof_outer': blocks['birch_plank'],
        'roof_corner': blocks['birch_log'],
    },
    # Coloured Terracotta
    {
        # white terracotta
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['white_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['black_glass'],
        'pool_container': blocks['light_blue_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['white_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
    {
        # orange terracotta
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['orange_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['light_blue_glass'],
        'pool_container': blocks['orange_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['orange_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
    {
        # lightblue terracotta
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['lightblue_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['white_glass'],
        'pool_container': blocks['light_blue_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['light_blue_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
    {
        # yellow terracotta
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['yellow_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['yellow_glass'],
        'pool_container': blocks['yellow_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['yellow_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
    {
        # lime terracotta
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['chiseled_sandstone'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['lime_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['birch_door'],

        'fence': blocks['birch_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['lime_glass'],
        'pool_container': blocks['yellow_glass'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['lime_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
    {
        # black terracotta; dark house
        'foundation': blocks['sandstone'],
        'stone': blocks['stone_brick'],
        'upstairs_floor': blocks['dark_log'],

        'walls': blocks['smooth_sandstone'],
        'pillars': blocks['black_terracotta'],
        'slab': blocks['sandstone_slab'],

        'stairs': blocks['sandstone_stairs'],
        'windows': blocks['black_glass'],
        'door': blocks['acacia_door'],

        'fence': blocks['dark_fence'],
        'fence_gate': blocks['birch_fence_gate'],

        'pool_wall': blocks['black_glass'],
        'pool_container': blocks['sandstone'],
        'pool_liquid': blocks['water'],

        'sunroof': blocks['black_glass'],
        'roof_outer': blocks['sandstone'],
        'roof_corner': blocks['beacon'],
    },
]

"""
FURNITURE TEMPLATE:
    {
        'main': blocks['air'],
        'main_above': blocks['air'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
"""
furniture = [

    # enchantment room

    {
        # 1
        'main': blocks['enchantment_table'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # ceil center
        'ceil_front': blocks['bookshelf'],
        'ceil_back': blocks['bookshelf'],
        'ceil_left': blocks['bookshelf'],
        'ceil_right': blocks['bookshelf'],

        # ceil corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        # floor center
        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # floor corner
        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['chest'],
        'floor_bl': blocks['air'],
    },
    {
        # 2
        'main': blocks['enchantment_table'],
        'main_above': blocks['air'],
        'main_ceil': blocks['diamond'],

        # ceil center
        'ceil_front': blocks['glowstone'],
        'ceil_back': blocks['glowstone'],
        'ceil_left': blocks['glowstone'],
        'ceil_right': blocks['glowstone'],

        # ceil corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        # floor center
        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # floor corner
        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # 3
        'main': blocks['enchantment_table'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # ceil center
        'ceil_front': blocks['gold'],
        'ceil_back': blocks['gold'],
        'ceil_left': blocks['gold'],
        'ceil_right': blocks['gold'],

        # ceil corners
        'ceil_tr': blocks['birch_fence'],
        'ceil_tl': blocks['birch_fence'],
        'ceil_br': blocks['birch_fence'],
        'ceil_bl': blocks['birch_fence'],

        # floor center
        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # floor corner
        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # blacksmith and metal working
    {
        # 1
        'main': blocks['anvil'],
        'main_above': blocks['air'],
        'main_ceil': blocks['redstone_lamp'],

        # centers
        'ceil_front': blocks['torch_away'],
        'ceil_back': blocks['torch_towards'],
        'ceil_left': blocks['torch_left'],
        'ceil_right': blocks['torch_right'],

        'floor_front': blocks['cauldron'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['furnace_left'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['furnace_left'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['cauldron']
    },
    {
        # 2
        'main': blocks['air'],
        'main_above': blocks['air'],
        'main_ceil': blocks['crafting_table'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # centers
        'ceil_front': blocks['torch_away'],
        'ceil_back': blocks['torch_towards'],
        'ceil_left': blocks['torch_left'],
        'ceil_right': blocks['torch_right'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['furnace_left'],
        'floor_tl': blocks['cauldron'],
        'floor_br': blocks['chest'],
        'floor_bl': blocks['anvil']
    },

    # map and command rooms
    {
        # beacon room
        'main': blocks['birch_plank'],
        'main_above': blocks['beacon'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['dark_fence'],
        'ceil_back': blocks['dark_fence'],
        'ceil_left': blocks['dark_fence'],
        'ceil_right': blocks['dark_fence'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['dark_fence'],
        'ceil_tl': blocks['dark_fence'],
        'ceil_br': blocks['dark_fence'],
        'ceil_bl': blocks['dark_fence'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # map room
        'main': blocks['birch_slab'],
        'main_above': blocks['white_terracotta'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['acacia_fence'],
        'ceil_back': blocks['acacia_fence'],
        'ceil_left': blocks['acacia_fence'],
        'ceil_right': blocks['acacia_fence'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['glowstone'],
        'ceil_tl': blocks['acacia_fence'],
        'ceil_br': blocks['acacia_fence'],
        'ceil_bl': blocks['acacia_fence'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # command room
        'main': blocks['command_block'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['birch_stairs_right'],

        # corners
        'ceil_tr': blocks['chest'],
        'ceil_tl': blocks['chest'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['acacia_stairs'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # entertainment rooms
    {
        # pole room
        'main': blocks['dark_plank'],
        'main_above': blocks['dark_fence'],
        'main_ceil': blocks['dark_fence'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['dark_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['redstone_lamp'],
        'ceil_tl': blocks['redstone_lamp'],
        'ceil_br': blocks['redstone_lamp'],
        'ceil_bl': blocks['redstone_lamp'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # pole room (golden)
        'main': blocks['gold'],
        'main_above': blocks['birch_fence'],
        'main_ceil': blocks['birch_fence'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['dark_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['glowstone'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # armory
    {
        # weapons store room
        'main': blocks['iron_pressure_plate'],
        'main_above': blocks['air'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['tnt'],
        'ceil_back': blocks['tnt'],
        'ceil_left': blocks['tnt'],
        'ceil_right': blocks['chest'],

        'floor_front': blocks['tnt'],
        'floor_back': blocks['tnt'],
        'floor_left': blocks['tnt'],
        'floor_right': blocks['chest'],

        # corners
        'ceil_tr': blocks['chest'],
        'ceil_tl': blocks['tnt'],
        'ceil_br': blocks['chest'],
        'ceil_bl': blocks['tnt'],

        'floor_tr': blocks['standing_banner'],
        'floor_tl': blocks['standing_banner'],
        'floor_br': blocks['tnt'],
        'floor_bl': blocks['air'],
    },
    {
        # monster spawner for haunted houses
        'main': blocks['monster_spawner'],
        'main_above': blocks['cobblestone_slab'],
        'main_ceil': blocks['jack_o_lantern'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['cobweb'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['dead_shrub'],
        'floor_back': blocks['cobweb'],
        'floor_left': blocks['air'],
        'floor_right': blocks['cobweb'],

        # corners
        'ceil_tr': blocks['cobweb'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['cobweb'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['dead_shrub'],
        'floor_bl': blocks['dead_shrub'],
    },

    # library
    {
        # libary (big)
        'main': blocks['bookshelf'],
        'main_above': blocks['bookshelf'],
        'main_ceil': blocks['spruce_fence'],

        # centers
        'ceil_front': blocks['bookshelf'],
        'ceil_back': blocks['bookshelf'],
        'ceil_left': blocks['bookshelf'],
        'ceil_right': blocks['bookshelf'],

        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['glowstone'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # libary (small)
        'main': blocks['bookshelf'],
        'main_above': blocks['bookshelf'],
        'main_ceil': blocks['bookshelf'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['glowstone'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # mechanical rooms (redstone)
    {
        # hydraulic tunneller (for creating mineshafts)
        'main': blocks['air'],
        'main_above': blocks['sticky_piston'],
        'main_ceil': blocks['lever'],

        # centers
        'ceil_front': blocks['redstone_lamp'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['redstone_lamp'],
        'ceil_right': blocks['redstone_lamp'],

        'floor_front': blocks['observer'],
        'floor_back': blocks['command_block'],
        'floor_left': blocks['wood_pressure_plate'],
        'floor_right': blocks['wood_pressure_plate'],

        # corners
        'ceil_tr': blocks['redstone_lamp'],
        'ceil_tl': blocks['redstone_lamp'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['wood_pressure_plate'],
        'floor_tl': blocks['wood_pressure_plate'],
        'floor_br': blocks['wood_pressure_plate'],
        'floor_bl': blocks['wood_pressure_plate'],
    },

    # lounge/couch rooms
    {
        # indo styled wooded couch room
        'main': blocks['acacia_plank'],
        'main_above': blocks['torch_standing'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['dark_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['dark_stairs'],
        'floor_tl': blocks['dark_stairs'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # western styled wooded couch room
        'main': blocks['oak_plank'],
        'main_above': blocks['flower_pot'],
        'main_ceil': blocks['dark_fence'],

        # centers
        'ceil_front': blocks['glowstone'],
        'ceil_back': blocks['glowstone'],
        'ceil_left': blocks['glowstone'],
        'ceil_right': blocks['glowstone'],

        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['birch_stairs'],
        'floor_tl': blocks['birch_stairs'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # japanese styled wooded couch room
        'main': blocks['oak_slab'],
        'main_above': blocks['air'],
        'main_ceil': blocks['birch_fence'],

        # centers
        'ceil_front': blocks['birch_fence'],
        'ceil_back': blocks['birch_fence'],
        'ceil_left': blocks['birch_fence'],
        'ceil_right': blocks['birch_fence'],

        'floor_front': blocks['birch_stairs_right'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['birch_stairs_right'],

        # corners
        'ceil_tr': blocks['birch_fence'],
        'ceil_tl': blocks['birch_fence'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['glowstone'],

        'floor_tr': blocks['wood_pressure_plate'],
        'floor_tl': blocks['wood_pressure_plate'],
        'floor_br': blocks['wood_pressure_plate'],
        'floor_bl': blocks['wood_pressure_plate'],
    },

    # laboratories and research rooms
    {
        # chem lab (def not used for cooking up any drugs because drugs are very bad) (͡°͜ʖ͡°)
        'main': blocks['white'],
        'main_above': blocks['brewing_stand'],  # not used to make meth 🧢
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['chest'],  # not used to store meth 🧢

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['chest'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['chest'],
        'ceil_bl': blocks['glowstone'],  # not used as a light-source to grow weed

        # def not weed plants just some regular green plants
        'floor_tr': blocks['flower_pot'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['flower_pot'],
    },
    {
        # exploding chem lab
        'main': blocks['tnt'],
        'main_above': blocks['brewing_stand'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['tnt'],
        'ceil_back': blocks['tnt'],
        'ceil_left': blocks['tnt'],
        'ceil_right': blocks['tnt'],

        'floor_front': blocks['fire'],
        'floor_back': blocks['fire'],
        'floor_left': blocks['fire'],
        'floor_right': blocks['fire'],

        # corners
        'ceil_tr': blocks['tnt'],
        'ceil_tl': blocks['tnt'],
        'ceil_br': blocks['tnt'],
        'ceil_bl': blocks['glowstone'],

        'floor_tr': blocks['fire'],
        'floor_tl': blocks['fire'],
        'floor_br': blocks['fire'],
        'floor_bl': blocks['fire'],
    },
    {
        # pickle ricks garage (this lab experiments with end portals)
        'main': blocks['white'],
        'main_above': blocks['flower_pot'],  # its pickle rick hahaha funny
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['end_portal_frame'],
        'floor_back': blocks['end_portal_frame'],
        'floor_left': blocks['end_portal_frame'],
        'floor_right': blocks['end_portal_frame'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['bookshelf'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['end_portal_frame'],
        'floor_tl': blocks['end_portal_frame'],
        'floor_br': blocks['end_portal_frame'],
        'floor_bl': blocks['end_portal_frame'],
    },

    # kitchen + bathrooms (yes i hve categorised this in one category, there is not enough blocks in mcpy :(. )
    {
        # kitchen or bathroom
        'main': blocks['red_carpet'],
        'main_above': blocks['air'],
        'main_ceil': blocks['air'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['chest'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['chest'],

        # corners
        'ceil_tr': blocks['glowstone'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['chest'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['cauldron'],
        'floor_bl': blocks['birch_plank'],
    },
    {
        # kitchen or bathroom (lights on fire)
        'main': blocks['red_carpet'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['chest'],

        'floor_front': blocks['fire'],
        'floor_back': blocks['fire'],
        'floor_left': blocks['fire'],
        'floor_right': blocks['chest'],

        # corners
        'ceil_tr': blocks['chest'],
        'ceil_tl': blocks['fire'],
        'ceil_br': blocks['chest'],
        'ceil_bl': blocks['fire'],

        'floor_tr': blocks['fire'],
        'floor_tl': blocks['fire'],
        'floor_br': blocks['cauldron'],
        'floor_bl': blocks['birch_plank'],
    },

    # a melon room?
    {
        # melon inspired pole room
        'main': blocks['melon'],
        'main_above': blocks['dark_fence'],
        'main_ceil': blocks['dark_fence'],

        # centers
        'ceil_front': blocks['melon'],
        'ceil_back': blocks['melon'],
        'ceil_left': blocks['melon'],
        'ceil_right': blocks['melon'],

        'floor_front': blocks['melon'],
        'floor_back': blocks['melon'],
        'floor_left': blocks['air'],
        'floor_right': blocks['dark_stairs_right'],

        # corners
        'ceil_tr': blocks['glowstone'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['glowstone'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # cake room!
    {
        # room with a cake and torch
        'main': blocks['red'],
        'main_above': blocks['cake'],
        'main_ceil': blocks['torch_standing'],

        # centers
        'ceil_front': blocks['air'],
        'ceil_back': blocks['air'],
        'ceil_left': blocks['air'],
        'ceil_right': blocks['air'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['air'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },

    # music room
    {
        # music room 1
        'main': blocks['jukebox'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # centers
        'ceil_front': blocks['redstone_lamp'],
        'ceil_back': blocks['redstone_lamp'],
        'ceil_left': blocks['redstone_lamp'],
        'ceil_right': blocks['redstone_lamp'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['chest'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
    {
        # music room 2
        'main': blocks['note_block'],
        'main_above': blocks['air'],
        'main_ceil': blocks['glowstone'],

        # centers
        'ceil_front': blocks['redstone_lamp'],
        'ceil_back': blocks['redstone_lamp'],
        'ceil_left': blocks['redstone_lamp'],
        'ceil_right': blocks['redstone_lamp'],

        'floor_front': blocks['air'],
        'floor_back': blocks['air'],
        'floor_left': blocks['air'],
        'floor_right': blocks['air'],

        # corners
        'ceil_tr': blocks['air'],
        'ceil_tl': blocks['air'],
        'ceil_br': blocks['air'],
        'ceil_bl': blocks['air'],

        'floor_tr': blocks['chest'],
        'floor_tl': blocks['air'],
        'floor_br': blocks['air'],
        'floor_bl': blocks['air'],
    },
]
