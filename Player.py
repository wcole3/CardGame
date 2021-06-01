#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:37:28 2020

Object representing a player.  The player has a strategy and a hand.  They use
the strategy to play their hand.

@author: wcole
"""

from Strategy import Strategy
from Card import Card

class Player:
    
    
    def __init__(self, name : str, hand : list = [], strat : Strategy = None):
        self.name = name
        self.hand = hand
        self.strat = strat
        print("Created player")
        
    def play(self):
        print("play")
        return self.strat.getPlay(self.hand, self.knownCards)
        
    def readGame(self, known):
        self.knownCards = known
        
    def drawCard(self, card : Card = None):
        self.hand.append(card)
        
        
        

