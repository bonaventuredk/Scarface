import random
from random_agent import RandomAgent

class WeightedRandomAgent(RandomAgent):
    """
    Random agent that prefers center columns
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

    def choose_action_weight(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        # TODO: Create weights that favor center (column 3)
        if terminated or truncated:
            return None
        if action_mask is None:
            raise ValueError("action_mask must be provided")
        base_weights = [1,2,3,5,3,2,1] #probability by column
        # TODO: Filter by action_mask
        valid_actions = []
        valid_weights = []
        for action, mask in enumerate(action_mask):
            if mask == 1:
                valid_actions.append(action)
                valid_weights.append(base_weights[action])
        # TODO: Use random.choices(actions, weights=weights)
        action = random.choices(valid_actions, weights = valid_weights, k = 1)[0]
        return action
        
