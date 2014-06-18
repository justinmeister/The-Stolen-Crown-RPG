from data.states import shop, levels, battle, main_menu, death
from data.states import credits
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
BROTHER_HOUSE = 'brotherhouse'
BATTLE = 'battle'
DUNGEON = 'dungeon'
DUNGEON2 = 'dungeon2'
DUNGEON3 = 'dungeon3'
DUNGEON4 = 'dungeon4'
DUNGEON5 = 'dungeon5'
INSTRUCTIONS = 'instructions'
DEATH_SCENE = 'death scene'
LOADGAME = 'load game'
CREDITS = 'credits'


def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {MAIN_MENU: main_menu.Menu(),
                  TOWN: levels.LevelState(TOWN),
                  CASTLE: levels.LevelState(CASTLE),
                  HOUSE: levels.LevelState(HOUSE),
                  OVERWORLD: levels.LevelState(OVERWORLD, True),
                  BROTHER_HOUSE: levels.LevelState(BROTHER_HOUSE),
                  INN: shop.Inn(),
                  ARMOR_SHOP: shop.ArmorShop(),
                  WEAPON_SHOP: shop.WeaponShop(),
                  MAGIC_SHOP: shop.MagicShop(),
                  POTION_SHOP: shop.PotionShop(),
                  BATTLE: battle.Battle(),
                  DUNGEON: levels.LevelState(DUNGEON, True),
                  DUNGEON2: levels.LevelState(DUNGEON2, True),
                  DUNGEON3: levels.LevelState(DUNGEON3, True),
                  DUNGEON4: levels.LevelState(DUNGEON4, True),
                  DUNGEON5: levels.LevelState(DUNGEON5, True),
                  INSTRUCTIONS: main_menu.Instructions(),
                  LOADGAME: main_menu.LoadGame(),
                  DEATH_SCENE: death.DeathScene(),
                  CREDITS: credits.Credits()
                  }

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()
