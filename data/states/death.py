import copy, pickle, sys
import pygame as pg
from .. import setup, tools
from ..components import person
from .. import constants as c

#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    import cPickle
    pickle = cPickle


class DeathScene(tools._State):
    """
    Scene when the player has died.
    """
    def __init__(self):
        super(DeathScene, self).__init__()
        self.next = c.TOWN
        self.music = None

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
        self.state_dict = self.make_state_dict()
        self.state = c.TRANSITION_IN
        self.alpha = 255
        self.name = c.DEATH_SCENE
        self.transition_surface = copy.copy(self.background)
        self.transition_surface.fill(c.BLACK_BLUE)
        self.transition_surface.set_alpha(self.alpha)

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

        temp_surf = pg.Surface(box_rect.size)
        temp_surf.set_colorkey(c.BLACK)
        temp_surf.blit(box_image, box_rect)
        temp_surf.blit(text_render, text_rect)
        
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

    def update(self, surface, *args):
        """
        Update scene.
        """
        update_level = self.state_dict[self.state]
        update_level()
        self.draw_level(surface)

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
            self.game_data = pickle.load(open("save.p", "rb"))
            self.game_data['last state'] = self.name
            self.done = True

    def normal_update(self):
        pass

    def draw_level(self, surface):
        """
        Draw background, player, and message box.
        """
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.image, self.player.rect)
        surface.blit(self.message_box.image, self.message_box.rect)





        
