__author__ = 'justinarmstrong'

import os
import pygame as pg
import tools, setup
from components import person


def create_town_sprite_sheet_dict():
    """Create a dictionary of sprite sheet tiles"""
    tile_dict = {}
    tileset1 = setup.GFX['tileset1']
    tileset2 = setup.GFX['tileset2']
    tileset3 = setup.GFX['tileset3']
    sword = setup.GFX['sword']
    shield = setup.GFX['shield']
    potion = setup.GFX['potion']
    gem = setup.GFX['gem']
    castle_door = setup.GFX['castledoor']

    tile_dict['pavement'] = get_tile(32, 48, tileset2)
    tile_dict['house wall'] = get_tile(64, 48, tileset2)
    tile_dict['house roof'] = get_tile(0, 144, tileset2)
    tile_dict['house door'] = get_tile(48, 64, tileset2)
    tile_dict['tree'] = get_tile(80, 48, tileset1, 16, 32)
    tile_dict['well'] = get_tile(96, 50, tileset1, 16, 32)
    tile_dict['moat'] = get_tile(16, 16, tileset2)
    tile_dict['fence'] = get_tile(48, 64, tileset1)
    tile_dict['grass'] = get_tile(0, 16, tileset1)
    tile_dict['sword'] = get_tile(0, 0, sword, 32, 32)
    tile_dict['shield'] = get_tile(0, 0, shield, 32, 32)
    tile_dict['potion'] = get_tile(0, 0, potion, 32, 32)
    tile_dict['gem'] = get_tile(0, 0, gem, 32, 32)
    tile_dict['castle bridge'] = get_tile(48, 27, tileset1, 16, 32 )
    tile_dict['flower1'] = get_tile(64, 64, tileset2)
    tile_dict['flower2'] = get_tile(80, 64, tileset2)
    tile_dict['horiz castle wall'] = get_tile(32, 0, tileset3, 48, 32)
    tile_dict['vert castle wall'] = get_tile(0, 16, tileset3)
    tile_dict['castle tower'] = get_tile(116, 16, tileset1, 48, 64)
    tile_dict['main castle roof'] = get_tile(0, 0, tileset1, 160, 16)
    tile_dict['left castle roof piece'] = get_tile(0, 0, tileset1, 48, 16)
    tile_dict['right castle roof piece'] = get_tile(112, 0, tileset1, 48, 16)
    tile_dict['castle side'] = get_tile(0, 72, tileset3)
    tile_dict['castle door'] = get_tile(0, 0, castle_door, 64, 96)
    tile_dict['carpet topleft'] = get_tile(112, 112, tileset2)
    tile_dict['carpet topright'] = get_tile(144, 112, tileset2)
    tile_dict['carpet bottomleft'] = get_tile(112, 144, tileset2)
    tile_dict['carpet bottomright'] = get_tile(144, 144, tileset2)
    tile_dict['carpet left'] = get_tile(112, 128, tileset2)
    tile_dict['carpet right'] = get_tile(144, 128, tileset2)
    tile_dict['castle window'] = get_tile(128, 59, tileset1)

    return tile_dict


def get_tile(x, y, tileset, width=16, height=16, scale=1):
    """Gets the surface and rect for a tile"""
    surface = get_image(x, y, width, height, tileset)
    surface = pg.transform.scale(surface, (int(width*scale), int(height*scale)))
    rect = surface.get_rect()

    tile_dict = {'surface': surface,
                 'rect': rect}

    return tile_dict


def create_town_map():
    """Blits the different layers of the map onto one surface"""
    map = create_background()
    map = create_map_layer1(map)
    map = create_map_layer2(map)
    map = scale_map(map)
    map = create_map_layer3(map)

    return map


def create_background():
    """Creates the background surface that the rest of
    the town map will be blitted on"""
    size = (25*16, 50*16)
    surface = pg.Surface(size)
    grass_tile = get_image(0, 0, 16, 16, setup.GFX['tileset2'])
    grass_rect = grass_tile.get_rect()

    for row in range(50):
        for column in range(25):
            grass_rect.y = row * 16
            grass_rect.x = column * 16
            surface.blit(grass_tile, grass_rect)

    surface_rect = surface.get_rect()

    background_dict = {'surface': surface,
                       'rect': surface_rect}

    return background_dict


def create_map_layer1(map):
    """Creates the town from a tile map and creates a
    surface on top of the background"""
    tile_map = open(os.path.join('data', 'states', 'town_map.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == '1':
                tile = town_map_dict['pavement']
                blit_tile_to_map(tile, row, column, map)

            elif letter == '2':
                tile = town_map_dict['house wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == '3':
                tile = town_map_dict['house roof']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'T':
                tile = town_map_dict['tree']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'W':
                tile = town_map_dict['well']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'M':
                tile = town_map_dict['moat']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'G':
                tile = town_map_dict['grass']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'B':
                tile = town_map_dict['castle bridge']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'C':
                tile = town_map_dict['horiz castle wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'V':
                tile = town_map_dict['vert castle wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'S':
                tile = town_map_dict['castle side']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'Q':
                tile = town_map_dict['carpet topleft']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'E':
                tile = town_map_dict['carpet topright']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'R':
                tile = town_map_dict['carpet bottomleft']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'U':
                tile = town_map_dict['carpet bottomright']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'P':
                tile = town_map_dict['carpet left']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'A':
                tile = town_map_dict['carpet right']
                blit_tile_to_map(tile, row, column, map)


    tile_map.close()

    return map


def create_map_layer2(map):
    """Creates doors and other items on top of the rest of the map"""
    tile_map = open(os.path.join('data', 'states', 'town_layer2.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'D':
                tile = town_map_dict['house door']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'F':
                tile = town_map_dict['fence']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '$':
                tile = town_map_dict['flower1']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '*':
                tile = town_map_dict['flower2']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'T':
                tile = town_map_dict['castle tower']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'W':
                tile = town_map_dict['vert castle wall']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'M':
                tile = town_map_dict['main castle roof']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'L':
                tile = town_map_dict['left castle roof piece']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'R':
                tile = town_map_dict['right castle roof piece']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '#':
                tile = town_map_dict['tree']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'O':
                tile = town_map_dict['castle door']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'Q':
                tile = town_map_dict['castle window']
                blit_tile_to_map(tile, row, column, map)

    tile_map.close()

    return map


def scale_map(map):
    """Double resolution of map to 32x32"""
    map['surface'] = pg.transform.scale2x(map['surface'])
    map['rect'] = map['surface'].get_rect()

    return map


def create_map_layer3(map):
    """Layers for images that are already 32x32"""
    tile_map = open(os.path.join('data', 'states', 'town_layer3.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'W':
                tile = town_map_dict['sword']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'A':
                tile = town_map_dict['shield']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'P':
                tile = town_map_dict['potion']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'M':
                tile = town_map_dict['gem']
                blit_tile_to_map(tile, row, column, map, 32)

    tile_map.close()

    return map



def blit_tile_to_map(tile, row, column, map, side_length=16):
    """Places tile to map"""
    tile['rect'].x = column * side_length
    tile['rect'].y = row * side_length

    map['surface'].blit(tile['surface'], tile['rect'])


def create_blockers():
    """Creates invisible rect objects that will prevent the player from
    walking into trees, buildings and other solid objects"""
    tile_map = open(os.path.join('data', 'states', 'town_blocker_layer.txt'), 'r')
    blockers = []

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'B':
                blockers.append(pg.Rect(column*32, row*32, 32, 32))

    tile_map.close()

    return blockers


def create_level_surface(map):
    """Creates the surface all images are blitted to"""
    width = map['rect'].width
    height = map['rect'].height

    return pg.Surface((width, height)).convert()


def create_viewport(map):
    """Create the viewport to view the level through"""
    return setup.SCREEN.get_rect(bottom=map['rect'].bottom)


def set_sprite_positions(player, level_sprites):
    """Set the start positions for all the sprites in the level"""
    tile_map = open(os.path.join('data', 'states', 'sprite_start_pos.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'P':
                player.rect = pg.Rect(column*32, row*32, 32, 32)
            elif letter == 'F':
                fem_villager = person.FemaleVillager(column*32, row*32)
                level_sprites.add(fem_villager)
            elif letter == 'S':
                soldier = person.Soldier(column*32, row*32)
                level_sprites.add(soldier)

    tile_map.close()


get_image = tools.get_image
town_map_dict = create_town_sprite_sheet_dict()



