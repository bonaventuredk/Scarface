import random
from random_agent import RandomAgent
from loguru import logger

class LogWeightedRandomAgent(RandomAgent):
    """
    Random agent that prefers center columns
    """
    def __init__(self, env, player_name=None):
        self.player_name = player_name
        super().__init__(env, player_name)
        logger.info(f"Initialized LoggedRandomAgent for {player_name}")

    def choose_action_weight(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        # TODO: Create weights that favor center (column 3)
        if terminated or truncated:
            logger.info(f"{self.player_name} - Game ended, returning None")
            return None
        valid_actions = [i for i, valid in enumerate(action_mask) if valid ==1]  
        logger.debug(f"{self.player_name} - Valid actions: {valid_actions}")
        action = random.choices(valid_actions)
        logger.info(f"{self.player_name} plays column {action}")
        return action
        
