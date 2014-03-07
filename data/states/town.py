__author__ = 'justinarmstrong'

import os
import pygame as pg
from .. import setup, tools
from .. import constants as c
from ..components.player import Player

class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()


    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.get_image = setup.tools.get_image
        self.town_map_dict = self.create_town_sprite_sheet_dict()
        self.town_map = self.create_town_map()
        self.viewport = self.create_viewport()
        self.level_surface = self.create_level_surface()
        self.level_rect = self.level_surface.get_rect()
        self.player = Player()
        self.start_positions = self.set_sprite_positions()


    def create_town_sprite_sheet_dict(self):
        """Create a dictionary of sprite sheet tiles"""
        tile_dict = {}
        tileset1 = setup.GFX['tileset1']
        tileset2 = setup.GFX['tileset2']
        sword = setup.GFX['sword']
        shield = setup.GFX['shield']
        potion = setup.GFX['potion']
        gem = setup.GFX['gem']

        tile_dict['pavement'] = self.get_tile(32, 48, tileset2)
        tile_dict['house wall'] = self.get_tile(64, 48, tileset2)
        tile_dict['house roof'] = self.get_tile(0, 144, tileset2)
        tile_dict['house door'] = self.get_tile(48, 64, tileset2)
        tile_dict['tree'] = self.get_tile(80, 48, tileset1, 16, 32)
        tile_dict['well'] = self.get_tile(96, 50, tileset1, 16, 32)
        tile_dict['moat'] = self.get_tile(16, 16, tileset2)
        tile_dict['fence'] = self.get_tile(48, 64, tileset1)
        tile_dict['grass'] = self.get_tile(0, 16, tileset1)
        tile_dict['sword'] = self.get_tile(0, 0, sword, 32, 32)
        tile_dict['shield'] = self.get_tile(0, 0, shield, 32, 32)
        tile_dict['potion'] = self.get_tile(0, 0, potion, 32, 32)
        tile_dict['gem'] = self.get_tile(0, 0, gem, 32, 32)
        tile_dict['castle bridge'] = self.get_tile(48, 27, tileset1, 16, 32 )
        tile_dict['flower1'] = self.get_tile(64, 64, tileset2)
        tile_dict['flower2'] = self.get_tile(80, 64, tileset2)

        return tile_dict


    def get_tile(self, x, y, tileset, width=16, height=16):
        """Gets the surface and rect for a tile"""
        surface = self.get_image(self, x, y, width, height, tileset)
        rect = surface.get_rect()

        tile_dict = {'surface': surface,
                     'rect': rect}

        return tile_dict


    def create_town_map(self):
        """Blits the different layers of the map onto one surface"""
        map = self.create_background()
        map = self.create_map_layer1(map)
        map = self.create_map_layer2(map)
        map = self.scale_map(map)
        map = self.create_map_layer3(map)

        return map


    def create_background(self):
        """Creates the background surface that the rest of
        the town map will be blitted on"""
        size = (25*16, 50*16)
        surface = pg.Surface(size)
        grass_tile = self.get_image(self, 0, 0, 16, 16, setup.GFX['tileset2'])
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


    def create_map_layer1(self, map):
        """Creates the town from a tile map and creates a
        surface on top of the background"""
        tile_map = open(os.path.join('data', 'states', 'town_map.txt'), 'r')

        for row, line in enumerate(tile_map):
            for column, letter in enumerate(line):
                if letter == '1':
                    tile = self.town_map_dict['pavement']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == '2':
                    tile = self.town_map_dict['house wall']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == '3':
                    tile = self.town_map_dict['house roof']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == 'T':
                    tile = self.town_map_dict['tree']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == 'W':
                    tile = self.town_map_dict['well']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == 'M':
                    tile = self.town_map_dict['moat']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == 'G':
                    tile = self.town_map_dict['grass']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == 'B':
                    tile = self.town_map_dict['castle bridge']
                    self.blit_tile_to_map(tile, row, column, map)


        tile_map.close()

        return map


    def create_map_layer2(self, map):
        """Creates doors and other items on top of the rest of the map"""
        tile_map = open(os.path.join('data', 'states', 'town_layer2.txt'), 'r')

        for row, line in enumerate(tile_map):
            for column, letter in enumerate(line):
                if letter == 'D':
                    tile = self.town_map_dict['house door']
                    self.blit_tile_to_map(tile, row, column, map)
                elif letter == 'F':
                    tile = self.town_map_dict['fence']
                    self.blit_tile_to_map(tile, row, column, map)
                elif letter == '$':
                    tile = self.town_map_dict['flower1']
                    self.blit_tile_to_map(tile, row, column, map)
                elif letter == '*':
                    tile = self.town_map_dict['flower2']
                    self.blit_tile_to_map(tile, row, column, map)

        tile_map.close()

        return map


    def scale_map(self, map):
        """Double resolution of map to 32x32"""
        map['surface'] = pg.transform.scale2x(map['surface'])
        map['rect'] = map['surface'].get_rect()

        return map


    def create_map_layer3(self, map):
        """Layers for images that are already 32x32"""
        tile_map = open(os.path.join('data', 'states', 'town_layer3.txt'), 'r')

        for row, line in enumerate(tile_map):
            for column, letter in enumerate(line):
                if letter == 'W':
                    tile = self.town_map_dict['sword']
                    self.blit_tile_to_map(tile, row, column, map, 32)
                elif letter == 'A':
                    tile = self.town_map_dict['shield']
                    self.blit_tile_to_map(tile, row, column, map, 32)
                elif letter == 'P':
                    tile = self.town_map_dict['potion']
                    self.blit_tile_to_map(tile, row, column, map, 32)
                elif letter == 'M':
                    tile = self.town_map_dict['gem']
                    self.blit_tile_to_map(tile, row, column, map, 32)

        tile_map.close()

        return map



    def blit_tile_to_map(self, tile, row, column, map, side_length=16):
        """Places tile to map"""
        tile['rect'].x = column * side_length
        tile['rect'].y = row * side_length

        map['surface'].blit(tile['surface'], tile['rect'])


    def create_viewport(self):
        """Create the viewport to view the level through"""
        return setup.SCREEN.get_rect(bottom=self.town_map['rect'].bottom)


    def create_level_surface(self):
        """Creates the surface all images are blitted to"""
        width = self.town_map['rect'].width
        height = self.town_map['rect'].height

        return pg.Surface((width, height)).convert()


    def set_sprite_positions(self):
        """Set the start positions for all the sprites in the level"""
        tile_map = open(os.path.join('data', 'states', 'sprite_start_pos.txt'), 'r')
        dict = {}

        for row, line in enumerate(tile_map):
            for column, letter in enumerate(line):
                if letter == 'P':
                    dict['player'] = pg.Rect(column*32, row*32, 32, 32)

        self.player.rect = dict['player']

        return dict


    def update(self, surface, keys, current_time):
        """Updates state"""
        self.keys = keys
        self.current_time = current_time
        self.player.update(keys, current_time)
        self.update_viewport()

        self.draw_level(surface)


    def draw_level(self, surface):
        """Blits all images to screen"""
        self.level_surface.blit(self.town_map['surface'], self.viewport, self.viewport)
        self.level_surface.blit(self.player.image, self.player.rect)

        surface.blit(self.level_surface, (0,0), self.viewport)


    def update_viewport(self):
        """Viewport stays centered on character, unless at edge of map"""
        self.viewport.center = self.player.rect.center
        self.viewport.clamp_ip(self.level_rect)










