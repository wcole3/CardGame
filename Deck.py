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
from collections import deque


class Deck:
    
    def __init__(self, suites : list, nameVal : dict, numberOfDecks : int = 1):
        self.cards = deque()
        #create a card for each suite-name combo
        for i in range(0, numberOfDecks):
            for suite in suites:
                for name, val in nameVal.items():
                    card = Card.Card(val, suite, name)
                    self.cards.append(card)
    
        
    def drawCard(self):
        return self.cards.pop()
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def printDeck(self):
        for card in self.cards:
            print(card.getFullName())
