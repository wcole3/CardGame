# -*- coding: utf-8 -*-
"""
Created on Mon May 31 16:51:47 2021

@author: wcole
"""

import argparse as ap
import sys
import os
import CardGameUtils as util
import GameConstants as gc
import matplotlib.pyplot as plt
import numpy as np
import configparser as cp

from Deck import Deck
from Strategy import Strategy
from Player import Player


DEBUG = gc.DEBUG
PLOT = True

BASE_RESULT_DIR = "../Results/"
BASE_CONFIG_DIR = "../Config/"

DEFAULT_HandsPlayed = 1
DEFAULT_NoPlayers = 1
DEFAULT_Strategy = Strategy(None)
DEFAULT_BetSize = 1.5
DEFAULT_DeckFile = "../Decks/TradDeck.xml"

housecolor = 'maroon'

KNOWNCARDS = []

#setup argparser
parser = ap.ArgumentParser(description="Run a blackjack simulation")
parser.add_argument("-cf", type=str, nargs="*", required=False, help="The configuration file for the simulation")

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

def setupPlayers(strats : [], betSizes : list = [], names : list = []):
    return [Player(names[i], [], strats[i], betSizes[i]) for i in range(len(strats))]
    
def dealOpeningHands(players : list = [], dealer : Player = None, deck : Deck = None):
    if deck.noOfDecks == 1: deck.shuffle()
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
                #Check for blackjack
                winners += 1
                if player.getScore() == 21 and len(player.hand) == 2:
                    player.win(True)
                    winnings += gc.BJ_MOD * player.bet
                else:
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
        #TODO implement split and surrender
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
            
def writeResultDict(results : dict, path : str, players : list = None):
    f = open(path, 'w')
    f.write("Summary of Simulation")
    f.write("\nTotal table wins: " + str(results['total_wins']))
    f.write("\nTotal table pushes: " + str(results['total_ties']))
    f.write("\nTotal table losses: " + str(results['total_losses']))
    f.write("\nTable winnings: " + str(results['total_winnings']))
    if players is not None:
        f.write("\nPlayer results")
        for player in players:
            f.write("\n\t" + str(player.name))
            f.write("\n\t\tWins: " + str(player.wins))
            f.write("\n\t\tPushes: " + str(player.ties))
            f.write("\n\t\tLosses: " + str(player.losses))
            f.write("\n\t\tWinnings: " + str(player.bank))
    f.close()
    
def main(confFile : cp.ConfigParser = None):
    print("running sim")
    suites, valDict = util.getDeckFromXML(confFile.get(gc.GameConst, gc.deck, fallback=DEFAULT_DeckFile).strip())
    deck = Deck(suites, valDict, int(confFile.get(gc.GameConst, gc.noOfDecks, fallback=1)))
    #setup players
    strats = []
    betSizes = []
    names = []
    i = 1
    while(confFile.has_option(gc.PlayerSetup, gc.playerTag+str(i))):
        playerNo = gc.playerTag+str(i)
        stratFile = Strategy(confFile.get(gc.PlayerSetup, playerNo).split(",")[1])
        betSize = float(confFile.get(gc.PlayerSetup, playerNo).split(",")[2])
        name = confFile.get(gc.PlayerSetup, playerNo).split(",")[0]
        names.append(name)
        strats.append(stratFile)
        betSizes.append(betSize)
        i += 1
    players = setupPlayers(strats, betSizes, names) 
    dealer = Player("Dealer", [], Strategy("../Strategies/DealerStrategy.xml"))
    
    RESULT_DICT = initResultDict(players)
    #game loop
    game = 0
    while game < int(confFile.get(gc.GameConst, gc.handsToPlay, fallback=DEFAULT_HandsPlayed)):
        dealOpeningHands(players, dealer, deck)
        #play game
        for i in range(len(players)):
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
    return RESULT_DICT, players
    
if __name__ == "__main__":
    config = None
    filename = ""
    filesToRun = []
    if len(sys.argv) > 1:
        args = parser.parse_args()
        if args is not None:
            filesToRun = args.cf
    else:
        filesToRun = ['Default']
    for file in filesToRun:
        config = util.parseConfig(BASE_CONFIG_DIR + str(file) + ".txt")
        filename = str(file) + "_results"
        RESULT_DIR = os.path.join(BASE_RESULT_DIR, str(file) + "_results")
        os.makedirs(RESULT_DIR, exist_ok=True)
        if config is not None:
            PLOT = config[gc.OutputOptions][gc.plotOutput].lower() == "true"
            SAVE = config[gc.OutputOptions][gc.saveOutput].lower() == "true"
            RESULT_DICT, players = main(config)
            
            #do plot if desired
            if PLOT:
                fig, ax = plt.subplots()
                x = np.linspace(1, len(RESULT_DICT['player_histories'][0]), len(RESULT_DICT['player_histories'][0]))
                ax.hlines(0, min(x), max(x), linestyles='dashed', linewidth = 0.5)
                playerMax = 0
                i = 0
                for hist in RESULT_DICT['player_histories']:
                    ax.plot(x, [entry[0] for entry in hist], label=RESULT_DICT['player_names'][i], marker=".")
                    #get player max
                    m = max(map(abs, [entry[0] for entry in hist]))
                    if m >= playerMax:
                        playerMax = m
                    i += 1
                ax2 = ax.twinx()
                ax2.plot(x, [-1*entry[0] for entry in RESULT_DICT['table_history']], c=housecolor, label="House", marker=".")
                maxVal = max(map(abs, [entry[0] for entry in RESULT_DICT['table_history']]))
                ax.set_ylim([-1*playerMax, playerMax])
                ax2.set_ylim([-1*maxVal, maxVal])
                ax2.tick_params(axis='y', labelcolor=housecolor)
                ax.set_xlim([min(x), max(x)])
                ax.legend(loc='upper left', bbox_to_anchor=(0,1)).set_zorder(20)
                ax.set_xlabel("Hands played")
                ax.set_ylabel("Player Winnings ($)")
                ax2.set_ylabel("House Winnings ($)", rotation=270, va="center_baseline", color=housecolor)
                ax.set_zorder(1)  # default zorder is 0 for ax1 and ax2
                ax.set_frame_on(False)  # prevents ax1 from hiding ax2
                fig.tight_layout()
                if SAVE:
                    fig.savefig(os.path.join(RESULT_DIR, filename + ".png"), dpi=400)
            if SAVE: writeResultDict(RESULT_DICT, os.path.join(RESULT_DIR, filename + ".txt"), players)
        else:
            print("Config file could not be openned or is not valid")
        