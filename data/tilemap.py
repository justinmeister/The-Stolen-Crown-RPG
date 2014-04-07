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
    houseoverworld = setup.GFX['houseoverworld']
    oldmanhouse = setup.GFX['house1']
    evilcastle = setup.GFX['evilcastle']

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
    tile_dict['bottomwater1'] = get_tile(16, 32, tileset2)
    tile_dict['bottomwater2'] = get_tile(32, 32, tileset2)
    tile_dict['bottomwater3'] = get_tile(48, 32, tileset2)
    tile_dict['topwater1'] = get_tile(16, 0, tileset2)
    tile_dict['topwater2'] = get_tile(32, 0, tileset2)
    tile_dict['topwater3'] = get_tile(48, 0, tileset2)
    tile_dict['leftwater1'] = get_tile(80, 0, tileset2)
    tile_dict['leftwater2'] = get_tile(80, 16, tileset2)
    tile_dict['leftwater3'] = get_tile(0, 16, tileset2)
    tile_dict['rightwater1'] = get_tile(144, 0, tileset2)
    tile_dict['rightwater2'] = get_tile(144, 16, tileset2)
    tile_dict['rightwater3'] = get_tile(64, 16, tileset2)
    tile_dict['houseoverworld'] = get_tile(0, 0, houseoverworld, 128, 128)
    tile_dict['oldmanhouse'] = get_tile(0, 0, oldmanhouse, 32, 32)
    tile_dict['evilcastle'] = get_tile(0, 0, evilcastle, 128, 128)

    return tile_dict

def create_layer1_tile_code_dict():
    """Creates a dictionary of codes to tiles for layer 1"""
    tile_dict = {'1': 'pavement',
                 '2': 'house wall',
                 '3': 'house roof',
                 'T': 'tree',
                 'W': 'well',
                 'M': 'moat',
                 'G': 'grass',
                 'B': 'castle bridge',
                 'V': 'left vert castle wall',
                 'C': 'horiz castle wall',
                 'X': 'right vert castle wall',
                 'S': 'castle side',
                 'Q': 'carpet topleft',
                 'E': 'carpet topright',
                 'J': 'carpet top',
                 'R': 'carpet bottomleft',
                 'U': 'carpet bottomright',
                 'D': 'carpet bottom',
                 'P': 'carpet left',
                 'A': 'carpet right',
                 'F': 'carpet center',
                 'H': 'marble floor',
                 'K': 'black tile',
                 'L': 'topwater1',
                 'N': 'topwater2',
                 'Y': 'topwater3',
                 'Z': 'leftwater1',
                 '4': 'leftwater2',
                 '5': 'leftwater3',
                 '6': 'rightwater1',
                 '7': 'rightwater2',
                 '8': 'rightwater3',
                 '9': 'bottomwater1',
                 'a': 'bottomwater2',
                 'b': 'bottomwater3'
                }

    return tile_dict

def create_layer2_tile_code_dict():
    """Creates a dictionary of tile codes for layer 2"""
    tile_dict = {'D': 'house door',
                 'F': 'fence',
                 '$': 'flower1',
                 '*': 'flower2',
                 'T': 'castle tower',
                 'W': 'left vert castle wall',
                 'M': 'main castle roof',
                 'L': 'left castle roof piece',
                 'R': 'right castle roof piece',
                 '#': 'tree',
                 'O': 'castle door',
                 'Q': 'castle window',
                 'A': 'banner1',
                 'B': 'banner2',
                 'C': 'banner3',
                 'E': 'bed',
                 'G': 'shelves',
                 'H': 'chair',
                 'I': 'table',
                 'J': 'fancy carpet',
                 'K': 'column',
                 'N': 'black tile',
                 'P': 'houseoverworld',
                 '4': 'oldmanhouse',
                 '5': 'evilcastle'
    }

    return tile_dict

def create_layer3_tile_code_dict():
    """Creates a dictionary of tile codes for layer 3"""
    tile_dict = {'W': 'sword',
                 'A': 'shield',
                 'P': 'potion',
                 'M': 'gem',
                 'I': 'inn sign',
                 'B': 'chair'}

    return tile_dict

def make_level_portals_code_dict():
    """Make the dictionary for codes for level portals"""
    portal_dict = {'A': c.CASTLE,
                   'B': c.TOWN,
                   'C': c.INN,
                   'D': c.MAGIC_SHOP,
                   'E': c.POTION_SHOP,
                   'F': c.WEAPON_SHOP,
                   'G': c.ARMOR_SHOP,
                   'H': c.HOUSE,
                   'J': c.OVERWORLD,
                   'K': c.BROTHER_HOUSE
    }

    return portal_dict

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
    if state_name == c.TOWN or state_name == c.OVERWORLD:
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
            if letter not in layer1_tile_code_dict:
                pass
            else:
                tile = tile_dict[layer1_tile_code_dict[letter]]
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
    layer2_tile_dict = create_layer2_tile_code_dict()

    tile_map = open(os.path.join('data', 'states', state, file_name), 'r')

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter not in layer2_tile_dict:
                pass
            else:
                tile = tile_dict[layer2_tile_dict[letter]]
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
    layer3_tile_dict = create_layer3_tile_code_dict()

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter not in layer3_tile_dict:
                pass
            else:
                tile = tile_dict[layer3_tile_dict[letter]]
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
    portal_code_dict = make_level_portals_code_dict()
    portal_group = pg.sprite.Group()

    for row, line in enumerate(tile_map):
        for column, letter in enumerate(line):
            if letter not in portal_code_dict:
                pass
            else:
                portal_group.add(portal.Portal(
                    column, row, portal_code_dict[letter]))

    return portal_group


get_image = tools.get_image
tile_dict = create_town_sprite_sheet_dict()
layer1_tile_code_dict = create_layer1_tile_code_dict()

