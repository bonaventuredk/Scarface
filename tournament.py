"""
Tournament

This script runs multiple games between different agents:
RandomAgent, SmartAgent, SmartAgentAmeliore, and MinimaxAgent.
"""

import numpy as np
from random_agent import RandomAgent
from smart_agent import SmartAgent
from smart_agent_ameliore import SmartAgentAmeliore
from agent_minimax import MinimaxAgent
from pettingzoo.classic import connect_four_v3


def play_one_game(agent1_class, agent2_class, render_mode="human", depth_minimax=3):
    """
    Play a single game of Connect Four between two agents.

    Parameters:
        agent1_class: class of player 0
        agent2_class: class of player 1
        render_mode: str, mode for environment rendering
        depth_minimax: int, depth for MinimaxAgent if used

    Returns:
        tuple: winner (str or None), total number of moves played
    """
    env = connect_four_v3.env(render_mode=render_mode)
    env.reset(seed=42)

    assert env.agents == ["player_0", "player_1"]

    # Initialize agents
    agent_dict = {}
    for name, cls in zip(["player_0", "player_1"], [agent1_class, agent2_class]):
        if cls == MinimaxAgent:
            agent_dict[name] = cls(env, depth=int(depth_minimax), player_name=name)
        else:
            agent_dict[name] = cls(env, name)

    winner = None
    move_count = 0

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
            mask = observation["action_mask"]
            action = agent_dict[agent].choose_action(
                observation=observation["observation"],
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                info=info,
                action_mask=mask,
            )
            move_count += 1

        env.step(action)

    env.close()
    return winner, move_count


def play_multiple_games(agent1_class, agent2_class, num_games=10, render_mode="human", depth_minimax=3):
    """
    Play multiple games between two agents and collect statistics.

    Parameters:
        agent1_class: class of player 0
        agent2_class: class of player 1
        num_games: int, number of games to play
        render_mode: str, environment render mode
        depth_minimax: int, depth for MinimaxAgent if used

    Returns:
        dict: statistics including wins, draws, rates, min/max/mean moves
    """
    results = {
        "player_0": 0,
        "player_1": 0,
        "draw": 0,
        "rate_0": 0.0,
        "rate_1": 0.0,
        "rate_draw": 0.0,
        "min_moves": 0,
        "max_moves": 0,
        "mean_moves": 0.0,
    }
    moves_list = []

    for _ in range(num_games):
        winner, moves = play_one_game(agent1_class, agent2_class, render_mode, depth_minimax)
        moves_list.append(moves)
        if winner is None:
            results["draw"] += 1
        elif winner == "player_0":
            results["player_0"] += 1
        else:
            results["player_1"] += 1

    results["rate_0"] = results["player_0"] / num_games
    results["rate_1"] = results["player_1"] / num_games
    results["rate_draw"] = results["draw"] / num_games
    results["min_moves"] = int(np.min(moves_list))
    results["max_moves"] = int(np.max(moves_list))
    results["mean_moves"] = float(np.mean(moves_list))

    print(f"\n{agent1_class.__name__} vs {agent2_class.__name__}\n")
    print(results)
    return results


if __name__ == "__main__":
    # Run all matchups
    play_multiple_games(RandomAgent, SmartAgent, num_games=1)
    play_multiple_games(RandomAgent, SmartAgentAmeliore, num_games=1)
    play_multiple_games(SmartAgent, SmartAgentAmeliore, num_games=1)
    play_multiple_games(MinimaxAgent, SmartAgentAmeliore, num_games=1, depth_minimax=3)
