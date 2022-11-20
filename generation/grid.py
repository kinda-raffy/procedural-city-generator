from biome import Biome
from mcpi.minecraft import Minecraft
from mcpi.vec3 import Vec3
import mcpi.block as block
from typing import TypeVar

T = TypeVar('T')

mc = Minecraft.create()
post = mc.postToChat
player_tile_position = mc.player.getTilePos
get_blocks = mc.getBlocks
get_block = mc.getBlock
set_blocks = mc.setBlocks
set_block = mc.setBlock
get_height = mc.getHeight


class Grid:
    """
    - Dynamically generates and maintains a weighted graph of connected tile objects that respects terrain.
    - Clears trees if necessary to allow for the placement of structures.
    - Implements methods to determine the shortest path from one tile to another, accounting for edge weights.
    
    """

    def __init__(self, max_size):
        self.adjacency_list = dict()
        self.edge_weights = dict()
        self.max_size = max_size
        self.start = player_tile_position()
        # Arbitrary constants.
        self.dimension = 8
        self.stride = 4
        self.tolerance = 2
        # Build smaller square grid of tiles.
        self.build()
        self.forest = False
        if self.test_trees():
            self.forest = True
            self.resolve_trees()
        self.connect()
        # Remove disconnected areas of matrix.
        self.adjacency_list = self.cull(
            self.connected_area()
        )
        self.explore()
        self.adjacency_list = self.cull(
            self.connected_area()
        )
        self.center = self.find_center()

    def __iter__(self):
        for tile in self.adjacency_list.keys():
            yield tile

    def __len__(self):
        return len(self.adjacency_list)

    def build(self):
        post(f'Generating matrix. Dimension {self.dimension}.')
        for i in range(self.dimension):
            x = self.start.x \
                + (i - self.dimension / 2) \
                * self.stride
            for j in range(self.dimension):
                z = self.start.z \
                    + (j - self.dimension / 2) \
                    * self.stride
                y = get_height(x, z)
                vector = Vec3(x, y, z)
                self.add_tile(Tile(vector, (i, j)))
            percentage = (i * self.dimension) / (self.dimension ** 2) * 100
            post(f'{percentage:.0f}%')
        post('Matrix complete.')

    def connect(self):
        post('Connecting matrix.')
        for tile in self:
            coordinate = tile.coordinate
            if coordinate[0] < self.dimension - 1:
                second = (coordinate[0] + 1, coordinate[1])
                self.add_edge(tile, self.find_tile(coordinate=second))
            if coordinate[1] < self.dimension - 1:
                second = (coordinate[0], coordinate[1] + 1)
                self.add_edge(tile, self.find_tile(coordinate=second))
        post('Matrix connected.')

    def explore(self):
        post('Building organic grid.')
        stride = self.stride
        maximum = self.max_size
        # minimum = 100
        discovered = set()
        network = list()
        # backup = list()
        indices = {0, self.dimension - 1}
        frontier = [
            # All tiles on the edges of the matrix.
            x for x in self
            if x.coordinate[0] in indices
            or x.coordinate[1] in indices
        ]
        while frontier and len(network) <= maximum:
            current = frontier.pop(0)
            # Ignore anything that isn't a tile.
            if not isinstance(current, Tile):
                continue
            if current not in discovered:
                discovered.add(current)
                network.append(current)
                x, z = current.coordinate
                tiles = self._connect(current, x, z)
                # North
                if tiles[0] is False:
                    vector = Vec3(
                        current.position.x - stride,
                        get_height(
                            current.position.x - stride,
                            current.position.z
                        ),
                        current.position.z
                    )
                    north = Tile(
                        vector,
                        (x - 1, z)
                    )
                    self.resolve_trees(tile=north) if self.forest else None
                    self._explore(current, north, frontier)
                # East
                if tiles[1] is False:
                    vector = Vec3(
                        current.position.x,
                        get_height(
                            current.position.x,
                            current.position.z + stride
                        ),
                        current.position.z + stride
                    )
                    east = Tile(
                        vector,
                        (x, z + 1)
                    )
                    self.resolve_trees(tile=east) if self.forest else None
                    self._explore(current, east, frontier)
                # South
                if tiles[2] is False:
                    vector = Vec3(
                        current.position.x + stride,
                        get_height(
                            current.position.x + stride,
                            current.position.z
                        ),
                        current.position.z
                    )
                    south = Tile(
                        vector,
                        (x + 1, z)
                    )
                    self.resolve_trees(tile=south) if self.forest else None
                    self._explore(current, south, frontier)
                # West
                if tiles[3] is False:
                    vector = Vec3(
                        current.position.x,
                        get_height(
                            current.position.x,
                            current.position.z - stride
                        ),
                        current.position.z - stride
                    )
                    west = Tile(
                        vector,
                        (x, z - 1)
                    )
                    self.resolve_trees(tile=west) if self.forest else None
                    self._explore(current, west, frontier)
            # Print percentage.
            if (percent := len(network)) % 10 == 0:
                post(f"{percent // (maximum // 100)}%")
        for tile in self:
            self._connect(tile)
        post('Organic grid complete.')
        return network

    def _explore(self, current, adjacent, frontier):
        self.add_tile(adjacent)
        if self.add_edge(current, adjacent):
            frontier.append(adjacent)

    def _connect(self, tile, x=None, z=None):
        if x is None or z is None:
            x, z = tile.coordinate
        tiles = [False, False, False, False]
        if north := self.find_tile(coordinate=(x - 1, z)):
            self.add_edge(tile, north)
            tiles[0] = True
        if east := self.find_tile(coordinate=(x, z + 1)):
            self.add_edge(tile, east)
            tiles[1] = True
        if south := self.find_tile(coordinate=(x + 1, z)):
            self.add_edge(tile, south)
            tiles[2] = True
        if west := self.find_tile(coordinate=(x, z - 1)):
            self.add_edge(tile, west)
            tiles[3] = True
        return tiles

    def cull(self, tiles):
        final = self.adjacency_list.copy()
        loop = self.adjacency_list.copy()
        for tile in loop:
            # If tile not in main area, delete from adjacency list.
            if tile not in tiles:
                del final[tile]
        return final

    def test_trees(self, threshold=0.4):
        total = 0
        cutoff = int(len(self) * threshold)
        for tile in self:
            if tile.terrain == Biome.TREE:
                total += 1
            if total >= cutoff:
                return True
        return False

    def resolve_trees(self, tile=None):
        if tile is None:
            trees = [x for x in self if x.terrain == Biome.TREE]
        else:
            trees = [tile]
            if tile.terrain != Biome.TREE:
                return
        for tile in trees:
            x = tile.position.x
            z = tile.position.z
            while True:
                if get_block(x, tile.position.y, z) in {
                    1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13,
                    14, 15, 16, 24, 49, 82,
                }:
                    set_blocks(
                        x - 1, tile.position.y + 1, z - 1,
                        x + 2, tile.position.y + 20, z + 2,
                        block.AIR.id
                    )
                    tile.terrain = tile.find_terrain()
                    break
                tile.position.y -= 1

    def find_tile(self, coordinate=None, vector=None):
        if isinstance(vector, Vec3):
            for tile in self:
                if tile.position == vector:
                    return tile
        elif isinstance(coordinate, tuple) \
                and len(coordinate) == 2:
            for tile in self:
                if tile.coordinate == coordinate:
                    return tile
        return None

    def add_tile(self, tile):
        try:
            if not isinstance(tile, Tile):
                raise TypeError('Only tiles can be added to grid.')
            self.adjacency_list[tile] = list()
        except TypeError as error:
            post(error)

    def add_edge(self, tile_a, tile_b):
        # If edge already exists, return false.
        if (tile_a, tile_b) in self.edge_weights or \
                (tile_b, tile_a) in self.edge_weights:
            return False
        weight = self.calculate_weight(tile_a, tile_b)
        # If weight invalid, return false.
        if weight is None:
            return False
        for x, y in {
            (tile_a, tile_b), (tile_b, tile_a)
        }:
            try:
                self.adjacency_list[x].append(y)
                self.edge_weights[(x, y)] = weight
            except KeyError as error:
                post(error)
        # If successful, return true.
        return True

    def calculate_weight(self, tile_a, tile_b):
        prohibited = {Biome.LAVA, Biome.TREE}
        if (tile_a.terrain in prohibited) or \
                (tile_b.terrain in prohibited):
            return None
        difference = abs(tile_a.position.y -
                         tile_b.position.y)
        if difference > self.tolerance:
            return None

        weight = difference + 2
        if tile_a.terrain == Biome.WATER or \
                tile_b.terrain == Biome.WATER:
            weight += 8

        return weight

    def connected_area(self):
        post('Finding largest connected area.')
        discovered = set()
        largest = list()
        for tile in self:
            # Breadth first search begins.
            if tile not in discovered:
                discovered.add(tile)
                frontier = list()
                network = list()
                frontier.append(tile)
                while frontier:
                    current_tile = frontier.pop(0)
                    network.append(current_tile)
                    for adjacent_tile in self.adjacency_list[current_tile]:
                        if adjacent_tile not in discovered:
                            discovered.add(adjacent_tile)
                            frontier.append(adjacent_tile)
                if len(network) > len(largest):
                    largest.clear()
                    largest.extend(network)
                    network.clear()
        return largest

    def find_center(self):
        post('Finding center.')
        available = list(
            filter(
                self.is_3x3,
                self.adjacency_list.keys()
            )
        )
        min_x = max_x = available[0].coordinate[0]
        min_z = max_z = available[0].coordinate[1]
        for current in available:
            cord = current.coordinate
            if cord[0] < min_x:
                min_x = cord[0]
            if cord[0] > max_x:
                max_x = cord[0]
            if cord[1] < min_z:
                min_z = cord[1]
            if cord[1] > max_z:
                max_z = cord[1]
        midpoint = (
            (min_x + max_x) // 2,
            (min_z + max_z) // 2,
        )
        closest_tile = None
        closest_dist = None
        for current_tile in available:
            cord = current_tile.coordinate
            if closest_tile is None:
                closest_tile = current_tile
                closest_dist = \
                    abs(cord[0] - midpoint[0]) + \
                    abs(cord[1] - midpoint[1])
            else:
                current_dist = \
                    abs(cord[0] - midpoint[0]) + \
                    abs(cord[1] - midpoint[1])
                if current_dist < closest_dist:
                    closest_tile = current_tile
                    closest_dist = current_dist
        return closest_tile

    def show_edges(self, tile):
        for neighbour in self.adjacency_list[tile]:
            if neighbour.position.x > tile.position.x:
                mc.setBlock(
                    tile.position.x + 2, tile.position.y,
                    tile.position.z, block.STONE.id
                )
            if neighbour.position.z > tile.position.z:
                mc.setBlock(
                    tile.position.x, tile.position.y,
                    tile.position.z + 2, block.STONE.id
                )

    def is_3x3(self, point, threshold=7):
        if len(self.adjacency_list[point]) < 4:
            return False
        count = 0
        px, pz = point.coordinate[0], point.coordinate[1]
        for coordinate in {
            (px - 1, pz - 1),
            (px - 1, pz + 1),
            (px + 1, pz - 1),
            (px + 1, pz + 1),
        }:
            for neighbour in self.adjacency_list[point]:
                if coordinate in list(
                    map(
                        lambda tile: tile.coordinate,
                        self.adjacency_list[neighbour]
                    )
                ):
                    count += 1
        return True if count > threshold else False

    def get_square(self, point, size=3):
        tiles = set()
        for i in range(-size // 2 + 1, size // 2 + 1):
            for j in range(-size // 2 + 1, size // 2 + 1):
                tiles.add(
                    self.find_tile(
                        coordinate=(point.coordinate[0] + i,
                                    point.coordinate[1] + j)
                    )
                )
        tiles = tiles.difference({None})
        return tiles

    def dijkstra(self, available: set = None):
        if available is None:
            available = self
        start = self.center
        unvisited = list()
        for tile in available:
            unvisited.append(tile)
        # Start tile has distance 0 from itself.
        start.distance = 0
        while unvisited:
            # Find index of tile with minimum distance from center.
            smallest = 0
            for index in range(1, len(unvisited)):
                if unvisited[index].distance < unvisited[smallest].distance:
                    smallest = index
            # Visit tile with minimum distance.
            current = unvisited.pop(smallest)

            # Check potential path lengths from current vertex to neighbours.
            for adjacent in self.adjacency_list[current]:
                if adjacent in available:
                    edge_weight = self.edge_weights[(current, adjacent)]
                    path_distance = current.distance + edge_weight
                    # If shorter path found, update adjacent distance and predecessor.
                    if path_distance < adjacent.distance:
                        adjacent.distance = path_distance
                        adjacent.predecessor = current

    def shortest_path(self, destination, start=None):
        if start is None:
            start = self.center
        path = list()
        current = destination
        while current is not start:
            try:
                if not isinstance(current, Tile):
                    raise TypeError
                path.append(current)
                current = current.predecessor
            except (AttributeError, TypeError):
                return False
        path.append(start)

        # Debugging messages.
        # coords = list(
        #     map(
        #         lambda x: f'({x[0]}, {x[1]})',
        #         map(lambda x: x.coordinate, path)
        #     )
        # )
        # coords = reversed(coords)
        # path_string = ' -> '.join(coords)
        # post(f'Path: {path_string}')

        return path


class Tile:
    """
    - 3x3 block vertices of graph structure in Grid.
    - Store the position of center block as a Vec3.
    - Store their unique Cartesian coordinate relative to the overall grid.
    - Store their distance from starting tile of last iteration of Dijkstra's algorithm.
    - Determines and stores the terrain type of the center tile.

    """

    def __init__(self, position, coordinate):
        self.position = position
        self.coordinate = coordinate
        self.predecessor = None
        self.distance = float('inf')
        self.terrain = self.find_terrain()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        if not isinstance(position, Vec3):
            raise TypeError('Position must be a vector.')
        self._position = position

    @property
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        if not isinstance(coordinate, tuple) or \
                len(coordinate) != 2:
            raise TypeError('Coordinate must be a tuple with two elements.')
        self._coordinate = coordinate

    def find_terrain(self):
        x = self.position.x
        y = self.position.y
        z = self.position.z
        under = get_block(x, y, z)

        if under in {8, 9}:
            return Biome.WATER
        elif under in {10, 11}:
            return Biome.LAVA
        elif under in {18, 81, 83, 39, 40, 17, 261, 579, 580}:
            return Biome.TREE
        elif under in {12, 24}:
            return Biome.SAND
        else:
            return Biome.GROUND


def main():
    pass


if __name__ == '__main__':
    main()
