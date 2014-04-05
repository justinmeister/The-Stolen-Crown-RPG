"""Basic map editor that creates a .txt file to work with my
tilemap module. Probably not the best way to do it."""

import os
import sys
import pygame as pg

from data import constants as c
from data import setup


class SheetSelectorBox(object):
    """The box to choose which sprite sheet to work with"""
    def __init__(self, editor):
        self.image = pg.Surface((200, 750))
        self.image.fill(c.WHITE)
        self.rect = self.image.get_rect()
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.editor = editor
        self.rect_dict = self.make_rect_dict()
        self.rect_to_draw = self.rect_dict['tileset1']
        self.draw_sheet_names()

    def make_rect_dict(self):
        sheet_list = ['tileset1',
                      'tileset2',
                      'tileset3']
        rect_list = [pg.Rect(0, (i*50), 190, 50) for i in range(3)]

        return dict(zip(sheet_list, rect_list))


    def draw_sheet_names(self):
        sheet_list = ['tileset1',
                      'tileset2',
                      'tileset3']

        for i, sheet in enumerate(sheet_list):
            font_render = self.font.render(sheet, True, c.NEAR_BLACK)
            font_rect = font_render.get_rect(x=10, y=10+(i*50))
            self.image.blit(font_render, font_rect)

    def update(self):
        self.check_for_click(self.editor.click_point)

    def check_for_click(self, click_point):
        if click_point:
            for key in self.rect_dict:
                if self.rect_dict[key].collidepoint(click_point):
                    if self.editor.mouse_clicked:
                        self.rect_to_draw = self.rect_dict[key]
                        self.tileset_selected = key
                        self.editor.mouse_clicked = False

    def draw(self, surface):
        """Draw box to surface"""
        surface.blit(self.image, self.rect)
        if self.rect_to_draw:
            pg.draw.rect(surface, c.DARK_RED, self.rect_to_draw, 10)


class SpriteSheetDisplay(pg.sprite.Sprite):
    def __init__(self, selector):
        self.image = setup.GFX['tileset1']
        self.rect = self.image.get_rect(x=200)

    def update(self):
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)



class MapCreator(object):
    """A simple map tile editor"""
    def __init__(self):
        self.dimensions = sys.argv[-1]
        self.screen = self.setup_pygame()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.mouse_clicked = False
        self.click_point = None
        self.sheet_selector_box = SheetSelectorBox(self)
        self.spritesheet_display = SpriteSheetDisplay(self.sheet_selector_box)


    def setup_pygame(self):
        """Set up pygame and return the main surface"""
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        pg.init()
        pg.display.set_mode((1100, 750))
        surface = pg.display.get_surface()
        surface.fill(c.BLACK_BLUE)

        return surface

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            pg.display.update()
            self.clock.tick(self.fps)

    def event_loop(self):
        for event in pg.event.get():
            self.keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
                self.done = True
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.mouse_clicked = True
                self.click_point = pg.mouse.get_pos()

    def update(self):
        self.sheet_selector_box.update()
        self.sheet_selector_box.draw(self.screen)
        self.spritesheet_display.draw(self.screen)


if __name__ == "__main__":
    map_creator = MapCreator()
    map_creator.main_loop()
    pg.quit()
    sys.exit()