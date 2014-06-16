import pickle, sys, os
import pygame as pg
from .. import setup, tools, tilerender
from .. import observer
from .. import constants as c
import death
 

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    import cPickle
    pickle = cPickle 


class Menu(tools._State):
    def __init__(self):
        super(Menu, self).__init__()
        self.music = setup.MUSIC['kings_theme']
        self.music_title = 'kings_theme'
        self.volume = 0.4
        self.next = c.INSTRUCTIONS
        self.tmx_map = setup.TMX['title']
        self.name = c.MAIN_MENU
        self.startup(0, 0)
    
    def startup(self, *args):
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.title_box = setup.GFX['title_box']
        self.title_rect = self.title_box.get_rect()
        self.title_rect.midbottom = self.viewport.midbottom
        self.title_rect.y -= 30
        self.state_dict = self.make_state_dict()
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
            self.done = True

    def normal_update(self):
        pass


class Instructions(tools._State):
    """
    Instructions page.
    """
    def __init__(self):
        super(Instructions, self).__init__()
        self.tmx_map = setup.TMX['title']
        self.music = None
        self.music_title = None
        
    def startup(self, *args):
        self.renderer = tilerender.Renderer(self.tmx_map)
        self.map_image = self.renderer.make_2x_map()
        self.map_rect = self.map_image.get_rect()
        self.viewport = self.make_viewport(self.map_image)
        self.level_surface = pg.Surface(self.map_rect.size)
        self.title_box = self.set_image()
        self.title_rect = self.title_box.get_rect()
        self.title_rect.midbottom = self.viewport.midbottom
        self.title_rect.y -= 30
        self.game_data = tools.create_game_data_dict()
        self.next = self.set_next_scene()
        self.state_dict = self.make_state_dict()
        self.name = c.MAIN_MENU
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.transition_surface = pg.Surface(setup.SCREEN_RECT.size)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)
        self.observers = [observer.SoundEffects()]

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def set_next_scene(self):
        """
        Check if there is a saved game. If not, start
        game at begining.  Otherwise go to load game scene.
        """
        if not os.path.isfile("save.p"):
            next_scene = c.OVERWORLD
        else:
            next_scene = c.LOADGAME

        return next_scene

    def set_image(self):
        """
        Set image for message box.
        """
        return setup.GFX['instructions_box']

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
        
    def update(self, surface, keys, *args):
        """
        Update scene.
        """
        update_level = self.state_dict[self.state]
        update_level(keys)
        self.draw_level(surface)

    def draw_level(self, surface):
        """
        Blit tmx map and title box onto screen.
        """
        self.level_surface.blit(self.map_image, self.viewport, self.viewport)
        self.level_surface.blit(self.title_box, self.title_rect)
        self.draw_arrow()
        surface.blit(self.level_surface, (0,0), self.viewport)
        surface.blit(self.transition_surface, (0,0))

    def draw_arrow(self):
        pass
        
    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            self.state = c.TRANSITION_OUT

    def transition_in(self, *args):
        """
        Transition into scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha -= c.TRANSITION_SPEED
        if self.alpha <= 0:
            self.alpha = 0
            self.state = c.NORMAL

    def transition_out(self, *args):
        """
        Transition out of scene with a fade.
        """
        self.transition_surface.set_alpha(self.alpha)
        self.alpha += c.TRANSITION_SPEED
        if self.alpha >= 255:
            self.done = True

    def normal_update(self, *args):
        pass


class LoadGame(Instructions):
    def __init__(self):
        super(LoadGame, self).__init__()
        self.arrow = death.Arrow(200, 260)
        self.arrow.pos_list[1] += 34
        self.allow_input = False

    def set_image(self):
        """
        Set image for message box.
        """
        return setup.GFX['loadgamebox']

    def draw_arrow(self):
        self.level_surface.blit(self.arrow.image, self.arrow.rect)

    def get_event(self, event):
        pass
    
    def normal_update(self, keys):
        if self.allow_input:
            if keys[pg.K_DOWN] and self.arrow.index == 0:
                self.arrow.index = 1
                self.notify(c.CLICK)
                self.allow_input = False
            elif keys[pg.K_UP] and self.arrow.index == 1:
                self.arrow.index = 0
                self.notify(c.CLICK)
                self.allow_input = False
            elif keys[pg.K_SPACE]:
                if self.arrow.index == 0:
                    self.game_data = pickle.load(open("save.p", "rb"))
                    self.next = c.TOWN
                    self.state = c.TRANSITION_OUT
                else:
                    self.next = c.OVERWORLD
                    self.state = c.TRANSITION_OUT
                self.notify(c.CLICK2)

            self.arrow.rect.y = self.arrow.pos_list[self.arrow.index]  

        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True

        


