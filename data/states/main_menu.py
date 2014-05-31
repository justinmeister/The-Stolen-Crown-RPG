import pygame as pg
from .. import setup, tools, tilerender
from .. import constants as c

class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()
        self.music = setup.MUSIC['kings_theme']
        pg.mixer.music.load(self.music)
        pg.mixer.music.set_volume(.4)
        pg.mixer.music.play(-1)
        self.next = c.INSTRUCTIONS
        self.tmx_map = setup.TMX['title']
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.title_box = setup.GFX['title_box']
        self.title_rect = self.title_box.get_rect()
        self.title_rect.midbottom = self.viewport.midbottom
        self.title_rect.y -= 30
        self.game_data = tools.create_game_data_dict()
        self.state_dict = self.make_state_dict()
        self.name = c.MAIN_MENU
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.transition_surface = pg.Surface(setup.SCREEN_RECT.size)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)

    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return setup.SCREEN.get_rect(bottomright=map_rect.bottomright)

    def make_state_dict(self):
        """
        Make the dictionary of state methods for the level.
        """
        state_dict = {c.TRANSITION_IN: self.transition_in,
                      c.TRANSITION_OUT: self.transition_out,
                      c.NORMAL: self.normal_update}

        return state_dict
        
    def update(self, surface, *args):
        """
        Update scene.
        """
        update_level = self.state_dict[self.state]
        update_level()
        self.draw_level(surface)

    def draw_level(self, surface):
        """
        Blit tmx map and title box onto screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.title_box, self.title_rect)
        surface.blit(self.level_surface, (0,0), self.viewport)
        surface.blit(self.transition_surface, (0,0))
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.state = c.TRANSITION_OUT

    def transition_in(self):
        """
        Transition into scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= c.TRANSITION_SPEED
        if self.alpha <= 0:
            self.alpha = 0
            self.state = c.NORMAL
        

    def transition_out(self):
        """
        Transition out of scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += c.TRANSITION_SPEED
        if self.alpha >= 255:
            self.game_data['last state'] = self.name
            self.done = True

    def normal_update(self):
        pass


class Instructions(tools._State):
    """
    Instructions page.
    """
    def __init__(self):
        super(Instructions, self).__init__()
        self.next = c.OVERWORLD
        self.tmx_map = setup.TMX['title']
        self.music = None

    def startup(self, *args):
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.title_box = setup.GFX['instructions_box']
        self.title_rect = self.title_box.get_rect()
        self.title_rect.midbottom = self.viewport.midbottom
        self.title_rect.y -= 30
        self.game_data = tools.create_game_data_dict()
        self.state_dict = self.make_state_dict()
        self.name = c.MAIN_MENU
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.transition_surface = pg.Surface(setup.SCREEN_RECT.size)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)

    def make_viewport(self, map_image):
        """
        Create the viewport to view the level through.
        """
        map_rect = map_image.get_rect()
        return setup.SCREEN.get_rect(bottomright=map_rect.bottomright)

    def make_state_dict(self):
        """
        Make the dictionary of state methods for the level.
        """
        state_dict = {c.TRANSITION_IN: self.transition_in,
                      c.TRANSITION_OUT: self.transition_out,
                      c.NORMAL: self.normal_update}

        return state_dict
        
    def update(self, surface, *args):
        """
        Update scene.
        """
        update_level = self.state_dict[self.state]
        update_level()
        self.draw_level(surface)

    def draw_level(self, surface):
        """
        Blit tmx map and title box onto screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.title_box, self.title_rect)
        surface.blit(self.level_surface, (0,0), self.viewport)
        surface.blit(self.transition_surface, (0,0))
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.state = c.TRANSITION_OUT

    def transition_in(self):
        """
        Transition into scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= c.TRANSITION_SPEED
        if self.alpha <= 0:
            self.alpha = 0
            self.state = c.NORMAL
        

    def transition_out(self):
        """
        Transition out of scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += c.TRANSITION_SPEED
        if self.alpha >= 255:
            self.game_data['last state'] = self.name
            self.done = True

    def normal_update(self):
        pass


