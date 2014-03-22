"""
This class is the parent class of all shop states.
This includes weapon, armour, magic and potion shops.
It also includes the inn.  These states are scaled
twice as big as a level state.
"""
import copy
import pygame as pg
from .. import tools, setup
from .. import constants as c
from .. components import textbox, person


class Gui(object):
    """Class that controls the GUI of the shop state"""
    def __init__(self, name, dialogue, level):
        self.level = level
        self.name = name
        self.state = 'dialogue'
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.index = 0
        self.timer = 0.0
        self.dialogue = dialogue
        self.arrow = textbox.NextArrow()
        self.selection_arrow = textbox.NextArrow()
        self.arrow_pos1 = (50, 485)
        self.arrow_pos2 = (50, 535)
        self.selection_arrow.rect.topleft = self.arrow_pos1
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)
        self.gold_box = self.make_gold_box()
        self.selection_box = self.make_selection_box()
        self.state_dict = self.make_state_dict()


    def make_dialogue_box(self, dialogue_list, index):
        """Make the sprite that controls the dialogue"""
        image = setup.GFX['dialoguebox']
        rect = image.get_rect()
        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, rect)
        dialogue = self.font.render(dialogue_list[index],
                                    True,
                                    c.NEAR_BLACK)
        dialogue_rect = dialogue.get_rect(left=50, top=50)
        surface.blit(dialogue, dialogue_rect)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect
        self.check_to_draw_arrow(sprite)

        return sprite


    def make_selection_box(self):
        """Make the box for the player to select options"""
        image = setup.GFX['shopbox']
        rect = image.get_rect(bottom=608)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))
        if self.state == 'select':
            choices = ['Rent a room. (30 Gold)',
                       'Leave.']
        elif self.state == 'confirm':
            choices = ['Yes',
                       'No']
        else:
            choices = ['Not',
                       'assigned']
        choice1 = self.font.render(choices[0], True, c.NEAR_BLACK)
        choice1_rect = choice1.get_rect(x=200, y=25)
        choice2 = self.font.render(choices[1], True, c.NEAR_BLACK)
        choice2_rect = choice2.get_rect(x=200, y=75)
        surface.blit(choice1, choice1_rect)
        surface.blit(choice2, choice2_rect)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def check_to_draw_arrow(self, sprite):
        """Blink arrow if more text needs to be read"""
        if self.index < len(self.dialogue) - 1:
            sprite.image.blit(self.arrow.image, self.arrow.rect)


    def make_gold_box(self):
        """Make the box to display total gold"""
        image = setup.GFX['goldbox']
        rect = image.get_rect(bottom=608, right=800)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))
        gold = self.level.game_data['player items']['gold']
        text = 'Gold: ' + str(gold)
        text_render = self.font.render(text, True, c.NEAR_BLACK)
        text_rect = text_render.get_rect(x=80, y=60)

        surface.blit(text_render, text_rect)

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite



    def make_state_dict(self):
        """Make the state dictionary for the GUI behavior"""
        state_dict = {'dialogue': self.control_dialogue,
                      'select': self.make_selection,
                      'confirm': self.confirm_selection,
                      'reject': self.reject_insufficient_gold,
                      'accept': self.accept_purchase}

        return state_dict


    def control_dialogue(self, keys, current_time):
        """Control the dialogue boxes"""
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)

        if self.index < (len(self.dialogue) - 1):
            if keys[pg.K_SPACE]:
                self.index += 1

        elif self.index == (len(self.dialogue) - 1):
            self.state = 'select'
            self.timer = current_time


    def make_selection(self, keys, current_time):
        """Control the selection"""
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)
        self.selection_box = self.make_selection_box()
        self.gold_box = self.make_gold_box()

        if keys[pg.K_DOWN]:
            self.selection_arrow.rect.topleft = self.arrow_pos2
        elif keys[pg.K_UP]:
            self.selection_arrow.rect.topleft = self.arrow_pos1
        elif keys[pg.K_SPACE] and (current_time - self.timer) > 200:
            if self.selection_arrow.rect.topleft == self.arrow_pos2:
                self.level.done = True
                self.level.game_data['last direction'] = 'down'
            elif self.selection_arrow.rect.topleft == self.arrow_pos1:
                self.state = 'confirm'
                self.timer = current_time



    def confirm_selection(self, keys, current_time):
        """Confirm selection state for GUI"""
        dialogue = ['Are you sure?']
        self.selection_box = self.make_selection_box()
        self.gold_box = self.make_gold_box()
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_DOWN]:
            self.selection_arrow.rect.topleft = self.arrow_pos2
        elif keys[pg.K_UP]:
            self.selection_arrow.rect.topleft = self.arrow_pos1
        elif keys[pg.K_SPACE] and (current_time - self.timer) > 200:
            if self.selection_arrow.rect.topleft == self.arrow_pos1:
                self.level.game_data['player items']['gold'] -= 30
                if self.level.game_data['player items']['gold'] < 0:
                    self.level.game_data['player items']['gold'] += 30
                    self.state = 'reject'
                else:
                    self.state = 'accept'
            else:
                self.state = 'select'
            self.timer = current_time
            self.selection_arrow.rect.topleft = self.arrow_pos1


    def reject_insufficient_gold(self, keys, current_time):
        """Reject player selection if they do not have enough gold"""
        dialogue = ["You don't have enough gold!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and (current_time - self.timer) > 200:
            self.state = 'select'
            self.timer = current_time
            self.selection_arrow.rect.topleft = self.arrow_pos1


    def accept_purchase(self, keys, current_time):
        """Accept purchase and confirm with message"""
        dialogue = ["Your health has been restored!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.gold_box = self.make_gold_box()

        if keys[pg.K_SPACE] and (current_time - self.timer) > 200:
            self.state = 'select'
            self.timer = current_time
            self.selection_arrow.rect.topleft = self.arrow_pos1


    def update(self, keys, current_time):
        """Updates the shop GUI"""
        state_function = self.state_dict[self.state]
        state_function(keys, current_time)


    def draw(self, surface):
        """Draw GUI to level surface"""
        state_list1 = ['dialogue', 'reject', 'accept']
        state_list2 = ['select', 'confirm']

        if self.state in state_list1:
            surface.blit(self.dialogue_box.image, self.dialogue_box.rect)
            surface.blit(self.gold_box.image, self.gold_box.rect)
        elif self.state in state_list2:
            surface.blit(self.dialogue_box.image, self.dialogue_box.rect)
            surface.blit(self.selection_box.image, self.selection_box.rect)
            surface.blit(self.selection_arrow.image, self.selection_arrow.rect)
            surface.blit(self.gold_box.image, self.gold_box.rect)




class Shop(tools._State):
    """Basic shop state"""
    def __init__(self, name):
        super(Shop, self).__init__(name)
        self.map_width = 13
        self.map_height = 10

    def startup(self, current_time, game_data):
        """Startup state"""
        self.game_data = game_data
        self.current_time = current_time
        self.state = 'normal'
        self.get_image = tools.get_image
        self.dialogue = self.make_dialogue()
        self.background = self.make_background()
        self.gui = Gui('Inn', self.dialogue, self)


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        dialogue = ["Welcome to the " + self.name + "!",
                    "Would you like to rent a room to restore your health?"]

        return dialogue



    def make_background(self):
        """Make the level surface"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()

        player = self.make_sprite('player', 96, 32, 150)
        shop_owner = self.make_sprite('man1', 32, 32, 600)
        counter = self.make_counter()

        background.image.blit(player.image, player.rect)
        background.image.blit(shop_owner.image, shop_owner.rect)
        background.image.blit(counter.image, counter.rect)

        return background


    def make_sprite(self, key, coordx, coordy, x, y=304):
        """Get the image for the player"""
        spritesheet = setup.GFX[key]
        surface = pg.Surface((32, 32))
        surface.set_colorkey(c.BLACK)
        image = self.get_image(coordx, coordy, 32, 32, spritesheet)
        rect = image.get_rect()
        surface.blit(image, rect)

        surface = pg.transform.scale(surface, (96, 96))
        rect = surface.get_rect(left=x, centery=y)
        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

        return sprite


    def make_counter(self):
        """Make the counter to conduct business"""
        sprite_sheet = copy.copy(setup.GFX['house'])
        sprite = pg.sprite.Sprite()
        sprite.image = self.get_image(102, 64, 26, 82, sprite_sheet)
        sprite.image = pg.transform.scale2x(sprite.image)
        sprite.rect = sprite.image.get_rect(left=550, top=225)

        return sprite




    def update(self, surface, keys, current_time):
        """Update level state"""
        self.gui.update(keys, current_time)
        self.draw_level(surface)
        if self.done:
            self.next = c.TOWN


    def draw_level(self, surface):
        """Blit graphics to game surface"""
        surface.blit(self.background.image, self.background.rect)
        self.gui.draw(surface)