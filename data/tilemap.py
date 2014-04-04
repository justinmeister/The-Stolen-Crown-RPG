__author__ = 'justinarmstrong'

import os
import pygame as pg
from . import tools, setup
from . components import person, portal
from . import constants as c


def create_town_sprite_sheet_dict():
    """Create a dictionary of sprite sheet tiles"""
    tile_dict = {}
    tileset1 = setup.GFX['tileset1']
    tileset2 = setup.GFX['tileset2']
    tileset3 = setup.GFX['tileset3']
    shopsigns = setup.GFX['shopsigns']
    castle_door = setup.GFX['castledoor']
    medieval_signs = setup.GFX['medievalsigns']
    house = setup.GFX['house']

    tile_dict['pavement'] = get_tile(32, 48, tileset2)
    tile_dict['house wall'] = get_tile(64, 48, tileset2)
    tile_dict['house roof'] = get_tile(0, 144, tileset2)
    tile_dict['house door'] = get_tile(48, 64, tileset2)
    tile_dict['tree'] = get_tile(80, 48, tileset1, 16, 32)
    tile_dict['well'] = get_tile(96, 50, tileset1, 16, 32)
    tile_dict['moat'] = get_tile(16, 16, tileset2)
    tile_dict['fence'] = get_tile(48, 64, tileset1)
    tile_dict['grass'] = get_tile(0, 16, tileset1)
    tile_dict['sword'] = get_tile(96, 0, shopsigns, 32, 32)
    tile_dict['shield'] = get_tile(64, 0, shopsigns, 32, 32)
    tile_dict['potion'] = get_tile(32, 0, shopsigns, 32, 32)
    tile_dict['gem'] = get_tile(0, 0, shopsigns, 32, 32)
    tile_dict['castle bridge'] = get_tile(48, 27, tileset1, 16, 32 )
    tile_dict['flower1'] = get_tile(64, 64, tileset2)
    tile_dict['flower2'] = get_tile(80, 64, tileset2)
    tile_dict['horiz castle wall'] = get_tile(32, 0, tileset3, 48, 32)
    tile_dict['left vert castle wall'] = get_tile(0, 16, tileset3)
    tile_dict['right vert castle wall'] = get_tile(162, 16, tileset3)
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
    tile_dict['carpet bottom'] = get_tile(128, 144, tileset2)
    tile_dict['carpet top'] = get_tile(128, 112, tileset2)
    tile_dict['carpet left'] = get_tile(112, 128, tileset2)
    tile_dict['carpet right'] = get_tile(144, 128, tileset2)
    tile_dict['carpet center'] = get_tile(128, 128, tileset2)
    tile_dict['castle window'] = get_tile(128, 59, tileset1)
    tile_dict['marble floor'] = get_tile(80, 96, tileset3)
    tile_dict['inn sign'] = get_tile(0, 96, medieval_signs, 32, 32)
    tile_dict['banner1'] = get_tile(112, 38, tileset3, 16, 22)
    tile_dict['banner2'] = get_tile(128, 38, tileset3, 16, 22)
    tile_dict['banner3'] = get_tile(144, 38, tileset3, 16, 22)
    tile_dict['black tile'] = make_black_surface_tile()
    tile_dict['bed'] = get_tile(456, 206, house, 48, 82)
    tile_dict['shelves'] = get_tile(352, 116, house, 160, 70)
    tile_dict['chair'] = get_tile(323, 256, house, 32, 32)
    tile_dict['table'] = get_tile(82, 161, tileset3, 46, 32)
    tile_dict['fancy carpet'] = get_tile(112, 96, tileset3, 64, 64)
    tile_dict['column'] = get_tile(64, 96, tileset3, 16, 48)

    return tile_dict


def get_tile(x, y, tileset, width=16, height=16, scale=1):
    """Gets the surface and rect for a tile"""
    surface = get_image(x, y, width, height, tileset)
    surface = pg.transform.scale(surface, (int(width*scale), int(height*scale)))
    rect = surface.get_rect()

    tile_dict = {'surface': surface,
                 'rect': rect}

    return tile_dict


def make_black_surface_tile():
    """Make a black surface"""
    surface = pg.Surface((32, 32))
    surface.fill(c.NEAR_BLACK_BLUE)
    rect = surface.get_rect()
    new_dict = {'surface': surface,
                'rect': rect}

    return new_dict


def make_background(state_name, width, height):
    """Creates the background surface that the rest of
    the town map will be blitted on"""
    size = (width*16, height*16)
    surface = pg.Surface(size)
    if state_name == c.TOWN:
        tile = get_image(0, 0, 16, 16, setup.GFX['tileset2'])
    else:
        tile = pg.Surface((16, 16))
        tile.fill(c.BLACK_BLUE)

    rect = tile.get_rect()

    for row in range(height):
        for column in range(width):
            rect.y = row * 16
            rect.x = column * 16
            surface.blit(tile, rect)

    return surface


def create_map_layer1(state, width, height):
    """Creates the town from a tile map and creates a
    surface on top of the background"""
    map = make_background(state, width, height)

    tile_map = open(os.path.join('data', 'states', state, 'layer1.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == '1':
                tile = tile_dict['pavement']
                blit_tile_to_map(tile, row, column, map)

            elif letter == '2':
                tile = tile_dict['house wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == '3':
                tile = tile_dict['house roof']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'T':
                tile = tile_dict['tree']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'W':
                tile = tile_dict['well']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'M':
                tile = tile_dict['moat']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'G':
                tile = tile_dict['grass']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'B':
                tile = tile_dict['castle bridge']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'C':
                tile = tile_dict['horiz castle wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'V':
                tile = tile_dict['left vert castle wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'X':
                tile = tile_dict['right vert castle wall']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'S':
                tile = tile_dict['castle side']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'Q':
                tile = tile_dict['carpet topleft']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'E':
                tile = tile_dict['carpet topright']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'J':
                tile = tile_dict['carpet top']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'R':
                tile = tile_dict['carpet bottomleft']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'U':
                tile = tile_dict['carpet bottomright']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'D':
                tile = tile_dict['carpet bottom']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'P':
                tile = tile_dict['carpet left']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'A':
                tile = tile_dict['carpet right']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'F':
                tile = tile_dict['carpet center']
                blit_tile_to_map(tile, row, column, map)

            elif letter == 'H':
                tile = tile_dict['marble floor']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'K':
                tile = tile_dict['black tile']
                blit_tile_to_map(tile, row, column, map)


    tile_map.close()

    layer1_extra = create_map_layer2(state, width, height, 'layer1extra.txt')
    map.blit(layer1_extra, (0,0))

    map = scale_map(map)

    return map


def create_map_layer2(state, width, height, file_name='layer2.txt'):
    """Creates doors and other items on top of the rest of the map"""
    map = make_background(None, width, height)
    map.set_colorkey(c.BLACK_BLUE)

    tile_map = open(os.path.join('data', 'states', state, file_name), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'D':
                tile = tile_dict['house door']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'F':
                tile = tile_dict['fence']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '$':
                tile = tile_dict['flower1']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '*':
                tile = tile_dict['flower2']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'T':
                tile = tile_dict['castle tower']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'W':
                tile = tile_dict['left vert castle wall']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'M':
                tile = tile_dict['main castle roof']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'L':
                tile = tile_dict['left castle roof piece']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'R':
                tile = tile_dict['right castle roof piece']
                blit_tile_to_map(tile, row, column, map)
            elif letter == '#':
                tile = tile_dict['tree']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'O':
                tile = tile_dict['castle door']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'Q':
                tile = tile_dict['castle window']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'A':
                tile = tile_dict['banner1']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'B':
                tile = tile_dict['banner2']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'C':
                tile = tile_dict['banner3']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'E':
                tile = tile_dict['bed']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'G':
                tile = tile_dict['shelves']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'H':
                tile = tile_dict['chair']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'I':
                tile = tile_dict['table']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'J':
                tile = tile_dict['fancy carpet']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'K':
                tile = tile_dict['column']
                blit_tile_to_map(tile, row, column, map)
            elif letter == 'N':
                tile = tile_dict['black tile']
                blit_tile_to_map(tile, row, column, map)

    tile_map.close()

    if file_name == 'layer2.txt':
        map = pg.transform.scale2x(map)
        map = create_map_layer3(map, state)

    return map


def scale_map(map):
    """Double resolution of map to 32x32"""
    map = pg.transform.scale2x(map)

    return map


def create_map_layer3(map, state):
    """Layers for images that are already 32x32"""
    tile_map = open(os.path.join('data', 'states', state, 'layer3.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'W':
                tile = tile_dict['sword']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'A':
                tile = tile_dict['shield']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'P':
                tile = tile_dict['potion']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'M':
                tile = tile_dict['gem']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'I':
                tile = tile_dict['inn sign']
                blit_tile_to_map(tile, row, column, map, 32)
            elif letter == 'B':
                tile = tile_dict['chair']
                blit_tile_to_map(tile, row, column, map, 32)


    tile_map.close()

    return map



def blit_tile_to_map(tile, row, column, map, side_length=16):
    """Places tile to map"""
    tile['rect'].x = column * side_length
    tile['rect'].y = row * side_length

    map.blit(tile['surface'], tile['rect'])


def create_blockers(state):
    """Creates invisible rect objects that will prevent the player from
    walking into trees, buildings and other solid objects"""
    tile_map = open(os.path.join('data', 'states', state, 'blockers.txt'), 'r')
    blockers = []

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'B':
                blockers.append(pg.Rect(column*32, row*32, 32, 32))

    tile_map.close()

    return blockers


def make_level_surface(map):
    """Creates the surface all images are blitted to"""
    map_rect = map.get_rect()
    size = map_rect.size


    return pg.Surface(size).convert()


def create_viewport(map):
    """Create the viewport to view the level through"""
    map_rect = map.get_rect()
    return setup.SCREEN.get_rect(bottom=map_rect.bottom)


def set_sprite_positions(player, level_sprites, state, game_data):
    """Set the start positions for all the sprites in the level"""
    start_pos_key = state + ' start pos'
    x =  game_data[start_pos_key][0]*32
    y = game_data[start_pos_key][1]*32
    player.rect = pg.Rect(x, y, 32, 32)

    tile_map = open(os.path.join('data', 'states', state, 'sprite_start_pos.txt'), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'F':
                fem_villager = person.FemaleVillager(column*32, row*32)
                level_sprites.add(fem_villager)
            elif letter == 'S':
                soldier = person.Soldier(column*32, row*32)
                level_sprites.add(soldier)
            elif letter == 'A':
                soldier = person.Soldier(column*32, row*32, 'right', 'resting')
                level_sprites.add(soldier)
            elif letter == 'B':
                soldier = person.Soldier(column*32, row*32, 'left', 'resting')
                level_sprites.add(soldier)
            elif letter == 'C':
                king = person.King(column*32, row*32, 'down', 'resting')
                level_sprites.add(king)
            elif letter == 'D':
                well = person.Well(column*32, row*32)
                level_sprites.add(well)
            elif letter == 'E':
                fem_villager = person.FemaleVillager2(column*32, row*32)
                level_sprites.add(fem_villager)
            elif letter == 'G':
                devil_villager = person.Devil(column*32, row*32)
                level_sprites.add(devil_villager)
            elif letter == 'H':
                old_villager = person.OldMan(column*32, row*32)
                level_sprites.add(old_villager)

    tile_map.close()


def make_level_portals(state):
    """Create portals to different levels on doors"""
    tile_map = open(os.path.join('data', 'states', state, 'portals.txt'), 'r')
    portal_group = pg.sprite.Group()

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter == 'A':
                portal_group.add(portal.Portal(column, row, c.CASTLE))
            elif letter == 'B':
                portal_group.add(portal.Portal(column, row, c.TOWN))
            elif letter == 'C':
                portal_group.add(portal.Portal(column, row, c.INN))
            elif letter == 'D':
                portal_group.add(portal.Portal(column, row, c.MAGIC_SHOP))
            elif letter == 'E':
                portal_group.add(portal.Portal(column, row, c.POTION_SHOP))
            elif letter == 'F':
                portal_group.add(portal.Portal(column, row, c.WEAPON_SHOP))
            elif letter == 'G':
                portal_group.add(portal.Portal(column, row, c.ARMOR_SHOP))
            elif letter == 'H':
                portal_group.add(portal.Portal(column, row, c.HOUSE))

    return portal_group



get_image = tools.get_image
tile_dict = create_town_sprite_sheet_dict()

