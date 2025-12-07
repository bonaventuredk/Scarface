"""
My Random Agent for Connect Four

This agent chooses moves randomly from the available (valid) columns.
"""


import random
from typing import Any
from typing import Optional

class RandomAgent:
    """A simple agent that plays Connect Four randomly."""

    def __init__(self, env: Any, player_name: Optional[str] = None) -> None:
        """
        Initialize the random agent.

        Args:
            env: PettingZoo environment instance.
            player_name: Optional name for the agent (for display purposes).
        """
        self.action_space = env.action_space(env.agents[0])
        self.name = player_name if player_name is not None else "RandomAgent"

    def choose_action(
        self,
        observation: Any,  # pylint: disable=unused-argument
        reward: float = 0.0,  # pylint: disable=unused-argument
        terminated: bool = False,  # pylint: disable=unused-argument
        truncated: bool = False,  # pylint: disable=unused-argument
        info: Optional[dict] = None,  # pylint: disable=unused-argument
        action_mask: Optional[Any] = None,
    ) -> int:
        """
        Choose a random valid action using the environment's action space.

        Args:
            observation: numpy array (6, 7, 2) - current board state.
            reward: float - reward from previous action (unused).
            terminated: bool - whether the game is over (unused).
            truncated: bool - whether the game was truncated (unused).
            info: dict - additional game information (unused).
            action_mask: numpy array (7,) - valid columns (1) vs full columns (0).

        Returns:
            int: Column index (0-6) where to play.
        """
        if action_mask is not None:
            action = self.action_space.sample(mask=action_mask)
        else:
            action = self.action_space.sample()
        return action

    def choose_action_manual(
        self,
        observation: Any,  # pylint: disable=unused-argument
        reward: float = 0.0,  # pylint: disable=unused-argument
        terminated: bool = False,  # pylint: disable=unused-argument
        truncated: bool = False,  # pylint: disable=unused-argument
        info: Optional[dict] = None,  # pylint: disable=unused-argument
        action_mask: Optional[Any] = None,
    ) -> Optional[int]:
        """
        Choose a random valid action without using action_space.sample().

        This method demonstrates manual action selection based on action_mask
        for educational purposes.

        Args:
            observation: numpy array (6, 7, 2) - current board state.
            reward: float - reward from previous action (unused).
            terminated: bool - whether the game is over (unused).
            truncated: bool - whether the game was truncated (unused).
            info: dict - additional game information (unused).
            action_mask: numpy array (7,) - valid columns (1) vs full columns (0).

        Returns:
            int or None: Column index (0-6) where to play, or None if no valid moves.
        """
        if action_mask is None:
            return self.action_space.sample()

        # Get list of valid actions from action_mask
        valid_actions = [
            i for i, valid in enumerate(action_mask) if valid == 1
        ]

        # If no valid actions, return None (shouldn't happen in Connect Four)
        if not valid_actions:
            return None

        # Choose randomly from valid actions
        action = random.choice(valid_actions)
        return action
