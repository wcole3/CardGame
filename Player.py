#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:37:28 2020

Object representing a player.  The player has a strategy and a hand.  They use
the strategy to play their hand.

@author: wcole
"""

from Strategy import Strategy

class Player:
    
    
    def __init__(self, name : str, hand : list = [], strat : Strategy = None):
        self.name = name
        self.hand = hand
        self.strat = strat
        print("Created player")
        
    def play():
        print("play")
        
        

