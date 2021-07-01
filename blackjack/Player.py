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
        self.hands = [hand]
        self.scores = [0]
        self.strat = strat
        self.wins = 0
        self.ties = 0
        self.losses = 0
        self.bet = betSize
        self.bets = [betSize]
        self.bank = 0.0
        self.winningsHistory = []
        self.roundHandStr = ""
        if(DEBUG): print("Created player")
        
    def play(self, handNo : int = 0, surrender : bool = False):
        if(DEBUG): print(self.name, " playing")
        action, handScore = self.strat.getPlay(self.hands[handNo], self.knownCards, self.dealerCard, surrender)
        self.scores[handNo] = handScore
        return action
        
    def readGame(self, known, dealerCard):
        self.knownCards = known
        self.dealerCard = dealerCard
        
    def drawCard(self, card : Card = None, handNo : int = 0):
        self.hands[handNo].append(card)
        
    def getScore(self, handNo : int = 0):
        return self.scores[handNo]
    
    def setBet(self, betSize : float = 0.0, handNo : int = 0):
        self.bets[handNo] = betSize
    
    def resetBet(self, betSize : float = 0.0):
        self.bets = [betSize]
        self.bet = betSize
        
    def win(self, bj : bool = False, handNo : int = 0):
        self.wins += 1
        if bj:
            self.bank += gc.BJ_MOD * self.bets[handNo]
        else:
            self.bank += self.bets[handNo]
        self.roundHandStr += str(self.getScore(handNo)) + "//"
        #self.winningsHistory.append((self.bank, self.getScore(handNo)))
    
    def push(self, handNo : int = 0):
        self.ties += 1
        self.roundHandStr += str(self.getScore(handNo)) + "//"
        #self.winningsHistory.append((self.bank, self.getScore(handNo)))
        
    def lose(self, handNo : int = 0):
        self.losses += 1
        self.bank -= self.bets[handNo]
        self.roundHandStr += str(self.getScore(handNo)) + "//"
        #self.winningsHistory.append((self.bank, self.getScore(handNo)))
        
    def roundEnd(self, betSize : float = 0.0):
        cards = []
        for hand in self.hands:
            for card in hand:
                cards.append(card)
        self.winningsHistory.append((self.bank, self.roundHandStr))
        self.roundHandStr = ""
        self.hands = [[]]
        self.resetBet(betSize)
        return cards
        
        
        
        
        
        

