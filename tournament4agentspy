import numpy as np
from smart_agent_ameliore import SmartAgentAmeliore 
from smart_agent import SmartAgent   
from agent_minimax import MinimaxAgent

from pettingzoo.classic import connect_four_v3

from random_agent import RandomAgent

#A tournament of : RandomAgent, SmartAgent and SmartAgentAmeliore

#
# INTEGRATION TESTS (RANDOM VS SMART_AGENT)
# 1: RANDOM VS SMART_AGENT
def OneGame1():  
    """
    Play a single game of Connect Four using two RandomAgent players.

    The function creates the environment, resets it, and lets both agents
    play until the game ends. It prints each move and the final result.

    Returns:
        tuple:
            - winner (str or None): the name of the winning agent
              ("player_0", "player_1") or None in case of a draw.
            - NbCoup (int): total number of moves played in the game.
    """
    env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)
    
    assert env.agents == ["player_0", "player_1"] #For after change manually the name of players
    
    agentdict = {
        "player_0": RandomAgent(env, "player_0"),
        "player_1": SmartAgent(env, "player_1")
    }
    winner = None
    NbCoup = 0 # NbCoup: Total number of games
    
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
            NbCoup += 1
            #print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, NbCoup


def AllGame1(num_games = 10): 
    """
    Play multiple games of Connect Four and collect statistics.

    Parameters:
        num_games (int): number of games to play.

    Returns:
        dict: a dictionary with:
            - number of wins for each player,
            - number of draws,
            - win rates,
            - minimum, maximum, and mean number of moves per game and others
    """
    RESU = {"player_0": 0, "player_1": 0, "Match_Nul": 0, "rate_0":0,"rate_1":0,"rate_Match_Nul":0, "MinCoup":0, "MaxCoup":0, "MeanCoup":0}
    liste1 = []
    for i in range(num_games):
        winner, NbCoup  = OneGame1()
        liste1.append(NbCoup)
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
    print("\n Random vs Smart_Agent\n")
    print(RESU)
    return RESU
            



# 2. RANDOM VS SMART_AGENT_AMELIORE

def OneGame2():  
    """
    Play a single game of Connect Four using two RandomAgent players.

    The function creates the environment, resets it, and lets both agents
    play until the game ends. It prints each move and the final result.

    Returns:
        tuple:
            - winner (str or None): the name of the winning agent
              ("player_0", "player_1") or None in case of a draw.
            - NbCoup (int): total number of moves played in the game.
    """
    env = connect_four_v3.env(render_mode="human") #
    env.reset(seed=42)


    assert env.agents == ["player_0", "player_1"] #For after change manually the name of players
    
    agentdict = {
        "player_0": RandomAgent(env, "player_0"),
        "player_1": SmartAgentAmeliore(env, "player_1")
    }
    winner = None
    NbCoup = 0 # NbCoup: Total number of games
    
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
            NbCoup += 1
            #print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, NbCoup


def AllGame2(num_games = 10): 
    """
    Play multiple games of Connect Four and collect statistics.

    Parameters:
        num_games (int): number of games to play.

    Returns:
        dict: a dictionary with:
            - number of wins for each player,
            - number of draws,
            - win rates,
            - minimum, maximum, and mean number of moves per game and others
    """
    RESU = {"player_0": 0, "player_1": 0, "Match_Nul": 0, "rate_0":0,"rate_1":0,"rate_Match_Nul":0, "MinCoup":0, "MaxCoup":0, "MeanCoup":0}
    liste1 = []
    for i in range(num_games):
        winner, NbCoup  = OneGame2()
        liste1.append(NbCoup)
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
    print("\n Random vs Smart_Agent_Ameliore\n")
    print(RESU)
    return RESU

# 3. SMART_AGENT VS SMART_AGENT_AMELIORE
def OneGame3():  
    """
    Play a single game of Connect Four using two RandomAgent players.

    The function creates the environment, resets it, and lets both agents
    play until the game ends. It prints each move and the final result.

    Returns:
        tuple:
            - winner (str or None): the name of the winning agent
              ("player_0", "player_1") or None in case of a draw.
            - NbCoup (int): total number of moves played in the game.
    """
    env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)


    assert env.agents == ["player_0", "player_1"] #For after change manually the name of players
    
    agentdict = {
        "player_0": SmartAgent(env, "player_0"),
        "player_1": SmartAgentAmeliore(env, "player_1")
    }
    winner = None
    NbCoup = 0 # NbCoup: Total number of games
    
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
            NbCoup += 1
            #print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, NbCoup


def AllGame3(num_games = 10): 
    """
    Play multiple games of Connect Four and collect statistics.

    Parameters:
        num_games (int): number of games to play.

    Returns:
        dict: a dictionary with:
            - number of wins for each player,
            - number of draws,
            - win rates,
            - minimum, maximum, and mean number of moves per game and others
    """
    RESU = {"player_0": 0, "player_1": 0, "Match_Nul": 0, "rate_0":0,"rate_1":0,"rate_Match_Nul":0, "MinCoup":0, "MaxCoup":0, "MeanCoup":0}
    liste1 = []
    for i in range(num_games):
        winner, NbCoup  = OneGame3()
        liste1.append(NbCoup)
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
    print("\nSmart_Agent vs Smart_Agent_Ameliore\n")
    print(RESU)
    return RESU


# 4.  minimax vs SMART_AGENT_AMELIORE 
def OneGame4():  
    """
    Play a single game of Connect Four using two RandomAgent players.

    The function creates the environment, resets it, and lets both agents
    play until the game ends. It prints each move and the final result.

    Returns:
        tuple:
            - winner (str or None): the name of the winning agent
              ("player_0", "player_1") or None in case of a draw.
            - NbCoup (int): total number of moves played in the game.
    """
    env = connect_four_v3.env(render_mode="human") # ou render_mode="rdb_array" ou bien None
    env.reset(seed=42)


    assert env.agents == ["player_0", "player_1"] #For after change manually the name of players
    
    agentdict = {
        "player_0": MinimaxAgent(env, "player_0"),
        "player_1": SmartAgent(env, "player_1")
    }
    winner = None
    NbCoup = 0 # NbCoup: Total number of games
    
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
            NbCoup += 1
            #print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, NbCoup


def AllGame4(num_games = 10): 
    """
    Play multiple games of Connect Four and collect statistics.

    Parameters:
        num_games (int): number of games to play.

    Returns:
        dict: a dictionary with:
            - number of wins for each player,
            - number of draws,
            - win rates,
            - minimum, maximum, and mean number of moves per game and others
    """
    RESU = {"player_0": 0, "player_1": 0, "Match_Nul": 0, "rate_0":0,"rate_1":0,"rate_Match_Nul":0, "MinCoup":0, "MaxCoup":0, "MeanCoup":0}
    liste1 = []
    for i in range(num_games):
        winner, NbCoup  = OneGame3()
        liste1.append(NbCoup)
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
    print("\n minimax vs Smart_Agent\n")
    print(RESU)
    return RESU


if __name__ == "__main__":
   #AllGame1(10)
   
   #AllGame2(10)
   
   AllGame3(20)

   #AllGame4(10)