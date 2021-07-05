#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:41:27 2020

Class for a deck object.  A deck contains enough cards to have one version
of each name suite combo defined in input xml.

@author: wcole
"""

import Card
import random
import GameConstants as gc
from collections import deque


class Deck:
    
    def __init__(self, suites : list, nameVal : dict, numberOfDecks : int = 1):
        self.cards = deque()
        self.noOfDecks = numberOfDecks
        self.discarded = 0#ticker to keep count of how far through the deck we got
        #create a card for each suite-name combo
        for i in range(0, numberOfDecks):
            for suite in suites:
                for name, val in nameVal.items():
                    card = Card.Card(val, suite, name)
                    self.cards.append(card)
        if gc.DEBUG: print("Size of deck: ", len(self.cards))
        
    def drawCard(self):
        return self.cards.pop()
    
    def shuffle(self):
        if gc.DEBUG: print("Deck shuffling at {perc:.4f}% played".format(perc=(self.discarded/len(self.cards))*100 ))
        self.discarded = 0
        random.shuffle(self.cards)
        
    def printDeck(self):
        for card in self.cards:
            print(card.getFullName())
    
    def discard(self, card : Card):
        self.discarded += 1
        self.cards.appendleft(card)
        
    def count(self):
        return len(self.cards)
    
    def getCard(self, suite : str, name : str):
        for card in self.cards:
            if card.suite == suite and card.name == name:
                return card
        return None
        