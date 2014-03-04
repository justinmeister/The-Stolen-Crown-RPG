__author__ = 'justinarmstrong'

from . import setup, tools
from . states import town, main_menu
from . import constants as c

def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {c.TOWN: town.Town(),
                  c.MAIN_MENU: main_menu.Menu()}

    run_it.setup_states(state_dict, c.MAIN_MENU)
    run_it.main()