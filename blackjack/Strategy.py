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
import xml.etree.ElementTree as ET
import random
import os
import Rule

from Card import Card

DEBUG = gc.DEBUG

class Strategy:
    #The idea is to have this be a series of logical statements which control
    #how a player would play.
    #For example, in blackjack the dealer strategy would be to hit until >=17,
    #then stand.
    
    def __init__(self, ruleFile):
        #I guess have an xml file that defines the rules for the strategy
        if ruleFile == None:
            self.file = "Dealer"
        elif ruleFile.lower() == "random":#Special
            self.file = "Random"
        else:
            self.file = ruleFile
            #parse file for rules
            self.parseRuleFile(self.file)
        self.score = 0
        
        
    def getPlay(self, hand : list = [], knownCards : list=[], dealerCard : Card = None, surrender : bool = False) -> tuple[int, int]:
        #checks the current hand and known cards against the rules
        if(DEBUG): print("Current Hand: " + str([card.getFullName() for card in hand]))
        if(DEBUG): print("Boardstate: " + str([card.getFullName() for card in knownCards]))
        if(DEBUG): print("Dealer shown card: ", dealerCard.getFullName())
        handVal = self.getValue(hand)
        self.hand = hand
        self.score = handVal[0]
        self.soft = handVal[1]
        self.dealer = dealerCard
        self.knowncount = self.getKnownCount(knownCards)
        if(DEBUG): print("Score: ", self.score)
        #check for special strategies
        if self.score > gc.MAX_SCORE or surrender:
            self.score = 0
            return gc.BUST, self.score
        if self.file == "Dealer":
            return self.getDealerPlay(hand, knownCards, dealerCard), self.score
        elif self.file == "Random":
            return random.randint(0, len(gc.AVAIL_ACTIONS)), self.score
        else:
            return self.getPlayFromRules(0), self.score
        
    def getKnownCount(self, knownCards : list):
        #TODO
        return 0
        
    #gets the max value of the hand below max score or BUST
    def getValue(self, hand : list = []) -> tuple[int, bool]:
        handVals, soft = util.getHandValues(hand)
        scores = sorted(zip(handVals, soft), key=lambda pair : pair[0], reverse=True)
        if(DEBUG): print(scores)
        for score in scores:
            if score[0] <= gc.MAX_SCORE:
                return score
        #all scores bust
        return (gc.BUST, False)
    
    def getScore(self) -> int:
        return self.score
    
    def getDealerPlay(self, hand : list = [], knownCards : list=[], dealerCard : Card = None) -> int:
        if self.score < 17:
            return gc.HIT
        else:
            return gc.STAND
        
    def getPlayFromRules(self, ruleNo : int) -> int:
        if self.rules is None or len(self.rules) == 0 or ruleNo >= len(self.rules):
            return gc.STAND
        else:
            action = self.rules[ruleNo].evaluate(self.score, self.dealer, self.knowncount, self.soft, self.hand)
            if action == Rule.ACTION_HIT:
                return gc.HIT
            elif action == Rule.ACTION_STAND:
                return gc.STAND
            elif action == Rule.ACTION_DOUBLE:
                return gc.DOUBLEDOWN
            elif action == Rule.ACTION_SPLIT:
                return gc.SPLIT
            elif action == Rule.ACTION_SURRENDER:
                return gc.SURRENDER
            elif action == Rule.ACTION_NEXTRULE:
                ruleNo += 1
                return self.getPlayFromRules(ruleNo)
            else:
                raise ValueError("Unknown action requested: " + str(action))
        
    def parseRuleFile(self, file):
        self.rules = []
        if os.path.exists(file):
            tree = ET.parse(file)
            root = tree.getroot()
            self.name = root.get("name")
            for rule in root.find('Rules').findall("Rule"):
                self.rules.append(Rule.Rule(rule))
            if len(self.rules) == 0:
                raise ValueError("No rules defined in strategy file.", file)
        else:
            raise FileNotFoundError("Strategy file not found.", file)
        
