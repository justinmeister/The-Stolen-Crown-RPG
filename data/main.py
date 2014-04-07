from data.states.main_menu import main_menu
from data.states.town import town
from data.states.castle import castle
from data.states import shop
from data.states.house import house
from data.states.overworld import overworld
from data.states.brother_house import brother_house
from . import setup, tools
from . import constants as c


TOWN = 'town'
MAIN_MENU = 'main menu'
CASTLE = 'castle'
HOUSE = 'house'
INN = 'Inn'
ARMOR_SHOP = 'armor shop'
WEAPON_SHOP = 'weapon shop'
MAGIC_SHOP = 'magic shop'
POTION_SHOP = 'potion shop'
PLAYER_MENU = 'player menu'
OVERWORLD = 'overworld'
BROTHER_HOUSE = 'brother_house'


def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {TOWN: town.Town(),
                  MAIN_MENU: main_menu.Menu(),
                  CASTLE: castle.Castle(),
                  HOUSE: house.House(),
                  INN: shop.Inn(),
                  ARMOR_SHOP: shop.ArmorShop(),
                  WEAPON_SHOP: shop.WeaponShop(),
                  MAGIC_SHOP: shop.MagicShop(),
                  POTION_SHOP: shop.PotionShop(),
                  OVERWORLD: overworld.Overworld(),
                  BROTHER_HOUSE: brother_house.House()
                  }

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()