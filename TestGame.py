#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:36:55 2020

Testing area

@author: wcole
"""

from Card import Card
from Deck import Deck
from Strategy import Strategy
from Player import Player
import CardGameUtils as util

cardAce = Card([1,11], "Hearts", "Ace")

#print(cardAce.getFullName())

#suites = ["Hearts", "Diamonds", "Clubs", "Spades"]
'''names = {"One" : 1, "Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5, "Six" : 6, "Seven" : 7,\
         "Eight" : 8, "Nine" : 9, "Ten" : 10, "Jack" : 10, "Queen" : 10, "King" : 10, "Ace" : [1, 11]}'''
    

suites, nameValDict = util.getDeckFromXML("./Decks/TradDeck.xml")

deck = Deck(suites, nameValDict)

deck.shuffle()

player = Player("Timmy")

strat = Strategy(None)

player.strat = strat

hand = [deck.drawCard(), deck.drawCard(), deck.drawCard()]

known = [deck.drawCard()]

player.hand = hand
player.readGame(known)

print("Action= ", player.play())

for card in hand:
    deck.discard(card)
    
for card in known:
    deck.discard(card)


    
