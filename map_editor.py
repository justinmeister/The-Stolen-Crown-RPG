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
        self.draw_sheet_names()
        self.button_rects = self.create_button_rects()
        


    def draw_sheet_names(self):
        sheet_list = ['tileset1',
                      'tileset2',
                      'tileset3']

        for i, sheet in enumerate(sheet_list):
            font_render = self.font.render(sheet, True, c.NEAR_BLACK)
            font_rect = font_render.get_rect(x=10, y=10+(i*50))
            self.image.blit(font_render, font_rect)




    def create_button_rects(self):
        rect_dict = {}

        for i in range(3):
            new_rect = pg.Rect(0, (i*50), 200, 50)
            rect_dict['rect'+str(i)] = new_rect

        return rect_dict


    def update(self):
        self.check_for_click(self.editor.click_point)


    def check_for_click(self, click_point):
        for rect in self.button_rects:
            if self.button_rects[rect].collidepoint(click_point):
                if self.editor.mouse_clicked:
                    self.rect_to_draw = self.button_rects[rect]
                    self.editor.mouse_clicked = False


    def draw(self, surface):
        """Draw box to surface"""
        surface.blit(self.image, self.rect)
        pg.draw.rect(surface, c.DARK_RED, self.rect_to_draw, 10)



class MapCreator(object):
    """A simple map tile editor"""
    def __init__(self):
        self.screen = self.setup_pygame()
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.fps = 60.0
        self.keys = pg.key.get_pressed()
        self.done = False
        self.mouse_click = False
        self.sheet_selector_box = SheetSelectorBox(self)


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
                self.mouse_click = True
                self.click_point = pg.mouse.get_pos()


    def update(self):
        self.sheet_selector_box.update()
        self.sheet_selector_box.draw(self.screen)


if __name__ == "__main__":
    map_creator = MapCreator()
    map_creator.main_loop()
    pg.quit()
    sys.exit()