# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 12:00:17 2021

Test cases for CardGameUtils

@author: Wellb_000
"""
import sys

sys.path.insert(0, "..")
import unittest
from Deck import Deck
import CardGameUtils as utils


class testUtils(unittest.TestCase):
    def testGetValues(self):
        suites, namevals = utils.getDeckFromXML("../../Decks/TradDeck.xml")
        deck = Deck(suites, namevals)
        twoClubs = deck.getCard("Clubs", "Two")
        aceHearts = deck.getCard("Hearts", "Ace")
        jackSpades = deck.getCard("Spades", "Jack")
        eightDia = deck.getCard("Diamonds", "Eight")

        hand1 = [twoClubs, eightDia]
        scores1 = utils.getHandValues(hand1)
        self.assertEqual(scores1[0], [10])

        hand1.append(jackSpades)
        scores2 = utils.getHandValues(hand1)
        self.assertEqual(scores2[0], [20])

        hand1.append(aceHearts)
        scores3, soft = utils.getHandValues(hand1)
        self.assertEqual(sorted(scores3, key=int, reverse=True), [31, 21])


if __name__ == "__main__":
    unittest.main()
