# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 11:59:47 2021

Constants for the game, eventually this should be moved to a file or something

@author: William_Cole
"""

#Debug flag
DEBUG = False

#Rule statics
MAX_SCORE = 21

#Game actions
HIT = 0
STAND = 1
DOUBLEDOWN = 2
BUST = 666

AVAIL_ACTIONS = [HIT, STAND, DOUBLEDOWN]

#Config file sections
GameConst = "Game Constants"
PlayerSetup = "Player Setup"
OutputOptions = "Output Options"

playerTag ="player"
noOfDecks = "number_of_decks"
handsToPlay = "hands_to_play"
deck = "deck_file"
plotOutput = "plot"
saveOutput = "save"