#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:03 2020

Abstraction of a strategy for a card game.  Dictates how a player would play a
round.

@author: wcole
"""

from Card import Card
from Player import Player
import weakref

class Strategy:
    #The idea is to have this be a series of logical statements whcih control
    #how a player would play.
    #For example, in blackjack the dealer strategy would be to hit until >=17,
    #then stand.
    
    def __init__(self, ruleFile, player : Player = None):
        #I guess have an xml file that defines the rules for the strategy
        self.file = ruleFile
        self.player = player
        
    def getPlay(self, currentScore : float, knownCards : list=[]):
        #checks the current score and known cards against the rules
        print("Current Score = " + str(currentScore) )
        
    def setPlayer(self, player : Player):
        self.player = weakref.ref(player)
    
    def getPlayer(self):
        return self.player
