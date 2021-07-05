#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 11:54:10 2020

Some utility functions to help out

@author: wcole
"""

import xml.etree.ElementTree as ET
import os
import itertools as it
import GameConstants as gc
import configparser as cp

DEBUG = gc.DEBUG

def getDeckFromXML(xmlFile):
    #check if file exists
    if(os.path.exists(xmlFile)):
        suites = []
        nameValDict = {}
        #load the suites, names, and values
        tree = ET.parse(xmlFile)
        rootEle = tree.getroot()
        suiteEle = rootEle.find("Suites")
        nameEle = rootEle.find("Names")
        if suiteEle is not None:
            for ele in suiteEle:
                suites.append(ele.get("name"))
        if nameEle is not None:
            for ele in nameEle:
                name = ele.get("name")
                values = []
                for value in ele:
                    values.append(float(value.text))
                nameValDict.update({name : values})
        return suites, nameValDict
    else:
        raise FileNotFoundError("Deck xml file not found at path: " + xmlFile)
        
def getHandValues(hand : list = []):
    cardValues = []
    for card in hand:
        cardValues.append(card.getValues())
    combs = list(it.product(*cardValues))
    if(DEBUG): print(combs)
    scores = []
    softList = []
    for o in combs:
        scores.append(sum(o))
        if 11 in o:
            softList.append(True)
        else:
            softList.append(False)
    return scores, softList

def parseConfig(file : str):
    conf = cp.ConfigParser()
    conf.read(file)
    for key in conf:
        if DEBUG: print(key)
    return conf

def getAllConfigFiles(path : str):
    return [file for file in os.listdir(path) if file.endswith(".txt")]
        
            