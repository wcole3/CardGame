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
        strat = Strategy(None)
        hand =[deck.getCard("Clubs", "Six"), deck.getCard("Diamonds", "Queen")]
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.HIT)
        self.assertEqual(strat.getScore(), 16)
        hand.append(deck.getCard("Spades", "Two"))
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.STAND)
        self.assertEqual(strat.getScore(), 18)
        hand.append(deck.getCard("Hearts", "King"))
        action = strat.getPlay(hand, hand, Card([1], "Hearts", "Ace"))
        self.assertEqual(action, gc.BUST)
        self.assertEqual(strat.getScore(), 0)
        
        
if __name__ == "__main__":
    unittest.main()
