"""
Connect Four simulation module.

This module simulates multiple Connect Four games between two random agents
and collects statistics about win rates, draws, and move counts.
"""

import numpy as np
from pettingzoo.classic import connect_four_v3

# Use absolute import assuming random_agent is in the same directory
try:
    from random_agent import RandomAgent
except ImportError:
    # For testing purposes only
    class RandomAgent:
        """Mock RandomAgent for testing."""
        def __init__(self, env, player_name=None):
            self.name = player_name if player_name is not None else "RandomAgent"
        
        def choose_action_manual(self, **kwargs):
            """Mock action selection."""
            return 0


def play_single_game(render_mode=None):
    """
    Play a single Connect Four game using two RandomAgent players.

    Args:
        render_mode: Optional render mode for visualization.
                     Options: "human", "rgb_array", or None.

    Returns:
        tuple: Contains:
            - winner (str or None): Name of winning agent ("player_0", "player_1")
                                    or None in case of a draw.
            - move_count (int): Total number of moves played in the game.
    """
    env = connect_four_v3.env(render_mode=render_mode)
    env.reset(seed=42)

    # Initialize agents
    agent1 = RandomAgent(env, player_name="Player_One")
    agent2 = RandomAgent(env, player_name="Player_Two")
    
    assert env.agents == ["player_0", "player_1"], "Unexpected agent names"
    agent_dict = {env.agents[0]: agent1, env.agents[1]: agent2}
    
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
            # Take a random valid action
            action_mask = observation["action_mask"]
            action = agent_dict[agent].choose_action_manual(
                observation=observation["observation"],
                reward=reward,
                terminated=terminated,
                truncated=truncated,
                info=info,
                action_mask=action_mask
            )
            move_count += 1
            print(f"{agent} plays column {action}")

        env.step(action)

    env.close()
    return winner, move_count


def simulate_multiple_games(num_games=10):
    """
    Simulate multiple Connect Four games and collect statistics.

    Args:
        num_games: Number of games to simulate (default: 10).

    Returns:
        dict: Dictionary containing statistics:
            - player_0_wins: Number of wins for player_0
            - player_1_wins: Number of wins for player_1
            - draws: Number of draws
            - player_0_win_rate: Win rate for player_0
            - player_1_win_rate: Win rate for player_1
            - draw_rate: Rate of draws
            - min_moves: Minimum moves in a game
            - max_moves: Maximum moves in a game
            - mean_moves: Average moves per game
    """
    results = {
        "player_0_wins": 0,
        "player_1_wins": 0,
        "draws": 0,
        "player_0_win_rate": 0.0,
        "player_1_win_rate": 0.0,
        "draw_rate": 0.0,
        "min_moves": 0,
        "max_moves": 0,
        "mean_moves": 0.0
    }
    
    move_counts = []

    for _ in range(num_games):
        winner, move_count = play_single_game(render_mode=None)
        move_counts.append(move_count)
        
        if winner is None:
            results["draws"] += 1
        elif winner == "player_0":
            results["player_0_wins"] += 1
        else:
            results["player_1_wins"] += 1

    # Calculate rates
    results["player_0_win_rate"] = results["player_0_wins"] / num_games
    results["player_1_win_rate"] = results["player_1_wins"] / num_games
    results["draw_rate"] = results["draws"] / num_games
    
    # Calculate move statistics
    if move_counts:
        results["min_moves"] = np.min(move_counts)
        results["max_moves"] = np.max(move_counts)
        results["mean_moves"] = np.mean(move_counts)

    print("\n" + "="*50)
    print("RESULTS".center(50))
    print("="*50)
    
    for key, value in results.items():
        if "rate" in key or "mean" in key:
            print(f"{key.replace('_', ' ').title()}: {value:.3f}")
        else:
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    return results


if __name__ == "__main__":
    simulate_multiple_games(100)