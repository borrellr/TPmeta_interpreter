def test_modus_ponens():
    """Test the modus_ponens inference rule."""
    from logical_engine.inference import modus_ponens
    
    # Test 1: Basic valid modus ponens
    p = "it_is_raining"
    implies_p_q = {'premise': 'it_is_raining', 'conclusion': 'the_ground_is_wet'}
    result = modus_ponens(p, implies_p_q)
    assert result == 'the_ground_is_wet', "Should return the conclusion when premise matches"
    
    # Test 2: Premise does not match
    p = "it_is_sunny"
    implies_p_q = {'premise': 'it_is_raining', 'conclusion': 'the_ground_is_wet'}
    result = modus_ponens(p, implies_p_q)
    assert result is None, "Should return None when premise doesn't match"
    
    # Test 3: Implication with complex propositions
    p = "bird(X)"
    implies_p_q = {'premise': 'bird(X)', 'conclusion': 'has_wings(X)'}
    result = modus_ponens(p, implies_p_q)
    assert result == 'has_wings(X)', "Should handle parameterized propositions"
    
    # Test 4: Invalid implication structure (not a dict)
    p = "it_is_raining"
    result = modus_ponens(p, "not_a_dict")
    assert result is None, "Should return None for non-dict implication"
    
    # Test 5: Implication dict missing 'premise' key
    p = "it_is_raining"
    implies_p_q = {'conclusion': 'the_ground_is_wet'}
    result = modus_ponens(p, implies_p_q)
    assert result is None, "Should return None when implication has no premise"
    
    # Test 6: Implication dict missing 'conclusion' key
    p = "it_is_raining"
    implies_p_q = {'premise': 'it_is_raining'}
    result = modus_ponens(p, implies_p_q)
    assert result is None, "Should return None when implication has no conclusion"
    
    # Test 7: Empty strings
    p = ""
    implies_p_q = {'premise': '', 'conclusion': 'something'}
    result = modus_ponens(p, implies_p_q)
    assert result == 'something', "Should work with empty string propositions"
    
    # Test 8: None as proposition
    p = None
    implies_p_q = {'premise': None, 'conclusion': 'result'}
    result = modus_ponens(p, implies_p_q)
    assert result == 'result', "Should work when premise is None"
    
    # Test 9: Numeric propositions
    p = 42
    implies_p_q = {'premise': 42, 'conclusion': 84}
    result = modus_ponens(p, implies_p_q)
    assert result == 84, "Should work with numeric values"
    
    # Test 10: Case sensitivity
    p = "IsRaining"
    implies_p_q = {'premise': 'israining', 'conclusion': 'wet'}
    result = modus_ponens(p, implies_p_q)
    assert result is None, "String matching should be case-sensitive"
    
    # Test 11: Complex nested structure
    p = {'type': 'predicate', 'name': 'likes'}
    implies_p_q = {
        'premise': {'type': 'predicate', 'name': 'likes'},
        'conclusion': {'type': 'fact', 'value': 'happy'}
    }
    result = modus_ponens(p, implies_p_q)
    assert result == {'type': 'fact', 'value': 'happy'}, "Should work with dict propositions"
    
    print("All modus_ponens tests passed!")
