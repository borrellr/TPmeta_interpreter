def test_variable():
    """Test the Variable class for term representation."""
    from logical_engine.terms import Variable, Term
    
    # Test 1: Basic instantiation
    var = Variable("X")
    assert var.name == "X", "Variable should store the name"
    assert isinstance(var, Variable), "Should be instance of Variable"
    assert isinstance(var, Term), "Variable should inherit from Term"
    
    # Test 2: Different variable names (uppercase)
    var1 = Variable("A")
    var2 = Variable("Z")
    assert var1.name == "A", "Should store uppercase variable"
    assert var2.name == "Z", "Should store uppercase variable"
    
    # Test 3: Different variable names (lowercase - valid for some logic systems)
    var3 = Variable("x")
    var4 = Variable("abc")
    assert var3.name == "x", "Should store lowercase variable"
    assert var4.name == "abc", "Should store multi-character variable"
    
    # Test 4: Variable names with numbers
    var5 = Variable("X1")
    var6 = Variable("Var2")
    assert var5.name == "X1", "Should allow variables with numbers"
    assert var6.name == "Var2", "Should allow multi-char variables with numbers"
    
    # Test 5: Variable names with underscores
    var7 = Variable("_X")
    var8 = Variable("my_var")
    assert var7.name == "_X", "Should allow underscore prefix"
    assert var8.name == "my_var", "Should allow underscores in name"
    
    # Test 6: Single character variables
    for char in "ABCXYZ":
        var = Variable(char)
        assert var.name == char, f"Should create variable {char}"
    
    # Test 7: Empty string variable (edge case)
    var_empty = Variable("")
    assert var_empty.name == "", "Should allow empty string as variable name"
    
    # Test 8: Variable with special characters
    var_special = Variable("X'")
    assert var_special.name == "X'", "Should allow apostrophes in variable name"
    
    # Test 9: Very long variable names
    long_name = "VeryLongVariableNameWithManyCharacters123"
    var_long = Variable(long_name)
    assert var_long.name == long_name, "Should handle long variable names"
    
    # Test 10: Variable equality (object identity)
    var_a = Variable("X")
    var_b = Variable("X")
    assert var_a is not var_b, "Different instances should not be identical"
    assert var_a.name == var_b.name, "Variables with same name should have equal names"
    
    # Test 11: Variable inequality
    var_x = Variable("X")
    var_y = Variable("Y")
    assert var_x.name != var_y.name, "Variables with different names should have different names"
    
    # Test 12: Variable name can be modified after creation
    var = Variable("X")
    var.name = "Y"
    assert var.name == "Y", "Should allow modification of name attribute"
    
    # Test 13: Variable type checking
    var = Variable("X")
    assert type(var).__name__ == "Variable", "Type name should be Variable"
    assert hasattr(var, "name"), "Variable should have 'name' attribute"
    
    # Test 14: Multiple variables with different names in list
    vars_list = [Variable("X"), Variable("Y"), Variable("Z")]
    names = [v.name for v in vars_list]
    assert names == ["X", "Y", "Z"], "Should create multiple variables correctly"
    
    # Test 15: Variable in set (hashability - may or may not work depending on implementation)
    var1 = Variable("X")
    var2 = Variable("Y")
    # Note: This test will pass/fail depending on whether Variable implements __hash__
    try:
        var_set = {var1, var2}
        assert len(var_set) == 2, "Should be able to add variables to set"
    except TypeError:
        # Variable may not be hashable, which is acceptable
        pass
    
    # Test 16: Variable string representation (using repr)
    var = Variable("X")
    var_repr = repr(var) if hasattr(var, '__repr__') else str(var)
    assert "Variable" in var_repr or "X" in var_repr, "String representation should contain Variable or name"
    
    # Test 17: Variable comparison with other types
    var = Variable("X")
    assert var != "X", "Variable should not equal a string with same name"
    assert var != 42, "Variable should not equal other types"
    
    # Test 18: Variable passed through function
    def get_var_name(v):
        return v.name
    
    var = Variable("TestVar")
    result = get_var_name(var)
    assert result == "TestVar", "Should retrieve variable name through function"
    
    # Test 19: Variable copy behavior
    import copy
    var1 = Variable("X")
    var2 = copy.copy(var1)
    assert var2.name == var1.name, "Copy should preserve name"
    var2.name = "Y"
    assert var1.name == "X", "Modifying copy should not affect original"
    
    # Test 20: Variable with numeric string names
    var_num = Variable("123")
    assert var_num.name == "123", "Should allow purely numeric string names"
    
    # Test 21: Multiple references to same variable object
    var = Variable("X")
    var1 = var
    var2 = var
    assert var1 is var2, "References should point to same object"
    assert var1.name == var2.name == "X", "All references should have same name"
    
    # Test 22: Variable attribute access
    var = Variable("Foo")
    assert getattr(var, "name") == "Foo", "Should support getattr access"
    
    # Test 23: Direction distinction (common in some systems)
    var_input = Variable("In_X")
    var_output = Variable("Out_Y")
    assert var_input.name != var_output.name, "Variables with different naming conventions should be distinct"
    
    # Test 24: Anonymous variable patterns
    var_anon1 = Variable("_")
    var_anon2 = Variable("_")
    assert var_anon1.name == var_anon2.name, "Anonymous variables should have same name pattern"
    assert var_anon1 is not var_anon2, "Anonymous variables should be different instances"
    
    print("All test_variable tests passed!")
