"""
INSTRUCTOR PLEASE READ;
house.py randomly generates the following:
House:
- Number of rooms
- Room placement
- Room size
- Different start room locations (for both stairs and doors)
- Different types of stairs
- Internal wall types (Global)
- Upstairs generation (incl. upstairs room size and placement + how many floors)
- Different material types depending on the type of biome the house generates on
- Accommodates for extremely rare disasters (kitchen fire and laboratory explosion): 1/196 per room spawned

Pools:
- Pool placement
- Pool size
- Different types of pool wall types
- Pool covers (shade)
- Indoor pools and outside pools

Room Parts:
- Different types of roofs (Global)
- Different types of windows
- Removal of random walls
- 27 different types of furnishing that are than scaled (in a way that makes sense) to randomly sized rooms.

Apartments and Skyscrapers:
- Randomly generates on the grass biome (1/3 chance)
- Disasters have a lower chance of occurring due to higher regulations in big buildings: 1/2744 per room spawned
- Apartments and skyscrapers both have different probability of generating a unique top
(the highest floors in the buildings will be placed differently to create a shape that is unique to the building)
- Skyscrapers randomly follows a different architectural rulebook (for example: some may have a fat base and skinny top
while others may have a skinny base and fat top).

High-level overview:
House class is responsible for the placement of entire rooms. It is the one that calls on the room class to generate
rooms. As it knows which room is placed where and how long each room is, it is responsible for furnishing as well.
It instructs the room class the type of room it will become and stores randomly generated options in its init that
we want to keep consistent throughout the entire house (for ex. roof types).
The room class just builds the room and stores some useful information about itself in its init. Some operations may
include building structure, adding roofs and internal walls.
TLDR; House class decides and instructs, room class just execute upon those instructions.

authors: Raf, Matt
"""
from mcpi.minecraft import Minecraft
from mcpi import block
from mcpi.vec3 import Vec3
import random
from time import sleep
from house_config import blocks, apartment_biome, sand_biome, grass_biome, water_biome, furniture

mc = Minecraft.create()
sleep_time = 0


class House:
    """
    House class randomly generates the structure of the house.
    - Most of the random generation goes on here.
    - Responsible for randomly generating 5 * 5 rooms based off a 3 * 3 grid.
    - Finds appropriate pool locations and size
    - Finds the length of each rooms based off a generated list, and furnishes the rooms randomly.
    """
    def __init__(self, center, door_room, biome=0):
        self.internal_wall_dice = random.randint(0, 2)
        self.stair_type = random.choice(['basic', 'double_stairs', 'double_slab'])
        self.roof_type = random.choices(['flat', 'angled_flat', 'stair_flat', 'stair_med'],
                                        weights=[1, 10, 6, 10])[0]
        self.global_index = 0
        self.large_building_type = ''
        self.apartment_pool = 0
        self.biome = biome
        self.door_room = door_room
        self.center = center
        self.mat_pack = self.biome_selection()
        self.generated_rooms = {}
        self.furnish = {}
        self.bob_the_builder()
        self.main_door(door_center=door_room)

    def clear_space(self):
        x = self.center.x
        y = self.center.y + 1
        z = self.center.z
        mc.setBlocks(x - 7, y + 1, z - 7,
                     x + 7, y + 7, z + 7, block.AIR.id)

    def biome_selection(self):
        biome = self.biome
        if biome == 0:
            return random.choice(grass_biome)
        elif biome == 1:
            return random.choice(sand_biome)
        elif biome == 2:
            return random.choice(water_biome)
        elif biome == 3:
            return random.choice(apartment_biome)
        else:
            raise RuntimeError('Incorrect biome input given')

    def bob_the_builder(self):
        """
        Bob the builder, can we build it?
        Decides which buildings to build based off parameters and randomness
        """
        if not self.biome == 3:
            self.house()
        elif self.biome == 3:
            if random.randint(1, 3) == 1:
                # Build skyscraper
                self.large_building_type = 'skyscraper'
                self.large_building(lb_low=10, lb_high=16, lb_mode=16)
            else:
                # Build apartment with default values
                self.large_building_type = 'apartment'
                self.large_building()

        else:
            raise RuntimeError("No I can't.")

    def large_building(self, lb_low=4, lb_high=8, lb_mode=8):
        # override global variables
        self.roof_type = 'flat'

        # create the first level
        self.create_downstairs()
        ground = House.dict_to_list(self.generated_rooms)
        if self.apartment_pool:
            self.find_pool_location(ground=ground)
        sleep(sleep_time)
        ground_floor = False
        upstairs = None
        start_room_vec = None
        start_room_name = ''
        level_y_start = 4
        self.global_index = 1

        # determine the number of floors the apartment will have (first floor excluded so max 6 [bias casts as int])
        for floor_num in range(1, bias_random(low=lb_low, high=lb_high, mode=lb_mode)):
            if self.generated_rooms['true_center'][0] is True:
                # handle the door room exception for the second level
                # find stair location
                if floor_num == 1:
                    start_room_name, start_room_vec = self.find_start_location(
                        no_spawn_room=self.door_room - Vec3(2, 0, 2))
                else:
                    if start_room_name is not False and start_room_vec is not False:
                        if start_room_vec is not None:
                            start_room_name, start_room_vec = self.find_start_location(
                                no_spawn_room=start_room_vec - Vec3(2, 0, 2))
                        else:
                            raise RuntimeError('Start room vec is', start_room_vec, 'on floor_num:', floor_num)
                    else:
                        print('An upstairs call has been denied due to impossible probability')
                        # furnishing for downstairs if upstairs call has been denied
                        for i in range(6, 9):
                            self.create_furnish(gr_list=upstairs, index=i)
                        self.place_furniture()

                if start_room_name is not False and start_room_vec is not False:
                    # change to stair room type
                    self.generated_rooms[start_room_name][1].room_type = 'downstairs_stairs'
                    self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)
                    # furnishing for ground floor
                    if floor_num == 1:
                        for i in range(6, 9):
                            self.create_furnish(gr_list=ground, index=i)
                        self.place_furniture()
                    # furnishing for the floor below (this happens at the next iteration)
                    else:
                        if upstairs is not None:
                            for i in range(6, 9):
                                self.create_furnish(gr_list=upstairs, index=i)
                            self.place_furniture()
                        else:
                            raise RuntimeError('upstairs is', upstairs, 'on floor_num:', floor_num)

                    # create the upstairs
                    upstairs_floor_map = self.create_upstairs(ground_floor=ground_floor,
                                                              start_room_vec=start_room_vec,
                                                              level_y_start=level_y_start)
                    level_y_start += 4
                    upstairs = House.dict_to_list(upstairs_floor_map)
                    # create upstairs stairs
                    self.generated_rooms[start_room_name][1].room_type = 'upstairs_stairs'
                    self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)
                    self.global_index += 1
                else:
                    if floor_num == 1:
                        print('An upstairs call has been denied due to impossible probability')
                        # furnishing for downstairs if upstairs call has been denied
                        for i in range(6, 9):
                            self.create_furnish(gr_list=ground, index=i)
                        self.place_furniture()
                    else:
                        print('An upstairs call has been denied due to impossible probability')
                        # furnishing for downstairs if upstairs call has been denied
                        for i in range(6, 9):
                            self.create_furnish(gr_list=upstairs, index=i)
                        self.place_furniture()
            else:
                print('An upstairs call has been denied | No true center')
                # furnishing for level below if upstairs call has been denied
                if floor_num == 1:
                    for i in range(6, 9):
                        self.create_furnish(gr_list=ground, index=i)
                    self.place_furniture()
                else:
                    for i in range(6, 9):
                        self.create_furnish(gr_list=upstairs, index=i)
                    self.place_furniture()

    def house(self):
        double_story = random.randint(0, 10)
        self.create_downstairs()
        ground = House.dict_to_list(self.generated_rooms)
        self.find_pool_location(ground=ground)
        sleep(sleep_time)

        if double_story > 2:
            ground_floor = False
            if self.generated_rooms['true_center'][0] is True:
                # find starting location of stairs
                start_room_name, start_room_vec = self.find_start_location(no_spawn_room=self.door_room - Vec3(2, 0, 2))
                if start_room_name is not False and start_room_vec is not False:
                    # change to stair room type
                    self.generated_rooms[start_room_name][1].room_type = 'downstairs_stairs'
                    self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)
                    # furnishing for downstairs
                    for i in range(6, 9):
                        self.create_furnish(gr_list=ground, index=i)
                    self.place_furniture()

                    # create the upstairs
                    upstairs_floor_map = self.create_upstairs(ground_floor=ground_floor,
                                                              start_room_vec=start_room_vec)
                    upstairs = House.dict_to_list(upstairs_floor_map)
                    # create upstairs stairs
                    self.generated_rooms[start_room_name][1].room_type = 'upstairs_stairs'
                    self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)

                    # find probability of triple story generation
                    if random.randint(1, 10) < 4:
                        start_room_name, start_room_vec = self.find_start_location(
                            no_spawn_room=start_room_vec - Vec3(2, 0, 2))
                        if start_room_name is not False and start_room_vec is not False:
                            # change to stair room type
                            self.generated_rooms[start_room_name][1].room_type = 'downstairs_stairs'
                            self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)
                            # furnishing for upstairs
                            for i in range(6, 9):
                                self.create_furnish(gr_list=upstairs, index=i)
                            self.place_furniture()

                            # create the level above
                            third_floor_map = self.create_upstairs(ground_floor=ground_floor,
                                                                   start_room_vec=start_room_vec, level_y_start=8)
                            if not third_floor_map:
                                return
                            third_level = House.dict_to_list(third_floor_map)
                            self.generated_rooms[start_room_name][1].room_type = 'upstairs_stairs'
                            self.generated_rooms[start_room_name][1].determine_room_type(stair_type=self.stair_type)
                            # furnishing for the third level
                            for i in range(6, 9):
                                self.create_furnish(gr_list=third_level, index=i)
                            self.place_furniture()
                        else:
                            print('An upstairs call has been denied due to impossible probability')
                            # furnishing for upstairs if level above has been denied
                            for i in range(6, 9):
                                self.create_furnish(gr_list=upstairs, index=i)
                            self.place_furniture()

                    else:
                        # furnishing for upstairs
                        for i in range(6, 9):
                            self.create_furnish(gr_list=upstairs, index=i)
                        self.place_furniture()
                else:
                    print('An upstairs call has been denied due to impossible probability')
                    # furnishing for downstairs if upstairs call has been denied
                    for i in range(6, 9):
                        self.create_furnish(gr_list=ground, index=i)
                    self.place_furniture()
            else:
                print('An upstairs call has been denied | No true center')
                # furnishing for downstairs if upstairs call has been denied
                for i in range(6, 9):
                    self.create_furnish(gr_list=ground, index=i)
                self.place_furniture()
        else:
            # furnishing for downstairs if upstairs call has been denied
            for i in range(6, 9):
                self.create_furnish(gr_list=ground, index=i)
            self.place_furniture()

    def create_furnish(self, gr_list: list, index: int):

        if gr_list[index][2].room_type == 'normal':
            if gr_list[index - 3][2].room_type == 'normal':
                if gr_list[index - 6][2].room_type == 'normal':
                    connected = House.get_room_ceil(gr_list[index][2].pos)
                    if not connected:
                        # add to connected rooms list: bottom_left size 1 end_cdr
                        self.furnish[str(gr_list[index][0]) + '1'] = \
                            [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index][2].pos + Vec3(3, 3, 3)]
                        connected = House.get_room_ceil(gr_list[index - 3][2].pos)
                        if not connected:
                            # center_left
                            self.furnish[str(gr_list[index - 3][0]) + '1'] = \
                                [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]
                            # top_left
                            self.furnish[str(gr_list[index - 6][0]) + '1'] = \
                                [gr_list[index - 6][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                        elif connected:
                            self.furnish[str(gr_list[index - 3][0]) + '-' + str(gr_list[index - 6][0]) + '2'] = \
                                [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                            return
                    else:
                        connected = House.get_room_ceil(gr_list[index - 3][2].pos)
                        if not connected:
                            # add to connected rooms list: bottom_left size 2 end_cdr (bottom_left and center_left)
                            self.furnish[str(gr_list[index][0]) + '-' + str(gr_list[index - 3][0]) + '2'] = \
                                [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]
                            # add to connected roms list: top left size 1
                            self.furnish[str(gr_list[index - 6][0]) + '1'] = \
                                [gr_list[index - 6][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                            return
                        else:
                            # add to connected rooms list: bottom_left size 3 end_cdr
                            # (bottom_left, center_left and top_left)
                            self.furnish[str(gr_list[index][0]) + '-' + str(gr_list[index - 3][0])
                                         + '-' + str(gr_list[index - 6][0]) + '3'] = \
                                [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                            return
                else:
                    connected = House.get_room_ceil(gr_list[index][2].pos)
                    if not connected:
                        # add to connected rooms list: bottom_left size 1 end_cdr
                        self.furnish[str(gr_list[index][0]) + '1'] = \
                            [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index][2].pos + Vec3(3, 3, 3)]
                        # add to connected rooms list: center_left size 1 end_cdr
                        self.furnish[str(gr_list[index - 3][0]) + '1'] = \
                            [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]

                    else:
                        self.furnish[str(gr_list[index][0]) + '-' + str(gr_list[index - 3][0]) + '2'] = \
                                [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]
            else:
                # add to connected rooms list: bottom_left size 1 end_cdr
                self.furnish[str(gr_list[index][0]) + '1'] = \
                    [gr_list[index][2].pos + Vec3(1, 1, 1), gr_list[index][2].pos + Vec3(3, 3, 3)]
                # check if top one exists
                if gr_list[index - 6][2].room_type == 'normal':
                    # add to connected rooms list: center_left size 1 end_cdr
                    self.furnish[str(gr_list[index - 6][0]) + '1'] = \
                        [gr_list[index - 6][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                    return

        # if bottom left doesnt exist but center left does
        elif gr_list[index - 3][2].room_type == 'normal':
            if gr_list[index - 6][2].room_type == 'normal':
                connected = House.get_room_ceil(gr_list[index - 3][2].pos)
                if not connected:
                    # add to connected rooms list: center_left size 1 end_cdr
                    self.furnish[str(gr_list[index - 3][0]) + '1'] = \
                        [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]
                    # add to connected rooms list: bottom_left size 1 end_cdr
                    self.furnish[str(gr_list[index - 6][0]) + '1'] = \
                        [gr_list[index - 6][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                    return
                else:
                    # add to connected rooms list: center_left size 2 end_cdr (center_left and  bottom_left)
                    self.furnish[str(gr_list[index - 3][0]) + '-' + str(gr_list[index - 6][0]) + '2'] = \
                        [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
                    return
            else:
                # add to connected rooms list: center_left size 1 end_cdr
                self.furnish[str(gr_list[index - 3][0]) + '1'] = \
                    [gr_list[index - 3][2].pos + Vec3(1, 1, 1), gr_list[index - 3][2].pos + Vec3(3, 3, 3)]

        elif gr_list[index - 6][2].room_type == 'normal':
            # add to connected rooms list: top_left size 1 end_cdr
            self.furnish[str(gr_list[index - 6][0]) + '1'] = \
                [gr_list[index - 6][2].pos + Vec3(1, 1, 1), gr_list[index - 6][2].pos + Vec3(3, 3, 3)]
            return

    @staticmethod
    def get_room_ceil(pos):
        air = 0
        ceil_check = mc.getBlock(pos.x + 4, pos.y + 3, pos.z + 3)
        if not ceil_check == air:
            return False
        else:
            return True

    def place_furniture(self):
        furnish = self.furnish
        local_furniture_list = furniture[:]
        matt_fur = random.choice(local_furniture_list)

        if matt_fur['floor_tl'] == blocks['fire']:
            matt_fur = random.choice(local_furniture_list)
        for key, value in furnish.items():
            start = value[0]
            end = value[1]
            print('Furnishing at:', key)
            if '1' in key:
                # main works well enough
                mc.setBlock(start.x + 1, start.y, start.z + 1, matt_fur['main'])
                sleep(sleep_time/2)
                mc.setBlock(start.x + 1, start.y + 1, start.z + 1, matt_fur['main_above'])
                sleep(sleep_time/2)
                mc.setBlock(start.x + 1, start.y + 2, start.z + 1, matt_fur['main_ceil'])
                sleep(sleep_time/2)
                # top corners works
                mc.setBlock(start.x, start.y + 2, start.z, matt_fur['ceil_tr'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z - 2, matt_fur['ceil_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y + 2, start.z + 2, matt_fur['ceil_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z, matt_fur['ceil_bl'])
                sleep(sleep_time/2)
                # bottom corners works
                mc.setBlock(start.x, start.y, start.z, matt_fur['floor_bl'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z - 2, matt_fur['floor_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y, start.z + 2, matt_fur['floor_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z, matt_fur['floor_tr'])
                sleep(sleep_time/2)
                # top centers
                mc.setBlock(start.x + 2, end.y, start.z + 1, matt_fur['ceil_front'])
                sleep(sleep_time/2)
                mc.setBlock(start.x + 1, end.y, start.z, matt_fur['ceil_left'])
                sleep(sleep_time/2)
                mc.setBlock(start.x + 1, end.y, start.z + 2, matt_fur['ceil_right'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y + 2, start.z + 1, matt_fur['ceil_back'])
                sleep(sleep_time/2)

            elif '2' in key:
                # main works
                mc.setBlocks(start.x + 2, start.y, start.z + 1, end.x - 2, start.y, end.z - 1, matt_fur['main'])
                sleep(sleep_time/2)

                mc.setBlocks(start.x + 3, start.y + 1, start.z + 1,
                             end.x - 3, start.y + 1, end.z - 1, matt_fur['main_above'])
                sleep(sleep_time/2)

                mc.setBlocks(start.x + 3, start.y + 2, start.z + 1, end.x - 3, end.y, end.z - 1, matt_fur['main_ceil'])
                sleep(sleep_time/2)
                # top corners works
                mc.setBlock(start.x, start.y + 2, start.z, matt_fur['ceil_tr'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z - 2, matt_fur['ceil_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y + 2, start.z + 2, matt_fur['ceil_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z, matt_fur['ceil_bl'])
                sleep(sleep_time/2)
                # bottom corners works
                mc.setBlock(start.x, start.y, start.z, matt_fur['floor_bl'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z - 2, matt_fur['floor_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y, start.z + 2, matt_fur['floor_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z, matt_fur['floor_tr'])
                sleep(sleep_time/2)
                # top centers
                mc.setBlock(end.x, end.y, end.z - 1,  matt_fur['ceil_front'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, end.y, start.z, end.x - 2, end.y, end.z - 2, matt_fur['ceil_left'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, end.y, start.z + 2, end.x - 2, end.y, end.z, matt_fur['ceil_right'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y + 2, start.z + 1, matt_fur['ceil_back'])
                sleep(sleep_time/2)
                # bottom centers
                # mc.setBlock(end.x, end.y - 2, end.z - 1, matt_fur['floor_front'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, start.y, start.z, start.x + 4, start.y, start.z, matt_fur['floor_left'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, start.y, start.z + 2,
                             start.x + 4, start.y, start.z + 2,
                             matt_fur['floor_right'])
                sleep(sleep_time/2)
                # mc.setBlock(start.x, start.y, start.z + 1, matt_fur['floor_back'])
                sleep(sleep_time/2)

            elif '3' in key:

                # main
                mc.setBlocks(start.x + 2, start.y, start.z + 1, start.x + 3, start.y, start.z + 1, matt_fur['main'])
                mc.setBlocks(end.x - 2, start.y, start.z + 1, end.x - 3, start.y, start.z + 1, matt_fur['main'])
                sleep(sleep_time/2)

                mc.setBlocks(start.x + 2, start.y + 1, start.z + 1,
                             start.x + 3, start.y + 1, start.z + 1,
                             matt_fur['main_above'])
                mc.setBlocks(end.x - 2, start.y + 1, start.z + 1,
                             end.x - 3, start.y + 1, start.z + 1, matt_fur['main_above'])
                sleep(sleep_time/2)

                mc.setBlocks(start.x + 2, end.y, start.z + 1, start.x + 3, end.y, start.z + 1, matt_fur['main_ceil'])
                mc.setBlocks(end.x - 2, end.y, start.z + 1, end.x - 3, end.y, start.z + 1, matt_fur['main_ceil'])
                sleep(sleep_time/2)
                # top corners
                mc.setBlock(start.x, start.y + 2, start.z, matt_fur['ceil_tr'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z - 2, matt_fur['ceil_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y + 2, start.z + 2, matt_fur['ceil_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y, end.z, matt_fur['ceil_bl'])
                sleep(sleep_time/2)
                # bottom corners
                mc.setBlock(start.x, start.y, start.z, matt_fur['floor_bl'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z - 2, matt_fur['floor_tl'])
                sleep(sleep_time/2)
                mc.setBlock(start.x, start.y, start.z + 2, matt_fur['floor_br'])
                sleep(sleep_time/2)
                mc.setBlock(end.x, end.y - 2, end.z, matt_fur['floor_tr'])
                sleep(sleep_time/2)
                # top centers

                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, end.y, start.z, start.x + 3, end.y, start.z, matt_fur['ceil_left'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, end.y, start.z + 2,
                             start.x + 3, end.y, start.z + 2,
                             matt_fur['ceil_right'])
                sleep(sleep_time/2)

                sleep(sleep_time/2)
                # bottom centers

                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, start.y, start.z, start.x + 3, start.y, start.z, matt_fur['ceil_left'])
                sleep(sleep_time/2)
                mc.setBlocks(start.x + 2, start.y, start.z + 2,
                             start.x + 3, start.y, start.z + 2,
                             matt_fur['ceil_right'])

                sleep(sleep_time/2)
                # middle centers top
                mc.setBlocks(end.x - 2, end.y, start.z, end.x - 3, end.y, start.z, matt_fur['ceil_left'])
                sleep(sleep_time/2)
                mc.setBlocks(end.x - 2, end.y, start.z + 2, end.x - 3, end.y, start.z + 2, matt_fur['ceil_right'])
                sleep(sleep_time/2)
                # middle centers bottom
                mc.setBlocks(end.x - 2, start.y, start.z, end.x - 3, start.y, start.z, matt_fur['floor_left'])
                sleep(sleep_time/2)
                mc.setBlocks(end.x - 2, start.y, start.z + 2, end.x - 3, start.y, start.z + 2, matt_fur['floor_right'])
                sleep(sleep_time/2)
            sleep(sleep_time)
            if not self.biome == 3:
                local_furniture_list.remove(matt_fur)
                try:
                    matt_fur = random.choice(local_furniture_list)
                except IndexError:
                    raise IndexError(f'''furniture list out of range
                    len(furniture) = {len(furniture)}
                    len(local_furniture_list) = {len(local_furniture_list)}''')
                if matt_fur['floor_tl'] == blocks['fire']:
                    matt_fur = random.choice(local_furniture_list)
            elif self.biome == 3:
                matt_fur = random.choice(local_furniture_list)
                if matt_fur['floor_tl'] == blocks['fire']:
                    matt_fur = random.choice(local_furniture_list)
                    if matt_fur['floor_tl'] == blocks['fire']:
                        matt_fur = random.choice(local_furniture_list)

    def find_pool_location(self, ground: list):
        # find the nearest empty room
        possible_pool = None
        large_pool = False

        for index in range(9):
            if ground[index][1] is False:
                possible_pool = ground[index][2]
                # find north
                if (index - 3) >= 0 and ground[index - 3][1] is False:

                    ground[index][2].room_type = 'pool'
                    ground[index][2].determine_room_type()
                    ground[index - 3][2].room_type = 'pool'
                    ground[index - 3][2].determine_room_type()
                    ground[index - 3][2].add_pool(large=True, direction='horizontal')
                    large_pool = True
                    break
                # find east
                elif (index - 1) >= 0 and ground[index - 1][1] is False:
                    if 'left' not in ground[index][0]:
                        self.generated_rooms[ground[index][2]].room_type = 'pool'
                        ground[index][2].determine_room_type()
                        ground[index - 1][2].room_type = 'pool'
                        ground[index - 1][2].determine_room_type()
                        ground[index - 1][2].add_pool(large=True, direction='vertical')
                        large_pool = True
                    break
                # find west
                elif (index + 1) < len(ground) and ground[index + 1][1] is False:

                    if 'right' not in ground[index][0]:
                        ground[index][2].room_type = 'pool'
                        ground[index][2].determine_room_type()
                        ground[index + 1][2].room_type = 'pool'
                        ground[index + 1][2].determine_room_type()
                        ground[index + 1][2].add_pool(large=True, direction='vertical')
                        large_pool = True
                    break
                # find south
                elif (index + 3) < len(ground) and ground[index + 3][1] is False:
                    ground[index][2].room_type = 'pool'
                    ground[index][2].determine_room_type()
                    ground[index + 3][2].room_type = 'pool'
                    ground[index + 3][2].determine_room_type()
                    ground[index + 3][2].add_pool(large=True, direction='horizontal')
                    large_pool = True
                    break
        if not large_pool:
            possible_pool.add_pool()

    @staticmethod
    def dict_to_list(dictionary):
        return_list = []
        for key, value in dictionary.items():
            if value[0] is True:
                return_list.append([key, value[0], value[1], 'normal'])
            else:
                return_list.append([key, value[0], value[1], 'empty'])
        return return_list

    def main_door(self, door_center):
        x_sign = door_center.x - self.center.x
        z_sign = door_center.z - self.center.z

        if x_sign > 0:
            Room.add_doors(door_x=door_center.x + 2, door_y=door_center.y + 1, door_z=door_center.z,
                           mat_pack=self.mat_pack, door_type='single')
        elif x_sign < 0:
            Room.add_doors(door_x=door_center.x - 2, door_y=door_center.y + 1, door_z=door_center.z,
                           mat_pack=self.mat_pack, door_type='single')
        elif z_sign > 0:
            Room.add_doors(door_x=door_center.x, door_y=door_center.y + 1, door_z=door_center.z + 2,
                           mat_pack=self.mat_pack, door_type='single')
        elif z_sign < 0:
            Room.add_doors(door_x=door_center.x, door_y=door_center.y + 1, door_z=door_center.z - 2,
                           mat_pack=self.mat_pack, door_type='single')
        else:
            raise RuntimeError('Incorrect calculations for door room, are you passing a corner door room?')

    def find_start_location(self, no_spawn_room: Vec3):
        """
        finds a randomised start room that is not the coordinates
        of the no_spawn_room. It also checks if the selected room is set to true.
        :returns start room vec from the center and start room name
        """
        # grab corners
        random_options = [1, 2, 3, 4, 5]
        start_room_dice = random.choice(random_options)
        start_room_vec = Vec3()
        is_door_room = True
        while is_door_room:
            if start_room_dice == 1 and self.generated_rooms['center_left'][0] \
                    and not no_spawn_room == self.generated_rooms['center_left'][1].pos:
                start_room_vec = self.generated_rooms['center_left'][1].pos
                break
            elif start_room_dice == 2 and self.generated_rooms['true_center'][0]:
                if self.generated_rooms['top_center'][0] and not \
                        self.generated_rooms['center_left'][0] or \
                        self.generated_rooms['center_right'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                if self.generated_rooms['top_left'][0] and not \
                        self.generated_rooms['center_left'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                if self.generated_rooms['top_right'][0] and not \
                        self.generated_rooms['center_right'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                start_room_vec = self.generated_rooms['true_center'][1].pos
                break

            elif start_room_dice == 3 and self.generated_rooms['bottom_center'][0] \
                    and not no_spawn_room == self.generated_rooms['bottom_center'][1].pos:
                if self.generated_rooms['true_center'][0] and not \
                        self.generated_rooms['bottom_left'][0] or \
                        self.generated_rooms['bottom_right'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                if self.generated_rooms['center_left'][0] and not \
                        self.generated_rooms['bottom_left'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                if self.generated_rooms['center_right'][0] and not \
                        self.generated_rooms['center_right'][0]:
                    random_options.remove(start_room_dice)
                    if len(random_options) == 0:
                        print(">>> random_done:", random_options)
                        return False, False
                    start_room_dice = random.choice(random_options)
                    continue
                start_room_vec = self.generated_rooms['bottom_center'][1].pos
                break

            elif start_room_dice == 4 and self.generated_rooms['top_center'][0] and not \
                    no_spawn_room == self.generated_rooms['top_center'][1].pos:
                start_room_vec = self.generated_rooms['top_center'][1].pos
                break

            elif start_room_dice == 5 and self.generated_rooms['center_right'][0] and not \
                    no_spawn_room == self.generated_rooms['center_right'][1].pos:
                start_room_vec = self.generated_rooms['center_right'][1].pos
                break

            else:
                print(">>> start_room_dice:", {start_room_dice})
                try:
                    random_options.remove(start_room_dice)
                except ValueError:
                    raise ValueError(f'''Error occurred while removing bad dice from random_options list:
                    random options: {random_options}
                    start_room_dice: {start_room_dice}''')
                if len(random_options) == 0:
                    print(">>> random_done:", random_options)
                    return False, False
                start_room_dice = random.choice(random_options)

        start_room_name = ''
        for key, value in self.generated_rooms.items():
            if value[0]:
                if start_room_vec == value[1].pos:
                    start_room_name = key
                    break
        if start_room_name == '':
            raise RuntimeError('No start room found')
        # start_room_name = House.get_key(start_room_vec, self.generated_rooms[1].pos)
        # change cdr to upstairs and to the center
        start_room = start_room_vec + Vec3(2, 4, 2)
        return start_room_name, start_room

    def create_upstairs(self, ground_floor, start_room_vec, level_y_start=4):
        upstairs_grid_cdr = {
            'top_left': [Vec3(self.center.x + 2, self.center.y + level_y_start, self.center.z - 6)],
            'top_center': [Vec3(self.center.x + 2, self.center.y + level_y_start, self.center.z - 2)],
            'top_right': [Vec3(self.center.x + 2, self.center.y + level_y_start, self.center.z + 2)],

            'center_left': [Vec3(self.center.x - 2, self.center.y + level_y_start, self.center.z - 6)],
            'true_center': [Vec3(self.center.x - 2, self.center.y + level_y_start, self.center.z - 2)],
            'center_right': [Vec3(self.center.x - 2, self.center.y + level_y_start, self.center.z + 2)],

            'bottom_left': [Vec3(self.center.x - 6, self.center.y + level_y_start, self.center.z - 6)],
            'bottom_center': [Vec3(self.center.x - 6, self.center.y + level_y_start, self.center.z - 2)],
            'bottom_right': [Vec3(self.center.x - 6, self.center.y + level_y_start, self.center.z + 2)]
        }
        # prepend bool values of downstairs list to upstairs_grid_cdr
        for upstairs_name, value in upstairs_grid_cdr.items():
            for generated_name, generated_bool in self.generated_rooms.items():
                if upstairs_name == generated_name:
                    upstairs_grid_cdr[generated_name].insert(0, generated_bool[0])

        self.create_level(grid_cdr=upstairs_grid_cdr, start_room=start_room_vec, ground_floor=ground_floor)
        # return the modified generated rooms
        return self.generated_rooms

    def create_downstairs(self):
        grid_cdr = {
            'top_left': [True, Vec3(self.center.x + 2, self.center.y, self.center.z - 6)],
            'top_center': [True, Vec3(self.center.x + 2, self.center.y, self.center.z - 2)],
            'top_right': [True, Vec3(self.center.x + 2, self.center.y, self.center.z + 2)],

            'center_left': [True, Vec3(self.center.x - 2, self.center.y, self.center.z - 6)],
            'true_center': [True, Vec3(self.center.x - 2, self.center.y, self.center.z - 2)],
            'center_right': [True, Vec3(self.center.x - 2, self.center.y, self.center.z + 2)],

            'bottom_left': [True, Vec3(self.center.x - 6, self.center.y, self.center.z - 6)],
            'bottom_center': [True, Vec3(self.center.x - 6, self.center.y, self.center.z - 2)],
            'bottom_right': [True, Vec3(self.center.x - 6, self.center.y, self.center.z + 2)]
        }
        ground_floor = True
        self.create_level(grid_cdr=grid_cdr, start_room=self.door_room, ground_floor=ground_floor)

    def create_level(self, grid_cdr, start_room, ground_floor, ran_low=2):
        # find maximum number of rooms that may generate
        ran_high = 0
        room_num = -1
        for name, value in grid_cdr.items():
            if value[0] is True:
                ran_high += 1

        if not self.biome == 3:
            if ran_high < 2:
                # mc.postToChat('ERR | CHECK CONSOLE > moving to next house')
                print(f"{bcolors.WARNING}ERR: ran_high is lower than 2{bcolors.ENDC}")
                return False
            elif ran_high < 4:
                mode = ran_high - 1
            else:
                mode = ran_high - 2
            room_num = bias_random(ran_low, ran_high, mode)

        elif self.biome == 3:
            if ran_high < 2:
                mc.postToChat('ERR | CHECK CONSOLE > moving to next house')
                print(f"{bcolors.WARNING}ERR: ran_high is lower than 2{bcolors.ENDC}")
                return False
            else:
                if self.large_building_type == 'skyscraper':
                    # Different types of skyscrapers
                    # Fat base; medium top
                    if random.randint(1, 3) == 1:
                        if self.global_index < 2:  # Below second level
                            room_num = ran_high
                        elif self.global_index == 2:  # At second level
                            room_num = ran_high - 1
                        elif self.global_index < 6:  # up to fifth level
                            room_num = ran_high
                        elif self.global_index == 6:  # At sixth level etc.
                            room_num = ran_high - 1
                        elif self.global_index < 10:
                            room_num = ran_high
                        elif self.global_index == 10:
                            room_num = ran_high - 1
                        elif self.global_index == 11:
                            room_num = ran_high
                        else:
                            room_num = ran_high - 1  # For the rest
                    # med base; skinny top
                    else:
                        if self.global_index < 2:  # Below second level
                            room_num = ran_high
                        elif self.global_index == 2:  # At second level
                            room_num = ran_high - 1
                        elif self.global_index == 4:  # At second level
                            room_num = ran_high - 1
                        elif self.global_index < 6:  # up to fifth level
                            room_num = ran_high
                        elif self.global_index == 6:  # At sixth level etc.
                            room_num = ran_high - 1
                        elif self.global_index == 8:
                            room_num = ran_high - 1
                        elif self.global_index < 10:
                            room_num = ran_high
                        elif self.global_index == 10:
                            room_num = ran_high - 1
                        elif self.global_index == 11:
                            room_num = ran_high - 1
                        else:
                            room_num = ran_high - 1  # For the rest

                elif self.large_building_type == 'apartment':
                    if not self.apartment_pool:
                        if self.global_index < 2:
                            room_num = ran_high
                        elif self.global_index < 4:
                            room_num = ran_high - 1
                        else:
                            room_num = ran_high - 2
                    elif self.apartment_pool:
                        if self.global_index < 2:
                            room_num = ran_high - 2
                        else:
                            room_num = ran_high - 1

        else:
            raise RuntimeError('Invalid biome passed through')
        print('numbers of rooms:', room_num, 'ran_high:', ran_high)

        # Get corner of the start room
        start_room = Vec3(start_room.x - 2, start_room.y, start_room.z - 2)

        # generate the start room
        for name, value in grid_cdr.items():
            if value[1] == start_room:
                self.generated_rooms[name] = []
                self.generated_rooms[name].append(True)
                self.generated_rooms[name].append(Room(pos=value[1], mat_pack=self.mat_pack, room_type='door',
                                                       room_name=name, ground_floor=ground_floor,
                                                       roof_type=self.roof_type))
                print(f'Start Room: {name} | Created')
                if not value[0]:
                    print('WARNING: Upstairs cannot be built, Start room is false ')
                    return
            else:
                self.generated_rooms[name] = []
                self.generated_rooms[name].append(False)

        possible_locations = [(grid_cdr['true_center'][1])]

        for _ in range(0, room_num - 1):
            for key_name, value in self.generated_rooms.items():
                if value[0]:
                    if 'left' in key_name:
                        if not key_name == 'top_left':
                            if not self.generated_rooms['bottom_left'][0] and \
                                    grid_cdr['bottom_left'][1] not in possible_locations and \
                                    grid_cdr['bottom_left'][0] is True:
                                possible_locations.append(grid_cdr['bottom_left'][1])
                        if not key_name == 'bottom_left':
                            if not self.generated_rooms['top_left'][0] and \
                                    grid_cdr['top_left'][1] not in possible_locations and \
                                    grid_cdr['top_left'][0] is True:
                                possible_locations.append(grid_cdr['top_left'][1])
                        if not self.generated_rooms['center_left'][0] and \
                                grid_cdr['center_left'][1] not in possible_locations and \
                                grid_cdr['center_left'][0] is True:
                            possible_locations.append(grid_cdr['center_left'][1])

                    if 'right' in key_name:
                        if not key_name == 'top_right':
                            if not self.generated_rooms['bottom_right'][0] and \
                                    grid_cdr['bottom_right'][1] not in possible_locations and \
                                    grid_cdr['bottom_right'][0] is True:
                                possible_locations.append(grid_cdr['bottom_right'][1])
                        if not key_name == 'bottom_right':
                            if not self.generated_rooms['top_right'][0] and \
                                    grid_cdr['top_right'][1] not in possible_locations and \
                                    grid_cdr['top_right'][0] is True:
                                possible_locations.append(grid_cdr['top_right'][1])
                        if not self.generated_rooms['center_right'][0] and \
                                grid_cdr['center_right'][1] not in possible_locations and \
                                grid_cdr['center_right'][0] is True:
                            possible_locations.append(grid_cdr['center_right'][1])

                    if 'top' in key_name:
                        if not key_name == 'top_left':
                            if not self.generated_rooms['top_right'][0] and \
                                    grid_cdr['top_right'][1] not in possible_locations and \
                                    grid_cdr['top_right'][0] is True:
                                possible_locations.append(grid_cdr['top_right'][1])
                        if not key_name == 'top_right':
                            if not self.generated_rooms['top_left'][0] and \
                                    grid_cdr['top_left'][1] not in possible_locations and \
                                    grid_cdr['top_left'][0] is True:
                                possible_locations.append(grid_cdr['top_left'][1])
                        if not self.generated_rooms['top_center'][0] and \
                                grid_cdr['top_center'][1] not in possible_locations and \
                                grid_cdr['top_center'][0] is True:
                            possible_locations.append(grid_cdr['top_center'][1])

                    if 'bottom' in key_name:
                        if not key_name == 'bottom_left':
                            if not self.generated_rooms['bottom_right'][0] and \
                                    grid_cdr['bottom_right'][1] not in possible_locations and \
                                    grid_cdr['bottom_right'][0] is True:
                                possible_locations.append(grid_cdr['bottom_right'][1])
                        if not key_name == 'bottom_right':
                            if not self.generated_rooms['bottom_left'][0] and \
                                    grid_cdr['bottom_left'][1] not in possible_locations and \
                                    grid_cdr['bottom_left'][0] is True:
                                possible_locations.append(grid_cdr['bottom_left'][1])
                        if not self.generated_rooms['bottom_center'][0] and \
                                grid_cdr['bottom_center'][1] not in possible_locations and \
                                grid_cdr['bottom_center'][0] is True:
                            possible_locations.append(grid_cdr['bottom_center'][1])

                    if 'true' in key_name:
                        if not self.generated_rooms['bottom_center'][0] \
                                and grid_cdr['bottom_center'][1] not in possible_locations and \
                                grid_cdr['bottom_center'][0] is True:
                            possible_locations.append(grid_cdr['bottom_center'][1])
                        if not self.generated_rooms['top_center'][0] and \
                                grid_cdr['top_center'][1] not in possible_locations and \
                                grid_cdr['top_center'][0] is True:
                            possible_locations.append(grid_cdr['top_center'][1])
                        if not self.generated_rooms['center_right'][0] and \
                                grid_cdr['center_right'][1] not in possible_locations and \
                                grid_cdr['center_right'][0] is True:
                            possible_locations.append(grid_cdr['center_right'][1])
                        if not self.generated_rooms['center_left'][0] and \
                                grid_cdr['center_left'][1] not in possible_locations and \
                                grid_cdr['center_left'][0] is True:
                            possible_locations.append(grid_cdr['center_left'][1])

            try:
                build_next_pos = random.randint(0, len(possible_locations) - 1)
            except ValueError:
                print(f'''Ran out of possibilities for the num of rooms required :(
                Length of possible locations list: {len(possible_locations)}''')
                mc.postToChat('possibilities ERR OCCURRED CHECK CONSOLE')
                return

            room_key = self.get_key(possible_locations[build_next_pos], grid_cdr)
            print(f'Room: {room_key} | Created')
            self.generated_rooms[room_key][0] = True
            add_to_generated = Room(pos=possible_locations[build_next_pos], mat_pack=self.mat_pack, room_type='normal',
                                    room_name=room_key, ground_floor=ground_floor, roof_type=self.roof_type)

            # Append the room object to the generated rooms list
            self.generated_rooms[room_key].append(add_to_generated)
            # remove generated room from possible locations
            possible_locations.remove(possible_locations[build_next_pos])

        for key, value in self.generated_rooms.items():
            if not self.generated_rooms[key][0]:
                empty_room_object = Room(grid_cdr[key][1], mat_pack=self.mat_pack, room_type='empty',
                                         room_name=key, ground_floor=ground_floor, roof_type=self.roof_type)
                self.generated_rooms[key].append(empty_room_object)

        for room_name, value in self.generated_rooms.items():
            if value[0]:
                value[1].window_locations(generated_rooms=self.generated_rooms)

        for room_name in self.generated_rooms:
            if self.generated_rooms[room_name][0]:
                self.generated_rooms[room_name][1].remove_walls(generated_rooms=self.generated_rooms,
                                                                internal_wall_dice=self.internal_wall_dice)
                # house pillars uncommented
                # generated_rooms[room_name][1].add_house_pillars(generated_rooms=generated_rooms, room_name=room_name)

        return

    # Return key for any dict value
    @staticmethod
    def get_key(val, dictionary):
        for key, value in dictionary.items():
            # WARNING: value needs a list of len 2
            if val == value[1]:
                return key
        raise KeyError('Failed to find key from given value')


class Room:
    """
    Handles specific properties of a single room.
    Some responsibilities are listed below:
    - structure, dimension, pillars,
     - roofs, doors, windows,
     - pools, pool windows + walls + shade
     - removal of walls to create bigger rooms
    """
    def __init__(self, pos, mat_pack: dict, room_type: str, room_name: str,
                 ground_floor: bool, roof_type: str):
        self.room_type = room_type
        self.ground_floor = ground_floor
        self.mat_pack = mat_pack
        self.room_name = room_name
        self.pos = pos
        self.roof_type = roof_type
        self.dimension = Vec3(4, 4, 4)
        self.determine_room_type()

    def determine_room_type(self, stair_type=''):
        if self.room_type == 'normal':
            self.add_foundation(ground_floor=self.ground_floor)
            sleep(sleep_time / 2)
            self.add_structure()
            sleep(sleep_time / 5)
            self.add_pillars(ground_floor=self.ground_floor)
            sleep(sleep_time / 5)
            self.add_roof(roof_type=self.roof_type)
        elif self.room_type == 'empty':
            pass
        elif self.room_type == 'pool':
            self.add_pool()
        elif self.room_type == 'door':
            self.add_foundation(ground_floor=self.ground_floor)
            sleep(sleep_time / 2)
            self.add_structure()
            sleep(sleep_time / 2)
            self.add_pillars(ground_floor=self.ground_floor)
            sleep(sleep_time / 2)
            self.add_roof(roof_type=self.roof_type)
            sleep(sleep_time / 2)
        elif self.room_type == 'downstairs_stairs':
            self.stair_room(stair_type=stair_type)
        elif self.room_type == 'upstairs_stairs':
            self.stair_room(downstairs=False, stair_type=stair_type)
            sleep(sleep_time / 2)

    def stair_room(self, stair_type, downstairs=True):
        if not downstairs:
            # clear out upstairs floor and air out room
            if stair_type == 'basic':
                mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                             self.pos.x + 2, self.pos.y, self.pos.z + 3, self.mat_pack['upstairs_floor'])
                mc.setBlocks(self.pos.x + 3, self.pos.y, self.pos.z + 1,
                             self.pos.x + 3, self.pos.y, self.pos.z + 3, block.AIR.id)

            elif stair_type == 'double_stairs':
                mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                             self.pos.x + 3, self.pos.y, self.pos.z + 3, block.AIR.id)
                mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                             self.pos.x + 1, self.pos.y, self.pos.z + 3,
                             self.mat_pack['slab'], 1)
                mc.setBlock(self.pos.x + 2, self.pos.y + 1, self.pos.z + 2,
                            self.mat_pack['slab'])
                mc.setBlock(self.pos.x + 3, self.pos.y + 1, self.pos.z + 2,
                            self.mat_pack['slab'])

            elif stair_type == 'double_slab':
                mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                             self.pos.x + 3, self.pos.y, self.pos.z + 3, block.AIR.id)
                mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                             self.pos.x + 1, self.pos.y, self.pos.z + 3,
                             self.mat_pack['slab'])
                mc.setBlock(self.pos.x + 2, self.pos.y, self.pos.z + 2,
                            self.mat_pack['slab'])
                mc.setBlock(self.pos.x + 3, self.pos.y + 1, self.pos.z + 2,
                            self.mat_pack['slab'])

        else:
            self.set_stairs(stair_type=stair_type)

    def set_stairs(self, stair_type):
        # stair_dice = random.choice(stair_options)
        mc.setBlocks(self.pos.x + 1, self.pos.y + 5, self.pos.z + 1,
                     self.pos.x + 3, self.pos.y + 5, self.pos.z + 3, block.AIR.id)
        if stair_type == 'basic':
            # basic stairs
            mc.setBlocks(self.pos.x + 1, self.pos.y + 4, self.pos.z + 1,
                         self.pos.x + 2, self.pos.y + 4, self.pos.z + 3, self.mat_pack['upstairs_floor'])
            mc.setBlocks(self.pos.x + 3, self.pos.y + 4, self.pos.z + 1,
                         self.pos.x + 3, self.pos.y + 4, self.pos.z + 3, block.AIR.id)
            mc.setBlock(self.pos.x + 3, self.pos.y + 1, self.pos.z + 1, self.mat_pack['stairs'], 2)
            mc.setBlock(self.pos.x + 3, self.pos.y + 2, self.pos.z + 2, self.mat_pack['stairs'], 2)
            mc.setBlock(self.pos.x + 3, self.pos.y + 3, self.pos.z + 3, self.mat_pack['stairs'], 2)
            mc.setBlocks(self.pos.x + 4, self.pos.y, self.pos.z + 1,
                         self.pos.x + 4, self.pos.y + 4, self.pos.z + 3, self.mat_pack['walls'])
            sleep(sleep_time/5)

        elif stair_type == 'double_stairs':
            # double stairs
            mc.setBlock(self.pos.x + 2, self.pos.y + 1, self.pos.z + 2, self.mat_pack['stairs'], 0)
            mc.setBlock(self.pos.x + 3, self.pos.y + 1, self.pos.z + 2, self.mat_pack['pillars'])
            mc.setBlock(self.pos.x + 3, self.pos.y + 2, self.pos.z + 1, self.mat_pack['stairs'], 3)
            mc.setBlock(self.pos.x + 3, self.pos.y + 2, self.pos.z + 3, self.mat_pack['stairs'], 2)
            mc.setBlock(self.pos.x + 2, self.pos.y + 3, self.pos.z + 1, self.mat_pack['stairs'], 1)

            mc.setBlock(self.pos.x + 2, self.pos.y + 3, self.pos.z + 3, self.mat_pack['stairs'], 1)
            mc.setBlocks(self.pos.x + 4, self.pos.y, self.pos.z + 1,
                         self.pos.x + 4, self.pos.y + 4, self.pos.z + 3, self.mat_pack['walls'])
            sleep(sleep_time/5)

        elif stair_type == 'double_slab':
            # double-stairs but with slabs
            mc.setBlocks(self.pos.x + 4, self.pos.y, self.pos.z + 1,
                         self.pos.x + 4, self.pos.y + 4, self.pos.z + 3, self.mat_pack['walls'])
            mc.setBlock(self.pos.x + 2, self.pos.y + 1, self.pos.z + 2, self.mat_pack['slab'])
            mc.setBlock(self.pos.x + 3, self.pos.y + 1, self.pos.z + 2, self.mat_pack['pillars'])
            mc.setBlock(self.pos.x + 3, self.pos.y + 2, self.pos.z + 1, self.mat_pack['slab'])
            mc.setBlock(self.pos.x + 3, self.pos.y + 2, self.pos.z + 3, self.mat_pack['slab'])
            mc.setBlock(self.pos.x + 2, self.pos.y + 3, self.pos.z + 1, self.mat_pack['slab'])
            mc.setBlock(self.pos.x + 2, self.pos.y + 3, self.pos.z + 3, self.mat_pack['slab'])
            sleep(sleep_time/5)

    def add_pool(self, large=False, direction=''):
        pool_shade_spawned = False
        if not large:
            sleep(sleep_time/5)
            # small_pool set water and a container for the water
            mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                         self.pos.x + 3, self.pos.y + 3, self.pos.z + 3, block.AIR.id)
            mc.setBlocks(self.pos, self.pos.x + 4, self.pos.y - 2, self.pos.z + 4, self.mat_pack['pool_container'])
            mc.setBlocks(self.pos.x + 1, self.pos.y, self.pos.z + 1,
                         self.pos.x + 3, self.pos.y - 1, self.pos.z + 3, self.mat_pack['pool_liquid'])
            # air out walls
            mc.setBlocks(self.pos.x + 1, self.pos.y + 1, self.pos.z, self.pos.x + 3, self.pos.y + 3, self.pos.z,
                         block.AIR.id)
            mc.setBlocks(self.pos.x + 1, self.pos.y + 1, self.pos.z + 4, self.pos.x + 3, self.pos.y + 3, self.pos.z + 4,
                         block.AIR.id)
            mc.setBlocks(self.pos.x, self.pos.y + 1, self.pos.z + 1, self.pos.x, self.pos.y + 3, self.pos.z + 3,
                         block.AIR.id)
            mc.setBlocks(self.pos.x + 4, self.pos.y + 1, self.pos.z + 1, self.pos.x + 4, self.pos.y + 3, self.pos.z + 3,
                         block.AIR.id)
            sleep(sleep_time/5)

            # place borders: full fences; glass doors: open; glass walls closed
            pool_border_dice = random.randint(0, 2)

            # indoor pool
            if pool_border_dice == 0:
                # top
                self.add_indoor_pool_door(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z,
                                          x2=self.pos.x + 4, y2=self.pos.y + 3, z2=self.pos.z + 4)
                # bottom
                self.add_indoor_pool_door(self.pos.x, self.pos.y + 1, self.pos.z,
                                          self.pos.x, self.pos.y + 3, self.pos.z + 4)
                # left
                self.add_indoor_pool_door(x=self.pos.x, y=self.pos.y + 1, z=self.pos.z,
                                          x2=self.pos.x + 4, y2=self.pos.y + 3, z2=self.pos.z)
                # right
                self.add_indoor_pool_door(self.pos.x, self.pos.y + 1, self.pos.z + 4,
                                          self.pos.x + 4, self.pos.y + 3, self.pos.z + 4)
                sleep(sleep_time / 5)
                # always spawn in shade
                self.add_single_pillar(Vec3(0, 0, 0))
                self.add_single_pillar(Vec3(4, 0, 0))
                self.add_single_pillar(Vec3(4, 0, 4))
                self.add_single_pillar(Vec3(0, 0, 4))
                self.add_roof()
                pool_shade_spawned = True

            # open pool walls
            elif pool_border_dice == 1:
                # Add in fences and gates
                self.add_fenced_pool()
                # top
                self.add_open_pool_door(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z + 1,
                                        x2=self.pos.x + 4, y2=self.pos.y + 3, z2=self.pos.z + 3)
                # bottom
                self.add_open_pool_door(self.pos.x, self.pos.y + 1, self.pos.z + 1,
                                        self.pos.x, self.pos.y + 3, self.pos.z + 3)
                # left
                self.add_open_pool_door(x=self.pos.x + 1, y=self.pos.y + 1, z=self.pos.z,
                                        x2=self.pos.x + 3, y2=self.pos.y + 3, z2=self.pos.z)
                # right
                self.add_open_pool_door(self.pos.x + 1, self.pos.y + 1, self.pos.z + 4,
                                        self.pos.x + 3, self.pos.y + 3, self.pos.z + 4)
                sleep(sleep_time / 5)
            # Fully open pool surrounded by fences
            elif pool_border_dice == 2:
                self.add_fenced_pool()

            spawn_pool_shade = random.randint(1, 100)
            if spawn_pool_shade > 60 and not pool_shade_spawned:
                self.add_single_pillar(Vec3(0, 0, 0))
                self.add_single_pillar(Vec3(4, 0, 0))
                self.add_single_pillar(Vec3(4, 0, 4))
                self.add_single_pillar(Vec3(0, 0, 4))
                self.add_roof()

        elif large:
            # air out the space in the middle of two pools
            if direction == 'vertical':
                mc.setBlocks(self.pos.x + 1, self.pos.y - 1, self.pos.z,
                             self.pos.x + 3, self.pos.y + 3, self.pos.z, block.AIR.id)
                sleep(sleep_time / 5)
            elif direction == 'horizontal':
                mc.setBlocks(self.pos.x + 4, self.pos.y - 1, self.pos.z + 1,
                             self.pos.x + 4, self.pos.y + 3, self.pos.z + 3, block.AIR.id)
                sleep(sleep_time / 5)
        mc.setBlocks(self.pos.x, self.pos.y - 3, self.pos.z, self.pos.x + 4, self.pos.y - 12, self.pos.z + 4,
                     self.mat_pack['foundation'])

    def add_fenced_pool(self):
        # left
        mc.setBlocks(self.pos.x + 1, self.pos.y + 1, self.pos.z,
                     self.pos.x + 3, self.pos.y + 1, self.pos.z,
                     self.mat_pack['fence'])
        self.block_above_fence(x=self.pos.x, y=self.pos.y + 1, z=self.pos.z)
        self.block_above_fence(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z)
        # top
        mc.setBlocks(self.pos.x + 4, self.pos.y + 1, self.pos.z + 1,
                     self.pos.x + 4, self.pos.y + 1, self.pos.z + 3,
                     self.mat_pack['fence'])
        self.block_above_fence(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z)
        self.block_above_fence(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z + 4)
        # bottom
        mc.setBlocks(self.pos.x, self.pos.y + 1, self.pos.z + 1,
                     self.pos.x, self.pos.y + 1, self.pos.z + 3,
                     self.mat_pack['fence'])
        self.block_above_fence(x=self.pos.x, y=self.pos.y + 1, z=self.pos.z)
        self.block_above_fence(x=self.pos.x, y=self.pos.y + 1, z=self.pos.z + 4)
        # right
        mc.setBlocks(self.pos.x + 1, self.pos.y + 1, self.pos.z + 4,
                     self.pos.x + 3, self.pos.y + 1, self.pos.z + 4,
                     self.mat_pack['fence'])
        self.block_above_fence(x=self.pos.x, y=self.pos.y + 1, z=self.pos.z + 4)
        self.block_above_fence(x=self.pos.x + 4, y=self.pos.y + 1, z=self.pos.z + 4)
        sleep(sleep_time / 5)

        # add gates
        mc.setBlock(self.pos.x, self.pos.y + 1, self.pos.z + 2, self.mat_pack['fence_gate'], 1)
        mc.setBlock(self.pos.x + 4, self.pos.y + 1, self.pos.z + 2, self.mat_pack['fence_gate'], 1)
        mc.setBlock(self.pos.x + 2, self.pos.y + 1, self.pos.z + 4, self.mat_pack['fence_gate'], 2)
        mc.setBlock(self.pos.x + 2, self.pos.y + 1, self.pos.z, self.mat_pack['fence_gate'], 2)
        sleep(sleep_time / 5)

    def add_open_pool_door(self, x, y, z, x2, y2, z2):
        x_diff = x2 - x
        z_diff = z2 - z
        # x increases
        if not x_diff == 0 and z_diff == 0:
            if not mc.getBlock(x + 1, y + 3, z) == 0:
                mc.setBlocks(x, y, z, x2, y2, z2,
                             self.mat_pack['pool_wall'])
                middle_block = Vec3((x2 + x) // 2, y, (z2 + z) // 2)
                Room.add_doors(door_x=middle_block.x, door_y=middle_block.y, door_z=middle_block.z,
                               mat_pack=self.mat_pack,
                               door_type='single')
        elif x_diff == 0 and not z_diff == 0:
            if not mc.getBlock(x, y + 3, z + 1) == 0:
                mc.setBlocks(x, y, z, x2, y2, z2,
                             self.mat_pack['pool_wall'])
                middle_block = Vec3((x2 + x) // 2, y, (z2 + z) // 2)
                Room.add_doors(door_x=middle_block.x, door_y=middle_block.y, door_z=middle_block.z,
                               mat_pack=self.mat_pack,
                               door_type='single')

    def add_indoor_pool_door(self, x, y, z, x2, y2, z2):
        mc.setBlocks(x, y, z, x2, y2, z2,
                     self.mat_pack['pool_wall'])
        x_diff = x2 - x
        z_diff = z2 - z
        # x increases
        if not x_diff == 0 and z_diff == 0:
            if not mc.getBlock(x + 1, y + 3, z) == 0:
                middle_block = Vec3((x2 + x) // 2, y, (z2 + z) // 2)
                Room.add_doors(door_x=middle_block.x, door_y=middle_block.y, door_z=middle_block.z,
                               mat_pack=self.mat_pack, door_type='single')
        elif x_diff == 0 and not z_diff == 0:
            if not mc.getBlock(x, y + 3, z + 1) == 0:
                middle_block = Vec3((x2 + x) // 2, y, (z2 + z) // 2)
                Room.add_doors(door_x=middle_block.x, door_y=middle_block.y, door_z=middle_block.z,
                               mat_pack=self.mat_pack, door_type='single')

    def block_above_fence(self, x, y, z, y_above=1):
        if mc.getBlock(x, y + y_above, z) == 0:
            mc.setBlock(x, y, z, self.mat_pack['fence'])
        else:
            mc.setBlock(x, y, z, self.mat_pack['pillars'])

    def window_locations(self, generated_rooms):
        start_top = self.pos + Vec3(4, 0, 1)
        start_left = self.pos + Vec3(1, 0, 0)
        start_right = self.pos + Vec3(1, 0, 4)
        start_bottom = self.pos + Vec3(0, 0, 1)

        end_top = self.pos + Vec3(4, 0, 3)
        end_left = self.pos + Vec3(3, 0, 0)
        end_right = self.pos + Vec3(3, 0, 4)
        end_bottom = self.pos + Vec3(0, 0, 3)

        if self.room_name == 'top_left':
            self.add_windows(start_left, end_left, direction='vertical')
            self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['top_center'][0]:
                self.add_windows(start_right, end_right, direction='vertical')
            if not generated_rooms['center_left'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')

        elif self.room_name == 'top_right':
            self.add_windows(start_right, end_right, direction='vertical')
            self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['top_center'][0]:
                self.add_windows(start_left, end_left, direction='vertical')
            if not generated_rooms['center_right'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')

        elif self.room_name == 'bottom_right':
            self.add_windows(start_right, end_right, direction='vertical')
            self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['center_right'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['bottom_center'][0]:
                self.add_windows(start_left, end_left, direction='vertical')

        elif self.room_name == 'bottom_left':
            self.add_windows(start_left, end_left, direction='vertical')
            self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['center_left'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['bottom_center'][0]:
                self.add_windows(start_right, end_right, direction='vertical')

        elif self.room_name == 'top_center':
            self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['top_right'][0]:
                self.add_windows(start_right, end_right, direction='vertical')
            if not generated_rooms['top_left'][0]:
                self.add_windows(start_left, end_left, direction='vertical')
            if not generated_rooms['true_center'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')

        elif self.room_name == 'center_left':
            self.add_windows(start_left, end_left, direction='vertical')
            if not generated_rooms['bottom_left'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['top_left'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['true_center'][0]:
                self.add_windows(start_right, end_right, direction='vertical')

        elif self.room_name == 'center_right':
            self.add_windows(start_right, end_right, direction='vertical')
            if not generated_rooms['bottom_right'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['top_right'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['true_center'][0]:
                self.add_windows(start_left, end_left, direction='vertical')

        elif self.room_name == 'bottom_center':
            self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['bottom_right'][0]:
                self.add_windows(start_right, end_right, direction='vertical')
            if not generated_rooms['bottom_left'][0]:
                self.add_windows(start_left, end_left, direction='vertical')
            if not generated_rooms['true_center'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')

        elif self.room_name == 'true_center':
            if not generated_rooms['bottom_center'][0]:
                self.add_windows(start_bottom, end_bottom, direction='horizontal')
            if not generated_rooms['top_center'][0]:
                self.add_windows(start_top, end_top, direction='horizontal')
            if not generated_rooms['center_left'][0]:
                self.add_windows(start_left, end_left, direction='vertical')
            if not generated_rooms['center_right'][0]:
                self.add_windows(start_right, end_right, direction='vertical')

    def add_windows(self, start_mod, end_mod, direction=''):
        start_pos = start_mod
        end_pos = end_mod
        is_window = bias_random(0, 100, 30)
        if is_window > 30:
            ran = bias_random(0, 4, 0)
            # double bar windows (top 2 bars)
            if ran == 0:
                mc.setBlocks(start_pos.x, start_pos.y + 2, start_pos.z,
                             end_pos.x, end_pos.y + 3, end_pos.z, self.mat_pack['windows'])
            elif ran == 1:
                # Horizontal strips
                mc.setBlocks(start_pos.x, start_pos.y + 2, start_pos.z,
                             end_pos.x, end_pos.y + 2, end_pos.z,
                             self.mat_pack['windows'])
                sleep(sleep_time / 5)
            elif ran == 2:
                # plus window in middle
                if direction == 'vertical':
                    mc.setBlock(start_pos.x + 1, start_pos.y + 1, start_pos.z,
                                self.mat_pack['windows'])
                    mc.setBlock(start_pos.x + 1, start_pos.y + 3, start_pos.z,
                                self.mat_pack['windows'])
                    mc.setBlocks(start_pos.x, start_pos.y + 2, start_pos.z,
                                 end_pos.x, end_pos.y + 2, end_pos.z,
                                 self.mat_pack['windows'])
                else:
                    mc.setBlock(start_pos.x, start_pos.y + 3, start_pos.z + 1,
                                self.mat_pack['windows'])
                    mc.setBlock(start_pos.x, start_pos.y + 1, start_pos.z + 1,
                                self.mat_pack['windows'])
                    mc.setBlocks(start_pos.x, start_pos.y + 2, start_pos.z,
                                 end_pos.x, end_pos.y + 2, end_pos.z,
                                 self.mat_pack['windows'])
                sleep(sleep_time / 5)
            elif ran == 3:
                # single window in centre
                if direction == 'vertical':
                    mc.setBlock(start_pos.x + 1, start_pos.y + 2, start_pos.z,
                                self.mat_pack['windows'])
                else:
                    mc.setBlock(start_pos.x, start_pos.y + 2, start_pos.z + 1,
                                self.mat_pack['windows'])
                sleep(sleep_time / 5)
            # full window
            elif ran == 4:
                mc.setBlocks(start_pos.x, start_pos.y + 1, start_pos.z,
                             end_pos.x, end_pos.y + 3, end_pos.z, self.mat_pack['windows'])

    def remove_walls(self, generated_rooms, internal_wall_dice):
        x = self.pos.x
        y = self.pos.y
        z = self.pos.z
        wall_pos = {
            'left': [Vec3(x + 1, y + 1, z), Vec3(x + 3, y + 3, z)],
            'right': [Vec3(x + 1, y + 1, z + 4), Vec3(x + 3, y + 3, z + 4)],
            'top': [Vec3(x + 4, y + 1, z + 1), Vec3(x + 4, y + 3, z + 3)],
            'bottom': [Vec3(x, y + 1, z + 1), Vec3(x, y + 3, z + 3)],
        }

        room_existence = bias_random(0, 100, 60)
        if room_existence > 50:
            if self.room_name == 'top_center':
                if generated_rooms['top_left'][0]:
                    mc.setBlocks(wall_pos['left'][0], wall_pos['left'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['top_right'][0]:
                    mc.setBlocks(wall_pos['right'][0], wall_pos['right'][1], block.AIR.id)
                    sleep(0.1)

            if self.room_name == 'center_left':
                if generated_rooms['top_left'][0]:
                    mc.setBlocks(wall_pos['top'][0], wall_pos['top'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['bottom_left'][0]:
                    mc.setBlocks(wall_pos['bottom'][0], wall_pos['bottom'][1], block.AIR.id)
                    sleep(0.1)

            if self.room_name == 'bottom_center':
                if generated_rooms['bottom_left'][0]:
                    mc.setBlocks(wall_pos['left'][0], wall_pos['left'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['bottom_right'][0]:
                    mc.setBlocks(wall_pos['right'][0], wall_pos['right'][1], block.AIR.id)
                    sleep(0.1)

            if self.room_name == 'center_right':
                if generated_rooms['top_right'][0]:
                    mc.setBlocks(wall_pos['top'][0], wall_pos['top'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['bottom_right'][0]:
                    mc.setBlocks(wall_pos['bottom'][0], wall_pos['bottom'][1], block.AIR.id)
                    sleep(0.1)

            if self.room_name == 'true_center':
                if generated_rooms['top_center'][0]:
                    mc.setBlocks(wall_pos['top'][0], wall_pos['top'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['center_left'][0]:
                    mc.setBlocks(wall_pos['left'][0], wall_pos['left'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['center_right'][0]:
                    mc.setBlocks(wall_pos['right'][0], wall_pos['right'][1], block.AIR.id)
                    sleep(0.1)
                if generated_rooms['bottom_center'][0]:
                    mc.setBlocks(wall_pos['bottom'][0], wall_pos['bottom'][1], block.AIR.id)
                    sleep(0.1)
        # else, if the two rooms are not connected, use airing options to separate rooms
        else:
            if self.room_name == 'top_center':
                if generated_rooms['top_left'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='left',
                                       mat_pack=self.mat_pack)
                if generated_rooms['top_right'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='right',
                                       mat_pack=self.mat_pack)

            if self.room_name == 'center_left':
                if generated_rooms['top_left'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='top',
                                       mat_pack=self.mat_pack)
                if generated_rooms['bottom_left'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='bottom',
                                       mat_pack=self.mat_pack)

            if self.room_name == 'bottom_center':
                if generated_rooms['bottom_left'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='left',
                                       mat_pack=self.mat_pack)
                if generated_rooms['bottom_right'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='right',
                                       mat_pack=self.mat_pack)

            if self.room_name == 'center_right':
                if generated_rooms['top_right'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='top',
                                       mat_pack=self.mat_pack)
                if generated_rooms['bottom_right'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='bottom',
                                       mat_pack=self.mat_pack)

            if self.room_name == 'true_center':
                if generated_rooms['top_center'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='top',
                                       mat_pack=self.mat_pack)
                if generated_rooms['center_left'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='left',
                                       mat_pack=self.mat_pack)
                if generated_rooms['center_right'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='right',
                                       mat_pack=self.mat_pack)
                if generated_rooms['bottom_center'][0]:
                    self.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str='bottom',
                                       mat_pack=self.mat_pack)

    @staticmethod
    def add_house_pillars(generated_rooms, room_name, ground_floor=False):
        bottom_left = Vec3(0, 0, 0)
        top_left = Vec3(4, 0, 0)
        top_right = Vec3(4, 0, 4)
        bottom_right = Vec3(0, 0, 4)

        if room_name == 'top_left':
            generated_rooms['top_left'][1].add_single_pillar(top_left, ground_floor)
            if generated_rooms['center_left'][0]:
                if not generated_rooms['bottom_left'][0]:
                    generated_rooms['center_left'][1].add_single_pillar(bottom_left, ground_floor)
            else:
                generated_rooms['top_left'][1].add_single_pillar(ground_floor)

            if generated_rooms['top_center'][0]:
                if not generated_rooms['top_right']:
                    generated_rooms['top_center'][1].add_single_pillar(top_right, ground_floor)
            else:
                generated_rooms['top_left'][1].add_single_pillar(top_right, ground_floor)

        elif room_name == 'top_right':
            generated_rooms['top_right'][1].add_single_pillar(top_right, ground_floor)
            if generated_rooms['center_right'][0]:
                if not generated_rooms['bottom_right'][0]:
                    generated_rooms['center_right'][1].add_single_pillar(bottom_right, ground_floor)
            else:
                generated_rooms['top_right'][1].add_single_pillar(bottom_right, ground_floor)

            if generated_rooms['top_center'][0]:
                if not generated_rooms['top_left'][0]:
                    generated_rooms['top_center'][1].add_single_pillar(top_left, ground_floor)
            else:
                generated_rooms['top_right'][1].add_single_pillar(top_left, ground_floor)

        elif room_name == 'center_left':

            if not generated_rooms['top_left'][0] and not generated_rooms['bottom_left'][0]:
                generated_rooms['center_left'][1].add_single_pillar(top_left, ground_floor)
                generated_rooms['center_left'][1].add_single_pillar(bottom_left, ground_floor)
            elif generated_rooms['top_left'][0] and not generated_rooms['bottom_left'][0]:
                generated_rooms['center_left'][1].add_single_pillar(bottom_left, ground_floor)
            elif generated_rooms['bottom_left'][0] and not generated_rooms['top_left'][0]:
                generated_rooms['center_left'][1].add_single_pillar(top_left, ground_floor)

            if generated_rooms['true_center'][0]:
                # generated_rooms['center_left'][1].add_single_pillar(top_right)
                # generated_rooms['center_left'][1].add_single_pillar(bottom_right)
                generated_rooms['center_left'][1].add_single_pillar(top_right, ground_floor)
                generated_rooms['center_left'][1].add_single_pillar(bottom_right, ground_floor)

        elif room_name == 'center_right':
            if not generated_rooms['top_right'][0] and not generated_rooms['bottom_right'][0]:
                generated_rooms['center_right'][1].add_single_pillar(bottom_right, ground_floor)
                generated_rooms['center_right'][1].add_single_pillar(top_right, ground_floor)
            elif generated_rooms['top_right'][0] and not generated_rooms['bottom_right'][0]:
                generated_rooms['center_right'][1].add_single_pillar(top_right, ground_floor)
            elif generated_rooms['bottom_right'][0] and not generated_rooms['top_right'][0]:
                generated_rooms['center_right'][1].add_single_pillar(top_right, ground_floor)
            if generated_rooms['true_center'][0]:
                # generated_rooms['center_right'][1].add_single_pillar(top_left)
                # generated_rooms['center_right'][1].add_single_pillar(bottom_left)

                generated_rooms['center_right'][1].add_single_pillar(top_left, ground_floor)
                generated_rooms['center_right'][1].add_single_pillar(bottom_left, ground_floor)

        elif room_name == 'top_center':
            if not generated_rooms['top_left'][0] and not generated_rooms['top_right'][0]:
                generated_rooms['top_center'][1].add_single_pillar(top_left, ground_floor)
                generated_rooms['top_center'][1].add_single_pillar(top_right, ground_floor)
            elif generated_rooms['top_right'][0] and not generated_rooms['top_left'][0]:
                generated_rooms['top_center'][1].add_single_pillar(top_right, ground_floor)

                generated_rooms['top_center'][1].add_single_pillar(top_right, ground_floor)
            # if not generated_rooms['top_left'][0] and not generated_rooms['top_right'][0]:

            if generated_rooms['true_center'][0]:
                # generated_rooms['top_center'][1].add_single_pillar(bottom_left)
                # generated_rooms['top_center'][1].add_single_pillar(bottom_right)

                generated_rooms['top_center'][1].add_single_pillar(bottom_left, ground_floor)
                generated_rooms['top_center'][1].add_single_pillar(bottom_right, ground_floor)

        elif room_name == 'bottom_center':
            if not generated_rooms['bottom_left'][0] and not generated_rooms['bottom_right'][0]:
                generated_rooms['bottom_center'][1].add_single_pillar(ground_floor)
                generated_rooms['bottom_center'][1].add_single_pillar(bottom_right, ground_floor)

            elif generated_rooms['bottom_right'][0] and not generated_rooms['bottom_left'][0]:
                generated_rooms['bottom_center'][1].add_single_pillar(bottom_left, ground_floor)
            elif generated_rooms['bottom_left'][0] and not generated_rooms['bottom_right'][0]:
                generated_rooms['bottom_center'][1].add_single_pillar(bottom_right, ground_floor)
            # if not generated_rooms['top_left'][0] and not generated_rooms['top_right'][0]:
            if generated_rooms['true_center'][0]:
                # generated_rooms['bottom_center'][1].add_single_pillar(top_left)
                # generated_rooms['bottom_center'][1].add_single_pillar(top_right)

                generated_rooms['bottom_center'][1].add_single_pillar(top_left, ground_floor)
                generated_rooms['bottom_center'][1].add_single_pillar(top_right, ground_floor)

        elif room_name == 'bottom_right':
            generated_rooms['bottom_right'][1].add_single_pillar(bottom_right, ground_floor)
            if generated_rooms['bottom_center'][0]:
                if not generated_rooms['bottom_left'][0]:
                    generated_rooms['bottom_center'][1].add_single_pillar(bottom_left, ground_floor)
            else:
                generated_rooms['bottom_right'][1].add_single_pillar(bottom_left, ground_floor)

            if generated_rooms['center_right'][0]:
                if not generated_rooms['top_right']:
                    generated_rooms['center_right'][1].add_single_pillar(top_right, ground_floor)
            else:
                generated_rooms['bottom_right'][1].add_single_pillar(top_right, ground_floor)

        elif room_name == 'bottom_left':
            generated_rooms['bottom_left'][1].add_single_pillar(bottom_left, ground_floor)
            if generated_rooms['bottom_center'][0]:
                if not generated_rooms['bottom_right'][0]:
                    generated_rooms['bottom_center'][1].add_single_pillar(bottom_right, ground_floor)
            else:
                generated_rooms['bottom_left'][1].add_single_pillar(Vec3(0, 0, 4), ground_floor)

            if generated_rooms['center_left'][0]:
                if not generated_rooms['top_left']:
                    generated_rooms['center_left'][1].add_single_pillar(top_left, ground_floor)
            else:
                generated_rooms['bottom_left'][1].add_single_pillar(top_left, ground_floor)

    @staticmethod
    def internal_wall(internal_wall_dice: int, wall_pos: dict, wall_pos_str: str, mat_pack: dict):
        wall_type = {
            'wall_door': 0,
            'ceil_bar': 1,
            'no_door': 2
        }
        start_cdr = wall_pos[wall_pos_str][0]
        end_cdr = wall_pos[wall_pos_str][1]

        if wall_type['wall_door'] == internal_wall_dice:
            mc.setBlocks(start_cdr, end_cdr, mat_pack['walls'])
            middle_block = Vec3((end_cdr.x + start_cdr.x) // 2, start_cdr.y, (end_cdr.z + start_cdr.z) // 2)
            Room.add_doors(door_x=middle_block.x, door_y=middle_block.y, door_z=middle_block.z, mat_pack=mat_pack,
                           door_type='single')
        elif wall_type['ceil_bar'] == internal_wall_dice:
            mc.setBlocks(start_cdr, end_cdr.x, end_cdr.y - 1, end_cdr.z, block.AIR.id)
            ceil_bar_start = start_cdr + Vec3(0, 3, 0)
            mc.setBlocks(ceil_bar_start.x, ceil_bar_start.y - 1,
                         ceil_bar_start.z, end_cdr.x, end_cdr.y, end_cdr.z,
                         mat_pack['walls'])
        elif wall_type['no_door'] == internal_wall_dice:
            mc.setBlocks(start_cdr, end_cdr, mat_pack['walls'])
            middle_block = Vec3((end_cdr.x + start_cdr.x) // 2, start_cdr.y, (end_cdr.z + start_cdr.z) // 2)
            mc.setBlocks(middle_block.x, middle_block.y, middle_block.z,
                         middle_block.x, middle_block.y + 1, middle_block.z,
                         block.AIR.id)
        else:
            # failsafe
            if internal_wall_dice > len(wall_type):
                print(f'''WARNING: house dice detected to be greater than wall_type dict
                House dice: {internal_wall_dice}; len(wall_type): {len(wall_type)}''')
                mc.postToChat('>>> WARN OCCURRED check console')
                internal_wall_dice = random.randint(0, len(wall_type))
                Room.internal_wall(internal_wall_dice=internal_wall_dice, wall_pos=wall_pos, wall_pos_str=wall_pos_str,
                                   mat_pack=mat_pack)
            else:
                mc.postToChat('>>> ERR OCCURRED check console')
                raise RuntimeError(f''''wall_type could not be found using the current house key
                House dice: {internal_wall_dice}; len(wall_type): {len(wall_type)}''')

    def add_foundation(self, ground_floor):
        if ground_floor:
            mc.setBlocks(self.pos,
                         self.pos.x + self.dimension.x, self.pos.y, self.pos.z + self.dimension.z,
                         self.mat_pack['foundation'])

            sleep(sleep_time/5)
            mc.setBlocks(self.pos.x, self.pos.y - 1, self.pos.z,
                         self.pos.x + self.dimension.x, self.pos.y - 15, self.pos.z + self.dimension.z,
                         self.mat_pack['foundation'])
            sleep(sleep_time/5)

            # Pyramid foundation.
            # for i in range(1, 12):
            #     mc.setBlocks(self.pos.x - i, self.pos.y - i, self.pos.z - i,
            #                  self.pos.x + self.dimension.x + i, self.pos.y - i, self.pos.z + self.dimension.z + i,
            #                  self.mat_pack['foundation'])

        else:
            # if upstairs
            mc.setBlocks(self.pos,
                         self.pos.x + self.dimension.x, self.pos.y, self.pos.z + self.dimension.z,
                         self.mat_pack['upstairs_floor'])
            sleep(sleep_time/5)
        pass

    def add_structure(self):
        foundation_height = 1
        mc.setBlocks(self.pos.x, self.pos.y + foundation_height, self.pos.z,
                     self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                     self.mat_pack['walls'])
        mc.setBlocks(self.pos.x + 1, self.pos.y + 1, self.pos.z + 1,
                     self.pos.x + (self.dimension.x - 1), self.pos.y + foundation_height + (self.dimension.y - 1),
                     self.pos.z + (self.dimension.z - 1),
                     block.AIR.id)

    def add_single_pillar(self, pillar_pos=Vec3(0, 0, 0), ground_floor=False):
        start_pos_pillar = self.pos + pillar_pos
        if ground_floor:
            mc.setBlocks(start_pos_pillar.x, start_pos_pillar.y, start_pos_pillar.z,
                         start_pos_pillar.x, start_pos_pillar.y + 4, start_pos_pillar.z, self.mat_pack['pillars'])
            mc.setBlocks(start_pos_pillar.x, start_pos_pillar.y, start_pos_pillar.z,
                         start_pos_pillar.x, start_pos_pillar.y - 15, start_pos_pillar.z, self.mat_pack['pillars'])
        else:
            mc.setBlocks(start_pos_pillar.x, start_pos_pillar.y, start_pos_pillar.z,
                         start_pos_pillar.x, start_pos_pillar.y + 4, start_pos_pillar.z, self.mat_pack['pillars'])

    def add_pillars(self, ground_floor=False):
        # Create corner pillars
        if not ground_floor:
            pointer_x, pointer_y, pointer_z = self.pos.x, self.pos.y, self.pos.z
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlocks(pointer_x, pointer_y, pointer_z,
                             pointer_x, pointer_y + 4, pointer_z,
                             self.mat_pack['pillars'])
                sleep(sleep_time/10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + self.dimension.z
                else:
                    pointer_z = self.pos.z
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x + self.dimension.x
        else:
            pointer_x, pointer_y, pointer_z = self.pos.x, self.pos.y, self.pos.z
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlocks(pointer_x, pointer_y - 15, pointer_z,
                             pointer_x, pointer_y + 4, pointer_z,
                             self.mat_pack['pillars'])
                sleep(sleep_time / 10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + self.dimension.z
                else:
                    pointer_z = self.pos.z
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x + self.dimension.x

    @staticmethod
    def add_doors(door_x, door_y, door_z, mat_pack,
                  door_type='single', door_pos='inside', door_state='closed', door_hinge_pos='left'):
        if door_type == 'double':
            if door_pos == 'outside':
                if door_state == 'closed':
                    # Make room
                    mc.setBlocks(door_x, door_y + 1, door_z + 2,
                                 door_x, door_y + 2, door_z + 3,
                                 block.AIR.id)
                    # Add doors
                    mc.setBlock(door_x, door_y + 2, door_z + 2,
                                block.DOOR_WOOD.id, 8)
                    mc.setBlock(door_x, door_y + 1, door_z + 3,
                                block.DOOR_WOOD.id, 0)

                    mc.setBlock(door_x + 1, door_y + 2, door_z,
                                block.DOOR_WOOD.id, 10)
                    mc.setBlock(door_x + 1, door_y + 1, door_z,
                                block.DOOR_WOOD.id, 5)
                elif door_state == 'opened':
                    # Make room
                    mc.setBlocks(door_x, door_y + 1, door_z + 2,
                                 door_x, door_y + 2, door_z + 3,
                                 block.AIR.id)
                    # Add doors
                    mc.setBlock(door_x, door_y + 2, door_z + 3,
                                block.DOOR_WOOD.id, 15)
                    mc.setBlock(door_x, door_y + 1, door_z + 3,
                                block.DOOR_WOOD.id, 4)

                    mc.setBlock(door_x, door_y + 2, door_z + 2,
                                block.DOOR_WOOD.id, 12)
                    mc.setBlock(door_x, door_y + 1, door_z + 2,
                                block.DOOR_WOOD.id, 1)
                else:
                    raise DoorError(door_type=door_type, door_state=door_state, door_pos=door_pos,
                                    door_hinge_pos=door_hinge_pos)
            elif door_pos == 'inside':
                pass
            else:
                raise DoorError(door_type=door_type, door_state=door_state, door_pos=door_pos,
                                door_hinge_pos=door_hinge_pos)
        elif door_type == 'single':
            if door_pos == 'inside':
                if door_hinge_pos == 'left':
                    if door_state == 'closed':
                        # Make room
                        mc.setBlocks(door_x, door_y, door_z,
                                     door_x, door_y + 1, door_z,
                                     block.AIR.id)
                        # Add first half of door above door_y
                        if mat_pack['door'] == blocks['oak_door']:
                            mc.setBlock(door_x, door_y + 1, door_z,
                                        blocks['oak_door'], 13)
                            # Add second half of door at door_y
                            mc.setBlock(door_x, door_y, door_z,
                                        blocks['oak_door'], 2)
                        else:
                            # Add first half of door above door_y
                            mc.setBlock(door_x, door_y + 1, door_z,
                                        mat_pack['door'], 10)
                            # Add second half of door at door_y
                            mc.setBlock(door_x, door_y, door_z,
                                        mat_pack['door'], 5)
                    elif door_state == 'opened':
                        pass
                    else:
                        raise DoorError(door_type=door_type, door_state=door_state, door_pos=door_pos,
                                        door_hinge_pos=door_hinge_pos)
                else:
                    pass
            elif door_pos == 'outside':
                pass
            else:
                raise DoorError(door_type=door_type, door_state=door_state, door_pos=door_pos,
                                door_hinge_pos=door_hinge_pos)
        else:
            raise DoorError(door_type=door_type, door_state=door_state, door_pos=door_pos,
                            door_hinge_pos=door_hinge_pos)

    def base_roof(self):
        # add the outer ring
        mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z,
                     self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                     self.mat_pack['roof_outer'])
        sleep(sleep_time / 10)
        # add sunroof in the middle (//2)
        middle_x = self.dimension.x // 2
        middle_z = self.dimension.z // 2
        mc.setBlock(self.pos.x + middle_x, self.pos.y + self.dimension.y, self.pos.z + middle_z,
                    self.mat_pack['sunroof'])

    def add_roof(self, roof_type='angled_flat'):
        if roof_type == 'base':
            self.base_roof()

        elif roof_type == 'flat':
            self.base_roof()

            pointer_x, pointer_y, pointer_z = self.pos.x, self.pos.y, self.pos.z
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlock(pointer_x, pointer_y + self.dimension.y, pointer_z,
                            self.mat_pack['roof_corner'])
                sleep(sleep_time / 10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + self.dimension.z
                else:
                    pointer_z = self.pos.z
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x + self.dimension.x

        elif roof_type == 'angled_flat':
            self.base_roof()
            # front
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                         self.mat_pack['slab'])
            # right
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y,
                         self.pos.z + self.dimension.z,
                         self.mat_pack['slab'])
            # left
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.mat_pack['slab'])
            # back
            mc.setBlocks(self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y,
                         self.pos.z + self.dimension.z,
                         self.mat_pack['slab'])

            # Add corner slabs
            pointer_x, pointer_y, pointer_z = self.pos.x, self.pos.y, self.pos.z
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlock(pointer_x, pointer_y + self.dimension.y, pointer_z,
                            self.mat_pack['roof_corner'])
                sleep(sleep_time / 10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + self.dimension.z
                else:
                    pointer_z = self.pos.z
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x + self.dimension.x

        elif roof_type == 'stair_flat':
            self.base_roof()
            # 0,1,2,3 = front,back,left,right
            front = 0
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                         self.mat_pack['stairs'], front)
            right = 3
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z + self.dimension.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y,
                         self.pos.z + self.dimension.z,
                         self.mat_pack['stairs'], right)
            left = 2
            mc.setBlocks(self.pos.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.mat_pack['stairs'], left)
            back = 1
            mc.setBlocks(self.pos.x + self.dimension.x, self.pos.y + self.dimension.y, self.pos.z,
                         self.pos.x + self.dimension.x, self.pos.y + self.dimension.y,
                         self.pos.z + self.dimension.z,
                         self.mat_pack['stairs'], back)

            # Add corner slabs
            pointer_x, pointer_y, pointer_z = self.pos.x, self.pos.y, self.pos.z
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlock(pointer_x, pointer_y + self.dimension.y, pointer_z,
                            self.mat_pack['roof_corner'])
                sleep(sleep_time / 10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + self.dimension.z
                else:
                    pointer_z = self.pos.z
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x + self.dimension.x
        elif roof_type == 'stair_med':
            self.add_roof(roof_type='stair_flat')
            # Second level
            x_deviation = 1
            z_deviation = -1
            y_deviation = 1
            front = 0
            mc.setBlocks(self.pos.x + x_deviation, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z - z_deviation,
                         self.pos.x + x_deviation, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z + z_deviation + self.dimension.z,
                         self.mat_pack['stairs'], front)
            right = 3
            mc.setBlocks(self.pos.x + x_deviation, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z + z_deviation + self.dimension.z,
                         self.pos.x - x_deviation + self.dimension.x, self.pos.y + y_deviation + self.dimension.y,
                         self.pos.z + z_deviation + self.dimension.z,
                         self.mat_pack['stairs'], right)
            left = 2
            mc.setBlocks(self.pos.x + x_deviation, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z - z_deviation,
                         self.pos.x - x_deviation + self.dimension.x, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z - z_deviation,
                         self.mat_pack['stairs'], left)
            back = 1
            mc.setBlocks(self.pos.x - x_deviation + self.dimension.x, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z - z_deviation,
                         self.pos.x - x_deviation + self.dimension.x, self.pos.y + self.dimension.y + y_deviation,
                         self.pos.z + z_deviation + self.dimension.z,
                         self.mat_pack['stairs'], back)

            # Add corner slabs
            pointer_x, pointer_y, pointer_z = self.pos.x + x_deviation, self.pos.y + y_deviation, self.pos.z - z_deviation
            for i in range(5):
                # Start from the front-left most corner
                mc.setBlock(pointer_x, pointer_y + self.dimension.y, pointer_z,
                            self.mat_pack['roof_corner'])
                sleep(sleep_time / 10)
                # Move the z pointer to the right if i is even; else move pointer to left
                if i % 2 == 0:
                    pointer_z = self.pos.z + z_deviation + self.dimension.z
                else:
                    pointer_z = self.pos.z - z_deviation
                # Move the x pointer to back after the front 2 corners are done
                if i > 1:
                    pointer_x = self.pos.x - x_deviation + self.dimension.x


# Random generation
def bias_random(low, high, mode):
    return int(random.triangular(low, high, mode))


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Error classes below
class DoorError(Exception):
    def __init__(self, door_type='unset', door_state='unset', door_pos='unset', door_hinge_pos='unset'):
        self.message = f'''\n
        Door TYPE is set to: {door_type}
        Door STATE is set to: {door_state}
        Door POS is set to: {door_pos}
        Door HINGE_POS is et to: {door_hinge_pos}'''
        super().__init__(self.message)


def main():
    center = mc.player.getPos()
    door_room = Vec3(center.x - 4, center.y, center.z)
    biome = 3

    House(center=center,
          door_room=door_room,
          biome=biome)
    print('-------------')


def create_many():
    center = mc.player.getPos()
    door_room = Vec3(center.x + 4, center.y, center.z)
    biome = 3

    house_count = 1
    vec_mod = Vec3()
    for i in range(1, 11):
        for j in range(1, 11):
            sleep(0.2)
            print(f'new house | {house_count}')
            House(center=(center + vec_mod),
                  door_room=door_room + vec_mod,
                  biome=biome)
            print('-------------')
            vec_mod.z += 18
            house_count += 1
        vec_mod.z = 0
        vec_mod.x += 20


def initialise():
    # previous positioning: x:952, y:203, z:1263
    mc.postToChat("Teleporting player...")
    mc.player.setPos(0, 50, 0)
    pos = mc.player.getPos()
    mc.postToChat("airing...")
    mc.setBlocks(pos.x + 100, pos.y, pos.z - 100, pos.x - 100, pos.y + 100, pos.z + 100, block.AIR.id)
    mc.postToChat("airing complete")
    mc.postToChat("setting blocks...")
    mc.setBlocks(pos.x + 100, pos.y, pos.z - 100, pos.x - 100, pos.y, pos.z + 100, block.STAINED_GLASS.id, 15)
    mc.postToChat("INITIALISE COMPLETE")


def test_dict():
    pos = mc.player.getPos()
    for key, value in blocks.items():
        mc.setBlock(pos.x + 1, pos.y + 1, pos.z - 2, value)
        pos.x = pos.x + 2


def test_door():
    pos = mc.player.getPos()
    pos += Vec3(1, 1, 1)
    i = 0
    k = 16
    for _ in range(16):
        mc.setBlock(pos.x, pos.y + 1, pos.z + i, blocks['birch_door'], k)
        k -= 1
        i += 2
    i = j = k = 0
    for _ in range(16):
        mc.setBlock(pos.x, pos.y, pos.z + i, blocks['birch_door'], k)
        j += 1
        i += 2


def find_blocks():
    pos = mc.player.getPos()
    pos += Vec3(1, 1, 1)

    for i in range(11):
        mc.setBlock(pos.x + i, pos.y, pos.z, 44, i)


def test():
    pos = mc.player.getPos()
    pos += Vec3(1, 0, 1)
    mc.setBlock(pos.x, pos.y, pos.z, blocks['birch_stairs'], 2)
    # for i in range(20):
    #     mc.spawnEntity(pos, 50)


if __name__ == '__main__':
    # initialise()
    create_many()
    # main()
    # test_dict()
    # test_door()
    # test_blocks()
    # test()
