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

def OneGame_SmartVsRandom(render=False):
    """
    One game between SmartAgent and RandomAgent.
    SmartAgent = player_0.
    """
    env = connect_four_v3.env(render_mode="human" if render else None)
    env.reset(seed=42)

    smart_agent = SmartAgent(env)
    random_agent = RandomAgent(env, player_name="Random")

    assert env.agents == ["player_0", "player_1"]

    agentdict = {
        "player_0": smart_agent,
        "player_1": random_agent
    }

    winner = None
    NbCoup = 0

    for agent in env.agent_iter():
        observation, reward, terminated, truncated, info = env.last()

        if terminated or truncated:
            action = None
            if reward == 1:
                winner = agent
            break

        mask = observation["action_mask"]

        # Sélection action via la bonne classe
        if agent == "player_0":
            action = smart_agent.choose_action(
                observation=observation["observation"],
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                info=info,
                action_mask=mask
            )
        else:
            action = random_agent.choose_action_manual(
                observation=observation["observation"],
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                info=info,
                action_mask=mask
            )

        NbCoup += 1
        env.step(action)

    env.close()
    return winner, NbCoup

def AllGame_SmartVsRandom(num_games=10, render=True):
    """
    Joue plusieurs parties SmartAgent vs RandomAgent.
    SmartAgent = player_0
    RandomAgent = player_1
    """
    RESU = {
        "Smart_win": 0,
        "Random_win": 0,
        "Match_Nul": 0,
        "rate_Smart": 0,
        "rate_Random": 0,
        "rate_Draw": 0,
        "MinCoup": 0,
        "MaxCoup": 0,
        "MeanCoup": 0
    }

    moves_list = []

    for i in range(num_games):
        winner, NbCoup = OneGame_SmartVsRandom(render=render)
        moves_list.append(NbCoup)

        if winner is None:
            RESU["Match_Nul"] += 1
        elif winner == "player_0":
            RESU["Smart_win"] += 1
        else:
            RESU["Random_win"] += 1

    # Stats
    RESU["rate_Smart"] = RESU["Smart_win"] / num_games
    RESU["rate_Random"] = RESU["Random_win"] / num_games
    RESU["rate_Draw"] = RESU["Match_Nul"] / num_games

    RESU["MinCoup"] = np.min(moves_list)
    RESU["MaxCoup"] = np.max(moves_list)
    RESU["MeanCoup"] = np.mean(moves_list)

    print("\n ====== SMART vs RANDOM RESULTS ======\n")
    print(RESU)
    return RESU



if __name__ == "__main__":
   test_get_valid_actions()
   test_get_next_row()
   test_check_win_from_position_vertical()
   test_find_winning_move()
   OneGame_SmartVsRandom(render = True)
   #llGame_SmartVsRandom(10)