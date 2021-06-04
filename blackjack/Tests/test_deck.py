# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 16:04:04 2021

Unit test for deck class

@author: William_Cole
"""
import sys
sys.path.insert(0,'..')
import unittest
from Deck import Deck
from Card import Card
import CardGameUtils as utils


class TestDeck(unittest.TestCase):
    
    def testGetDeck(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        self.deck = Deck(suites, namevals)
        self.assertEqual(self.deck.count(), 52)
    
    def testDrawDiscard(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        self.deck = Deck(suites, namevals)
        card = self.deck.drawCard()
        self.assertEqual(self.deck.count(), 51)
        self.deck.discard(card)
        self.assertEqual(self.deck.count(), 52)
        
        
if __name__ == "__main__":
    unittest.main()