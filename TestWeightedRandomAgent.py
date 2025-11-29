from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent
from WeightedRandomAgent import WeightedRandomAgent
import numpy as np


env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
env.reset(seed=42)

agent1 = WeightedRandomAgent(env, player_name ="Un")
agent2 = WeightedRandomAgent(env, player_name ="Deux")
agentdict = {env.agents[0]: agent1, env.agents[1]: agent2}
winner = None
nbcoup = 0

for agent in env.agent_iter():
    observation, reward, terminated, truncated, info = env.last()

    if terminated or truncated:
        action = None
        if reward == 1:
            print(f"{agent} wins!")
            winner = agent
        elif reward == 0:
            print("It's a draw!")
    else:
        # Take a random valid action
        mask = observation["action_mask"]
        action = agentdict[agent].choose_action_weight(observation = observation["observation"], reward = reward, terminated = terminated, truncated = truncated, info = info, action_mask = mask)
        #action = env.action_space(agent).sample(mask)
        nbcoup += 1
        print(f"{agent} plays column {action}")

    env.step(action)

#input("Press Enter to close...")
env.close()

