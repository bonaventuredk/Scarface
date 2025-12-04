"""
Connect Four environment exploration script.

This module demonstrates basic interaction with the Connect Four environment
from PettingZoo, showing observation structure and taking a random action.
"""

import numpy as np
from pettingzoo.classic import connect_four_v3



"""
Explore the Connect Four environment.

This function initializes the environment, retrieves the first observation,
prints its structure, and takes a random action in column 3.
"""
# Create environment
env = connect_four_v3.env()
env.reset(seed=42)

# Get first observation
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    # Print the observation structure
    print("Agent:", agent)
    print("Observation keys:", observation.keys())
    print("Observation shape:", observation["observation"].shape)
    print("Action mask:", observation["action_mask"])

    # Take a random action (column 3)
    env.step(3)
    break

env.close()
