from biome import Biome
from grid import Grid, Tile
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block
import random
from generation.building.reference.house import House

mc = Minecraft.create()
post = mc.postToChat
player_tile_position = mc.player.getTilePos
get_blocks = mc.getBlocks
get_block = mc.getBlock
set_blocks = mc.setBlocks
set_block = mc.setBlock
get_height = mc.getHeight


class Village:
    """
    - Manages generation and layout of town plan.
    - Determines optimal placement of a random number of house blocks.
    - Determines and stores road tiles according to shortest path algorithm.
    - Randomly generates landmark and minor structures to accompany houses.

    """

    def __init__(self, max_houses, max_grid_size):
        self.grid = Grid(max_grid_size)
        self.max_houses = max_houses
        self.available = None
        self.houses = list()
        self.town_planner()

        self.sand_tcs = [
            self._tc_pyramid,
            self._tc_temple,
            self._tc_obelisk,
            self._tc_fountain,
            self._tc_nether_portal,
            self._tc_end_portal,
        ]
        self.grass_tcs = [
            self._tc_well,
            self._tc_obelisk,
            self._tc_fountain,
            self._tc_nether_portal,
            self._tc_end_portal,
            self._tc_melon_pumpkin,
        ]
        self.water_tcs = [
            self._tc_pool,
            self._tc_nether_portal,
            self._tc_end_portal,
        ]

        self.build_tc()

    def __iter__(self):
        for house_tile in self.houses:
            yield house_tile

    def get_global_biome(self):
        ground = 0
        sand = 0
        for house_tile in self:
            if house_tile.terrain == Biome.GROUND:
                ground += 1
            elif house_tile.terrain == Biome.SAND:
                sand += 1
        return Biome.GROUND if ground > sand else Biome.SAND

    def town_planner(self):
        """
        Primary method of village class.
        - Determines and allocates 3x3 tile house blocks, biasing land over water.
        - Determines roads to each house individually, altering grid edge weights to 
        ensure each subsequent road follows previous roads when necessary.
        - Determines global biome and passes to house class.
        - Instantiates house objects.
        - Calls method to build roads.
        - Determines leftover tiles and calls functions to build miscellaneous structures
        around roads and town centers.

        """
        post('Planning town.')
        plots = set()
        roads = set()
        allocated = set()
        available = set(
            filter(
                self.grid.is_3x3,
                self.grid.adjacency_list
            )
        )

        # Remove the center tiles from available.
        roads = roads.union(self.grid.get_square(self.grid.center, size=3))
        available = available.difference(roads)
        roads.remove(self.grid.center)
        available = available.difference(
            (self.grid.get_square(self.grid.center, size=5)))
        available_water = {
            tile for tile in available if tile.terrain == Biome.WATER
        }
        available_ground = available.difference(available_water)
        min_houses = 10  # Arbitrary limit.
        max_houses = self.max_houses
        water_houses = 0
        land_houses = 0
        for i in range(max_houses):
            if len(available_ground) > 0:
                plot = random.choice(tuple(available_ground))
                available_ground = available_ground.difference(
                    self.grid.get_square(plot, size=7)
                )
                available_water = available_water.difference(
                    self.grid.get_square(plot, size=7)
                )
                allocated = allocated.union(
                    self.grid.get_square(plot, size=3)
                )
                plots.add(plot)
                land_houses += 1
            else:
                if land_houses + water_houses < min_houses:
                    if len(available_water) > 0:
                        plot = random.choice(tuple(available_water))
                        available_water = available_water.difference(
                            self.grid.get_square(plot, size=7)
                        )
                        allocated = allocated.union(
                            self.grid.get_square(plot, size=3)
                        )
                        plots.add(plot)
                        water_houses += 1
                    else:
                        break
        post(
            f"building {land_houses} on ground, {water_houses} on water"
        )

        possible_roads = set(self.grid.adjacency_list.keys()
                             ).difference(allocated)
        houses_to_build = set()

        plots = list(plots)
        for index in range(max_houses):
            # post(f'Running Dijkstra {index + 1}')
            self.grid.dijkstra(possible_roads)
            if index > len(plots) - 1:
                break
            for plot in plots[index::200]:
                # Check if plot is a valid 3x3 square.
                if not self.grid.is_3x3(plot):
                    continue
                door_options = list(self._get_candidate_doors(plot))
                best_option = None
                chosen_door = None
                for option in door_options:
                    option_path = self.grid.shortest_path(option)
                    if option_path is False:
                        continue
                    if best_option is None or len(option_path) < len(best_option):
                        best_option = option_path
                        chosen_door = option
                if best_option is None:
                    # Don't add if unreachable.
                    post('Found unreachable house.')
                    plots.remove(plot)
                    continue
                # Adjust relevant edge weights.
                for tile in best_option:
                    for adjacent in self.grid.adjacency_list:
                        if adjacent in best_option:
                            self.grid.edge_weights[(tile, adjacent)] = 1
                            self.grid.edge_weights[(adjacent, tile)] = 1
                roads = roads.union(best_option)
                houses_to_build.add((plot, chosen_door))
                self.houses.append(plot)

        global_biome = self.get_global_biome()
        # Temporary alteration until house class complete.
        if global_biome == Biome.GROUND:
            if random.randint(1, 3) == 3:
                global_biome = 3
            else:
                global_biome = 0
        elif global_biome == Biome.SAND:
            global_biome = 1

        # Instantiate House Objects
        built_count = 0
        post("Building Houses...")

        for house in houses_to_build:
            center_vec = Vec3(
                house[0].position.x, house[1].position.y, house[0].position.z
            )
            door_vec = self.get_door_vec(center_vec, house[1])
            if house[0].terrain == Biome.WATER:
                House(center_vec, door_vec, biome=2)
            else:
                House(center_vec, door_vec, biome=global_biome)
            built_count += 1

            post(f"{float(built_count / len(houses_to_build)) * 100 :.2f}%")

        self.available = available_ground.difference(roads)
        self._place_roads(roads)

        available_for_misc = set()
        for tile in roads:
            for neighbor in self.grid.adjacency_list[tile]:
                available_for_misc.add(neighbor)
        available_for_misc = (available_for_misc.difference(
            roads)).difference(allocated)
        self.place_misc(available_for_misc)

        self.place_lights(roads)

    def place_lights(self, roads):

        lantern_tiles = []

        for tile in roads:
            neighbour_count = 0
            for neighbour in self.grid.adjacency_list[tile]:
                if neighbour in roads:
                    neighbour_count += 1
            
            if neighbour_count == 3:
                if random.randint(1, 8) == 1:
                    lantern_tiles.append(tile)

            elif neighbour_count == 2:
                if random.randint(1, 4) == 1:
                    lantern_tiles.append(tile)
            elif neighbour_count == 1:
                if random.randint(1, 2) == 1:
                    lantern_tiles.append(tile)

        for tile in lantern_tiles:
            a = tile.position
            if get_block(a.x, a.y+1, a.z) == block.AIR.id:
                set_blocks(a.x, a.y+1, a.z, a.x, a.y+3, a.z, block.FENCE_DARK_OAK)  # Cobblestone wall
                set_block(a.x, a.y+4, a.z, 138)  # Beacon

    def place_misc(self, available):
        num_misc = 8
        center = self.grid.center
        closest_tiles = []
        for i in range(num_misc):
            closest_dist = 9999
            closest_tile = None
            for tile in available:
                distance = abs(tile.position.x - center.position.x) + \
                    abs(tile.position.z - center.position.z)
                if distance < closest_dist:
                    if tile not in closest_tiles:
                        closest_dist = distance
                        closest_tile = tile
            closest_tiles.append(closest_tile)

        for tile in closest_tiles:
            self.build_tent(tile)

    @staticmethod
    def build_tent(tile):

        if not isinstance(tile, Tile):
            return

        a = tile.position

        # place foundation
        if tile.terrain == Biome.WATER:
            set_blocks(a.x-2, a.y-3, a.z-2, a.x+2, a.y,
                       a.z+2, block.WOOD_PLANKS.id)
        else:
            set_blocks(a.x-2, a.y-3, a.z-2, a.x+2, a.y,
                       a.z+2, block.COBBLESTONE.id)
        set_blocks(a.x-1, a.y+1, a.z-1, a.x+1, a.y+3, a.z+1, block.AIR.id)
        # place corner fences
        if get_block(a.x-2, a.y+3, a.z-2) == block.AIR.id:
            set_blocks(a.x-2, a.y+1, a.z-2, a.x-2, a.y +
                       3, a.z-2, block.FENCE_DARK_OAK)
        if get_block(a.x+2, a.y+3, a.z-2) == block.AIR.id:
            set_blocks(a.x+2, a.y+1, a.z-2, a.x+2, a.y +
                       3, a.z-2, block.FENCE_DARK_OAK)
        if get_block(a.x-2, a.y+3, a.z+2) == block.AIR.id:
            set_blocks(a.x-2, a.y+1, a.z+2, a.x-2, a.y +
                       3, a.z+2, block.FENCE_DARK_OAK)
        if get_block(a.x+2, a.y+3, a.z+2) == block.AIR.id:
            set_blocks(a.x+2, a.y+1, a.z+2, a.x+2, a.y +
                       3, a.z+2, block.FENCE_DARK_OAK)

        colour1 = (35, random.randint(1, 15))
        colour2 = (35, random.randint(1, 15))
        # place tarp
        direction = random.randint(0, 1)
        colour = None
        for i in range(5):
            if direction == 0:
                if i % 2 == 0:
                    colour = colour1
                else:
                    colour = colour2
            for j in range(5):
                if direction == 1:
                    if j % 2 == 1:
                        colour = colour1
                    else:
                        colour = colour2
                if get_block(a.x-2 + i, a.y + 4, a.z-2 + j) == block.AIR.id \
                        and colour is not None:
                    if i % 4 == 0:
                        if j % 4 == 0:
                            set_block(a.x-2 + i, a.y + 3, a.z-2 + j, colour)
                        else:
                            set_block(a.x-2 + i, a.y + 4, a.z-2 + j, colour)
                    else:
                        set_block(a.x-2 + i, a.y + 4, a.z-2 + j, colour)

        # place carpet
            set_blocks(a.x-1, a.y, a.z-1, a.x+1, a.y, a.z+1, colour)

        # place goods
        for i in range(random.randint(0, 6)):
            goods_type = random.choice(
                [block.MELON.id, block.PUMPKIN.id, block.BOOKSHELF.id, 170, 117, 54, 145])
            set_block(a.x + random.randint(-1, 1), a.y+1,
                      a.z + random.randint(-1, 1), goods_type)

    @staticmethod
    def get_door_vec(center, door):
        c = center
        d = door.position
        if c.x > d.x:
            return Vec3(
                c.x - 4, c.y, c.z
            )
        elif c.x < d.x:
            return Vec3(
                c.x + 4, c.y, c.z
            )
        elif c.z < d.z:
            return Vec3(
                c.x, c.y, c.z + 4
            )
        else:
            return Vec3(
                c.x, c.y, c.z - 4
            )

    def _place_roads(self, roads):
        for road in roads:
            neighbors = []
            second_block = None
            if road.terrain == Biome.WATER:
                block_type = block.WOOD_PLANKS.id
                second_block = block.WOOD.id
                random_type = None
            elif road.terrain == Biome.SAND:
                block_type = block.COBBLESTONE.id
                random_type = [block.SAND.id]

            else:
                block_type = block.COBBLESTONE.id
                random_type = [block.GRASS.id, block.MOSS_STONE.id,
                               block.MOSS_STONE.id, block.COBBLESTONE.id]

            for adjacent in self.grid.adjacency_list[road]:
                if adjacent in roads:
                    neighbors.append(adjacent)

            self._place_road_square(road.position, block_type, random_type)

            for join in neighbors:
                self._place_road_connector(
                    road.position, join.position, block_type, second_block)

    @staticmethod
    def _place_road_square(a, block_type, random_type):
        set_blocks(
            a.x - 1, a.y - 1, a.z - 1,
            a.x + 1, a.y, a.z + 1, block_type
        )

        if random_type is not None:
            for i in range(3):
                for j in range(3):
                    if random.randint(1, 4) == 1:
                        set_block(a.x - 1 + i, a.y, a.z - 1 +
                                  j, random.choice(random_type))

        set_blocks(
            a.x - 1, a.y + 1, a.z - 1,
            a.x + 1, a.y + 30, a.z + 1, block.AIR.id
        )

    @staticmethod
    def _place_road_connector(a, b, block_type, second):
        # if the tiles are connected via the x axis
        height_difference = (b.y - a.y) // 2

        if a.x != b.x:
            if a.x < b.x:
                set_blocks(a.x + 2, a.y - 1, a.z - 1,
                           a.x + 2, a.y + height_difference, a.z + 1, block_type)

                set_blocks(a.x + 2, a.y + height_difference + 1, a.z - 1,
                           a.x + 2, a.y + height_difference + 30, a.z + 1, block.AIR.id)
                if second:
                    set_blocks(a.x + 2, a.y - 10, a.z + 2,
                               a.x + 2, a.y, a.z + 2, second)
                    set_blocks(a.x + 2, a.y - 10, a.z - 2,
                               a.x + 2, a.y, a.z - 2, second)
            elif a.x > b.x:
                set_blocks(a.x - 2, a.y - 1, a.z - 1,
                           a.x - 2, a.y + height_difference, a.z + 1, block_type)

                set_blocks(a.x - 2, a.y + height_difference + 1, a.z - 1,
                           a.x - 2, a.y + height_difference + 30, a.z + 1, block.AIR.id)
                if second:
                    set_blocks(a.x - 2, a.y - 10, a.z + 2,
                               a.x - 2, a.y, a.z + 2, second)
                    set_blocks(a.x - 2, a.y - 10, a.z - 2,
                               a.x - 2, a.y, a.z - 2, second)

        # if the tiles are connected via the z axis
        else:
            if a.z < b.z:
                set_blocks(a.x - 1, a.y - 1, a.z + 2,
                           a.x + 1, a.y + height_difference, a.z + 2, block_type)

                set_blocks(a.x - 1, a.y + height_difference + 1, a.z + 2,
                           a.x + 1, a.y + height_difference + 30, a.z + 2, block.AIR.id)
                if second:
                    set_blocks(a.x + 2, a.y - 10, a.z + 2,
                               a.x + 2, a.y, a.z + 2, second)
                    set_blocks(a.x - 2, a.y - 10, a.z + 2,
                               a.x - 2, a.y, a.z + 2, second)

            elif a.z > b.z:
                set_blocks(a.x - 1, a.y - 1, a.z - 2,
                           a.x + 1, a.y + height_difference, a.z - 2, block_type)

                set_blocks(a.x - 1, a.y + height_difference + 1, a.z - 2,
                           a.x + 1, a.y + height_difference + 30, a.z - 2, block.AIR.id)
                if second:
                    set_blocks(a.x + 2, a.y - 30, a.z - 2,
                               a.x + 2, a.y, a.z - 2, second)
                    set_blocks(a.x - 2, a.y - 30, a.z - 2,
                               a.x - 2, a.y, a.z - 2, second)

    def _get_candidate_doors(self, plot):
        doors = set()

        start_coord = plot.coordinate

        options = [
            (start_coord[0] - 2, start_coord[1]),
            (start_coord[0] + 2, start_coord[1]),
            (start_coord[0], start_coord[1] - 2),
            (start_coord[0], start_coord[1] + 2)
        ]

        for coord in options:
            tile = self.grid.find_tile(coordinate=coord)
            if tile is None:
                continue
            else:
                doors.add(tile)
        return doors

    def build_tc(self):
        # Select possible tc functions for each type at random.
        if self.grid.center.terrain == Biome.SAND:
            tc_function = random.choice(self.sand_tcs)
        elif self.grid.center.terrain == Biome.GROUND:
            tc_function = random.choice(self.grass_tcs)
        elif self.grid.center.terrain == Biome.WATER:
            tc_function = random.choice(self.water_tcs)
        else:
            post('Invalid town center tile.')
            return

        tc_function()

    def _tc_pyramid(self):
        c = self.grid.center.position
        sandstones = [(24, 2), (179, 2)]
        offset = 1
        for index in reversed(range(5)):
            mod = index % 2
            set_blocks(
                c.x - index, c.y - 1 + offset, c.z - index,
                c.x + index, c.y - 1 + offset, c.z + index,
                sandstones[mod]
            )
            offset += 1
        set_blocks(
            c.x - 6, c.y - 1, c.z - 6,
            c.x + 6, c.y - 10, c.z + 6,
            sandstones[0]
        )

    def _tc_temple(self):
        self._tc_pyramid()
        c = self.grid.center.position
        set_blocks(
            c.x + 1, c.y + 4, c.z + 1,
            c.x - 1, c.y + 7, c.z - 1,
            block.AIR.id
        )
        for index in range(2):
            set_block(c.x + 1, c.y + 4 + index, c.z + 1, (24, 2))
            set_block(c.x + 1, c.y + 4 + index, c.z - 1, (24, 2))
            set_block(c.x - 1, c.y + 4 + index, c.z + 1, (24, 2))
            set_block(c.x - 1, c.y + 4 + index, c.z - 1, (24, 2))
        set_blocks(
            c.x + 1, c.y + 6, c.z + 1,
            c.x - 1, c.y + 6, c.z - 1,
            (179, 1)
        )
        set_block(c.x + 1, c.y + 6, c.z, (179, 2))
        set_block(c.x - 1, c.y + 6, c.z, (179, 2))
        set_block(c.x, c.y + 6, c.z + 1, (179, 2))
        set_block(c.x, c.y + 6, c.z - 1, (179, 2))

    def _tc_well(self):
        c = self.grid.center.position
        well = [
            block.WATER.id, block.LAVA.id
        ]
        set_blocks(
            c.x + 1, c.y, c.z + 1,
            c.x - 1, c.y - 6, c.z - 1,
            block.STONE.id
        )
        set_blocks(
            c.x, c.y, c.z,
            c.x, c.y - 6, c.z,
            block.AIR.id
        )
        set_blocks(
            c.x, c.y - 3, c.z,
            c.x, c.y - 6, c.z,
            random.choice(well)
        )
        for index in range(1, 5):
            material = block.COBBLESTONE.id if index == 1 else block.FENCE.id
            set_block(c.x - 1, c.y + index, c.z - 1, material)
            set_block(c.x + 1, c.y + index, c.z - 1, material)
            set_block(c.x - 1, c.y + index, c.z + 1, material)
            set_block(c.x + 1, c.y + index, c.z + 1, material)

        material = block.FENCE.id
        set_block(c.x - 1, c.y + 4, c.z, material)
        set_block(c.x + 1, c.y + 4, c.z, material)
        set_blocks(
            c.x + 1, c.y + 5, c.z + 1,
            c.x - 1, c.y + 5, c.z - 1,
            (126, 5)
        )
        set_block(c.x, c.y + 5, c.z, (5, 5))

        set_block(c.x - 1, c.y + 1, c.z, block.STONE_SLAB.id)
        set_block(c.x + 1, c.y + 1, c.z, block.STONE_SLAB.id)
        set_block(c.x, c.y + 1, c.z + 1, block.STONE_SLAB.id)
        set_block(c.x, c.y + 1, c.z - 1, block.STONE_SLAB.id)

    def _tc_melon_pumpkin(self):
        choice = random.choice([
            (block.MELON.id, [35, 14]),
            # Pumpkin doesn't work because they're carved. :(
            # (block.PUMPKIN.id, [35, 1])
        ])
        c = self.grid.center.position
        set_blocks(
            c.x + 2, c.y + 1, c.z + 2,
            c.x - 2, c.y + 5, c.z - 2,
            choice[0]
        )
        for i in {1, 5}:
            set_block(c.x + 2, c.y + i, c.z + 2, block.AIR.id)
            set_block(c.x - 2, c.y + i, c.z + 2, block.AIR.id)
            set_block(c.x + 2, c.y + i, c.z - 2, block.AIR.id)
            set_block(c.x - 2, c.y + i, c.z - 2, block.AIR.id)
        set_blocks(
            c.x + 1, c.y + 2, c.z + 1,
            c.x - 1, c.y + 4, c.z - 1,
            choice[1]  # Wool Interior
        )
        # Scatter a random number of smaller ones around the place.
        count = random.randint(6, 18)
        coordinates = list()
        for i in range(count):
            x = random.randint(-7, 7)
            y = random.randint(-7, 7)
            coordinates.append((x, y))
        disallowed = set(range(-3, 4))
        for x, y in coordinates[::-1]:
            if x in disallowed or y in disallowed:
                coordinates.remove((x, y))
        for i, j in coordinates:
            set_block(
                c.x + i, get_height(c.x + i, c.z + j) + 1, c.z + j,
                choice[0]
            )
        if choice[0] == block.PUMPKIN.id:
            spruce = [17, 1]
            set_block(c.x, c.y + 6, c.z, spruce)
            set_block(c.x, c.y + 7, c.z + 1, spruce)

    def _tc_pool(self):
        c = self.grid.center.position
        set_blocks(
            c.x + 3, c.y, c.z + 3,
            c.x - 3, c.y, c.z - 3,
            (5, 1)
        )
        set_blocks(
            c.x + 2, c.y, c.z + 2,
            c.x - 2, c.y - 3, c.z - 2,
            block.WATER.id
        )
        set_blocks(
            c.x + 3, c.y + 1, c.z + 3,
            c.x - 3, c.y + 1, c.z - 3,
            block.FENCE_DARK_OAK.id
        )
        set_blocks(
            c.x + 2, c.y + 1, c.z + 2,
            c.x - 2, c.y + 1, c.z - 2,
            block.AIR.id
        )
        set_block(c.x + 3, c.y + 1, c.z, block.AIR.id)
        set_block(c.x - 3, c.y + 1, c.z, block.AIR.id)
        set_block(c.x, c.y + 1, c.z + 3, block.AIR.id)
        set_block(c.x, c.y + 1, c.z - 3, block.AIR.id)

    def _tc_obelisk(self):
        c = self.grid.center.position
        set_blocks(
            c.x + 2, c.y, c.z + 2,
            c.x - 2, c.y + 50, c.z - 2,
            block.OBSIDIAN.id)

        set_blocks(
            c.x + 1, c.y + 50, c.z + 1,
            c.x - 1, c.y + 55, c.z - 1,
            block.OBSIDIAN.id)

        set_blocks(
            c.x, c.y + 55, c.z,
            c.x, c.y + 57, c.z,
            block.OBSIDIAN.id)

    def _tc_fountain(self):
        if self.grid.center.terrain == Biome.SAND:
            materials = {
                'border': (24, 2),
                'corner': (24, 1),
                'slab': (44, 1),
            }
        else:
            materials = {
                'border': 98,
                'corner': (98, 3),
                'slab': (44, 5),
            }
        c = self.grid.center.position
        for index in range(-2, 2):
            set_blocks(
                c.x + 2, c.y + index, c.z + 2,
                c.x - 2, c.y + index, c.z - 2,
                materials['border']
            )
            set_blocks(
                c.x + 1, c.y + index, c.z + 1,
                c.x - 1, c.y + index, c.z - 1,
                block.WATER.id
            )
        for index, element in enumerate(
            [materials['corner'], materials['slab']]
        ):
            set_block(c.x + 2, c.y + index + 1, c.z + 2, element)
            set_block(c.x + 2, c.y + index + 1, c.z - 2, element)
            set_block(c.x - 2, c.y + index + 1, c.z + 2, element)
            set_block(c.x - 2, c.y + index + 1, c.z - 2, element)
        set_blocks(
            c.x, c.y - 2, c.z,
            c.x, c.y + 4, c.z,
            251  # White Concrete
        )
        set_block(c.x, c.y + 5, c.z, block.WATER.id)

    def _tc_nether_portal(self):
        if self.grid.center.terrain == Biome.SAND:
            blocks = [
                block.COBBLESTONE.id,
                block.SAND.id,
            ]
        elif self.grid.center.terrain == Biome.WATER:
            blocks = [
                block.WOOD_PLANKS.id,
                (5, 1),  # Spruce Wood Planks
            ]
        else:
            blocks = [
                block.COBBLESTONE.id,
                block.GRASS.id,
            ]
        blocks.extend([
            block.NETHERRACK.id,
            213,  # Magma
            214,  # Nether Wart
        ])
        c = self.grid.center.position
        selections = random.choices(blocks, weights=(40, 20, 30, 5, 5), k=121)
        index = 0
        for i in range(-5, 6):
            for j in range(-5, 6):
                set_block(c.x + i, get_height(c.x + 1, c.z + j),
                          c.z + j, selections[index])
                index += 1
        # Change weights for denser inner area.
        selections = random.choices(blocks, weights=(15, 5, 50, 5, 25), k=49)
        index = 0
        for i in range(-3, 4):
            for j in range(-3, 4):
                set_block(c.x + i, get_height(c.x + 1, c.z + j),
                          c.z + j, selections[index])
                index += 1
        set_blocks(
            c.x - 2, c.y + 1, c.z,
            c.x + 2, c.y + 10, c.z,
            block.OBSIDIAN.id
        )
        set_blocks(
            c.x + 1, c.y + 2, c.z,
            c.x - 1, c.y + 9, c.z,
            90  # Nether Portal
        )

    def _tc_end_portal(self):
        blocks = [98, (98, 1), (98, 2)]
        selections = random.choices(blocks, weights=(50, 25, 25), k=49)
        c = self.grid.center.position
        set_blocks(
            c.x - 4, c.y + 1, c.z + 4,
            c.x + 4, c.y + 1, c.z - 4,
            (44, 5)  # Stone Brick Slab
        )
        index = 0
        for i in range(-3, 4):
            for j in range(-3, 4):
                set_block(c.x + i, c.y + 1, c.z + j, selections[index])
                index += 1
        set_blocks(
            c.x - 2, c.y + 1, c.z + 2,
            c.x + 2, c.y + 1, c.z - 2,
            120  # End Portal Frame
        )
        set_blocks(
            c.x - 1, c.y + 1, c.z + 1,
            c.x + 1, c.y + 1, c.z - 1,
            119  # End Portal
        )


def main():
    Village(max_houses=200, max_grid_size=1000)


if __name__ == '__main__':
    main()
