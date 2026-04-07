"""
Knowledge Base Loader
Provides utilities for loading facts, rules, and rewrite systems.
"""

import json
from .horn_clauses import KnowledgeBase, Fact, Rule


def load_kb_from_file(path):
    """
    Load a knowledge base from a JSON file.
    
    File format:
    {
        "facts": [
            {"head": "predicate(arg1, arg2)"},
            ...
        ],
        "rules": [
            {"head": "consequence(x)", "body": ["premise1(x)", "premise2(x)"]},
            ...
        ]
    }
    
    Args:
        path: Path to the JSON file containing the knowledge base
    
    Returns:
        KnowledgeBase: A populated knowledge base instance
    
    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not valid JSON
        ValueError: If the file format is invalid
    """
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Knowledge base file not found: {path}")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in knowledge base file: {e}", e.doc, e.pos)
    
    kb = KnowledgeBase()
    
    # Load facts
    if 'facts' in data and isinstance(data['facts'], list):
        for fact_data in data['facts']:
            if isinstance(fact_data, dict) and 'head' in fact_data:
                fact = Fact(fact_data['head'])
                kb.add_fact(fact)
            else:
                raise ValueError("Each fact must have a 'head' field")
    
    # Load rules
    if 'rules' in data and isinstance(data['rules'], list):
        for rule_data in data['rules']:
            if isinstance(rule_data, dict) and 'head' in rule_data and 'body' in rule_data:
                if isinstance(rule_data['body'], list):
                    rule = Rule(rule_data['head'], rule_data['body'])
                    kb.add_rule(rule)
                else:
                    raise ValueError("Rule 'body' must be a list of goals")
            else:
                raise ValueError("Each rule must have 'head' and 'body' fields")
    
    return kb


def save_kb_to_file(kb, path):
    """
    Save a knowledge base to a JSON file.
    
    Args:
        kb: KnowledgeBase instance to save
        path: Path to write the JSON file to
    
    Raises:
        IOError: If the file cannot be written
        AttributeError: If kb doesn't have facts and rules
    """
    data = {
        'facts': [{'head': fact.head} for fact in kb.facts],
        'rules': [{'head': rule.head, 'body': rule.body} for rule in kb.rules]
    }
    
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        raise IOError(f"Unable to write knowledge base file: {e}")


def merge_kbs(kb1, kb2):
    """
    Merge two knowledge bases into a new knowledge base.
    
    Args:
        kb1: First knowledge base
        kb2: Second knowledge base
    
    Returns:
        KnowledgeBase: A new knowledge base containing all facts and rules from both
    """
    merged_kb = KnowledgeBase()
    
    # Add all facts from both knowledge bases
    for fact in kb1.facts:
        merged_kb.add_fact(fact)
    for fact in kb2.facts:
        merged_kb.add_fact(fact)
    
    # Add all rules from both knowledge bases
    for rule in kb1.rules:
        merged_kb.add_rule(rule)
    for rule in kb2.rules:
        merged_kb.add_rule(rule)
    
    return merged_kb


def filter_kb_by_predicate(kb, predicate_name):
    """
    Filter a knowledge base to contain only facts and rules with a specific predicate.
    
    Args:
        kb: Knowledge base to filter
        predicate_name: Name of the predicate to filter by (e.g., 'parent' in 'parent(x, y)')
    
    Returns:
        KnowledgeBase: A new filtered knowledge base
    """
    filtered_kb = KnowledgeBase()
    
    # Apply a simple name-based filter
    for fact in kb.facts:
        if predicate_name in fact.head:
            filtered_kb.add_fact(fact)
    
    for rule in kb.rules:
        # Include rule if head matches predicate or any body goal matches
        if predicate_name in rule.head or any(predicate_name in goal for goal in rule.body):
            filtered_kb.add_rule(rule)
    
    return filtered_kb
