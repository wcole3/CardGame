# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 16:04:04 2021

Unit test for deck class

@author: William_Cole
"""
import sys

sys.path.insert(0, "..")
import unittest
from Deck import Deck
import CardGameUtils as utils


class TestDeck(unittest.TestCase):
    def testGetDeck(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        self.assertEqual(deck.count(), 52)

    def testDrawDiscard(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        cards = [deck.drawCard(), deck.drawCard(), deck.drawCard()]
        self.assertEqual(deck.count(), 49)
        deck.discard(cards.pop(0))
        self.assertEqual(deck.count(), 50)
        for card in cards:
            deck.discard(card)
        self.assertEqual(deck.count(), 52)

    def testGetCard(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        card1 = deck.getCard("Clubs", "Two")
        self.assertEqual(card1.getFullName(), "Two of Clubs")
        card2 = deck.getCard("Bubbles", "Three")
        self.assertEqual(card2, None)


if __name__ == "__main__":
    unittest.main()
