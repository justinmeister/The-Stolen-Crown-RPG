__author__ = 'justinarmstrong'

from . import setup, tools
from . states import town
from . import constants as c

def main():
    """Add states to control here"""
    run_it = tools.Control(setup.ORIGINAL_CAPTION)
    state_dict = {c.TOWN: town.Town()}

    run_it.setup_states(state_dict, c.TOWN)
    run_it.main()