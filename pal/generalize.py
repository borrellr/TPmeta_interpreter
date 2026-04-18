"""
Generalization Algorithm for PAL System
Functional implementation of the Generalize algorithm for inductive logic programming.
"""

from typing import List, Set, Optional, Dict, Any
import sys
import os

# Add the logical_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logical_engine.terms import Variable, Constant, Function
from logical_engine.horn_clauses import Fact, Rule, KnowledgeBase
from logical_engine.parser import parse_term
from rlgg_ilp.rlgg_ilp import RLGGSystem, Clause, term_to_string


class GeneralizationSystem:
    """
    System for generalizing concepts using domain theory expansion and LGG.
    """

    def __init__(self, background_kb: Optional[KnowledgeBase] = None):
        self.background_kb = background_kb or KnowledgeBase()
        self.rlgg_system = RLGGSystem(self.background_kb)
        self.variable_counter = 0

    def fresh_variable(self, prefix: str = "X") -> str:
        """Generate a fresh variable name."""
        self.variable_counter += 1
        return f"{prefix}{self.variable_counter}"

    def derive_atoms(self, domain: Set[str], new_example: Clause) -> List[str]:
        """
        Derive atoms from the domain theory and new example.
        This is a simplified implementation - in practice, this would
        use theorem proving or background knowledge inference.
        """
        # For demonstration, derive some basic atoms from the example
        atoms = []

        # Parse the example
        if '(' in new_example.head:
            pred_name = new_example.head.split('(')[0]
            args = [arg.strip() for arg in new_example.head.split('(')[1].rstrip(')').split(',')]

            # Generate derived atoms based on common patterns
            if pred_name == "parent":
                # Derive ancestor relationships
                atoms.extend([
                    f"ancestor({args[0]}, {args[1]})",
                    f"person({args[0]})",
                    f"person({args[1]})"
                ])
            elif pred_name == "ancestor":
                atoms.extend([
                    f"person({args[0]})",
                    f"person({args[1]})"
                ])

        # Add atoms from domain
        atoms.extend(list(domain))

        return list(set(atoms))  # Remove duplicates

    def construct_head_from_input_predicates(self, new_example: Clause) -> str:
        """
        Construct the head predicate from the input example.
        """
        # For simplicity, use the same predicate but with variables
        if '(' in new_example.head:
            pred_name = new_example.head.split('(')[0]
            args_part = new_example.head.split('(')[1].rstrip(')')
            args = args_part.split(',')

            # Replace constants with variables
            var_args = [self.fresh_variable() for _ in args]
            return f"{pred_name}({', '.join(var_args)})"

        return new_example.head

    def lgg(self, clause1: Clause, clause2: Clause) -> Optional[Clause]:
        """
        Compute the Least General Generalization of two clauses.
        Handles mixed fact/rule cases and different body lengths.
        """
        # If one is a fact and one is a rule, the generalization is the rule
        if clause1.is_fact() and clause2.is_rule():
            return clause2
        elif clause2.is_fact() and clause1.is_rule():
            return clause1

        # Both are facts - use standard LGG
        if clause1.is_fact() and clause2.is_fact():
            return self.rlgg_system.relative_lgg(clause1, clause2)

        # Both are rules - if same body length, use standard LGG
        if len(clause1.body) == len(clause2.body):
            return self.rlgg_system.relative_lgg(clause1, clause2)

        # Different body lengths - combine bodies (simplified approach)
        head_lgg = self.rlgg_system.lgg_terms(clause1.parse_head(), clause2.parse_head())
        if head_lgg is None:
            return None

        # Combine all body literals
        combined_body = list(set(clause1.body + clause2.body))
        return Clause(term_to_string(head_lgg), combined_body)

    def remove_unused_head_variables(self, clause: Clause) -> Clause:
        """
        Remove head variables that are not used in the body or feature definitions.
        This is a simplified implementation.
        """
        if clause.is_fact():
            return clause

        # Parse head to get variables
        head_vars = set()
        if '(' in clause.head:
            args_part = clause.head.split('(')[1].rstrip(')')
            args = args_part.split(',')
            for arg in args:
                arg = arg.strip()
                if arg.startswith(('X', 'Y', 'Z')):  # Simple variable detection
                    head_vars.add(arg)

        # Check which variables are used in body
        used_vars = set()
        for literal in clause.body:
            if '(' in literal:
                args_part = literal.split('(')[1].rstrip(')')
                args = args_part.split(',')
                for arg in args:
                    arg = arg.strip()
                    if arg in head_vars:
                        used_vars.add(arg)

        # If all head variables are used, return as-is
        if head_vars.issubset(used_vars) or not used_vars:
            return clause

        # Otherwise, create a new head with only used variables
        # This is simplified - in practice, would need more sophisticated logic
        return clause

    def remove_isolated_variable_literals(self, clause: Clause) -> Clause:
        """
        Remove literals containing variables that appear nowhere else.
        """
        if clause.is_fact():
            return clause

        # Collect all variables used in the clause
        all_vars = set()

        # Variables in head
        if '(' in clause.head:
            args_part = clause.head.split('(')[1].rstrip(')')
            args = args_part.split(',')
            for arg in args:
                arg = arg.strip()
                if arg.startswith(('X', 'Y', 'Z')):
                    all_vars.add(arg)

        # Variables in body
        for literal in clause.body:
            if '(' in literal:
                args_part = literal.split('(')[1].rstrip(')')
                args = args_part.split(',')
                for arg in args:
                    arg = arg.strip()
                    if arg.startswith(('X', 'Y', 'Z')):
                        all_vars.add(arg)

        # Check each body literal
        filtered_body = []
        for literal in clause.body:
            literal_vars = set()
            if '(' in literal:
                args_part = literal.split('(')[1].rstrip(')')
                args = args_part.split(',')
                for arg in args:
                    arg = arg.strip()
                    if arg.startswith(('X', 'Y', 'Z')):
                        literal_vars.add(arg)

            # Keep literal if all its variables appear elsewhere
            if literal_vars.issubset(all_vars - literal_vars):
                filtered_body.append(literal)

        return Clause(clause.head, filtered_body)


def generalize(new_example: Clause, feature_definitions: Set[str],
               current_concept: Clause, gen_system: GeneralizationSystem) -> Optional[Clause]:
    """
    FUNCTION Generalize(new_example, feature_definitions, current_concept):

        // Expand domain theory with the new example
        domain ← feature_definitions ∪ {new_example}

        // Build clause from derived atoms
        body ← DeriveAtoms(domain, new_example)
        head ← ConstructHeadFromInputPredicates(new_example)

        new_clause ← (head ← body)

        // Compute LGG with current concept clause
        generalized_clause ← LGG(new_clause, current_concept)

        // Remove head variables not used in Fi or move predicates
        generalized_clause ← RemoveUnusedHeadVariables(generalized_clause)

        // Remove literals containing variables that appear nowhere else
        generalized_clause ← RemoveIsolatedVariableLiterals(generalized_clause)

        RETURN generalized_clause
    END FUNCTION
    """

    # Expand domain theory with the new example
    domain = feature_definitions | {str(new_example)}

    # Build clause from derived atoms
    body = gen_system.derive_atoms(domain, new_example)
    head = gen_system.construct_head_from_input_predicates(new_example)

    # If current_concept is a fact, create a rule with the derived atoms
    # If current_concept is a rule, combine bodies
    if current_concept.is_fact():
        new_clause = Clause(head, body)
    else:
        # Combine bodies from both clauses
        combined_body = list(set(current_concept.body + body))
        new_clause = Clause(head, combined_body)

    # Compute LGG with current concept clause
    generalized_clause = gen_system.lgg(new_clause, current_concept)

    if generalized_clause is None:
        return None

    # Remove head variables not used in Fi or move predicates
    generalized_clause = gen_system.remove_unused_head_variables(generalized_clause)

    # Remove literals containing variables that appear nowhere else
    generalized_clause = gen_system.remove_isolated_variable_literals(generalized_clause)

    return generalized_clause


def main():
    """Example usage of the Generalize algorithm."""
    print("Generalization Algorithm for PAL System")
    print("=" * 40)

    # Create background knowledge
    bk = KnowledgeBase()
    bk.add_fact(Fact("parent(john, mary)"))
    bk.add_fact(Fact("parent(mary, alice)"))

    # Create generalization system
    gen_system = GeneralizationSystem(background_kb=bk)

    # Feature definitions
    feature_definitions = {
        "person(john)",
        "person(mary)",
        "person(alice)"
    }

    # Current concept (learned so far)
    current_concept = Clause("parent(X1, X2)")

    # New example to generalize with
    new_example = Clause("parent(mary, alice)")

    # Generalize
    generalized_clause = generalize(new_example, feature_definitions,
                                   current_concept, gen_system)

    if generalized_clause:
        print(f"Generalized clause: {generalized_clause}")
    else:
        print("Could not generalize the clauses")


if __name__ == "__main__":
    main()