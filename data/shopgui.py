"""
This class controls the textbox GUI for any shop state.
A Gui object is created and updated by the shop state.
"""
import sys
import pickle
import pygame as pg
from . import setup, observer
from . components import textbox
from . import constants as c


#Python 2/3 compatibility.
if sys.version_info[0] == 2:
    import cPickle
    pickle = cPickle 


class Gui(object):
    """Class that controls the GUI of the shop state"""
    def __init__(self, level):
        self.level = level
        self.game_data = self.level.game_data
        self.level.game_data['last direction'] = 'down'
        self.SFX_observer = observer.SoundEffects()
        self.observers = [self.SFX_observer]
        self.sellable_items = level.sell_items
        self.player_inventory = level.game_data['player inventory']
        self.name = level.name
        self.state = 'dialogue'
        self.no_selling = ['Inn', 'magic shop']
        self.weapon_list = ['Long Sword', 'Rapier']
        self.armor_list = ['Chain Mail', 'Wooden Shield']
        self.font = pg.font.Font(setup.FONTS[c.MAIN_FONT], 22)
        self.index = 0
        self.timer = 0.0
        self.allow_input = False
        self.items = level.items
        self.item_to_be_sold = None
        self.item_to_be_purchased = None
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
            choices = self.items[0]['dialogue']
        else:
            choices = ['Buy', 'Sell', 'Leave']
        self.selection_box = self.make_selection_box(choices)
        self.state_dict = self.make_state_dict()

    def notify(self, event):
        """
        Notify all observers of event.
        """
        for observer in self.observers:
            observer.on_notify(event)

    def make_dialogue_box(self, dialogue_list, index):
        """
        Make the sprite that controls the dialogue.
        """
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

    def check_to_draw_arrow(self, sprite):
        """
        Blink arrow if more text needs to be read.
        """
        if self.index < len(self.dialogue) - 1:
            sprite.image.blit(self.arrow.image, self.arrow.rect)

    def make_gold_box(self):
        """Make the box to display total gold"""
        image = setup.GFX['goldbox']
        rect = image.get_rect(bottom=608, right=800)

        surface = pg.Surface(rect.size)
        surface.set_colorkey(c.BLACK)
        surface.blit(image, (0, 0))
        gold = self.player_inventory['GOLD']['quantity']
        text = 'Gold: ' + str(gold)
        text_render = self.font.render(text, True, c.NEAR_BLACK)
        text_rect = text_render.get_rect(x=80, y=60)

        surface.blit(text_render, text_rect)

        sprite = pg.sprite.Sprite()
        sprite.image = surface
        sprite.rect = rect

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
                      'cantsell': self.cant_sell,
                      'cantsellequippedweapon': self.cant_sell_equipped_weapon,
                      'cantsellequippedarmor': self.cant_sell_equipped_armor}

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
                self.notify(c.CLICK2)

        if not keys[pg.K_SPACE]:
            self.allow_input = True

    def begin_new_transaction(self):
        """Set state to buysell or select, depending if the shop
        is a Inn/Magic shop or not"""
        if self.level.name in self.no_selling:
            state = 'select'
        else:
            state = 'buysell'

        return state

    def make_selection(self, keys, current_time):
        """Control the selection"""
        choices = []
        for item in self.items:
            choices.append(item['dialogue'])
        if self.name in self.no_selling:
            choices.append('Leave')
        else:
            choices.append('Cancel')
        self.dialogue_box = self.make_dialogue_box(self.dialogue, self.index)
        self.selection_box = self.make_selection_box(choices)
        self.gold_box = self.make_gold_box()

        if len(choices) == 2:
            arrow_list = self.two_arrow_pos_list
        elif len(choices) == 3:
            arrow_list = self.arrow_pos_list
        else:
            arrow_list = None
            AssertionError('Only two items supported')

        self.selection_arrow.rect.topleft = arrow_list[self.arrow_index]


        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.state = 'confirmpurchase'
                self.item_to_be_purchased = self.items[0]

            elif self.arrow_index == 1 and len(choices) == 3:
                self.state = 'confirmpurchase'
                self.item_to_be_purchased = self.items[1]

            else:
                if self.level.name in self.no_selling:
                    self.level.state = 'transition out'
                    self.game_data['last state'] = self.level.name
                else:
                    self.state = 'buysell'

            self.notify(c.CLICK2)
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
                self.notify(c.CLICK)
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.buy_item()
            elif self.arrow_index == 1:
                self.state = self.begin_new_transaction()
            self.notify(c.CLICK2)
            self.arrow_index = 0
            self.allow_input = False

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


    def buy_item(self):
        """Attempt to allow player to purchase item"""
        item = self.item_to_be_purchased

        self.player_inventory['GOLD']['quantity'] -= item['price']

        if self.player_inventory['GOLD']['quantity'] < 0:
            self.player_inventory['GOLD']['quantity'] += item['price']
            self.state = 'reject'
        else:
            if (item['type'] in self.player_inventory and
                        not self.name == c.POTION_SHOP):
                self.state = 'hasitem'
                self.player_inventory['GOLD']['quantity'] += item['price']
            else:
                self.notify(c.CLOTH_BELT)
                self.state = 'accept'
                self.add_player_item(item)


    def add_player_item(self, item):
        """
        Add item to player's inventory.
        """
        item_type = item['type']
        quantity = item['quantity']
        value = item['price']
        power = item['power']
        magic_list = ['Cure', 'Fire Blast']
        player_armor = ['Chain Mail', 'Wooden Shield']
        player_weapons = ['Rapier', 'Long Sword']
        player_items = self.level.game_data['player inventory']
        player_health = self.level.game_data['player stats']['health']
        player_magic = self.level.game_data['player stats']['magic']
        equipped_armor = self.level.game_data['player inventory']['equipped armor']

        item_to_add = {'quantity': quantity,
                       'value': value,
                       'power': power}

        if item_type in magic_list:
            item_to_add = {'magic points': item['magic points'],
                           'power': item['power']}
            player_items[item_type] = item_to_add
        if item_type in player_armor:
            equipped_armor.append(item_type)
        if item_type in player_weapons:
            player_items['equipped weapon'] = item_type
        if item_type in player_items and item_type not in magic_list:
            player_items[item_type]['quantity'] += quantity
        elif quantity > 0:
            player_items[item_type] = item_to_add
        elif item_type == 'room':
            player_health['current'] = player_health['maximum']
            player_magic['current'] = player_magic['maximum']
            pickle.dump(self.game_data, open( "save.p", "wb"))

    def confirm_sell(self, keys, current_time):
        """
        Confirm player wants to sell item.
        """
        dialogue = ['Are you sure?']
        choices = ['Yes', 'No']
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_box = self.make_selection_box(choices)
        self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.sell_item_from_inventory()
            elif self.arrow_index == 1:
                self.state = self.begin_new_transaction()
                self.notify(c.CLICK2)
            self.allow_input = False
            self.arrow_index = 0

        if not keys[pg.K_SPACE] and not keys[pg.K_UP] and not keys[pg.K_DOWN]:
            self.allow_input = True


    def sell_item_from_inventory(self):
        """
        Allow player to sell item to shop.
        """
        item_price = self.item_to_be_sold['price']
        item_name = self.item_to_be_sold['type']

        if item_name in self.weapon_list:
            if item_name == self.game_data['player inventory']['equipped weapon']:
                self.state = 'cantsellequippedweapon'
            else:
                self.notify(c.CLOTH_BELT)
                self.sell_inventory_data_adjust(item_price, item_name)

        elif item_name in self.armor_list:
            if item_name in self.game_data['player inventory']['equipped armor']:
                self.state = 'cantsellequippedarmor'
            else:
                self.notify(c.CLOTH_BELT)
                self.sell_inventory_data_adjust(item_price, item_name)
        else:
            self.notify(c.CLOTH_BELT)
            self.sell_inventory_data_adjust(item_price, item_name)

    def sell_inventory_data_adjust(self, item_price, item_name):
        """
        Add gold and subtract item during sale.
        """
        self.player_inventory['GOLD']['quantity'] += (item_price / 2)
        self.state = 'acceptsell'
        if self.player_inventory[item_name]['quantity'] > 1:
            self.player_inventory[item_name]['quantity'] -= 1
        else:
            del self.player_inventory[self.item_to_be_sold['type']]

    def reject_insufficient_gold(self, keys, current_time):
        """Reject player selection if they do not have enough gold"""
        dialogue = ["You don't have enough gold!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.notify(c.CLICK2)
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
            self.notify(c.CLICK2)
            self.state = self.begin_new_transaction()
            self.selection_arrow.rect.topleft = self.arrow_pos1
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True

    def accept_sale(self, keys, current_time):
        """Confirm to player that item was sold"""
        self.dialogue_box = self.make_dialogue_box(self.accept_sale_dialogue, 0)
        self.gold_box = self.make_gold_box()

        if keys[pg.K_SPACE] and self.allow_input:
            self.notify(c.CLICK2)
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
            self.notify(c.CLICK2)

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
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
                self.notify(c.CLICK)

        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
                self.notify(c.CLICK)
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
                self.level.state = 'transition out'
                self.game_data['last state'] = self.level.name

            self.arrow_index = 0
            self.notify(c.CLICK2)

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True

    def check_for_sellable_items(self):
        """Check for sellable items"""
        for item in self.player_inventory:
            if item in self.sellable_items:
                return True
        else:
            return False

    def sell_items(self, keys, current_time):
        """Have player select items to sell"""
        dialogue = ["What would you like to sell?"]
        choices = []
        item_list = []
        for item in self.items:
            if item['type'] in self.player_inventory:
                name = item['type']
                price = " (" + str(item['price'] / 2) + " gold)"
                choices.append(name + price)
                item_list.append(name)
        choices.append('Cancel')
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)
        self.selection_box = self.make_selection_box(choices)

        if len(choices) == 2:
            self.selection_arrow.rect.topleft = self.two_arrow_pos_list[self.arrow_index]
        elif len(choices) == 3:
            self.selection_arrow.rect.topleft = self.arrow_pos_list[self.arrow_index]

        if keys[pg.K_DOWN] and self.allow_input:
            if self.arrow_index < (len(choices) - 1):
                self.arrow_index += 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_UP] and self.allow_input:
            if self.arrow_index > 0:
                self.arrow_index -= 1
                self.allow_input = False
                self.notify(c.CLICK)
        elif keys[pg.K_SPACE] and self.allow_input:
            if self.arrow_index == 0:
                self.state = 'confirmsell'
                self.allow_input = False
                for item in self.items:
                    if item['type'] == item_list[0]:
                        self.item_to_be_sold = item

            elif self.arrow_index == 1 and len(choices) == 3:
                self.state = 'confirmsell'
                self.allow_input = False
                for item in self.items:
                    if item['type'] == item_list[1]:
                        self.item_to_be_sold = item
            else:
                self.state = 'buysell'
                self.allow_input = False
            self.arrow_index = 0
            self.notify(c.CLICK2)

        if not keys[pg.K_SPACE] and not keys[pg.K_DOWN] and not keys[pg.K_UP]:
            self.allow_input = True


    def cant_sell(self, keys, current_time):
        """Do not allow player to sell anything"""
        dialogue = ["You don't have anything to sell!"]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = 'buysell'
            self.allow_input = False
            self.notify(c.CLICK2)


        if not keys[pg.K_SPACE]:
            self.allow_input = True

    def cant_sell_equipped_weapon(self, keys, *args):
        """
        Do not sell weapon the player has equipped.
        """
        dialogue = ["You can't sell an equipped weapon."]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = 'buysell'
            self.allow_input = False
            self.notify(c.CLICK2)

        if not keys[pg.K_SPACE]:
            self.allow_input = True

    def cant_sell_equipped_armor(self, keys, *args):
        """
        Do not sell armor the player has equipped.
        """
        dialogue = ["You can't sell equipped armor."]
        self.dialogue_box = self.make_dialogue_box(dialogue, 0)

        if keys[pg.K_SPACE] and self.allow_input:
            self.state = 'buysell'
            self.allow_input = False

        if not keys[pg.K_SPACE]:
            self.allow_input = True



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

