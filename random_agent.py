"""
My Random Agent for Connect Four

This agent chooses moves randomly from the available (valid) columns.
"""

import random


class RandomAgent:
    """
    A simple agent that plays randomly
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the random agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent (for display)
        """
        self.action_space = env.action_space(env.agents[0])
        self.name = player_name if player_name is not None else "RandomAgent"
        
        
    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose a random valid action

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            reward: float - reward from previous action
            terminated: bool - is the game over?
            truncated: bool - was the game truncated?
            info: dict - additional info
            action_mask: numpy array (7,) - which columns are valid (1) or full (0)

        Returns:
            action: int (0-6) - which column to play
        """
        if action_mask is not None:
            action = self.action_space.sample(mask=action_mask)
        else:
            action = self.action_space.sample()
        return action
        
    def choose_action_manual(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose a random valid action without using .sample()

        This is a learning exercise to understand what action_mask does
        """
        # TODO: Get list of valid actions from action_mask
        valid_actions = [i for i, valid in enumerate(action_mask) if valid ==1]  

        # TODO: If no valid actions, return None (shouldn't happen in Connect Four)
        if not valid_actions:
            return None

        # TODO: Choose randomly from valid actions
        action = random.choice(valid_actions)
        return action 
