# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 16:53:37 2021

Object repr of rule from xml file

@author: Wellb_000
"""

import GameConstants as gc
from Card import Card

DEBUG = gc.DEBUG

ATTR_TrueAction = "true_action"
ATTR_FalseAction = "false_action"
ATTR_operation = "operation"
ATTR_variable = "var"
ATTR_check = "check"
ATTR_value = "value"

LOGIC_IF = "IF"
LOGIC_AND = "AND"
LOGIC_OR = "OR"
LOGIC_NOT = "NOT"

VAR_SCORE = "SCORE"
VAR_DEALERSHOWN = "DEALERSHOWN"
VAR_KNOWNCOUNT = "COUNT"
VAR_SOFT = "SOFT"
VAR_PAIR = "PAIR"

CHECK_LESSTHAN = "lt"
CHECK_LESSTHANEQ = "lte"
CHECK_EQUALS = "eq"
CHECK_GREATERTHAN = "gt"
CHECK_GREATERTHANEQ = "gte"

ACTION_HIT = "HIT"
ACTION_STAND = "STAND"
ACTION_DOUBLE = "DOUBLEDOWN"
ACTION_SPLIT = "SPLIT"
ACTION_SURRENDER = "SURRENDER"
ACTION_NEXTRULE = "NEXTRULE"


class Rule:
    
    def __init__(self, root_element):
        if root_element is not None:
            self.true_action = root_element.get(ATTR_TrueAction)
            self.false_action = root_element.get(ATTR_FalseAction)
            self.ruleStatements = self.parseLogic(root_element.find("Logic"))
            if(DEBUG): print(self.ruleStatements)
        else:
            raise ValueError("Rule cannot be constructed from None-type object")
            
    def parseLogic(self, element) -> list:
        #figure out which logic operation
        attrs = []
        op = element.get(ATTR_operation)
        if op == LOGIC_IF:
            #working logic
            var = element.get(ATTR_variable)
            check = element.get(ATTR_check)
            value = element.get(ATTR_value)
            attrs = [LOGIC_IF, var, check, value]
        elif op == LOGIC_AND:
            attrs = [LOGIC_AND]
            children = []
            for logic in element.findall("Logic"):
                children.append(self.parseLogic(logic))
            attrs.append(children)
        elif op == LOGIC_OR:
            attrs = [LOGIC_OR]
            children = []
            for logic in element.findall("Logic"):
                children.append(self.parseLogic(logic))
            attrs.append(children)
        elif op == LOGIC_NOT:
            attrs = [LOGIC_NOT, self.parseLogic(element.find("Logic"))]
        return attrs
    
    def evaluate(self, score : int, dealerCard : Card, count : int, soft : bool, hand : list):
        self.score = score
        self.dealer = dealerCard
        self.count = count
        self.soft = soft
        self.hand = hand
        return self.true_action if self.evaluateRule(self.ruleStatements) else self.false_action
    
    def evaluateRule(self, rules):
        #evaluate the rule and return the true or false action
        if len(rules) != 0:
            op = rules[0]
            if op == LOGIC_IF:
                return self.evaluateIF(rules)
            elif op == LOGIC_AND:
                for rule in rules[1]:
                    # early return if any rule is false
                    if self.evaluateRule(rule) == False:
                        return False
                return True
            elif op == LOGIC_OR:
                for rule in rules[1]:
                    # early return if any rule is true
                    if self.evaluateRule(rule):
                        return True
                return False
            elif op == LOGIC_NOT:
                return not self.evaluateRule(rules[1])
        else:
            raise ValueError("No rule statements found for rule")
            
    def evaluateIF(self, logic):
        #get the variable
        var = None
        if logic[1] == VAR_SCORE:
            var = self.score
        elif logic[1] == VAR_DEALERSHOWN:
            var = max(self.dealer.getValues())
        elif logic[1] == VAR_KNOWNCOUNT:
            var = self.count
        elif logic[1] == VAR_SOFT:
            return self.soft
        elif logic[1] == VAR_PAIR:
            if len(self.hand) != 2:
                return False
            elif self.hand[0].getName() is not self.hand[1].getName():
                return False
            else:
                var = self.hand[0].getValues()[0]
        else:
            raise ValueError("Unknown variable type encountered in rule: " + str(logic[1]))
        #Get the value once we know it isnt soft
        value = int(logic[3])
        #Get the operation and evaluate
        if logic[2] == CHECK_EQUALS:
            return var == value
        elif logic[2] == CHECK_GREATERTHAN:
            return var > value
        elif logic[2] == CHECK_GREATERTHANEQ:
            return var >= value
        elif logic[2] == CHECK_LESSTHAN:
            return var < value
        elif logic[2] == CHECK_LESSTHANEQ:
            return var <= value
        else:
            raise ValueError("Unknown check encountered in rule: " + str(logic[2]))
        
            
