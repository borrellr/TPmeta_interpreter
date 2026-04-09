"""
Golem ILP System - Usage Examples

Demonstrates learning with Golem on family relations and other domains.
"""

from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from golem_learner import GolemLearner, Example


def example_family_relations():
    """
    Learn family relations using Golem.
    
    Background knowledge includes parent relationships.
    Task: Learn 'grandparent' relation from positive examples.
    """
    print("\n" + "="*60)
    print("EXAMPLE 1: Family Relations (Grandparent)")
    print("="*60)
    
    # Create knowledge base with family facts
    kb = KnowledgeBase()
    
    # Facts: parent(X, Y) relations
    facts = [
        "parent(john, mary)",
        "parent(john, tom)",
        "parent(mary, alice)",
        "parent(mary, bob)",
        "parent(tom, charlie)",
        "parent(alice, diana)",
    ]
    
    for fact in facts:
        kb.add_fact(Fact(fact))
    
    # Additional rules (background theory)
    kb.add_rule(Rule("child(X, Y)", ["parent(Y, X)"]))
    kb.add_rule(Rule("sibling(X, Y)", ["parent(Z, X)", "parent(Z, Y)"]))
    
    # Positive examples: grandparent relationships
    positive_examples = [
        Example("grandparent(john, alice)"),
        Example("grandparent(john, bob)"),
        Example("grandparent(john, charlie)"),
        Example("grandparent(mary, diana)"),
    ]
    
    # Learn the grandparent relation
    learner = GolemLearner(kb, max_clause_length=2, verbose=True)
    learned_rules = learner.learn(positive_examples, "grandparent")
    
    learner.print_learned_rules()
    
    # Test the learned rules
    print("\n=== Testing Learned Rules ===")
    learned_kb = kb  # Add learned rules to KB
    for rule in learned_rules:
        learned_kb.add_rule(rule.to_horn_clause())
    
    from logical_engine.meta_interpreter import solve
    test_queries = [
        "grandparent(john, alice)",
        "grandparent(mary, diana)",
        "grandparent(john, diana)",
    ]
    
    for query in test_queries:
        solutions = list(solve(query, learned_kb))
        print(f"Query: {query}")
        print(f"  Result: {'Yes' if solutions else 'No'}")


def example_simple_pattern():
    """
    Learn a simple pattern from positive examples.
    """
    print("\n" + "="*60)
    print("EXAMPLE 2: Simple Pattern Learning")
    print("="*60)
    
    kb = KnowledgeBase()
    
    # Add some background facts
    kb.add_fact(Fact("color(apple, red)"))
    kb.add_fact(Fact("color(banana, yellow)"))
    kb.add_fact(Fact("color(grass, green)"))
    kb.add_fact(Fact("shape(apple, round)"))
    kb.add_fact(Fact("shape(ball, round)"))
    kb.add_fact(Fact("shape(cube, cube)"))
    
    # Positive examples for "round objects"
    positive_examples = [
        Example("round(apple)"),
        Example("round(ball)"),
    ]
    
    # Learn what makes something round
    learner = GolemLearner(kb, max_clause_length=1, verbose=True)
    learned_rules = learner.learn(positive_examples, "round")
    
    learner.print_learned_rules()


def example_ancestor_chain():
    """
    Learn ancestor relation from positive examples.
    """
    print("\n" + "="*60)
    print("EXAMPLE 3: Ancestor Relation")
    print("="*60)
    
    kb = KnowledgeBase()
    
    # Parent relationships across generations
    kb.add_fact(Fact("parent(adam, ben)"))
    kb.add_fact(Fact("parent(ben, carl)"))
    kb.add_fact(Fact("parent(carl, david)"))
    kb.add_fact(Fact("parent(alice, ben)"))
    kb.add_fact(Fact("parent(ben, emily)"))
    
    # Positive examples: ancestor relationships
    positive_examples = [
        Example("ancestor(adam, ben)"),
        Example("ancestor(adam, carl)"),
        Example("ancestor(adam, david)"),
        Example("ancestor(ben, carl)"),
        Example("ancestor(ben, david)"),
        Example("ancestor(ben, emily)"),
        Example("ancestor(carl, david)"),
    ]
    
    # Learn the ancestor relation
    learner = GolemLearner(kb, max_clause_length=2, verbose=True)
    learned_rules = learner.learn(positive_examples, "ancestor")
    
    learner.print_learned_rules()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("GOLEM ILP SYSTEM - EXAMPLES")
    print("Muggleton and Feng's Inductive Logic Programming System")
    print("="*60)
    
    # Run examples
    example_family_relations()
    example_simple_pattern()
    example_ancestor_chain()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60)
