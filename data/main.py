from data.states.main_menu import main_menu
from data.states.town import town
from data.states.castle import castle

__author__ = 'justinarmstrong'

from . import setup, tools
from . import constants as c

def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {c.TOWN: town.Town(c.TOWN, 25, 50),
                  c.MAIN_MENU: main_menu.Menu(c.MAIN_MENU),
                  c.CASTLE: castle.Castle(c.CASTLE, 25, 27)}

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()