"""
Initial Chess Knowledge Base
Using logical_engine to create a knowledge base with basic chess facts.
"""

import sys
import os

# Add the logical_engine to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from logical_engine.horn_clauses import KnowledgeBase, Fact
from logical_engine.kb import save_kb_to_file


def logic_engine():
    """
    Create and return a knowledge base for chess domain.
    """
    kb = KnowledgeBase()
    return kb


# Create the knowledge base
kb = logic_engine()

# Add the facts
kb.add_fact(Fact("side(White)"))
kb.add_fact(Fact("side(Black)"))
kb.add_fact(Fact("piece(pawn)"))
kb.add_fact(Fact("piece(knight)"))
kb.add_fact(Fact("piece(bishop)"))
kb.add_fact(Fact("piece(rook)"))
kb.add_fact(Fact("piece(queen)"))
kb.add_fact(Fact("piece(king)"))
kb.add_fact(Fact("square(1,1)"))
kb.add_fact(Fact("square(1,2)"))
kb.add_fact(Fact("square(1,3)"))
kb.add_fact(Fact("square(1,4)"))
kb.add_fact(Fact("square(1,5)"))
kb.add_fact(Fact("square(1,6)"))
kb.add_fact(Fact("square(1,7)"))
kb.add_fact(Fact("square(1,8)"))
kb.add_fact(Fact("square(2,1)"))
kb.add_fact(Fact("square(2,2)"))
kb.add_fact(Fact("square(2,3)"))
kb.add_fact(Fact("square(2,4)"))
kb.add_fact(Fact("square(2,5)"))
kb.add_fact(Fact("square(2,6)"))
kb.add_fact(Fact("square(2,7)"))
kb.add_fact(Fact("square(2,8)"))
kb.add_fact(Fact("square(3,1)"))
kb.add_fact(Fact("square(3,2)"))
kb.add_fact(Fact("square(3,3)"))
kb.add_fact(Fact("square(3,4)"))
kb.add_fact(Fact("square(3,5)"))
kb.add_fact(Fact("square(3,6)"))
kb.add_fact(Fact("square(3,7)"))
kb.add_fact(Fact("square(3,8)"))
kb.add_fact(Fact("square(4,1)"))
kb.add_fact(Fact("square(4,2)"))
kb.add_fact(Fact("square(4,3)"))
kb.add_fact(Fact("square(4,4)"))
kb.add_fact(Fact("square(4,5)"))
kb.add_fact(Fact("square(4,6)"))
kb.add_fact(Fact("square(4,7)"))
kb.add_fact(Fact("square(4,8)"))
kb.add_fact(Fact("square(5,1)"))
kb.add_fact(Fact("square(5,2)"))
kb.add_fact(Fact("square(5,3)"))
kb.add_fact(Fact("square(5,4)"))
kb.add_fact(Fact("square(5,5)"))
kb.add_fact(Fact("square(5,6)"))
kb.add_fact(Fact("square(5,7)"))
kb.add_fact(Fact("square(5,8)"))
kb.add_fact(Fact("square(6,1)"))
kb.add_fact(Fact("square(6,2)"))
kb.add_fact(Fact("square(6,3)"))
kb.add_fact(Fact("square(6,4)"))
kb.add_fact(Fact("square(6,5)"))
kb.add_fact(Fact("square(6,6)"))
kb.add_fact(Fact("square(6,7)"))
kb.add_fact(Fact("square(6,8)"))
kb.add_fact(Fact("square(7,1)"))
kb.add_fact(Fact("square(7,2)"))
kb.add_fact(Fact("square(7,3)"))
kb.add_fact(Fact("square(7,4)"))
kb.add_fact(Fact("square(7,5)"))
kb.add_fact(Fact("square(7,6)"))
kb.add_fact(Fact("square(7,7)"))
kb.add_fact(Fact("square(7,8)"))
kb.add_fact(Fact("square(8,1)"))
kb.add_fact(Fact("square(8,2)"))
kb.add_fact(Fact("square(8,3)"))
kb.add_fact(Fact("square(8,4)"))
kb.add_fact(Fact("square(8,5)"))
kb.add_fact(Fact("square(8,6)"))
kb.add_fact(Fact("square(8,7)"))
kb.add_fact(Fact("square(8,8)"))

# Display the knowledge base contents
kb.display_kb_contents()

# Save the knowledge base to file
save_kb_to_file(kb, "chess_domain.kb")
