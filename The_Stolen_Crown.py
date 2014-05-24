#!/usr/bin/env python
__author__ = 'justinarmstrong'

"""This is a fantasy RPG game about a warrior whose
quest is to recover a magic crown"""
    
import sys
import pygame as pg
from data import setup
from data.main import main

if __name__ =='__main__':
    setup.GAME
    main()
    pg.quit()
    sys.exit()
