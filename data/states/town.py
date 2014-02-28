__author__ = 'justinarmstrong'

from .. import setup, tools
from .. import constants as c

class Town(tools._State):
    def __init__(self):
        super(Town, self).__init__()

    def startup(self, current_time, persist):
        """Called when the State object is created"""
        self.persist = persist
        self.current_time = current_time

    def update(self, surface, keys, current_time):
        """Updates state"""
        self.keys = keys
        self.current_time = current_time