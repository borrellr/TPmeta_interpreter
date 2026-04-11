"""
Unit Tests for Ivan Bratko's Advice Logic 3 System

Tests the core functionality of the advice logic system including:
- Fact addition and querying
- Rule creation and inference
- Complex multi-premise rules
- Multiple solution paths
"""

import unittest
from .advice_logic_3 import AdviceLogic3, create_default_kb


class TestAdviceLogic3Basic(unittest.TestCase):
    """Test basic fact and query functionality."""
    
    def setUp(self):
        """Create a fresh knowledge base for each test."""
        self.al3 = AdviceLogic3()
    
    def test_add_and_query_fact(self):
        """Test adding and querying simple facts."""
        self.al3.add_fact("parent(john, mary)")
        
        solutions = self.al3.query("parent(john, mary)")
        self.assertTrue(len(solutions) > 0)
    
    def test_query_nonexistent_fact(self):
        """Test querying facts that don't exist."""
        self.al3.add_fact("parent(john, mary)")
        
        solutions = self.al3.query("parent(jane, alice)")
        self.assertEqual(len(solutions), 0)
    
    def test_multiple_facts(self):
        """Test adding and querying multiple facts."""
        self.al3.add_fact("weather(sunny)")
        self.al3.add_fact("weather(rainy)")
        self.al3.add_fact("weather(overcast)")
        
        sunny = self.al3.query("weather(sunny)")
        rainy = self.al3.query("weather(rainy)")
        overcast = self.al3.query("weather(overcast)")
        
        self.assertTrue(len(sunny) > 0)
        self.assertTrue(len(rainy) > 0)
        self.assertTrue(len(overcast) > 0)


class TestAdviceLogic3Rules(unittest.TestCase):
    """Test rule creation and inference."""
    
    def setUp(self):
        """Create knowledge base with facts and rules."""
        self.al3 = AdviceLogic3()
        
        # Add facts
        self.al3.add_fact("weather(sunny)")
        self.al3.add_fact("weather(rainy)")
        self.al3.add_fact("temperature(mild)")
        self.al3.add_fact("temperature(hot)")
    
    def test_simple_rule(self):
        """Test inference with a simple rule."""
        self.al3.add_rule("good_weather(X)", ["weather(X)"])
        
        # Should derive good_weather(sunny) from weather(sunny)
        solutions = self.al3.query("good_weather(sunny)")
        self.assertTrue(len(solutions) > 0)
    
    def test_rule_with_constant(self):
        """Test rule with constant conclusions."""
        self.al3.add_rule("good_day", ["weather(sunny)"])
        
        solutions = self.al3.query("good_day")
        self.assertTrue(len(solutions) > 0)
    
    def test_multi_premise_rule(self):
        """Test rule with multiple premises."""
        self.al3.add_rule(
            "good_conditions",
            ["weather(sunny)", "temperature(mild)"]
        )
        
        # Should succeed when all premises are true
        solutions = self.al3.query("good_conditions")
        self.assertTrue(len(solutions) > 0)


class TestAdviceLogic3Recommendations(unittest.TestCase):
    """Test recommendation functionality."""
    
    def setUp(self):
        """Create recommendation system."""
        self.al3 = AdviceLogic3()
    
    def test_recommend_true(self):
        """Test positive recommendation."""
        self.al3.add_fact("weather(sunny)")
        self.al3.add_rule("go_outside", ["weather(sunny)"])
        
        result = self.al3.recommend("go_outside")
        self.assertTrue(result)
    
    def test_recommend_false(self):
        """Test negative recommendation."""
        self.al3.add_fact("weather(rainy)")
        self.al3.add_rule("go_outside", ["weather(sunny)"])
        
        result = self.al3.recommend("go_outside")
        self.assertFalse(result)
    
    def test_recommend_complex(self):
        """Test recommendation with complex rules."""
        self.al3.add_fact("weather(sunny)")
        self.al3.add_fact("temperature(mild)")
        self.al3.add_fact("wind(calm)")
        
        self.al3.add_rule(
            "perfect_day",
            ["weather(sunny)", "temperature(mild)", "wind(calm)"]
        )
        
        result = self.al3.recommend("perfect_day")
        self.assertTrue(result)


class TestAdviceLogic3Default(unittest.TestCase):
    """Test default knowledge base."""
    
    def setUp(self):
        """Create default knowledge base."""
        self.kb = create_default_kb()
    
    def test_default_kb_has_facts(self):
        """Test that default KB contains facts."""
        self.assertTrue(len(self.kb.kb.facts) > 0)
    
    def test_default_kb_has_rules(self):
        """Test that default KB contains rules."""
        self.assertTrue(len(self.kb.kb.rules) > 0)
    
    def test_weather_facts_exist(self):
        """Test that weather facts exist."""
        solutions = self.kb.query("weather(sunny)")
        self.assertTrue(len(solutions) > 0)
    
    def test_good_weather_inference(self):
        """Test inference of good weather."""
        solutions = self.kb.query("good_weather(sunny)")
        self.assertTrue(len(solutions) > 0)
    
    def test_bad_weather_inference(self):
        """Test that rainy is not good weather."""
        solutions = self.kb.query("good_weather(rainy)")
        self.assertEqual(len(solutions), 0)
    
    def test_acceptable_wind(self):
        """Test wind condition evaluation."""
        solutions = self.kb.query("acceptable_wind_strength(calm)")
        self.assertTrue(len(solutions) > 0)
    
    def test_unacceptable_wind(self):
        """Test that strong wind is not acceptable."""
        solutions = self.kb.query("acceptable_wind_strength(strong)")
        self.assertEqual(len(solutions), 0)


class TestAdviceLogic3TennisScenario(unittest.TestCase):
    """Test tennis-specific scenarios."""
    
    def setUp(self):
        """Create tennis recommendation system."""
        self.al3 = AdviceLogic3()
        
        # Setup tennis conditions
        self.al3.add_fact("weather(sunny)")
        self.al3.add_fact("temperature(mild)")
        self.al3.add_fact("wind(calm)")
        self.al3.add_fact("court_available(grass)")
        
        # Tennis rules
        self.al3.add_rule("good_weather(sunny)", [])
        self.al3.add_rule("good_weather(overcast)", [])
        
        self.al3.add_rule(
            "should_play",
            ["weather(sunny)", "temperature(mild)"]
        )
        
        self.al3.add_rule(
            "ideal_conditions",
            ["should_play", "wind(calm)", "court_available(grass)"]
        )
    
    def test_should_play_sunny_mild(self):
        """Test that should play in sunny, mild weather."""
        result = self.al3.recommend("should_play")
        self.assertTrue(result)
    
    def test_ideal_tennis_conditions(self):
        """Test ideal conditions for tennis."""
        result = self.al3.recommend("ideal_conditions")
        self.assertTrue(result)


class TestAdviceLogic3DomainSpecific(unittest.TestCase):
    """Test domain-specific applications."""
    
    def test_medical_diagnosis(self):
        """Test medical diagnosis scenario."""
        al3 = AdviceLogic3()
        
        # Patient facts
        al3.add_fact("symptom(fever)")
        al3.add_fact("symptom(cough)")
        al3.add_fact("symptom(headache)")
        
        # Diagnostic rules
        al3.add_rule("possible_cold", ["symptom(cough)", "symptom(fever)"])
        al3.add_rule("possible_flu", 
                     ["symptom(fever)", "symptom(cough)", "symptom(headache)"])
        
        # Check diagnoses
        self.assertTrue(al3.recommend("possible_cold"))
        self.assertTrue(al3.recommend("possible_flu"))
    
    def test_business_decision(self):
        """Test business decision scenario."""
        al3 = AdviceLogic3()
        
        # Business factors
        al3.add_fact("budget_available(true)")
        al3.add_fact("market_demand(high)")
        al3.add_fact("resource_availability(sufficient)")
        
        # Decision rules
        al3.add_rule(
            "launch_product",
            ["budget_available(true)", "market_demand(high)"]
        )
        
        al3.add_rule(
            "go_ahead",
            ["launch_product", "resource_availability(sufficient)"]
        )
        
        self.assertTrue(al3.recommend("launch_product"))
        self.assertTrue(al3.recommend("go_ahead"))
    
    def test_activity_recommendation(self):
        """Test activity recommendation scenario."""
        al3 = AdviceLogic3()
        
        # Conditions
        al3.add_fact("time(morning)")
        al3.add_fact("weather(sunny)")
        al3.add_fact("energy_level(high)")
        
        # Activity rules
        al3.add_rule(
            "good_for_exercise",
            ["time(morning)", "energy_level(high)"]
        )
        
        al3.add_rule(
            "good_for_outdoor_run",
            ["good_for_exercise", "weather(sunny)"]
        )
        
        self.assertTrue(al3.recommend("good_for_exercise"))
        self.assertTrue(al3.recommend("good_for_outdoor_run"))


if __name__ == "__main__":
    unittest.main()
