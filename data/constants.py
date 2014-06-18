#Constants used throughout the game 
SCREEN_SIZE = (800, 608)

##GAME STATES

TOWN = 'town'
MAIN_MENU = 'main menu'
CASTLE = 'castle'
INN = 'Inn'
POTION_SHOP = 'potion shop'
ARMOR_SHOP = 'armor shop'
WEAPON_SHOP = 'weapon shop'
MAGIC_SHOP = 'magic shop'
HOUSE = 'house'
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

##Colors

BLACK = 0, 0, 0
NEAR_BLACK = 1, 0, 0
WHITE = 255, 255, 255
BLACK_BLUE = 19, 15, 48
NEAR_BLACK_BLUE = 20, 15, 48
LIGHT_BLUE = 0, 153, 204
DARK_RED = 118, 27, 12
REALLY_DARK_RED = 15, 0, 0
RED = 255, 0, 0
GREEN = 0, 255, 0
PINK = 208, 32, 144
TRANSITION_COLOR = BLACK_BLUE

MAIN_FONT = 'DroidSans'

#BATTLE STATES

SELECT_ACTION = 'select action'
SELECT_ENEMY = 'select enemy'
ENEMY_ATTACK = 'enemy attack'
SWITCH_ENEMY = 'switch enemy'
PLAYER_ATTACK = 'player attack'
SELECT_ITEM = 'select item'
SELECT_MAGIC = 'select magic'
RUN_AWAY = 'run_away'
ATTACK_ANIMATION = 'attack animation'
BATTLE_WON = 'battle won'
ENEMY_DAMAGED = 'enemy damaged'
ENEMY_DEAD = 'enemy dead'
PLAYER_FINISHED_ATTACK = 'player finished attack'
PLAYER_DAMAGED = 'enemy attack damage'
DRINK_HEALING_POTION = 'drink healing potion'
DRINK_ETHER_POTION = 'drink ether potion'
CURE_SPELL = 'cure spell'
FIRE_SPELL = 'fire spell'
VICTORY_DANCE = 'victory dance'
KNOCK_BACK = 'knock back'
FLEE = 'flee'
FADE_DEATH = 'fade death'
SHOW_EXPERIENCE = 'show experience'
LEVEL_UP = 'level up'
TWO_ACTIONS = 'two actions'
SHOW_GOLD = 'show gold'
DEATH_FADE = 'death fade'

#EVENTS

END_BATTLE = 'end battle'

#SOUND EFFECTS

CLICK = 'click'
CLICK2 = 'click2'
CLOTH_BELT = 'cloth_belt'
SWORD = 'sword'
FIRE = 'fire'
PUNCH = 'punch'
POWERUP = 'powerup'
TALK = 'talk'
MISS = 'whoosh'

TRANSITION_SPEED = 35 
DEATH_TRANSITION_SPEED = 5

#LEVEL STATES

NORMAL = 'normal'
TRANSITION_IN = 'transition in'
TRANSITION_OUT = 'transition out'
