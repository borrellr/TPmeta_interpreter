"""
Ivan Bratko's Advice Logic 3 System Implementation

Horn clause-based knowledge representation system for decision-making.
Demonstrates:
  - Factual knowledge (weather, court conditions)
  - Rules for recommendations (play/don't play)
  - Inference through backward chaining
"""

from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from logical_engine.meta_interpreter import solve


class AdviceLogic3:
    """
    A decision-support system using Horn clauses for recommendations.
    
    Typical scenario: Given weather and court conditions, advise on 
    whether to play tennis.
    """
    
    def __init__(self, kb=None):
        """Initialize with optional knowledge base."""
        self.kb = kb or KnowledgeBase()
    
    def add_fact(self, fact_string):
        """Add a fact to the knowledge base."""
        fact = Fact(fact_string)
        self.kb.add_fact(fact)
        return fact
    
    def add_rule(self, head, body):
        """
        Add a rule to the knowledge base.
        
        Args:
            head: consequent of the rule (string)
            body: list of antecedents (list of strings)
        """
        rule = Rule(head, body)
        self.kb.add_rule(rule)
        return rule
    
    def query(self, goal):
        """
        Query the knowledge base for a goal.
        
        Args:
            goal: goal to prove (string)
        
        Returns:
            list of solutions (variable bindings)
        """
        return list(solve(goal, self.kb))
    
    def recommend(self, goal):
        """
        Get a recommendation by querying the knowledge base.
        
        Args:
            goal: recommendation goal to seek
        
        Returns:
            True if goal is provable, False otherwise
        """
        solutions = self.query(goal)
        return len(solutions) > 0
    
    def print_kb(self):
        """Print knowledge base contents."""
        print("\n=== Knowledge Base ===")
        print("\nFacts:")
        for fact in self.kb.facts:
            print(f"  {fact.head}")
        print("\nRules:")
        for rule in self.kb.rules:
            body_str = ", ".join(rule.body)
            print(f"  {rule.head} :- {body_str}")
        print()


def create_default_kb():
    """
    Create a default knowledge base for the classic tennis advice scenario.
    
    Returns:
        AdviceLogic3 instance with standard rules and facts
    """
    al3 = AdviceLogic3()
    
    # Weather facts
    al3.add_fact("weather(sunny)")
    al3.add_fact("weather(rainy)")
    al3.add_fact("weather(overcast)")
    
    # Court condition facts
    al3.add_fact("court_surface(grass)")
    al3.add_fact("court_surface(clay)")
    al3.add_fact("court_surface(hard)")
    
    # Player strength facts
    al3.add_fact("player_strength(weak)")
    al3.add_fact("player_strength(medium)")
    al3.add_fact("player_strength(strong)")
    
    # Temperature aspects
    al3.add_fact("temperature(hot)")
    al3.add_fact("temperature(mild)")
    al3.add_fact("temperature(cold)")
    
    # Wind conditions
    al3.add_fact("wind(strong)")
    al3.add_fact("wind(moderate)")
    al3.add_fact("wind(calm)")
    
    # === DECISION RULES ===
    
    # Main rule: Play/don't play based on conditions
    al3.add_rule(
        "play_tennis(X)",
        ["weather(X)", "good_weather(X)"]
    )
    
    # Good weather conditions
    al3.add_rule("good_weather(sunny)", [])
    al3.add_rule("good_weather(overcast)", [])
    
    # Don't play in rain
    al3.add_rule("bad_weather(rainy)", [])
    
    # Court preference rules
    al3.add_rule(
        "good_court(grass)",
        []
    )
    al3.add_rule(
        "acceptable_court(clay)",
        []
    )
    al3.add_rule(
        "acceptable_court(hard)",
        []
    )
    
    # Temperature rules
    al3.add_rule(
        "comfortable_temp(T)",
        ["temperature(T)", "not_too_hot(T)", "not_too_cold(T)"]
    )
    
    al3.add_rule("not_too_hot(mild)", [])
    al3.add_rule("not_too_hot(cold)", [])
    
    al3.add_rule("not_too_cold(mild)", [])
    al3.add_rule("not_too_cold(hot)", [])
    
    # Wind rules
    al3.add_rule(
        "playable_wind(W)",
        ["wind(W)", "acceptable_wind_strength(W)"]
    )
    
    al3.add_rule("acceptable_wind_strength(calm)", [])
    al3.add_rule("acceptable_wind_strength(moderate)", [])
    
    # Player strength adaptation
    al3.add_rule(
        "suitable_for_player(strong)",
        []
    )
    al3.add_rule(
        "suitable_for_player(medium)",
        []
    )
    al3.add_rule(
        "suitable_for_player(weak)",
        []
    )
    
    # Overall recommendation
    al3.add_rule(
        "recommend_play",
        ["weather(W)", "good_weather(W)", "playable_wind(calm)"]
    )
    
    return al3
