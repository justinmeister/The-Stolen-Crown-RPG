__author__ = 'justinarmstrong'

"""
This module initializes the display and
creates dictionaries of resources.
"""

import os
import pygame as pg
from . import tools
from . import constants as c

GAME = 'BEGIN GAME'

ORIGINAL_CAPTION = 'The Stolen Crown'

os.environ['SDL_VIDEO_CENTERED'] = '1'
pg.init()
pg.event.set_allowed([pg.KEYDOWN, pg.KEYUP, pg.QUIT])
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode((800, 608))
SCREEN_RECT = SCREEN.get_rect()

FONTS = tools.load_all_fonts(os.path.join('resources', 'fonts'))
MUSIC = tools.load_all_music(os.path.join('resources', 'music'))
GFX = tools.load_all_gfx(os.path.join('resources', 'graphics'))
SFX = tools.load_all_sfx(os.path.join('resources', 'sound'))
TMX = tools.load_all_tmx(os.path.join('resources', 'tmx'))

FONT = pg.font.Font(FONTS['Fixedsys500c'], 20)



