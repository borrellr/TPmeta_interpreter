def test_unify_simple():
    """Test simple unification cases without complex recursion."""
    from logical_engine.unification import unify, Substitution
    from logical_engine.terms import Variable, Constant, Function
    
    # Test 1: Identical constants unify with empty substitution
    result = unify(Constant("a"), Constant("a"))
    assert result is not None, "Identical constants should unify"
    assert len(result) == 0, "Unifying identical constants should produce empty substitution"
    
    # Test 2: Different constants don't unify
    result = unify(Constant("a"), Constant("b"))
    assert result is None, "Different constants should not unify"
    
    # Test 3: Variable unifies with constant
    result = unify(Variable("X"), Constant("a"))
    assert result is not None, "Variable should unify with constant"
    assert "X" in result, "Substitution should contain variable X"
    assert isinstance(result["X"], Constant), "X should bind to a Constant"
    assert result["X"].value == "a", "X should bind to constant 'a'"
    
    # Test 4: Constant unifies with variable (symmetric)
    result = unify(Constant("a"), Variable("X"))
    assert result is not None, "Constant should unify with variable (symmetric)"
    assert "X" in result, "Substitution should contain variable X"
    assert result["X"].value == "a", "X should bind to constant 'a'"
    
    # Test 5: Variable unifies with variable
    result = unify(Variable("X"), Variable("X"))
    assert result is not None, "Identical variable should unify with itself"
    assert len(result) == 0, "Unifying variable with itself produces empty substitution"
    
    # Test 6: Different variables unify (one binds to the other)
    result = unify(Variable("X"), Variable("Y"))
    assert result is not None, "Different variables should unify"
    assert "Y" in result, "Y should be bound in substitution"
    assert isinstance(result["Y"], Variable), "Y should bind to a Variable"
    assert result["Y"].name == "X", "Y should bind to X"
    
    # Test 7: String-based unification with variables
    result = unify("X", "a")
    assert result is not None, "String variable should unify with string constant"
    assert "X" in result, "X should be in substitution"
    assert result["X"] == "a", "X should bind to 'a'"
    
    # Test 8: String-based unification with identical constants
    result = unify("a", "a")
    assert result is not None, "Identical string constants should unify"
    assert len(result) == 0, "Identical constants produce empty substitution"
    
    # Test 9: String-based unification with different constants
    result = unify("a", "b")
    assert result is None, "Different string constants should not unify"
    
    # Test 10: Empty substitution is correctly created
    result = unify("a", "a")
    assert isinstance(result, Substitution), "Result should be a Substitution"
    assert isinstance(result, dict), "Substitution should be dict-like"
    
    # Test 11: With initial substitution parameter
    initial_subst = Substitution({"X": Constant("a")})
    result = unify(Variable("X"), Constant("a"), initial_subst)
    assert result is not None, "Should unify with initial substitution"
    assert result["X"].value == "a", "Initial binding should be preserved"
    
    # Test 12: Unification respects initial substitution
    initial_subst = Substitution({"X": Constant("a")})
    result = unify(Variable("X"), Constant("b"), initial_subst)
    assert result is None, "Should fail if variable already bound to different constant"
    
    # Test 13: Function with identical structure unifies
    f_a = Function("f", [Constant("a")])
    result = unify(f_a, f_a)
    assert result is not None, "Identical function should unify with itself"
    assert len(result) == 0, "Identical functions produce empty substitution"
    
    # Test 14: Functions with different names don't unify
    f_a = Function("f", [Constant("a")])
    g_a = Function("g", [Constant("a")])
    result = unify(f_a, g_a)
    assert result is None, "Functions with different names should not unify"
    
    # Test 15: Functions with different arities don't unify
    f_a = Function("f", [Constant("a")])
    f_a_b = Function("f", [Constant("a"), Constant("b")])
    result = unify(f_a, f_a_b)
    assert result is None, "Functions with different arities should not unify"
    
    # Test 16: Function unifies variable with constant in argument
    f_x = Function("f", [Variable("X")])
    f_a = Function("f", [Constant("a")])
    result = unify(f_x, f_a)
    assert result is not None, "Function f(X) should unify with f(a)"
    assert "X" in result, "X should be in substitution"
    assert result["X"].value == "a", "X should bind to 'a'"
    
    # Test 17: Nullary function (no arguments)
    f_empty1 = Function("f", [])
    f_empty2 = Function("f", [])
    result = unify(f_empty1, f_empty2)
    assert result is not None, "Nullary functions with same name should unify"
    assert len(result) == 0, "Nullary functions produce empty substitution"
    
    # Test 18: None substitution creates fresh one
    result = unify("a", "a", None)
    assert result is not None, "Should work with None substitution"
    assert len(result) == 0, "Should produce empty substitution"
    
    # Test 19: Variable in both terms
    result = unify(Variable("X"), Variable("X"))
    assert result is not None, "Same variable should unify"
    assert "X" not in result or len(result) == 0, "Same variable doesn't create binding"
    
    # Test 20: Case-sensitive variable names
    result = unify(Variable("X"), Variable("x"))
    assert result is not None, "Different case variables should unify"
    # One should bind to the other
    assert len(result) > 0, "Different case variables should create binding"
    
    # Test 21: Numeric string unification
    result = unify("123", "123")
    assert result is not None, "Numeric strings should unify"
    
    # Test 22: Mixed variable and constant in function
    f_x_a = Function("f", [Variable("X"), Constant("a")])
    f_b_a = Function("f", [Constant("b"), Constant("a")])
    result = unify(f_x_a, f_b_a)
    assert result is not None, "Should unify with mixed args"
    assert result["X"].value == "b", "X should bind to 'b'"
    
    # Test 23: Empty function name
    f_empty_name = Function("", [Constant("a")])
    g_empty_name = Function("", [Constant("a")])
    result = unify(f_empty_name, g_empty_name)
    assert result is not None, "Empty function names should unify"
    
    # Test 24: Special characters in constant value
    special_const = Constant("a'b")
    result = unify(Variable("X"), special_const)
    assert result is not None, "Should handle special characters in constant"
    assert result["X"].value == "a'b", "Should preserve special characters"
    
    print("All test_unify_simple tests passed!")
