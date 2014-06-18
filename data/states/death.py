import copy, pickle, sys, os
import pygame as pg
from .. import setup, tools
from .. import observer
from ..components import person
from .. import constants as c

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    import cPickle
    pickle = cPickle


class Arrow(pg.sprite.Sprite):
    """
    Arrow to select restart or saved gamed.
    """
    def __init__(self, x, y):
        super(Arrow, self).__init__()
        self.image = setup.GFX['smallarrow']
        self.rect = self.image.get_rect(x=x,
                                        y=y)
        self.index = 0
        self.pos_list = [y, y+34]
        self.allow_input = False
        self.observers = [observer.SoundEffects()]
       
    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def update(self, keys):
        """
        Update arrow position.
        """
        if self.allow_input:
            if keys[pg.K_DOWN] and not keys[pg.K_UP] and self.index == 0:
                self.index = 1
                self.allow_input = False
                self.notify(c.CLICK)
            elif keys[pg.K_UP] and not keys[pg.K_DOWN] and self.index == 1:
                self.index = 0
                self.allow_input = False
                self.notify(c.CLICK)

            self.rect.y = self.pos_list[self.index]

        if not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


class DeathScene(tools._State):
    """
    Scene when the player has died.
    """
    def __init__(self):
        super(DeathScene, self).__init__()
        self.next = c.TOWN
        self.music = setup.MUSIC['shop_theme']
        self.volume = 0.5
        self.music_title = 'shop_theme'

    def startup(self, current_time, game_data):
        self.game_data = game_data
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.background = pg.Surface(setup.SCREEN_RECT.size)
        self.background.fill(c.BLACK_BLUE)
        self.player = person.Player('down', self.game_data, 1, 1, 'resting', 1)
        self.player.image = pg.transform.scale2x(self.player.image)
        self.player.rect = self.player.image.get_rect()
        self.player.rect.center = setup.SCREEN_RECT.center
        self.message_box = self.make_message_box()
        self.arrow = Arrow(300, 532)
        self.state_dict = self.make_state_dict()
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.name = c.DEATH_SCENE
        self.transition_surface = pg.Surface(setup.SCREEN_RECT.size)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)
        if not os.path.isfile("save.p"):
            game_data = tools.create_game_data_dict()
            pickle.dump(game_data, open("save.p", "wb"))
        self.observers = [observer.SoundEffects()]

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def make_message_box(self):
        """
        Make the text box informing of death.
        """
        box_image = setup.GFX['dialoguebox']
        box_rect = box_image.get_rect()
        text = 'You have died. Restart from last save point?'
        text_render = self.font.render(text, True, c.NEAR_BLACK) 
        text_rect = text_render.get_rect(centerx=box_rect.centerx,
                                         y=30)
        text2 = 'Yes'
        text2_render = self.font.render(text2, True, c.NEAR_BLACK)
        text2_rect = text2_render.get_rect(centerx=box_rect.centerx,
                                           y=70)

        text3 = 'No'
        text3_render = self.font.render(text3, True, c.NEAR_BLACK)
        text3_rect = text3_render.get_rect(centerx=box_rect.centerx,
                                           y=105)

        temp_surf = pg.Surface(box_rect.size)
        temp_surf.set_colorkey(c.BLACK)
        temp_surf.blit(box_image, box_rect)
        temp_surf.blit(text_render, text_rect)
        temp_surf.blit(text2_render, text2_rect)
        temp_surf.blit(text3_render, text3_rect)
        
        box_sprite = pg.sprite.Sprite()
        box_sprite.image = temp_surf
        box_sprite.rect = temp_surf.get_rect(bottom=608)
        
        return box_sprite

    def make_state_dict(self):
        """
        Make the dicitonary of state methods for the scene.
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

    def normal_update(self, keys):
        self.arrow.update(keys)
        self.check_for_input(keys)

    def check_for_input(self, keys):
        """
        Check if player wants to restart from last save point
        or just start from the beginning of the game.
        """
        if keys[pg.K_SPACE]:
            if self.arrow.index == 0:
                self.next = c.TOWN
                self.game_data = pickle.load(open("save.p", "rb"))
            elif self.arrow.index == 1:
                self.next = c.MAIN_MENU
            self.state = c.TRANSITION_OUT
            self.notify(c.CLICK2)

    def draw_level(self, surface):
        """
        Draw background, player, and message box.
        """
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.message_box.image, self.message_box.rect)
        surface.blit(self.arrow.image, self.arrow.rect)
        surface.blit(self.transition_surface, (0, 0))





        
