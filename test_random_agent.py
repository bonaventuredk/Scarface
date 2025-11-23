from pettingzoo.classic import connect_four_v3
from random_agent import RandomAgent
import numpy as np

def game0(): 
    env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)

    agent1 = RandomAgent(env, player_name ="Un")
    agent2 = RandomAgent(env, player_name ="Deux")
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
            action = agentdict[agent].choose_action(observation = observation["observation"], reward = reward, terminated = terminated, truncated = truncated, info = info, action_mask = mask)
            #action = env.action_space(agent).sample(mask)
            nbcoup += 1
            print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, nbcoup


def game(num_games = 10):
    RESU = {"player_0": 0, "player_1": 0, "Match_Nul": 0, "rate_0":0,"rate_1":0,"rate_Match_Nul":0, "MinCoup":0, "MaxCoup":0, "MeanCoup":0}
    liste1 = []
    for i in range(num_games):
        winner, nbcoup  = game0()
        liste1.append(nbcoup)
        if winner is None:
            RESU["Match_Nul"] += 1
        elif winner == "player_0":
            RESU["player_0"] += 1
        else:
            RESU["player_1"] += 1
    RESU["rate_0"] = RESU["player_0"]/num_games
    RESU["rate_1"] = RESU["player_1"]/num_games
    RESU["rate_Match_Nul"] = RESU["Match_Nul"]/num_games
    RESU["MinCoup"] = np.min(liste1)
    RESU["MaxCoup"] = np.max(liste1)
    RESU["MeanCoup"] = np.mean(liste1)
    print("\n ======Resultats finaux=====\n")
    print(RESU)
    return RESU
            

if __name__ == "__main__":
   game(100)

