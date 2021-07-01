# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:19:40 2021

Test case for Strategy

@author: Wellb_000
"""
import sys
sys.path.insert(0,'..')#hack it
import unittest
import CardGameUtils as utils
import GameConstants as gc
from Deck import Deck
from Card import Card
from Strategy import Strategy


class testStrategy(unittest.TestCase):
    
    def testDealerStrategy(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        strat = Strategy("../../Strategies/DealerStrategy.xml")
        hand =[deck.getCard("Clubs", "Six"), deck.getCard("Diamonds", "Queen")]
        action, score = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.HIT)
        self.assertEqual(score, 16)
        hand.append(deck.getCard("Spades", "Two"))
        action, score = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.STAND)
        self.assertEqual(score, 18)
        hand.append(deck.getCard("Hearts", "King"))
        action, score = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.BUST)
        self.assertEqual(strat.getScore(), 0)
        
    def testSurrenderStrategy(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        strat = Strategy("../../Strategies/TestStrategySurrender.xml")
        hand =[deck.getCard("Clubs", "Six"), deck.getCard("Diamonds", "Queen")]
        action, score = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.SURRENDER)
        action, score = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"), True)
        self.assertEqual(action, gc.BUST)
        
if __name__ == "__main__":
    unittest.main()
