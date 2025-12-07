import numpy as np
from smart_agent import SmartAgent  

from pettingzoo.classic import connect_four_v3

from random_agent import RandomAgent



class DummyEnv:
    def __init__(self):
        self.agents = ["player_0"]
    def action_space(self, agent):
        return None


def test_get_valid_actions():
    env = DummyEnv()
    agent = SmartAgent(env)

    action_mask = np.array([1,0,1,1,0,1,0])
    result = agent._get_valid_actions(action_mask)

    print("\nTEST get_valid_actions", result)
    assert result == [0,2,3,5]



def test_get_next_row():
    env = DummyEnv()
    agent = SmartAgent(env)

    board = np.zeros((6,7,2))

    row = agent._get_next_row(board, 3)

    print("\nTEST get_next_row → row =", row)
    assert row == 5  
    print()


def test_check_win_from_position_vertical():
    env = DummyEnv()
    agent = SmartAgent(env)

    board = np.zeros((6,7,2))

    # simulate 3 aligned pieces at rows 5,4,3 in column 2
    board[5,2,0] = 1
    board[4,2,0] = 1
    board[3,2,0] = 1

    # placing at row 2 must win
    win = agent._check_win_from_position(board, 2, 2, channel=0)

    print("\nTEST check_win_from_position (vertical) ", win)
    ##new test
    
    board[5,3,0] = 1

    # placing at row 2 must win
    win = agent._check_win_from_position(board, 4, 3, channel=0)

    print("\nTEST check_win_from_position (vertical) ", win)
    
def test_find_winning_move():
    env = DummyEnv()
    agent = SmartAgent(env)

    board = np.zeros((6,7,2))
    valid = [2,3,4]

    # create 3 pieces in column 3  winning move = col 3
    #board[5,3,0] = 1
    #board[4,3,0] = 1
    #board[3,3,0] = 1

    col = agent._find_winning_move(board, valid_actions = valid, channel=0)

    print("\nTEST find_winning_move ", col)
    ##new test
    # create 3 pieces in column 3  winning move = col 3
    board[5,2,0] = 1
    board[4,2,0] = 1
    board[5,3,0] = 1


    col = agent._find_winning_move(board, valid_actions = valid, channel=0)

    print("\nTEST find_winning_move ", col)

# INTEGRATION TESTS (RANDOM VS SMART)

def OneGame():  
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
        "player_1": RandomAgent(env, "player_1")
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
            print(f"{agent} plays column {action}")

        env.step(action)
    
    #input("Press Enter to close...")
    env.close()
    return winner, NbCoup


def AllGame_SmartVsRandom(num_games = 10): 
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
        winner, NbCoup  = OneGame()
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
    print("\n ======RESULTS=====\n")
    print(RESU)
    return RESU




if __name__ == "__main__":
   test_get_valid_actions()
   test_get_next_row()
   test_check_win_from_position_vertical()
   test_find_winning_move()
   #OneGame_SmartVsRandom(render = True)
   AllGame_SmartVsRandom(3)
