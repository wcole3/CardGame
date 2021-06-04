#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:55:03 2020

Abstraction of a strategy for a card game.  Dictates how a player would play a
round.

@author: wcole
"""
import CardGameUtils as util
import GameConstants as gc

from Card import Card

DEBUG = gc.DEBUG

class Strategy:
    #The idea is to have this be a series of logical statements whcih control
    #how a player would play.
    #For example, in blackjack the dealer strategy would be to hit until >=17,
    #then stand.
    
    def __init__(self, ruleFile):
        #I guess have an xml file that defines the rules for the strategy
        self.file = ruleFile
        self.score = 0
        
    def getPlay(self, hand : list = [], knownCards : list=[]):
        #checks the current hand and known cards against the rules
        if(DEBUG): print("Current Hand: " + str([card.getFullName() for card in hand]))
        if(DEBUG): print("Boardstate: " + str([card.getFullName() for card in knownCards]))
        self.score = self.getValue(hand)
        if(DEBUG): print("Score: ", self.score)
        #todo logic to do things
        if self.score > gc.MAX_SCORE:
            self.score = 0
            return gc.BUST
        elif self.score < 17:
            return gc.HIT
        else:
            return gc.STAND
        
    #gets the max value of the hand
    def getValue(self, hand : list = []):
        scores = sorted(util.getHandValues(hand), key=int, reverse=True)
        if(DEBUG): print(scores)
        for score in scores:
            if score <= gc.MAX_SCORE:
                return score
        #all scores bust
        return gc.BUST
    
    def getScore(self):
        return self.score
        