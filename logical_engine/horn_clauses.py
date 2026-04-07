"""
Horn Clause Representation
Defines facts, rules, and a simple Horn clause knowledge base.
"""

class Fact:
    def __init__(self, head):
        self.head = head

class Rule:
    def __init__(self, head, body):
        self.head = head
        self.body = body  # list of goals

class KnowledgeBase:
    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)
