"""
This class controls the textbox GUI for any shop state.
A Gui object is created and updated by the shop state.
"""

import pygame as pg
from . import setup
from . components import textbox
from . import constants as c


class Gui(object):
    """Class that controls the GUI of the shop state"""
    def __init__(self, level):
        self.level = level
        self.sellable_items = level.sell_items
        self.player_inventory = level.game_data['player inventory']
        self.name = level.name
        self.state = 'dialogue'
        self.no_selling = ['Inn', 'Magic Shop']
        self.font = pg.font.Font(setup.FONTS['Fixedsys500c'], 22)
        self.index = 0
        self.timer = 0.0
        self.allow_input = False
        self.item = level.item
        self.item_to_be_sold = None
        self.dialogue = level.dialogue
        self.accept_dialogue = level.accept_dialogue
        self.accept_sale_dialogue = level.accept_sale_dialogue
        self.arrow = textbox.NextArrow()
        self.selection_arrow = textbox.NextArrow()
        self.arrow_pos1 = (50, 475)
        self.arrow_pos2 = (50, 515)
        self.arrow_pos3 = (50, 555)
        self.arrow_pos4 = (50, 495)
        self.arrow_pos5 = (50, 535)
        self.arrow_pos_list = [self.arrow_pos1, self.arrow_pos2, self.arrow_pos3]
        self.two_arrow_pos_list = [self.arrow_pos4, self.arrow_pos5]
        self.arrow_index = 0
        self.selection_arrow.rect.topleft = self.arrow_pos1
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)
        self.gold_box = self.make_gold_box()
        if self.name in self.no_selling:
            choices = self.item['dialogue']
        else:
            choices = ['Buy', 'Sell', 'Leave']
        self.selection_box = self.make_selection_box(choices)
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


    def make_selection_box(self, choices):
        """Make the box for the player to select options"""
        image = setup.GFX['shopbox']
        rect = image.get_rect(bottom=608)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))

        if len(choices) == 2:
            choice1 = self.font.render(choices[0], True, c.NEAR_BLACK)
            choice1_rect = choice1.get_rect(x=200, y=35)
            choice2 = self.font.render(choices[1], True, c.NEAR_BLACK)
            choice2_rect = choice2.get_rect(x=200, y=75)

            surface.blit(choice1, choice1_rect)
            surface.blit(choice2, choice2_rect)

        elif len(choices) == 3:
            choice1 = self.font.render(choices[0], True, c.NEAR_BLACK)
            choice1_rect = choice1.get_rect(x=200, y=15)
            choice2 = self.font.render(choices[1], True, c.NEAR_BLACK)
            choice2_rect = choice2.get_rect(x=200, y=55)
            choice3 = self.font.render(choices[2], True, c.NEAR_BLACK)
            choice3_rect = choice3.get_rect(x=200, y=95)

            surface.blit(choice1, choice1_rect)
            surface.blit(choice2, choice2_rect)
            surface.blit(choice3, choice3_rect)

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
        gold = self.player_inventory['gold']
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
                      'confirmpurchase': self.confirm_purchase,
                      'confirmsell': self.confirm_sell,
                      'reject': self.reject_insufficient_gold,
                      'accept': self.accept_purchase,
                      'acceptsell': self.accept_sale,
                      'hasitem': self.has_item,
                      'buysell': self.buy_sell,
                      'sell': self.sell_items,
                      'cantsell': self.cant_sell}

        return state_dict


    def control_dialogue(self, keys, current_time):
        """Control the dialogue boxes"""
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)

        if self.index < (len(self.dialogue) - 1) and self.allow_input:
            if keys[pg.K_SPACE]:
                self.index += 1
                self.allow_input = False

                if self.index == (len(self.dialogue) - 1):
                    self.state = self.begin_new_transaction()


        if not keys[pg.K_SPACE]:
            self.allow_input = True


    def make_selection(self, keys, current_time):
        """Control the selection"""
        choices = self.item['dialogue']
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)
        self.selection_box = self.make_selection_box(choices)
        self.gold_box = self.make_gold_box()

        self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]


        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(self.two_arrow_pos_list) - 1):
                self.arrow_index += 1
                self.allow_input = False
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.state = 'confirmpurchase'

            elif self.arrow_index == 1:
                if self.level.name in self.no_selling:
                    self.level.done = True
                    self.level.game_data['last direction'] = 'down'
                else:
                    self.state = 'buysell'

            self.arrow_index = 0
            self.allow_input = False

        if not keys[pg.K_SPACE] and not keys[pg.K_UP] and not keys[pg.K_DOWN]:
            self.allow_input = True



    def confirm_purchase(self, keys, current_time):
        """Confirm selection state for GUI"""
        dialogue = ['Are you sure?']
        choices = ['Yes', 'No']
        self.selection_box = self.make_selection_box(choices)
        self.gold_box = self.make_gold_box()
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.buy_item()
            elif self.arrow_index == 1:
                self.state = self.begin_new_transaction()
            self.arrow_index = 0
            self.allow_input = False

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


    def confirm_sell(self, keys, current_time):
        """Confirm player wants to sell item"""
        dialogue = ['Are you sure?']
        choices = ['Yes', 'No']
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_box = self.make_selection_box(choices)
        self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
        elif keys[pg.K_UP]:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.sell_item()
            elif self.arrow_index == 1:
                self.state = self.begin_new_transaction()
            self.allow_input = False
            self.arrow_index = 0

        if not keys[pg.K_SPACE] and not keys[pg.K_UP] and not keys[pg.K_DOWN]:
            self.allow_input = True


    def begin_new_transaction(self):
        """Set state to buysell or select, depending if the shop
        is a Inn/Magic shop or not"""
        if self.level.name in self.no_selling:
            state = 'select'
        else:
            state = 'buysell'

        return state
    
    
    def buy_item(self):
        """Attempt to allow player to purchase item"""
        self.player_inventory['gold'] -= self.item['price']
        
        if self.player_inventory['gold'] < 0:
            self.player_inventory['gold'] += self.item['price']
            self.state = 'reject'
        else:
            if (self.item['type'] == 'Fire Spell' and
                        'Fire Spell' in self.player_inventory):
                    self.state = 'hasitem'
                    self.player_inventory['gold'] += self.item['price']
            else:
                self.state = 'accept'
                self.add_player_item(self.item)


    def sell_item(self):
        """Allow player to sell item to shop"""
        self.player_inventory['gold'] += (self.item['price'] / 2)
        self.state = 'acceptsell'
        del self.player_inventory[self.item['type']]



    def accept_sale(self, keys, current_time):
        """Confirm to player that item was sold"""
        self.dialogue_box = self.make_dialogue_box(self.accept_sale_dialogue, 0)
        self.gold_box = self.make_gold_box()

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = self.begin_new_transaction()
            self.selection_arrow.rect.topleft = self.arrow_pos1
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True








    def reject_insufficient_gold(self, keys, current_time):
        """Reject player selection if they do not have enough gold"""
        dialogue = ["You don't have enough gold!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = self.begin_new_transaction()
            self.selection_arrow.rect.topleft = self.arrow_pos1
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True


    def accept_purchase(self, keys, current_time):
        """Accept purchase and confirm with message"""
        self.dialogue_box = self.make_dialogue_box(self.accept_dialogue, 0)
        self.gold_box = self.make_gold_box()

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = self.begin_new_transaction()
            self.selection_arrow.rect.topleft = self.arrow_pos1
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True


    def has_item(self, keys, current_time):
        """Tell player he has item already"""
        dialogue = ["You have that item already."]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = self.begin_new_transaction()
            self.selection_arrow.rect.topleft = self.arrow_pos1
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True


    def buy_sell(self, keys, current_time):
        """Ask player if they want to buy or sell something"""
        dialogue = ["Would you like to buy or sell an item?"]
        choices = ['Buy', 'Sell', 'Leave']
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_box = self.make_selection_box(choices)
        self.selection_arrow.rect.topleft = self.arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(self.arrow_pos_list) - 1):
                self.arrow_index += 1
                self.allow_input = False

        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.state = 'select'
                self.allow_input = False
                self.arrow_index = 0
            elif self.arrow_index == 1:
                if self.check_for_sellable_items():
                    self.state = 'sell'
                    self.allow_input = False
                    self.arrow_index = 0
                else:
                    self.state = 'cantsell'
                    self.allow_input = False
                    self.arrow_index = 0

            else:
                self.level.done = True
                self.level.game_data['last direction'] = 'down'

            self.arrow_index = 0

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


    def sell_items(self, keys, current_time):
        """Have player select items to sell"""
        dialogue = ["What would you like to sell?"]
        choices = [self.item_to_be_sold, 'Cancel']
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_box = self.make_selection_box(choices)
        self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(self.arrow_pos_list) - 1):
                self.arrow_index += 1
                self.allow_input = False
        elif keys[pg.K_UP]:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.state = 'confirmsell'
                self.allow_input = False
            else:
                self.state = 'buysell'
                self.allow_input = False
            self.arrow_index = 0

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


    def check_for_sellable_items(self):
        """Check for sellable items"""

        for item in self.player_inventory:
            if item in self.sellable_items:
                sell_price = self.player_inventory[item]['value'] / 2
                self.item_to_be_sold = item + " (" + str(sell_price) + " gold)"
                return True
        else:
            return False


    def cant_sell(self, keys, current_time):
        """Do not allow player to sell anything"""
        dialogue = ["You don't have anything to sell!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = 'buysell'
            self.allow_input = False


        if not keys[pg.K_SPACE]:
            self.allow_input = True




    def add_player_item(self, item):
        """Add item to player's inventory"""
        item_type = item['type']
        quantity = item['quantity']
        value = item['price']
        player_items = self.level.game_data['player inventory']

        item_to_add = {'quantity': quantity,
                       'value': value}

        if item_type in player_items:
            player_items[item_type]['quantity'] += quantity
        elif quantity > 0:
            player_items[item_type] = item_to_add




    def update(self, keys, current_time):
        """Updates the shop GUI"""
        state_function = self.state_dict[self.state]
        state_function(keys, current_time)


    def draw(self, surface):
        """Draw GUI to level surface"""
        state_list1 = ['dialogue', 'reject', 'accept', 'hasitem']
        state_list2 = ['select', 'confirmpurchase', 'buysell', 'sell', 'confirmsell']

        surface.blit(self.dialogue_box.image, self.dialogue_box.rect)
        surface.blit(self.gold_box.image, self.gold_box.rect)
        if self.state in state_list2:
            surface.blit(self.selection_box.image, self.selection_box.rect)
            surface.blit(self.selection_arrow.image, self.selection_arrow.rect)

