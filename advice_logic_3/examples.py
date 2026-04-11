"""
Examples and Use Cases for Ivan Bratko's Advice Logic 3 System

Demonstrates practical applications of the horn clause-based
decision support system.
"""

from .advice_logic_3 import AdviceLogic3, create_default_kb


def example_basic_queries():
    """Basic queries demonstrating simple inference."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Queries")
    print("=" * 60)
    
    kb = create_default_kb()
    kb.print_kb()
    
    # Test basic facts
    print("Query: weather(sunny)")
    solutions = kb.query("weather(sunny)")
    print(f"  Result: {bool(solutions)} (solutions: {solutions})\n")
    
    print("Query: weather(rainy)")
    solutions = kb.query("weather(rainy)")
    print(f"  Result: {bool(solutions)} (solutions: {solutions})\n")
    
    print("Query: temperature(hot)")
    solutions = kb.query("temperature(hot)")
    print(f"  Result: {bool(solutions)} (solutions: {solutions})\n")


def example_rule_inference():
    """Demonstrate inference through rules."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Rule-Based Inference")
    print("=" * 60)
    
    kb = create_default_kb()
    
    print("Query: good_weather(sunny)")
    solutions = kb.query("good_weather(sunny)")
    print(f"  Result: {bool(solutions)}\n")
    
    print("Query: good_weather(rainy)")
    solutions = kb.query("good_weather(rainy)")
    print(f"  Result: {bool(solutions)}\n")
    
    print("Query: acceptable_wind_strength(calm)")
    solutions = kb.query("acceptable_wind_strength(calm)")
    print(f"  Result: {bool(solutions)}\n")
    
    print("Query: acceptable_wind_strength(strong)")
    solutions = kb.query("acceptable_wind_strength(strong)")
    print(f"  Result: {bool(solutions)}\n")


def example_custom_scenario():
    """Create a custom scenario with specific conditions."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Custom Scenario - Tennis Court Recommendation")
    print("=" * 60)
    
    # Build custom knowledge base
    al3 = AdviceLogic3()
    
    # Current conditions
    al3.add_fact("today_weather(sunny)")
    al3.add_fact("today_temp(mild)")
    al3.add_fact("today_wind(calm)")
    al3.add_fact("court_available(grass_court)")
    al3.add_fact("player_skill(advanced)")
    
    # Recommendation rules
    al3.add_rule(
        "should_play(today)",
        ["today_weather(sunny)", "today_wind(calm)"]
    )
    
    al3.add_rule(
        "prefer_court(grass_court)",
        ["court_available(grass_court)"]
    )
    
    al3.add_rule(
        "ideal_conditions",
        ["today_weather(sunny)", "today_temp(mild)", "today_wind(calm)"]
    )
    
    print("\nCurrent Conditions:")
    print("  Weather: sunny")
    print("  Temperature: mild")
    print("  Wind: calm")
    print("  Court: grass_court (available)")
    print("  Player Skill: advanced")
    
    print("\nQuery: should_play(today)")
    if al3.recommend("should_play(today)"):
        print("  Recommendation: ✓ YES, play today")
    else:
        print("  Recommendation: ✗ NO, don't play")
    
    print("\nQuery: prefer_court(grass_court)")
    if al3.recommend("prefer_court(grass_court)"):
        print("  Recommendation: ✓ Grass court is preferred")
    else:
        print("  Recommendation: ✗ Grass court not preferred")
    
    print("\nQuery: ideal_conditions")
    if al3.recommend("ideal_conditions"):
        print("  Recommendation: ✓ Ideal conditions!")
    else:
        print("  Recommendation: ✗ Not ideal conditions")


def example_domain_specific():
    """Example with a different domain (medical diagnosis)."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Domain-Specific Use (Medical Diagnosis Advice)")
    print("=" * 60)
    
    al3 = AdviceLogic3()
    
    # Patient facts
    al3.add_fact("symptom(fever)")
    al3.add_fact("symptom(cough)")
    al3.add_fact("symptom(fatigue)")
    
    al3.add_fact("severity(moderate)")
    al3.add_fact("duration(few_days)")
    
    # Diagnostic rules
    al3.add_rule(
        "possible_cold",
        ["symptom(cough)", "symptom(fever)"]
    )
    
    al3.add_rule(
        "caution_needed",
        ["possible_cold", "severity(moderate)"]
    )
    
    al3.add_rule(
        "consult_doctor",
        ["caution_needed", "duration(few_days)"]
    )
    
    print("\nPatient Symptoms:")
    print("  - fever")
    print("  - cough")
    print("  - fatigue")
    print("  Severity: moderate")
    print("  Duration: a few days")
    
    print("\nQuery: possible_cold")
    if al3.recommend("possible_cold"):
        print("  Diagnosis: ✓ Possible cold detected")
    
    print("\nQuery: caution_needed")
    if al3.recommend("caution_needed"):
        print("  Advice: ⚠ Caution needed with moderate severity")
    
    print("\nQuery: consult_doctor")
    if al3.recommend("consult_doctor"):
        print("  Recommendation: ✓ CONSULT A DOCTOR")


def example_multi_choice():
    """Example showing multiple choice recommendations."""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Multi-Choice Recommendations")
    print("=" * 60)
    
    al3 = AdviceLogic3()
    
    # Activity recommendations
    al3.add_fact("time(morning)")
    al3.add_fact("weather(sunny)")
    al3.add_fact("energy_level(high)")
    
    # Rules for different activities
    al3.add_rule("good_for_outdoor_exercise", ["time(morning)", "weather(sunny)"])
    al3.add_rule("good_for_sports", ["energy_level(high)", "weather(sunny)"])
    al3.add_rule("good_for_tennis", ["good_for_outdoor_exercise", "good_for_sports"])
    al3.add_rule("good_for_reading", ["weather(rainy)"])
    
    al3.add_fact("weather(sunny)")
    
    print("\nCurrent State:")
    print("  Time: morning")
    print("  Weather: sunny")
    print("  Energy: high")
    
    print("\nActivity Recommendations:")
    activities = [
        ("good_for_outdoor_exercise", "Outdoor Exercise"),
        ("good_for_sports", "Sports"),
        ("good_for_tennis", "Tennis"),
    ]
    
    for goal, activity in activities:
        if al3.recommend(goal):
            print(f"  ✓ {activity}: Recommended")
        else:
            print(f"  ✗ {activity}: Not recommended")


if __name__ == "__main__":
    # Run all examples
    example_basic_queries()
    example_rule_inference()
    example_custom_scenario()
    example_domain_specific()
    example_multi_choice()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")
