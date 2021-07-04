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
        handNo = 0
        while handNo < len(player.hands):
            score = player.getScore(handNo)
            if(DEBUG): print(player.name, "hand #: ", handNo, " score: ", score)
            if score > 0:#player loses regardless
                if score == dealer.getScore():
                    #special check for natural dealer blackjack
                    if dealer.getScore() == 21 and len(dealer.hands[0]) == 2:
                        if len(player.hands[handNo]) == 2:
                            pushes += 1
                            player.push()
                        else:
                            player.lose()
                            winnings -= player.bets[handNo]
                    else:
                        pushes += 1
                        player.push()
                elif score > dealer.getScore():
                    #Check for blackjack
                    winners += 1
                    if player.getScore() == 21 and len(player.hands[handNo]) == 2:
                        player.win(True)
                        winnings += gc.BJ_MOD * player.bet
                    else:
                        player.win()
                        winnings += player.bets[handNo]
                else:
                    player.lose()
                    winnings -= player.bets[handNo]
            else:
                player.lose()
                winnings -= player.bets[handNo]
            handNo += 1
    return winners, pushes, len(players) - winners - pushes, winnings

def getPlays(player : Player, deck : Deck):
    handNo = 0
    while handNo < len(player.hands):
        playing = True
        while playing:
            player.readGame(KNOWNCARDS, DEALER_SHOWN)
            action = player.play(handNo)
            if action == gc.BUST:
                playing = False
            elif action == gc.HIT or action == gc.DOUBLEDOWN:
                card = deck.drawCard()
                player.drawCard(card, handNo)
                KNOWNCARDS.append(card)
                if action == gc.DOUBLEDOWN:
                    player.setBet(player.bet*2)
                    player.play(handNo)#call to set score
                    playing = False
            elif action == gc.STAND:
                playing = False
            elif action == gc.SURRENDER:
                player.setBet(player.bet*0.5, handNo)
                player.play(handNo, True)
                playing = False
            elif action == gc.SPLIT:
                if(len(player.hands) < gc.MAX_HANDS):
                    #split into two hands and add card
                    hand1 = [player.hands[handNo][0]]
                    hand2 = [player.hands[handNo][1]]
                    player.scores.append(0)
                    player.bets.append(player.bet)
                    player.hands[handNo] = hand1
                    player.hands.append(hand2)
                    card1 = deck.drawCard()
                    player.drawCard(card1, handNo)
                    KNOWNCARDS.append(card1)
                    card2 = deck.drawCard()
                    player.drawCard(card2, len(player.hands)-1)
                    KNOWNCARDS.append(card2)
                else:
                    #Cant split get last false action
                    player.play(handNo)
                    playing = False
            else: playing = False
        handNo += 1
    
def cleanupGame(players : list = None, dealer : Player = None, deck : Deck = None, betSizes : list = []):
    for i in range(len(players)):
        cards = players[i].roundEnd(betSizes[i])
        for card in cards:
            deck.discard(card)
    for card in dealer.hands[0]:
        deck.discard(card)
    dealer.hands[0].clear()
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
            gc.MAX_HANDS = config.get(gc.GameConst, gc.maxHandTag, fallback=4)
            gc.BJ_MOD = config.get(gc.GameConst, gc.blackjackModTag, fallback=1.5)
            #Run sim
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
        