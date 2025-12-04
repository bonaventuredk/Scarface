from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation: np.ndarray) -> None:
    """
    Print the Connect Four board in a human-readable format.

    Args:
        observation: A 6x7x2 numpy array representing the game board.
                     The third dimension contains two channels:
                     - channel 0: Player 0's pieces
                     - channel 1: Player 1's pieces
    """
    for i in range(6):
        row = ""
        for j in range(7):
            if observation[i, j, 0] == 1:
                row += "X "
            elif observation[i, j, 1] == 1:
                row += "O "
            else:
                row += ". "
        print(row)

# Initialize environment
env = connect_four_v3.env()
env.reset(seed=42)

# Display initial board state
for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print("Initial board:")
    print_board(observation["observation"])

    # Make one move to show board evolution
    env.step(3)
    if agent == env.agents[0]:
        break

# Play several moves to demonstrate board evolution
print("\nBoard after several moves:")
env.reset(seed=42)

# Execute a sequence of moves
moves = [5, 2, 3, 1, 1]
for move in moves:
    env.step(move)

# Get and display current state
observation, reward, termination, truncation, info = env.last()
print_board(observation["observation"])

# Clean up
env.close()