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
import GameConstants as gc

DEBUG = gc.DEBUG

DEFAULT_HandsPlayed = 1
DEFAULT_NoPlayers = 5
DEFAULT_Strategy = Strategy(None)

KNOWNCARDS = []

RESULT_DICT = {}

def initResultDict():
    #Setup the dict used to accumulate the results of the sim
    RESULT_DICT = dict()
    RESULT_DICT['total_wins'] = 0
    RESULT_DICT['total_ties'] = 0
    RESULT_DICT['total_losses'] = 0
    return RESULT_DICT

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
        if player.getScore() > 0:#player loses regardless
            if player.getScore() == dealer.getScore():
                #special check for natural dealer blackjack
                if dealer.getScore() == 21 and len(dealer.hand) == 2:
                    if len(player.hand) == 2:
                        pushes += 1
                        player.ties += 1
                    else:
                        player.losses += 1
                else:
                    pushes += 1
                    player.ties += 1
            elif player.getScore() > dealer.getScore():
                winners += 1
                player.wins += 1
            else:
                player.losses += 1
        else:
            player.losses += 1
    return winners, pushes, len(players) - winners - pushes

def getPlays(player : Player, deck : Deck):
    playing = True
    while playing:
        player.readGame(KNOWNCARDS)
        action = player.play()
        if action == gc.BUST:
            playing = False
        elif action == gc.HIT:
            card = deck.drawCard()
            player.drawCard(card)
            KNOWNCARDS.append(card)
        elif action == gc.STAND:
            playing = False
        else: playing = False
    
def cleanupGame(players : list = None, dealer : Player = None, deck : Deck = None):
    for player in players:
        for card in player.hand:
            deck.discard(card)
        player.hand.clear()
    for card in dealer.hand:
        deck.discard(card)
    dealer.hand.clear()
    KNOWNCARDS.clear()
    
def printSummary(results : dict, players : list = None):
    print("Summary of Simulation")
    print("Total table wins: ", results['total_wins'])
    print("Total table pushes: ", results['total_ties'])
    print("Total table losses: ", results['total_losses'])
    if players is not None:
        print("Player results")
        for player in players:
            print("\t", player.name)
            print("\t\tWins: ", player.wins)
            print("\t\tPushes: ", player.ties)
            print("\t\tLosses: ", player.losses)
    
if __name__ == "__main__":
    #get game vars; eventually get from file
    loops = DEFAULT_HandsPlayed
    numberOfplayers = DEFAULT_NoPlayers
    print("running sim")
    #get the deck
    suites, valDict = util.getDeckFromXML("./Decks/TradDeck.xml")
    deck = Deck(suites, valDict)
    #setup players
    strats = []
    for i in range(numberOfplayers):
        strats.append(Strategy(None))
    players = setupPlayers(numberOfplayers, strats) 
    dealer = Player("Dealer", [], DEFAULT_Strategy)
    RESULT_DICT = initResultDict()
    #game loop
    game = 0
    while game < loops:
        dealOpeningHands(players, dealer, deck)
        #play game
        for player in players:
            getPlays(player, deck)
        getPlays(dealer, deck)
        #Check results of game
        win, tie, loss = getResults(players, dealer)
        if(DEBUG): print("wins: ", win)
        if(DEBUG): print("Pushes: ", tie)
        if(DEBUG): print("Losses: ", loss)
        RESULT_DICT['total_wins'] += win
        RESULT_DICT['total_ties'] += tie
        RESULT_DICT['total_losses'] += loss
        cleanupGame(players, dealer, deck)
        game+=1
    
    print("sim finished")
    printSummary(RESULT_DICT, players)