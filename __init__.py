"""
Package

Project for M2 Ingénierie Mathématique – Sorbonne Université.

Authors:
- Bonaventure Dohemeto
- Sakiye Balakimbiyou

Version: 0.1.0
"""

# Package version
__version__ = "0.1.0"

# Agents
from .random_agent import RandomAgent
from .smart_agent import SmartAgent
from .smart_agent_ameliore import SmartAgentAmeliore
from .agent_minimax import MinimaxAgent
from .WeightedRandomAgent import WeightedRandomAgent
from .LogWeightedRandomAgent import LogWeightedRandomAgent

from .print_board import print_board
from .tournament import run_tournament

__all__ = [
    "RandomAgent",
    "WeightedRandomAgent",
    "LogWeightedRandomAgent",
    "SmartAgent",
    "SmartAgentAmeliore",
    "MinimaxAgent",
    "print_board",
    "run_tournament",
]

