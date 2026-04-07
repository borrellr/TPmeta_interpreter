def test_meta_interpreter():
    """Test the meta-interpreter solve and prove functions."""
    from logical_engine.meta_interpreter import solve, solve_goals, apply_substitution, prove
    from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
    from logical_engine.unification import Substitution
    
    # Test 1: Query a simple fact
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    
    solutions = list(solve("parent(john, mary)", kb))
    assert len(solutions) == 1, "Should find exactly one solution for a matching fact"
    assert isinstance(solutions[0], Substitution), "Solution should be a Substitution object"
    
    # Test 2: Query that doesn't match any facts
    solutions = list(solve("parent(john, bob)", kb))
    assert len(solutions) == 0, "Should find no solutions for non-matching facts"
    
    # Test 3: Simple rule with a single subgoal
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_rule(Rule("child(X, Y)", ["parent(Y, X)"]))
    
    solutions = list(solve("child(mary, john)", kb))
    assert len(solutions) == 1, "Should find one solution using a simple rule"
    
    # Test 4: Rule with multiple subgoals (conjunction)
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_fact(Fact("parent(john, bob)"))
    kb.add_fact(Fact("sibling(mary, bob)"))
    kb.add_rule(Rule("siblings(X, Y)", ["parent(john, X)", "parent(john, Y)"]))
    
    solutions = list(solve("siblings(mary, bob)", kb))
    assert len(solutions) > 0, "Should find solutions with multiple subgoals"
    
    # Test 5: Rule chain (transitive rules)
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_fact(Fact("parent(mary, alice)"))
    kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Y)"]))
    kb.add_rule(Rule("ancestor(X, Y)", ["parent(X, Z)", "ancestor(Z, Y)"]))
    
    solutions = list(solve("ancestor(john, alice)", kb))
    assert len(solutions) > 0, "Should find transitive solutions through rule chains"
    
    # Test 6: Multiple solutions from different facts
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_fact(Fact("parent(john, bob)"))
    kb.add_rule(Rule("child(X, Y)", ["parent(Y, X)"]))
    
    solutions = list(solve("child(X, john)", kb))
    assert len(solutions) == 2, "Should find multiple solutions for different facts"
    
    # Test 7: apply_substitution with string terms
    subst = Substitution({'X': 'john', 'Y': 'mary'})
    result = apply_substitution("parent(X, Y)", subst)
    assert result == "parent(john, mary)", "Should apply substitutions to string terms"
    
    # Test 8: apply_substitution with partial matches
    subst = Substitution({'X': 'john'})
    result = apply_substitution("parent(X, Y)", subst)
    assert 'john' in result, "Should apply available substitutions"
    assert 'Y' in result, "Should leave unbound variables unchanged"
    
    # Test 9: Empty knowledge base
    kb = KnowledgeBase()
    solutions = list(solve("anything(X)", kb))
    assert len(solutions) == 0, "Should find no solutions in empty knowledge base"
    
    # Test 10: solve_goals with empty goal list
    kb = KnowledgeBase()
    subst = Substitution()
    solutions = list(solve_goals([], kb, subst))
    assert len(solutions) == 1, "Should succeed with empty goal list"
    assert solutions[0] == subst, "Should return the same substitution with no goals"
    
    # Test 11: solve_goals with single goal
    kb = KnowledgeBase()
    kb.add_fact(Fact("fact(a)"))
    subst = Substitution()
    solutions = list(solve_goals(["fact(a)"], kb, subst))
    assert len(solutions) == 1, "Should solve single goal correctly"
    
    # Test 12: solve_goals with multiple goals
    kb = KnowledgeBase()
    kb.add_fact(Fact("fact(a)"))
    kb.add_fact(Fact("fact(b)"))
    subst = Substitution()
    solutions = list(solve_goals(["fact(a)", "fact(b)"], kb, subst))
    assert len(solutions) == 1, "Should solve conjunction of goals"
    
    # Test 13: prove creates proof tree
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    
    proofs = prove("parent(john, mary)", kb)
    assert len(proofs) > 0, "Should create at least one proof"
    assert proofs[0]['source'] == 'fact', "Proof should identify fact source"
    assert proofs[0]['goal'] == 'parent(john, mary)', "Proof should contain the goal"
    
    # Test 14: prove with rules
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_rule(Rule("child(X, Y)", ["parent(Y, X)"]))
    
    proofs = prove("child(mary, john)", kb)
    assert len(proofs) > 0, "Should create proofs through rules"
    
    # Test 15: Complex knowledge base with multiple rules and facts
    kb = KnowledgeBase()
    kb.add_fact(Fact("parent(john, mary)"))
    kb.add_fact(Fact("parent(mary, alice)"))
    kb.add_fact(Fact("male(john)"))
    kb.add_fact(Fact("female(mary)"))
    kb.add_rule(Rule("father(X, Y)", ["parent(X, Y)", "male(X)"]))
    kb.add_rule(Rule("mother(X, Y)", ["parent(X, Y)", "female(X)"]))
    
    solutions = list(solve("father(john, mary)", kb))
    assert len(solutions) > 0, "Should solve complex queries with multiple rule conditions"
    
    solutions = list(solve("mother(mary, alice)", kb))
    assert len(solutions) > 0, "Should solve different complex queries"
    
    print("All meta_interpreter tests passed!")
