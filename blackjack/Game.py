# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:51:47 2021

@author: wcole
"""

import argparse as ap
import sys
import CardGameUtils as util
import GameConstants as gc
import matplotlib.pyplot as plt
import numpy as np

from Deck import Deck
from Strategy import Strategy
from Player import Player


DEBUG = gc.DEBUG
PLOT = False

DEFAULT_HandsPlayed = 1
DEFAULT_NoPlayers = 1
DEFAULT_Strategy = Strategy(None)
DEFAULT_BetSize = 1.5
DEFAULT_DeckFile = "../Decks/TradDeck.xml"

KNOWNCARDS = []

#setup argparser
parser = ap.ArgumentParser(description="Run a blackjack simulation")
parser.add_argument("-cf", type=str, nargs=1, required=False, help="The configuration file for the simulation")

def initResultDict(players : list = []):
    #Setup the dict used to accumulate the results of the sim
    RESULT_DICT = dict()
    RESULT_DICT['total_wins'] = 0
    RESULT_DICT['total_ties'] = 0
    RESULT_DICT['total_losses'] = 0
    RESULT_DICT['total_winnings'] = 0.0
    RESULT_DICT['table_history'] = []
    RESULT_DICT['player_names'] = [player.name for player in players]
    RESULT_DICT['player_histories'] = [player.winningsHistory for player in players]
    return RESULT_DICT

def setupPlayers(numberOfplayers : int, strats : [], betSizes : list = []):
    return [Player("Player" + str(i), [], strats[i], betSizes[i]) for i in range(numberOfplayers)]
    
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
            global DEALER_SHOWN
            DEALER_SHOWN = card
            
def getResults(players : list, dealer : Player):
    winners = 0
    pushes = 0
    winnings = 0.0
    if(DEBUG): print("Dealer score: ", dealer.getScore())
    for player in players:
        if(DEBUG): print(player.name, " score: ", player.getScore())
        if player.getScore() > 0:#player loses regardless
            if player.getScore() == dealer.getScore():
                #special check for natural dealer blackjack
                if dealer.getScore() == 21 and len(dealer.hand) == 2:
                    if len(player.hand) == 2:
                        pushes += 1
                        player.push()
                    else:
                        player.lose()
                        winnings -= player.bet
                else:
                    pushes += 1
                    player.push()
            elif player.getScore() > dealer.getScore():
                winners += 1
                player.win()
                winnings += player.bet
            else:
                player.lose()
                winnings -= player.bet
        else:
            player.lose()
            winnings -= player.bet
    return winners, pushes, len(players) - winners - pushes, winnings

def getPlays(player : Player, deck : Deck):
    playing = True
    while playing:
        player.readGame(KNOWNCARDS, DEALER_SHOWN)
        action = player.play()
        if action == gc.BUST:
            playing = False
        elif action == gc.HIT or action == gc.DOUBLEDOWN:
            card = deck.drawCard()
            player.drawCard(card)
            KNOWNCARDS.append(card)
            if action == gc.DOUBLEDOWN:
                player.setBet(player.bet*2)
                player.play()#call to set score
                playing = False
        elif action == gc.STAND:
            playing = False
        else: playing = False
    
def cleanupGame(players : list = None, dealer : Player = None, deck : Deck = None, betSizes : list = []):
    for i in range(len(players)):
        for card in players[i].hand:
            deck.discard(card)
        players[i].hand.clear()
        players[i].setBet(betSizes[i])
    for card in dealer.hand:
        deck.discard(card)
    dealer.hand.clear()
    KNOWNCARDS.clear()
    
def printSummary(results : dict, players : list = None):
    print("Summary of Simulation")
    print("Total table wins: ", results['total_wins'])
    print("Total table pushes: ", results['total_ties'])
    print("Total table losses: ", results['total_losses'])
    print("Table winnings: ", results['total_winnings'])
    if players is not None:
        print("Player results")
        for player in players:
            print("\t", player.name)
            print("\t\tWins: ", player.wins)
            print("\t\tPushes: ", player.ties)
            print("\t\tLosses: ", player.losses)
            print("\t\tWinnings: ", player.bank)
    
def main(loops : int = DEFAULT_HandsPlayed, numberOfplayers : int = DEFAULT_NoPlayers, deckFile : str = DEFAULT_DeckFile):
    #get game vars; eventually get from file
    print("running sim")
    #get the deck
    suites, valDict = util.getDeckFromXML(deckFile)
    deck = Deck(suites, valDict)
    #setup players
    strats = []
    betSizes = []
    for i in range(numberOfplayers):
        strats.append(Strategy(None))
        betSizes.append(DEFAULT_BetSize)
    players = setupPlayers(numberOfplayers, strats, betSizes) 
    dealer = Player("Dealer", [], Strategy("../Strategies/DealerStrategy.xml"))
    RESULT_DICT = initResultDict(players)
    
    #game loop
    game = 0
    while game < loops:
        dealOpeningHands(players, dealer, deck)
        #play game
        for i in range(numberOfplayers):
            getPlays(players[i], deck)
        getPlays(dealer, deck)
        #Check results of game
        win, tie, loss, winnings = getResults(players, dealer)
        if(DEBUG): print("wins: ", win)
        if(DEBUG): print("Pushes: ", tie)
        if(DEBUG): print("Losses: ", loss)
        RESULT_DICT['total_wins'] += win
        RESULT_DICT['total_ties'] += tie
        RESULT_DICT['total_losses'] += loss
        RESULT_DICT['total_winnings'] += winnings
        RESULT_DICT['table_history'].append((RESULT_DICT['total_winnings'], dealer.getScore()))
        RESULT_DICT['player_histories'] = [player.winningsHistory for player in players]
        cleanupGame(players, dealer, deck, betSizes)
        game+=1
        
    
    print("sim finished")
    printSummary(RESULT_DICT, players)
    return RESULT_DICT
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args is not None:
            print("parse config file and get plot flag")
    RESULT_DICT = main(1)
    
    #do plot if desired
    if PLOT:
        fig, ax = plt.subplots()
        x = np.linspace(0, len(RESULT_DICT['player_histories'][0]) - 1, len(RESULT_DICT['player_histories'][0]))
        ax.hlines(0, min(x), max(x), linestyles='dashed', linewidth = 0.5)
        ax.plot(x, [-1*entry[0] for entry in RESULT_DICT['table_history']], c='k', label="House", marker=".")
        i = 0
        for hist in RESULT_DICT['player_histories']:
            ax.plot(x, [entry[0] for entry in hist], label=RESULT_DICT['player_names'][i], marker=".")
            i += 1
        ax.legend(bbox_to_anchor=(1,1))
        ax.set_xlabel("Hands played")
        ax.set_ylabel("Winnings ($)")
        ax.set_xlim([min(x), max(x)])
        