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
import GameConstants as gc

DEBUG = gc.DEBUG

class Player:
    
    
    def __init__(self, name : str, hand : list = [], strat : Strategy = None, betSize : float = 0.0):
        self.name = name
        self.hand = hand
        self.strat = strat
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.bet = betSize
        self.bank = 0.0
        self.winningsHistory = []
        if(DEBUG): print("Created player")
        
    def play(self):
        if(DEBUG): print(self.name, " playing")
        return self.strat.getPlay(self.hand, self.knownCards, self.dealerCard)
        
    def readGame(self, known, dealerCard):
        self.knownCards = known
        self.dealerCard = dealerCard
        
    def drawCard(self, card : Card = None):
        self.hand.append(card)
        
    def getScore(self):
        return self.strat.getScore()
    
    def setBet(self, betSize : float = 0.0):
        self.bet = betSize
        
    def win(self):
        self.wins += 1
        self.bank += self.bet
        self.winningsHistory.append((self.bank, self.getScore()))
    
    def push(self):
        self.ties += 1
        self.winningsHistory.append((self.bank, self.getScore()))
        
    def lose(self):
        self.losses += 1
        self.bank -= self.bet
        self.winningsHistory.append((self.bank, self.getScore()))
        
        
        
        

