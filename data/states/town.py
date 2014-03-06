__author__ = 'justinarmstrong'

import os
import pygame as pg
from .. import setup, tools
from .. import constants as c

class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()


    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time
        self.get_image = setup.tools.get_image
        self.sprite_sheet_dict = self.create_sprite_sheet_dict()
        self.town_map = self.create_town_map()
        self.viewport = self.create_viewport()


    def create_sprite_sheet_dict(self):
        """Create a dictionary of sprite sheet tiles"""
        dict = {}
        tileset2 = setup.GFX['tileset2']

        dict['pavement'] = self.get_tile(32, 48, tileset2)
        dict['house wall'] = self.get_tile(64, 48, tileset2)
        dict['house roof'] = self.get_tile(0, 144, tileset2)
        dict['house door'] = self.get_tile(48, 64, tileset2)

        return dict


    def get_tile(self, x, y, tileset):
        """Gets the surface and rect for a tile"""
        surface = self.get_image(self, x, y, 16, 16, tileset)
        rect = surface.get_rect()

        dict = {'surface': surface,
                'rect': rect}

        return dict


    def create_town_map(self):
        """Blits the different layers of the map onto one surface"""
        map = self.create_background()
        map = self.create_map_layer1(map)
        map = self.create_map_layer2(map)
        map = self.scale_map(map)

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
                    tile = self.sprite_sheet_dict['pavement']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == '2':
                    tile = self.sprite_sheet_dict['house wall']
                    self.blit_tile_to_map(tile, row, column, map)

                elif letter == '3':
                    tile = self.sprite_sheet_dict['house roof']
                    self.blit_tile_to_map(tile, row, column, map)

        tile_map.close()

        return map


    def create_map_layer2(self, map):
        """Creates doors and other items on top of the rest of the map"""
        tile_map = open(os.path.join('data', 'states', 'town_layer2.txt'), 'r')

        for row, line in enumerate(tile_map):
            for column, letter in enumerate(line):
                if letter == 'D':
                    print 'hi'
                    tile = self.sprite_sheet_dict['house door']
                    self.blit_tile_to_map(tile, row, column, map)

        tile_map.close()

        return map


    def scale_map(self, map):
        """Doubles the size of map to fit a (800x600) aspect ratio"""
        map['surface'] = pg.transform.scale2x(map['surface'])
        map['rect'] = map['surface'].get_rect()

        return map


    def blit_tile_to_map(self, tile, row, column, map):
        """Places tile to map"""
        tile['rect'].x = column * 16
        tile['rect'].y = row * 16

        map['surface'].blit(tile['surface'], tile['rect'])


    def create_viewport(self):
        """Create the viewport to view the level through"""
        return setup.SCREEN.get_rect(bottom=self.town_map['rect'].bottom)


    def update(self, surface, keys, current_time):
        """Updates state"""
        self.keys = keys
        self.current_time = current_time
        surface.blit(self.town_map['surface'], (0,0), self.viewport)









