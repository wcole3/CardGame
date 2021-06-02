# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:51:47 2021

@author: wcole
"""

import argparse as ap
from Card import Card
from Deck import Deck
from Strategy import Strategy
from Player import Player
import CardGameUtils as util

DEBUG = True

DEFAULT_HandsPlayed = 1
DEFAULT_NoPlayers = 5
DEFAULT_Strategy = Strategy(None)

KNOWNCARDS = []

def setupPlayers(numberOfplayers : int, strats : []):
    return [Player("Player" + str(i), [], strats[i]) for i in range(numberOfplayers)]
    
def dealOpeningHands(players : list = [], dealer : Player = None, deck : Deck = None):
    deck.shuffle()
    #deal opening hands
    for i in range(2):
        for player in players:
            card = deck.drawCard()
            player.drawCard(card)
            KNOWNCARDS.append(card)
        card = deck.drawCard()
        dealer.drawCard(card)
        if i != 0:
            KNOWNCARDS.append(card)
            
def getResults(players : list, dealer : Player):
    winners = 0
    pushes = 0
    if(DEBUG): print("Dealer score: ", dealer.getScore())
    for player in players:
        if(DEBUG): print(player.name, " score: ", player.getScore())
        if player.getScore() == dealer.getScore():
            pushes += 1
        elif player.getScore() > dealer.getScore():
            winners += 1
    return winners, pushes, len(players) - winners - pushes
    
def cleanupGame(players : list = None, dealer : Player = None, deck : Deck = None):
    for player in players:
        for card in player.hand:
            deck.discard(card)
        player.hand = []
    for card in dealer.hand:
        deck.discard(card)
    dealer.hand = []
    KNOWNCARDS = []
    
if __name__ == "__main__":
    print("running sim")
    #get the deck
    suites, valDict = util.getDeckFromXML("./Decks/TradDeck.xml")
    deck = Deck(suites, valDict)
    #setup players
    strats = []
    for i in range(DEFAULT_NoPlayers):
        strats.append(Strategy(None))
    players = setupPlayers(DEFAULT_NoPlayers, strats) 
    dealer = Player("Dealer", [], DEFAULT_Strategy)
    #game loop
    game = 0
    while game < DEFAULT_HandsPlayed:
        dealOpeningHands(players, dealer, deck)
        #play game
        for player in players:
            player.readGame(KNOWNCARDS)
            player.play()
        dealer.readGame(KNOWNCARDS)
        dealer.play()
        #Check results of game
        win, tie, loss = getResults(players, dealer)
        if(DEBUG): print("wins: ", win)
        if(DEBUG): print("Pushes: ", tie)
        if(DEBUG): print("Losses: ", loss)
        cleanupGame(players, dealer, deck)
        print(deck.count())
        game+=1
    
    print("sim finished")
    