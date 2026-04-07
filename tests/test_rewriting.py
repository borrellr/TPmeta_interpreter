def test_rewrite_once():
    """Test the rewrite_once function for single rewriting step."""
    from logical_engine.rewriting import rewrite_once, RewriteRule
    from logical_engine.terms import Variable, Constant, Function
    
    # Test 1: Basic string-based rewriting
    rules = [RewriteRule("a", "b")]
    result = rewrite_once("a", rules)
    assert result == "b", "Should rewrite 'a' to 'b' with simple string rule"
    
    # Test 2: No matching rules
    rules = [RewriteRule("a", "b")]
    result = rewrite_once("c", rules)
    assert result == "c", "Should return original term if no rules match"
    
    # Test 3: First matching rule wins
    rules = [
        RewriteRule("a", "b"),
        RewriteRule("a", "c")
    ]
    result = rewrite_once("a", rules)
    assert result == "b", "Should apply first matching rule"
    
    # Test 4: Rewriting with variable substitution in RHS
    rules = [RewriteRule("f(X, X)", "g(X)")]
    result = rewrite_once("f(a, a)", rules)
    assert result == "g(a)", "Should apply substitution {X: a} to g(X)"
    
    # Test 5: Variable pattern doesn't match different values
    rules = [RewriteRule("f(X, X)", "g(X)")]
    result = rewrite_once("f(a, b)", rules)
    assert result == "f(a, b)", "Should not rewrite f(a, b) when rule requires f(X, X)"
    
    # Test 6: Rewriting Function terms with unification
    a = Constant("a")
    b = Constant("b")
    x = Variable("X")
    
    f_x_x = Function("f", [x, x])
    g_x = Function("g", [x])
    f_a_a = Function("f", [a, a])
    
    rules = [RewriteRule(f_x_x, g_x)]
    result = rewrite_once(f_a_a, rules)
    
    # Result should be g(a)
    assert isinstance(result, Function), "Result should be a Function"
    assert result.name == "g", "Function name should be 'g'"
    assert len(result.args) == 1, "Should have one argument"
    assert isinstance(result.args[0], Constant), "Argument should be a Constant"
    assert result.args[0].value == "a", "Argument should be 'a'"
    
    # Test 7: Subterm rewriting in nested functions
    rules = [RewriteRule("f(X)", "g(X)")]
    result = rewrite_once("h(f(a))", rules)
    # Should rewrite f(a) to g(a), resulting in h(g(a))
    assert result == "h(g(a))", "Should rewrite nested subterm"
    
    # Test 8: No rewriting for constants of different types
    a_const = Constant("a")
    b_const = Constant("b")
    rules = [RewriteRule(a_const, b_const)]
    result = rewrite_once(a_const, rules)
    assert isinstance(result, Constant), "Result should be a Constant"
    assert result.value == "b", "Should rewrite constant to constant"
    
    # Test 9: Empty rule list
    result = rewrite_once("a", [])
    assert result == "a", "Should return term unchanged with empty rule list"
    
    # Test 10: Variable term with matching rule
    rules = [RewriteRule(Variable("X"), Constant("a"))]
    x = Variable("X")
    result = rewrite_once(x, rules)
    assert isinstance(result, Constant), "Should unify variable with rule"
    assert result.value == "a", "Should return the RHS of the matched rule"
    
    # Test 11: Complex function rewriting with multiple arguments
    x = Variable("X")
    y = Variable("Y")
    f_x_y = Function("f", [x, y])
    g_x_y = Function("g", [x, y])
    
    f_a_b = Function("f", [Constant("a"), Constant("b")])
    rules = [RewriteRule(f_x_y, g_x_y)]
    result = rewrite_once(f_a_b, rules)
    
    assert isinstance(result, Function), "Result should be a Function"
    assert result.name == "g", "Function name should be rewritten to 'g'"
    assert len(result.args) == 2, "Should preserve argument count"
    
    # Test 12: Rewriting deep nested structures
    rules = [RewriteRule("a", "b")]
    result = rewrite_once("f(g(h(a)))", rules)
    assert "b" in str(result), "Should rewrite deeply nested subterm"
    
    # Test 13: Multiple argument rewriting with pattern
    x = Variable("X")
    f_x = Function("f", [x])
    g_x = Function("g", [x])
    h_f_x = Function("h", [f_x])
    
    nested = Function("h", [Function("f", [Constant("a")])])
    rules = [RewriteRule(f_x, g_x)]
    result = rewrite_once(nested, rules)
    
    assert isinstance(result, Function), "Result should be a Function"
    assert result.name == "h", "Outer function name should be 'h'"
    assert isinstance(result.args[0], Function), "Inner term should be a Function"
    assert result.args[0].name == "g", "Inner function should be rewritten to 'g'"
    
    # Test 14: Rule with no variables (simple constant replacement)
    rules = [RewriteRule(Function("f", []), Function("g", []))]
    f_empty = Function("f", [])
    result = rewrite_once(f_empty, rules)
    
    assert isinstance(result, Function), "Result should be a Function"
    assert result.name == "g", "Function should be rewritten to 'g'"
    
    # Test 15: String-based rules with parentheses
    rules = [RewriteRule("f(a)", "g(a)")]
    result = rewrite_once("f(a)", rules)
    assert result == "g(a)", "Should handle string-based function-like terms"
    
    # Test 16: Rewriting doesn't affect non-matching subterms
    rules = [RewriteRule("f(X)", "g(X)")]
    result = rewrite_once("h(f(a), b)", rules)
    # Should find f(a) and rewrite it to g(a)
    assert "g(a)" in str(result), "Should rewrite matching subterm"
    assert "b" in str(result), "Should preserve non-matching subterms"
    
    print("All rewrite_once tests passed!")
