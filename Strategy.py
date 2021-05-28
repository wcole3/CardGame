#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:03 2020

Abstraction of a strategy for a card game.  Dictates how a player would play a
round.

@author: wcole
"""

from Card import Card

class Strategy:
    #The idea is to have this be a series of logical statements whcih control
    #how a player would play.
    #For example, in blackjack the dealer strategy would be to hit until >=17,
    #then stand.
    
    def __init__(self, ruleFile):
        #I guess have an xml file that defines the rules for the strategy
        self.file = ruleFile
        
    def getPlay(self, hand : list = [], knownCards : list=[]):
        #checks the current hand and known cards against the rules
        print("Current Hand: " + str(hand))
        print("Boardstate: " + str(knownCards))

