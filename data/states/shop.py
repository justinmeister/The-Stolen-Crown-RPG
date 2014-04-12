"""
This class is the parent class of all shop states.
This includes weapon, armour, magic and potion shops.
It also includes the inn.  These states are scaled
twice as big as a level state. The self.gui controls
all the textboxes.
"""

import copy
import pygame as pg
from .. import tools, setup, shopgui
from .. import constants as c


class Shop(tools._State):
    """Basic shop state"""
    def __init__(self):
        super(Shop, self).__init__()
        self.key = None
        self.sell_items = None

    def startup(self, current_time, game_data):
        """Startup state"""
        self.game_data = game_data
        self.current_time = current_time
        self.state = 'normal'
        self.next = c.TOWN
        self.get_image = tools.get_image
        self.dialogue = self.make_dialogue()
        self.accept_dialogue = self.make_accept_dialogue()
        self.accept_sale_dialogue = self.make_accept_sale_dialogue()
        self.items = self.make_purchasable_items()
        self.background = self.make_background()
        self.gui = shopgui.Gui(self)


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        raise NotImplementedError


    def make_accept_dialogue(self):
        """Make the dialogue for when the player buys an item"""
        return ['Item purchased.']


    def make_accept_sale_dialogue(self):
        """Make the dialogue for when the player sells an item"""
        return ['Item sold.']


    def make_purchasable_items(self):
        """Make the list of items to be bought at shop"""
        raise NotImplementedError


    def make_background(self):
        """Make the level surface"""
        background = pg.sprite.Sprite()
        surface = pg.Surface(c.SCREEN_SIZE).convert()
        surface.fill(c.BLACK_BLUE)
        background.image = surface
        background.rect = background.image.get_rect()

        player = self.make_sprite('player', 96, 32, 150)
        shop_owner = self.make_sprite(self.key, 32, 32, 600)
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


    def draw_level(self, surface):
        """Blit graphics to game surface"""
        surface.blit(self.background.image, self.background.rect)
        self.gui.draw(surface)



class Inn(Shop):
    """Where our hero gets rest"""
    def __init__(self):
        super(Inn, self).__init__()
        self.name = c.INN
        self.key = 'innman'

    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        return ["Welcome to the " + self.name + "!",
                "Would you like a room to restore your health?"]


    def make_accept_dialogue(self):
        """Make the dialogue for when the player buys an item"""
        return ['Your health has been replenished!']


    def make_purchasable_items(self):
        """Make list of items to be chosen"""
        dialogue = 'Rent a room (30 gold)'

        item = {'type': 'room',
                'price': 30,
                'quantity': 0,
                'dialogue': dialogue}

        return [item]



class WeaponShop(Shop):
    """A place to buy weapons"""
    def __init__(self):
        super(WeaponShop, self).__init__()
        self.name = c.WEAPON_SHOP
        self.key = 'weaponman'
        self.sell_items = ['Long Sword', 'Rapier']


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        return ["Welcome to the " + self.name + "!",
                "What weapon would you like to buy?"]


    def make_purchasable_items(self):
        """Make list of items to be chosen"""
        longsword_dialogue = 'Long Sword (100 gold)'
        rapier_dialogue = 'Rapier (50 gold)'

        item2 = {'type': 'Long Sword',
                'price': 100,
                'quantity': 1,
                'dialogue': longsword_dialogue}

        item1 = {'type': 'Rapier',
                 'price': 50,
                 'quantity': 1,
                 'dialogue': rapier_dialogue}

        return [item1, item2]


class ArmorShop(Shop):
    """A place to buy armor"""
    def __init__(self):
        super(ArmorShop, self).__init__()
        self.name = c.ARMOR_SHOP
        self.key = 'armorman'
        self.sell_items = ['Chain Mail', 'Wooden Shield']


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        return ["Welcome to the " + self.name + "!",
                "Would piece of armor would you like to buy?"]


    def make_purchasable_items(self):
        """Make list of items to be chosen"""
        chainmail_dialogue = 'Chain Mail (50 gold)'
        shield_dialogue = 'Wooden Shield (75 gold)'

        item = {'type': 'Chain Mail',
                'price': 50,
                'quantity': 1,
                'dialogue': chainmail_dialogue}

        item2 = {'type': 'Wooden Shield',
                 'price': 75,
                 'quantity': 1,
                 'dialogue': shield_dialogue}

        return [item, item2]


class MagicShop(Shop):
    """A place to buy magic"""
    def __init__(self):
        super(MagicShop, self).__init__()
        self.name = c.MAGIC_SHOP
        self.key = 'magiclady'


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        return ["Welcome to the " + self.name + "!",
                "Would magic spell would you like to buy?"]


    def make_purchasable_items(self):
        """Make list of items to be chosen"""
        fire_dialogue = 'Fire Blast (150 gold)'
        cure_dialogue = 'Cure (150 gold)'

        item1 = {'type': 'Cure',
                 'price': 150,
                 'quantity': 1,
                 'dialogue': cure_dialogue}

        item2 = {'type': 'Fire Blast',
                'price': 150,
                'quantity': 1,
                'dialogue': fire_dialogue}

        return [item1, item2]


class PotionShop(Shop):
    """A place to buy potions"""
    def __init__(self):
        super(PotionShop, self).__init__()
        self.name = c.POTION_SHOP
        self.key = 'potionlady'
        self.sell_items = 'Healing Potion'


    def make_dialogue(self):
        """Make the list of dialogue phrases"""
        return ["Welcome to the " + self.name + "!",
                "What potion would you like to buy?"]


    def make_purchasable_items(self):
        """Make list of items to be chosen"""
        healing_dialogue = 'Healing Potion (15 gold)'


        item = {'type': 'Healing Potion',
                'price': 15,
                'quantity': 1,
                'dialogue': healing_dialogue}

        return [item]

