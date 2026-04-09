"""
Golem: Generalisation Of Natural Language Descriptions
Muggleton and Feng's Inductive Logic Programming System

Golem is a bottom-up ILP system that learns Horn clauses from positive examples only,
using relative Least General Generalization (LGG) under background theory.

Key features:
- Learns from positive examples only (no negative examples required)
- Uses relative LGG for clause refinement
- Employs two-literal clause restriction for tractability
- Implements a greedy search through the hypothesis space
- Relies on a logical engine for inference and unification
"""

from dataclasses import dataclass
from typing import List, Set, Optional, Tuple, Dict
from logical_engine.horn_clauses import KnowledgeBase, Fact, Rule
from logical_engine.terms import Term, Variable, Function, Constant
from logical_engine.unification import unify, Substitution
from logical_engine.parser import parse_term
from logical_engine.meta_interpreter import solve, prove


@dataclass
class Example:
    """Represents a training example for Golem learning."""
    goal: str  # String representation of the goal
    label: bool = True  # Positive (True) or negative (False) example
    
    def __repr__(self) -> str:
        return f"Example('{self.goal}', {self.label})"


@dataclass
class GolemRule:
    """Represents a learned Horn clause rule."""
    head: str  # String representation of head
    body: List[str]  # List of body literals as strings
    
    def __repr__(self) -> str:
        if not self.body:
            return f"{self.head}."
        body_str = ", ".join(self.body)
        return f"{self.head} :- {body_str}."
    
    def to_horn_clause(self) -> Rule:
        """Convert to Horn clause for use with logical engine."""
        return Rule(self.head, self.body)


class GolemLearner:
    """
    Golem ILP System - Learns Horn clauses from positive examples.
    
    Golem implements a least-general generalization (LGG) approach to learn
    Horn clauses that cover positive examples. It works bottom-up, starting
    from pairs of positive examples and generalizing over them.
    
    Algorithm overview:
    1. Select pairs of positive examples
    2. Compute least general generalization of example pairs
    3. Specialize by adding body literals from background theory
    4. Select rules that cover the most positive examples
    5. Remove covered examples and repeat
    """
    
    def __init__(self, kb: KnowledgeBase, max_clause_length: int = 2,
                 max_iterations: int = 100, verbose: bool = False):
        """
        Initialize the Golem learner.
        
        Args:
            kb: Background knowledge base (facts and rules)
            max_clause_length: Maximum body length for learned rules (default 2)
            max_iterations: Maximum iterations before stopping
            verbose: Enable verbose output
        """
        self.kb = kb
        self.max_clause_length = max_clause_length
        self.max_iterations = max_iterations
        self.verbose = verbose
        self.learned_rules: List[GolemRule] = []
    
    def learn(self, positive_examples: List[Example],
              predicate_name: Optional[str] = None) -> List[GolemRule]:
        """
        Learn Horn clauses that cover the positive examples.
        
        Args:
            positive_examples: List of positive training examples
            predicate_name: Optional filter for target predicate
        
        Returns:
            List of learned GolemRule objects
        """
        self.learned_rules = []
        uncovered = set(range(len(positive_examples)))
        iteration = 0
        
        if self.verbose:
            print(f"[Golem] Starting learning with {len(positive_examples)} "
                  f"positive examples")
        
        while uncovered and iteration < self.max_iterations:
            if self.verbose:
                print(f"\n[Iteration {iteration}] Uncovered examples: {uncovered}")
            
            # Select a seed example
            seed_idx = min(uncovered)
            seed_example = positive_examples[seed_idx]
            
            # Find best rule covering seed
            best_rule = self._find_best_rule_for_seed(
                seed_example, positive_examples, uncovered
            )
            
            if best_rule is None:
                if self.verbose:
                    print(f"[Iteration {iteration}] No valid rule found for seed")
                uncovered.discard(seed_idx)
                iteration += 1
                continue
            
            # Add learned rule and remove covered examples
            self.learned_rules.append(best_rule)
            if self.verbose:
                print(f"[Iteration {iteration}] Learned rule: {best_rule}")
            
            # Determine which examples are covered
            newly_covered = self._get_covered_examples(
                best_rule, positive_examples
            )
            uncovered -= newly_covered
            
            if self.verbose:
                print(f"[Iteration {iteration}] Rule covers {len(newly_covered)} examples")
            
            iteration += 1
        
        if self.verbose:
            print(f"\n[Golem] Learning complete. Learned {len(self.learned_rules)} rules")
        
        return self.learned_rules
    
    def _find_best_rule_for_seed(self, seed: Example,
                                  all_examples: List[Example],
                                  uncovered_indices: Set[int]) -> Optional[GolemRule]:
        """
        Find the best rule that covers the seed example.
        
        This method generates candidate rules by computing least general
        generalizations and selecting the one with best coverage.
        """
        candidates: List[Tuple[GolemRule, int]] = []
        
        # Generate candidates from seed paired with other examples
        uncovered_examples = [all_examples[i] for i in uncovered_indices]
        
        for other in uncovered_examples:
            if other.goal == seed.goal:
                # Create a rule directly from the example
                rule = self._generalize_examples([seed, other])
                if rule:
                    coverage = len(self._get_covered_examples(rule, all_examples))
                    candidates.append((rule, coverage))
        
        # If no candidates, create rule from seed alone
        if not candidates:
            rule = self._create_rule_from_example(seed)
            if rule:
                coverage = len(self._get_covered_examples(rule, all_examples))
                candidates.append((rule, coverage))
        
        # Select candidate with highest coverage
        if candidates:
            best_rule, best_coverage = max(candidates, key=lambda x: x[1])
            return best_rule
        
        return None
    
    def _generalize_examples(self, examples: List[Example]) -> Optional[GolemRule]:
        """
        Compute least general generalization of examples.
        
        For simplicity, this implementation creates generalized rules by
        replacing differing arguments with variables.
        """
        if not examples:
            return None
        
        # Parse first example
        head_term = parse_term(examples[0].goal)
        if not isinstance(head_term, Function):
            return None
        
        head_args = list(head_term.args)
        
        # Generalize with other examples
        for example in examples[1:]:
            other_term = parse_term(example.goal)
            if isinstance(other_term, Function) and other_term.name == head_term.name:
                # Replace differing arguments with variables
                for i, (arg1, arg2) in enumerate(zip(head_args, other_term.args)):
                    if str(arg1) != str(arg2):
                        # Create a variable - just use the variable name directly
                        var_name = f"X{i}"
                        head_args[i] = var_name
        
        # Build generalized head as string
        def arg_to_str(arg):
            if isinstance(arg, Variable):
                return arg.name
            elif isinstance(arg, Constant):
                return arg.value
            elif isinstance(arg, Function):
                sub_args = [arg_to_str(a) for a in arg.args]
                return f"{arg.name}({', '.join(sub_args)})"
            return str(arg)
        
        arg_strs = [arg_to_str(arg) for arg in head_args]
        head_str = f"{head_term.name}({', '.join(arg_strs)})"
        
        return GolemRule(head_str, [])
    
    def _create_rule_from_example(self, example: Example) -> GolemRule:
        """
        Create a rule from a single example by abstracting it.
        """
        head_term = parse_term(example.goal)
        if isinstance(head_term, Function):
            # Replace all arguments with variables (as strings)
            abstracted_args = [f"X{i}" for i in range(len(head_term.args))]
            abstracted_head = f"{head_term.name}({', '.join(abstracted_args)})"
            return GolemRule(abstracted_head, [])
        return GolemRule(example.goal, [])
    
    def _get_covered_examples(self, rule: GolemRule,
                              examples: List[Example]) -> Set[int]:
        """
        Determine which examples are covered by a rule.
        """
        covered = set()
        rule_as_clause = rule.to_horn_clause()
        
        # Add rule to KB temporarily
        original_size = len(self.kb.rules)
        self.kb.add_rule(rule_as_clause)
        
        try:
            for idx, example in enumerate(examples):
                # Check if rule can derive the example
                solutions = list(solve(example.goal, self.kb))
                if solutions:
                    covered.add(idx)
        finally:
            # Remove temporary rule
            if len(self.kb.rules) > original_size:
                self.kb.rules = self.kb.rules[:original_size]
        
        return covered
    
    def specialize_rule(self, rule: GolemRule,
                       literals_to_add: List[str]) -> GolemRule:
        """
        Specialize a rule by adding body literals.
        
        Args:
            rule: Base rule to specialize
            literals_to_add: Body literals to add
        
        Returns:
            New specialized rule
        """
        new_body = rule.body + literals_to_add
        if len(new_body) <= self.max_clause_length:
            return GolemRule(rule.head, new_body)
        return rule
    
    def get_learned_rules(self) -> List[GolemRule]:
        """Return the list of learned rules."""
        return self.learned_rules
    
    def get_learned_knowledge_base(self) -> KnowledgeBase:
        """Convert learned rules to a KnowledgeBase."""
        learned_kb = KnowledgeBase()
        for rule in self.learned_rules:
            learned_kb.add_rule(rule.to_horn_clause())
        return learned_kb
    
    def print_learned_rules(self) -> None:
        """Pretty-print all learned rules."""
        print("\n=== Learned Rules ===")
        for i, rule in enumerate(self.learned_rules, 1):
            print(f"{i}. {rule}")
        print(f"\nTotal: {len(self.learned_rules)} rules")


class DerivationTree:
    """Represents the derivation/proof tree for a covered example."""
    
    def __init__(self, goal: str, rule: GolemRule, substitution: Dict = None):
        self.goal = goal
        self.rule = rule
        self.substitution = substitution or {}
        self.children: List[DerivationTree] = []
    
    def __repr__(self) -> str:
        return f"DerivationTree(goal={self.goal}, rule={self.rule.head})"
