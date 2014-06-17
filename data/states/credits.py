import pygame as pg
from .. import tools, setup
from .. import constants as c


class CreditEntry(object):
    """
    The text for each credit for the game.
    """
    def __init__(self):
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.credit_sprites = self.make_credits()
        self.index = 0
        self.current_credit = self.credit_sprites[self.index]
        self.state_dict = self.make_state_dict()
        self.state = c.TRANSITION_IN
        self.alpha = 0
        self.timer = 0.0

    def make_credits(self):
        """
        Make a list of lists for all the credit surfaces.
        """
        credits = [['PROGRAMMING AND GAME DESIGN', 'Justin Armstrong'],
                   ['ART', 'John Smith'],
                   ['MUSIC', 'John Smith'],
                   ['SPECIAL THANKS', '/r/pygame']]
        
        credit_sprites = []

        for credit in credits:
            subcredit_list = []
            for i, subcredit in enumerate(credit):
                text_sprite = pg.sprite.Sprite()
                text_sprite.image = self.font.render(subcredit, True, c.WHITE)
                text_sprite.rect = text_sprite.image.get_rect(centerx = 400,
                                                              y=300+(i*50))
                subcredit_list.append(text_sprite)
            credit_sprites.append(subcredit_list)
        
        return credit_sprites

    def make_state_dict(self):
        """
        Make the dictionary of state methods used to update credit.
        """
        state_dict = {c.TRANSITION_IN: self.transition_in, 
                      c.TRANSITION_OUT: self.transition_out,
                      c.NORMAL: self.normal_update}

        return state_dict

    def transition_in(self):
        for credit in self.current_credit:
            credit.image.set_alpha(self.alpha)

        self.alpha += c.TRANSITION_SPEED
        if self.alpha >= 255:
            self.alpha = 255
            self.state = c.NORMAL
            self.timer = self.current_time

    def transition_out(self):
        for credit in self.current_credit:
            credit.image.set_alpha(self.alpha)
        self.alpha -= c.TRANSITION_SPEED
        if self.alpha <= 0:
            self.alpha = 0
            self.index += 1
            self.current_credit = self.credit_sprites[self.index]
            self.state = c.TRANSITION_IN

    def normal_update(self):
        if (self.current_time - self.timer) > 5000:
            self.state = c.TRANSITION_OUT

    def update(self, surface, current_time, *args):
        self.current_time = current_time
        update_method = self.state_dict[self.state]
        update()

    def draw(self, surface):
        """
        Draw the current credit to main surface.
        """
        for credit_sprite in self.current_credit:
            surface.blit(credit_sprite.image, credit_sprite.rect)


class Credits(tools._state):
    """
    End Credits Scene.
    """
    def __init__(self):
        super(Credits, self).__init__()
        self.name = c.CREDITS
        self.music_title = None
        self.previous_music = None
        self.music = None
        self.volume = None
        self.credit = None
    
    def startup(self, current_time, game_data):
        """
        Initialize data at scene start. 
        """
        self.game_data = game_data
        self.music = setup.MUSIC['overworld']
        self.volume = 0.4
        self.current_time = current_time
        self.background = pg.Surface(setup.SCREEN_RECT.size)
        self.background.fill(c.BLACKBLUE)
        self.credit = CreditEntry()

    def update(self, surface, current_time, *args):
        """
        Update scene.
        """
        self.credit.update(current_time)
        self.draw_scene(surface)

    def draw_scene(self, surface):
        """
        Draw all graphics to the window surface.
        """
        surface.blit(self.background, (0, 0))
        self.credit.draw(surface)
        
    

