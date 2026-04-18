"""
Perturbation Method for PAL System
Functional implementation of the PerturbationMethod algorithm for generating examples.
"""

from typing import List, Optional, Set, Dict, Any
import sys
import os

# Add the logical_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logical_engine.terms import Variable, Constant, Function
from logical_engine.horn_clauses import Fact, Rule, KnowledgeBase
from logical_engine.parser import parse_term
from rlgg_ilp.rlgg_ilp import RLGGSystem, Clause


class PerturbationSystem:
    """
    System for generating perturbed examples using different perturbation classes.
    """

    def __init__(self, background_kb: Optional[KnowledgeBase] = None):
        self.background_kb = background_kb or KnowledgeBase()
        self.variable_counter = 0

    def fresh_variable(self, prefix: str = "X") -> str:
        """Generate a fresh variable name."""
        self.variable_counter += 1
        return f"{prefix}{self.variable_counter}"

    def generate_failing_example(self, clause: Clause, perturbation_class: str) -> Optional[Clause]:
        """
        Try to generate an example that fails at least one literal in the clause.
        This is a simplified implementation - in practice, this would use
        domain-specific generation strategies based on the perturbation class.
        """
        # For demonstration, generate examples based on perturbation class
        if perturbation_class == "add_constraint":
            # Try to add a constraint that fails
            if clause.is_fact():
                # For facts, try to create a more specific version that might fail
                return Clause("parent(alice, bob)")  # This might not be in background
            else:
                # For rules, try to create an example that doesn't satisfy the body
                return Clause("parent(charlie, david)")

        elif perturbation_class == "remove_constraint":
            # Try to remove a constraint
            return Clause("ancestor(eve, frank)")

        elif perturbation_class == "modify_predicate":
            # Try to modify predicate arguments
            return Clause("parent(bob, alice)")  # Reversed arguments

        return None

    def literals_failed_by(self, example: Clause, clause: Clause) -> List[str]:
        """
        Return the literals in the clause that are failed by the example.
        This is a simplified check - in practice, would use theorem proving.
        """
        failed_literals = []

        if clause.is_fact():
            # For facts, check if the example matches the fact
            if example.head != clause.head:
                failed_literals.append(clause.head)
        else:
            # For rules, check each body literal
            for literal in clause.body:
                # Simplified check: if the literal predicate appears in the example
                if not any(literal.split('(')[0] in ex_lit for ex_lit in [example.head]):
                    failed_literals.append(literal)

        return failed_literals

    def generate_succeeding_example(self, clause: Clause, failed_literals: List[str]) -> Optional[Clause]:
        """
        Try to generate an example that succeeds on at least one of the failed literals.
        This is a simplified implementation.
        """
        if not failed_literals:
            return None

        # For demonstration, generate examples that might succeed on failed literals
        for failed_lit in failed_literals:
            pred_name = failed_lit.split('(')[0] if '(' in failed_lit else failed_lit

            if pred_name == "person":
                return Clause("person(alice)")
            elif pred_name == "ancestor":
                return Clause("ancestor(john, alice)")
            elif pred_name == "parent":
                return Clause("parent(mary, alice)")

        return None


def perturbation_method(clause: Clause, perturbation_classes: List[str],
                       pert_system: PerturbationSystem) -> Optional[Clause]:
    """
    FUNCTION PerturbationMethod(clause, perturbation_classes):

        FOR EACH class IN perturbation_classes:

            // Try to generate an example that fails at least one literal
            neg_example ← GenerateFailingExample(clause, class)

            IF neg_example ≠ NONE THEN

                failed_literals ← LiteralsFailedBy(neg_example, clause)

                // Try to generate an example that succeeds on at least one failed literal
                pos_example ← GenerateSucceedingExample(clause, failed_literals)

                IF pos_example ≠ NONE THEN
                    RETURN pos_example
                ENDIF
            ENDIF

            // If neither failing nor succeeding examples can be generated,
            // move to the next perturbation class
        END FOR

        RETURN NONE   // all classes exhausted
    END FUNCTION
    """

    for perturbation_class in perturbation_classes:
        # Try to generate an example that fails at least one literal
        neg_example = pert_system.generate_failing_example(clause, perturbation_class)

        if neg_example is not None:
            failed_literals = pert_system.literals_failed_by(neg_example, clause)

            # Try to generate an example that succeeds on at least one failed literal
            pos_example = pert_system.generate_succeeding_example(clause, failed_literals)

            if pos_example is not None:
                return pos_example

        # If neither failing nor succeeding examples can be generated,
        # move to the next perturbation class

    return None  # all classes exhausted


def main():
    """Example usage of the PerturbationMethod."""
    print("Perturbation Method for PAL System")
    print("=" * 35)

    # Create background knowledge
    bk = KnowledgeBase()
    bk.add_fact(Fact("parent(john, mary)"))
    bk.add_fact(Fact("parent(mary, alice)"))

    # Create perturbation system
    pert_system = PerturbationSystem(background_kb=bk)

    # Current clause
    clause = Clause("parent(X1, X2)")

    # Perturbation classes
    perturbation_classes = ["add_constraint", "remove_constraint", "modify_predicate"]

    # Generate perturbation
    perturbed_example = perturbation_method(clause, perturbation_classes, pert_system)

    if perturbed_example:
        print(f"Generated perturbed example: {perturbed_example}")
    else:
        print("No perturbed example could be generated")


if __name__ == "__main__":
    main()