"""
RLGG ILP System
Implementation of Relative Least General Generalization algorithm for Inductive Logic Programming
Based on the work of Stephen Muggleton and collaborators.

This system learns Horn clause rules from positive and negative examples
using the RLGG algorithm to compute generalizations relative to background knowledge.
"""

from typing import List, Optional, Set
import sys
import os

# Add the logical_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logical_engine.terms import Variable, Constant, Function
from logical_engine.horn_clauses import Fact, Rule, KnowledgeBase
from logical_engine.unification import Substitution, unify
from logical_engine.parser import parse_term
def term_to_string(term):
    """Convert a term back to string representation."""
    if hasattr(term, 'name') and hasattr(term, 'args'):
        # Function or Predicate
        args_str = ", ".join(term_to_string(arg) for arg in term.args)
        return f"{term.name}({args_str})"
    elif hasattr(term, 'name'):
        # Variable
        return term.name
    elif hasattr(term, 'value'):
        # Constant
        return str(term.value)
    else:
        return str(term)


class Clause:
    """
    Represents a Horn clause: head :- body
    If body is empty, it's a fact.
    """

    def __init__(self, head, body=None):
        """
        Args:
            head: String or parsed term representing the head predicate
            body: List of strings or parsed terms representing body predicates
        """
        self.head = head if isinstance(head, str) else str(head)
        self.body = [goal if isinstance(goal, str) else str(goal) for goal in (body or [])]

    def __repr__(self):
        if not self.body:
            return f"{self.head}"
        body_str = ", ".join(self.body)
        return f"{self.head} :- {body_str}"

    def is_fact(self):
        return len(self.body) == 0

    def is_rule(self):
        return len(self.body) > 0

    def parse_head(self):
        """Parse the head as a term."""
        return parse_term(self.head)

    def parse_body(self):
        """Parse the body as terms."""
        return [parse_term(goal) for goal in self.body]


class RLGGSystem:
    """
    Inductive Logic Programming system using Relative Least General Generalization.
    """

    def __init__(self, background_kb=None):
        self.background_kb = background_kb or KnowledgeBase()
        self.variable_counter = 0

    def fresh_variable(self):
        """Generate a fresh variable name."""
        self.variable_counter += 1
        return f"X{self.variable_counter}"

    def lgg_terms(self, term1, term2):
        """
        Compute the Least General Generalization (anti-unification) of two terms.

        Returns the most specific term that both terms unify to.
        This is the anti-unification algorithm.
        """
        from logical_engine.terms import Variable

        # If terms are identical, return one
        if str(term1) == str(term2):
            return term1

        # If one is a variable, return that variable
        if isinstance(term1, Variable):
            return term1
        if isinstance(term2, Variable):
            return term2

        # If both are constants, they must be different, so introduce variable
        if hasattr(term1, 'value') and hasattr(term2, 'value'):
            return Variable(self.fresh_variable())

        # If both are functions with same name and arity
        if (hasattr(term1, 'name') and hasattr(term2, 'name') and
            term1.name == term2.name and
            hasattr(term1, 'args') and hasattr(term2, 'args') and
            len(term1.args) == len(term2.args)):

            # Recursively compute LGG of arguments
            generalized_args = []
            for arg1, arg2 in zip(term1.args, term2.args):
                gen_arg = self.lgg_terms(arg1, arg2)
                generalized_args.append(gen_arg)

            return Function(term1.name, generalized_args)

        # Otherwise, introduce a new variable
        return Variable(self.fresh_variable())

    def lgg(self, clause1: Clause, clause2: Clause):
        """
        Compute the Least General Generalization of two clauses.

        Returns the most specific clause that subsumes both input clauses,
        or None if no such generalization exists.
        """
        # Parse the clauses
        head1 = clause1.parse_head()
        head2 = clause2.parse_head()

        # Compute LGG of heads
        generalized_head = self.lgg_terms(head1, head2)
        if generalized_head is None:
            return None

        if clause1.is_fact() and clause2.is_fact():
            # Both are facts
            return Clause(term_to_string(generalized_head))

        elif clause1.is_rule() and clause2.is_rule():
            # Both are rules
            if len(clause1.body) == len(clause2.body):
                # For simplicity, assume same number of body literals
                body1 = clause1.parse_body()
                body2 = clause2.parse_body()

                generalized_body = []
                for b1, b2 in zip(body1, body2):
                    gen_body = self.lgg_terms(b1, b2)
                    if gen_body is None:
                        return None
                    generalized_body.append(term_to_string(gen_body))

                return Clause(term_to_string(generalized_head), generalized_body)

        return None

    def relative_lgg(self, clause1: Clause, clause2: Clause):
        """
        Compute the Relative Least General Generalization.

        This ensures the generalization is consistent with background knowledge.
        """
        # First compute basic LGG
        lgg_clause = self.lgg(clause1, clause2)
        if lgg_clause is None:
            return None

        # For relative LGG, we need to ensure the clause is entailed by background knowledge
        # This is a simplified implementation - full relative LGG involves
        # checking subsumption relative to the background theory

        # For now, just return the basic LGG
        return lgg_clause

    def learn_rule(self, positive_examples: List[Clause]):
        """
        Learn a rule from positive examples using RLGG.

        For multiple examples, repeatedly apply RLGG to find a general rule.
        """
        if not positive_examples:
            return None

        if len(positive_examples) == 1:
            # Single example - return it as a rule
            example = positive_examples[0]
            return Rule(example.head, example.body)

        # Multiple examples - compute successive LGGs
        current_generalization = positive_examples[0]

        for example in positive_examples[1:]:
            current_generalization = self.relative_lgg(current_generalization, example)
            if current_generalization is None:
                return None

        # Convert back to Rule format
        return Rule(current_generalization.head, current_generalization.body)


def main():
    """Example usage of the RLGG ILP system."""
    print("RLGG Inductive Logic Programming System")
    print("=" * 40)

    # Create background knowledge
    bk = KnowledgeBase()
    bk.add_fact(Fact("parent(john, mary)"))
    bk.add_fact(Fact("parent(mary, alice)"))
    bk.add_rule(Rule("ancestor(X, Y)", ["parent(X, Y)"]))
    bk.add_rule(Rule("ancestor(X, Y)", ["parent(X, Z)", "ancestor(Z, Y)"]))

    # Create RLGG system
    ilp_system = RLGGSystem(bk)

    # Example: Learn the parent relationship
    # Positive examples
    pos_examples = [
        Clause("parent(john, mary)"),
        Clause("parent(mary, alice)")
    ]

    learned_rule = ilp_system.learn_rule(pos_examples)
    if learned_rule:
        print(f"Learned rule: {learned_rule}")
    else:
        print("Could not learn a rule from the examples")


if __name__ == "__main__":
    main()