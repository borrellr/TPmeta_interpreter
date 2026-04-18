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

    def display_kb_contents(self):
        """Display the contents of the knowledge base."""
        print("\n=== Knowledge Base Contents ===")
        print(f"\nFacts ({len(self.facts)}):")
        for fact in self.facts:
            print(f"  {fact.head}")
        print(f"\nRules ({len(self.rules)}):")
        for rule in self.rules:
            body_str = ", ".join(rule.body)
            print(f"  {rule.head} :- {body_str}")
        print()
