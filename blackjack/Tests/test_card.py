# -*- coding: utf-8 -*-
"""
Created on Fri Jun  4 15:53:26 2021

Test cases for Card object

@author: William_Cole
"""
import sys
import unittest
sys.path.insert(0,'..')
from Card import Card

class testCard(unittest.TestCase):
    def testCardName(self):
        card = Card([2], "Clubs", "Two")
        self.assertEqual(card.getName(), "Two")
        self.assertEqual(card.getSuite(), "Clubs")
        self.assertEqual(card.getFullName(), "Two of Clubs")
    
    def testCardValue(self):
        card = Card([2, 4, 6], "Clubs", "Two")
        self.assertEqual(card.getValues(), [6, 4, 2])
        card = Card([2], "", "")
        self.assertEqual(card.getValues(), [2])

if __name__ == "__main__":
    unittest.main()
    