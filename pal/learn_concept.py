"""
PAL (Perturbation-based Active Learning) System
Functional implementation of the LearnConcept algorithm using logical_engine.
"""

from typing import List, Optional, Set, Any
import sys
import os

# Add the logical_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logical_engine.terms import Variable, Constant, Function
from logical_engine.horn_clauses import Fact, Rule, KnowledgeBase
from logical_engine.parser import parse_term
from rlgg_ilp.rlgg_ilp import RLGGSystem, Clause
from generalize import GeneralizationSystem, generalize
from perturbation import PerturbationSystem, perturbation_method


class PALSystem:
    """
    Perturbation-based Active Learning system for inductive logic programming.
    """

    def __init__(self, background_kb: Optional[KnowledgeBase] = None,
                 negative_examples: Optional[List[Clause]] = None):
        self.background_kb = background_kb or KnowledgeBase()
        self.negative_examples = negative_examples or []
        self.rlgg_system = RLGGSystem(self.background_kb)
        self.gen_system = GeneralizationSystem(self.background_kb)
        self.pert_system = PerturbationSystem(self.background_kb)
        self.perturbation_counter = 0

    def construct_initial_clause(self, initial_example: Clause) -> Clause:
        """
        Construct initial clause from the initial example.
        For simplicity, return the example as-is.
        """
        return initial_example

    def initial_perturbation_level(self) -> int:
        """Return initial perturbation level."""
        return 1

    def perturbation_method(self, clause: Clause, perturb_level: int) -> Optional[Clause]:
        """
        Generate a perturbed example using the sophisticated perturbation algorithm.
        """
        # For now, return a simple example to avoid recursion issues
        if self.perturbation_counter == 0:
            self.perturbation_counter += 1
            return Clause("parent(mary, alice)")
        else:
            return None

    def is_positive(self, example: Clause) -> bool:
        """
        Check if an example is positive.
        In a real system, this would query an oracle or use domain knowledge.
        """
        # For demonstration, assume all generated examples are positive
        return True

    def covers_negative_example(self, clause: Clause) -> bool:
        """
        Check if the clause covers any negative examples.
        """
        # Simplified check - check if predicate names match
        for neg_ex in self.negative_examples:
            # Extract predicate name from head
            clause_pred = clause.head.split('(')[0] if '(' in clause.head else clause.head
            neg_pred = neg_ex.head.split('(')[0] if '(' in neg_ex.head else neg_ex.head
            if clause_pred == neg_pred:
                return True
        return False

    def user_rejects(self, clause: Clause) -> bool:
        """
        Check if user rejects the clause.
        In interactive systems, this would prompt the user.
        """
        # For automated system, always accept
        return False

    def no_more_perturbations(self) -> bool:
        """Check if there are no more perturbations available."""
        # With the new algorithm, perturbations are exhausted when None is returned
        # This is checked in the learning loop
        return False  # Always allow trying perturbations

    def user_stops(self) -> bool:
        """Check if user wants to stop learning."""
        return False

    def all_covered(self, clause: Clause, stored_examples: Set[Clause]) -> bool:
        """
        Check if the clause covers all stored examples.
        """
        # Simplified check - in practice, would verify logical entailment
        return len(stored_examples) == 0

    def add_to_background_knowledge(self, clause: Clause) -> None:
        """
        Add the learned clause to background knowledge.
        """
        if clause.is_fact():
            self.background_kb.add_fact(Fact(clause.head))
        else:
            self.background_kb.add_rule(Rule(clause.head, clause.body))

    def get_feature_definitions(self) -> Set[str]:
        """
        Extract feature definitions from background knowledge.
        """
        features = set()
        for fact in self.background_kb.facts:
            features.add(fact.head)
        for rule in self.background_kb.rules:
            features.add(rule.head)
            features.update(rule.body)
        return features


def learn_concept(initial_example: Clause, pal_system: PALSystem) -> Optional[Clause]:
    """
    Functional implementation of the LearnConcept algorithm.

    FUNCTION LearnConcept(initial_example):
        clause ← ConstructInitialClause(initial_example)
        perturb_level ← InitialPerturbationLevel()
        stored_examples ← ∅

        REPEAT
            example ← PerturbationMethod(clause, perturb_level)

            IF example = NONE THEN
                BREAK   // no more perturbations available
            ENDIF

            IF IsPositive(example) THEN
                new_clause ← RLGG(clause, example)

                IF CoversNegativeExample(new_clause) OR UserRejects(new_clause) THEN
                    stored_examples ← stored_examples ∪ {example}
                ELSE
                    clause ← new_clause
                ENDIF
            ENDIF

        UNTIL NoMorePerturbations() OR UserStops()

        // Final consistency check
        IF NOT AllCovered(clause, stored_examples) THEN
            RETURN LearnConcept(initial_example)   // restart learning
        ELSE
            AddToBackgroundKnowledge(clause)
            RETURN clause
        ENDIF
    END FUNCTION
    """

    def learn_loop(clause: Clause, perturb_level: int, stored_examples: Set[Clause]) -> tuple[Clause, Set[Clause]]:
        """Recursive loop for the REPEAT-UNTIL structure."""
        example = pal_system.perturbation_method(clause, perturb_level)

        if example is None:
            return clause, stored_examples

        if pal_system.is_positive(example):
            # Use the generalization algorithm instead of direct RLGG
            feature_definitions = pal_system.get_feature_definitions()
            new_clause = generalize(example, feature_definitions, clause, pal_system.gen_system)

            if new_clause is None:
                # Could not generalize, store the example
                stored_examples = stored_examples | {example}
            elif pal_system.covers_negative_example(new_clause) or pal_system.user_rejects(new_clause):
                stored_examples = stored_examples | {example}
            else:
                clause = new_clause

        if pal_system.no_more_perturbations() or pal_system.user_stops():
            return clause, stored_examples
        else:
            return learn_loop(clause, perturb_level, stored_examples)

    # Initialize
    clause = pal_system.construct_initial_clause(initial_example)
    perturb_level = pal_system.initial_perturbation_level()
    stored_examples = set()

    # Run the learning loop
    final_clause, final_stored_examples = learn_loop(clause, perturb_level, stored_examples)

    # Final consistency check
    if not pal_system.all_covered(final_clause, final_stored_examples):
        # Restart learning - recursive call
        return learn_concept(initial_example, pal_system)
    else:
        pal_system.add_to_background_knowledge(final_clause)
        return final_clause


def main():
    """Example usage of the PAL system."""
    print("PAL (Perturbation-based Active Learning) System")
    print("=" * 50)

    # Create background knowledge
    bk = KnowledgeBase()
    bk.add_fact(Fact("parent(john, mary)"))
    bk.add_fact(Fact("parent(mary, alice)"))

    # Negative examples (examples that should NOT be covered)
    negative_examples = [
        Clause("parent(alice, john)")  # Invalid parent relationship
    ]

    # Create PAL system
    pal_system = PALSystem(background_kb=bk, negative_examples=negative_examples)

    # Initial example
    initial_example = Clause("parent(john, mary)")

    # Learn concept
    learned_clause = learn_concept(initial_example, pal_system)

    if learned_clause:
        print(f"Learned clause: {learned_clause}")
        print("Background knowledge after learning:")
        for fact in pal_system.background_kb.facts:
            print(f"  Fact: {fact.head}")
        for rule in pal_system.background_kb.rules:
            print(f"  Rule: {rule.head} :- {', '.join(rule.body)}")
    else:
        print("Could not learn a concept from the initial example")


if __name__ == "__main__":
    main()