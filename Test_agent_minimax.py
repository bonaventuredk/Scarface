"""
Test suite for MinimaxAgent class
Tests all core functionality with detailed output
"""

import numpy as np
from agent_minimax import MinimaxAgent


# ----------------------------------------
# Fake environment for testing
# ----------------------------------------
class FakeEnv:
    """Minimal environment mock for testing"""

    def __init__(self):
        self.agents = ["player_0"]

    def action_space(self, agent):
        """Return action space with 7 columns"""

        class ActionSpace:
            def __init__(self):
                self.n = 7

        return ActionSpace()


# ----------------------------------------
# Helper functions
# ----------------------------------------
def empty_board():
    """Create empty 6x7 Connect Four board"""
    return np.zeros((6, 7, 2), dtype=int)


def print_board(board):
    """Pretty print board state"""
    rows, cols = board.shape[0], board.shape[1]
    grid = np.zeros((rows, cols), dtype=int)
    grid[board[:, :, 0] == 1] = 1
    grid[board[:, :, 1] == 1] = 2

    print("  0 1 2 3 4 5 6")
    print(" +" + "-" * 14 + "+")
    for r in range(rows):
        row_str = " |"
        for c in range(cols):
            if grid[r, c] == 1:
                row_str += " X"
            elif grid[r, c] == 2:
                row_str += " O"
            else:
                row_str += " ."
        row_str += " |"
        print(row_str)
    print(" +" + "-" * 14 + "+")


# ----------------------------------------
# Test functions
# ----------------------------------------
def test_get_valid_moves(agent):
    """Test valid move detection"""
    print("\n" + "=" * 50)
    print("TEST 1: _get_valid_moves")
    print("=" * 50)

    # Test 1: Empty board
    board = empty_board()
    valid = agent._get_valid_moves(board)
    print("\nEmpty board - Valid moves:", valid)
    assert valid == [0, 1, 2, 3, 4, 5, 6], "All columns should be valid"

    # Test 2: Fill column 3
    for row in range(6):
        board[row, 3, 0] = 1
    valid = agent._get_valid_moves(board)
    print("Column 3 full - Valid moves:", valid)
    assert 3 not in valid, "Column 3 should be invalid"

    print("✓ Test passed!")


def test_simulate_move(agent):
    """Test move simulation"""
    print("\n" + "=" * 50)
    print("TEST 2: _simulate_move")
    print("=" * 50)

    # Test 1: Place piece in empty column
    board = empty_board()
    new_board = agent._simulate_move(board, col=3, channel=0)
    print("\nPlaced piece in column 3 (player 1):")
    print_board(new_board)
    assert new_board[5, 3, 0] == 1, "Piece should be at bottom"

    # Test 2: Stack pieces
    new_board = agent._simulate_move(new_board, col=3, channel=1)
    print("\nStacked piece in column 3 (player 2):")
    print_board(new_board)
    assert new_board[4, 3, 1] == 1, "Piece should stack on top"

    print("✓ Test passed!")


def test_check_win(agent):
    """Test win detection"""
    print("\n" + "=" * 50)
    print("TEST 3: _check_win")
    print("=" * 50)

    # Test 1: Horizontal win
    board = empty_board()
    for c in range(4):
        board[5, c, 0] = 1
    print("\nHorizontal win (player 1):")
    print_board(board)
    assert agent._check_win(board, 0), "Should detect horizontal win"
    assert not agent._check_win(board, 1), "Player 2 hasn't won"

    # Test 2: Vertical win
    board = empty_board()
    for r in range(4):
        board[5 - r, 3, 1] = 1
    print("\nVertical win (player 2):")
    print_board(board)
    assert agent._check_win(board, 1), "Should detect vertical win"

    # Test 3: Diagonal win (positive slope)
    board = empty_board()
    for i in range(4):
        board[5 - i, i, 0] = 1
    print("\nDiagonal win (player 1, positive slope):")
    print_board(board)
    assert agent._check_win(board, 0), "Should detect diagonal win"

    # Test 4: Diagonal win (negative slope)
    board = empty_board()
    for i in range(4):
        board[2 + i, i, 1] = 1
    print("\nDiagonal win (player 2, negative slope):")
    print_board(board)
    assert agent._check_win(board, 1), "Should detect diagonal win"

    print("✓ Test passed!")


def test_evaluate(agent):
    """Test board evaluation"""
    print("\n" + "=" * 50)
    print("TEST 4: _evaluate")
    print("=" * 50)

    # Test 1: Empty board
    board = empty_board()
    score = agent._evaluate(board)
    print(f"\nEmpty board score: {score}")
    assert score == 0, "Empty board should score 0"

    # Test 2: Center control
    board = empty_board()
    board[5, 3, 0] = 1
    board[4, 3, 0] = 1
    print("\nCenter control (player 1):")
    print_board(board)
    score = agent._evaluate(board)
    print(f"Score: {score}")
    assert score > 0, "Center control should give positive score"

    # Test 3: Threat detection
    board = empty_board()
    for c in range(3):
        board[5, c, 1] = 1
    print("\nOpponent threat (3 in a row):")
    print_board(board)
    score = agent._evaluate(board)
    print(f"Score: {score}")
    assert score < 0, "Should recognize opponent threat"

    print("✓ Test passed!")


def test_minimax(agent):
    """Test minimax algorithm"""
    print("\n" + "=" * 50)
    print("TEST 5: _minimax")
    print("=" * 50)

    # Test 1: Detect immediate win
    board = empty_board()
    for c in range(3):
        board[5, c, 0] = 1
    print("\nImmediate win available at column 3:")
    print_board(board)

    scores = {}
    for col in range(7):
        if board[0, col, 0] == 0 and board[0, col, 1] == 0:
            new_board = agent._simulate_move(board, col, channel=0)
            score = agent._minimax(new_board, depth=2, alpha=float('-inf'),
                                   beta=float('inf'), maximizing=False)
            scores[col] = score

    print("\nColumn scores:", scores)
    assert scores[3] == float('inf'), "Should detect winning move"

    # Test 2: Block opponent win
    board = empty_board()
    for c in range(3):
        board[5, c, 1] = 1
    print("\nMust block opponent at column 3:")
    print_board(board)

    best_col = None
    best_score = float('-inf')
    for col in range(7):
        if board[0, col, 0] == 0 and board[0, col, 1] == 0:
            new_board = agent._simulate_move(board, col, channel=0)
            score = agent._minimax(new_board, depth=2, alpha=float('-inf'),
                                   beta=float('inf'), maximizing=False)
            if score > best_score:
                best_score = score
                best_col = col

    print(f"Best move: column {best_col}")
    assert best_col == 3, "Should block opponent's winning move"

    print("✓ Test passed!")


def test_choose_action(agent):
    """Test action selection"""
    print("\n" + "=" * 50)
    print("TEST 6: choose_action")
    print("=" * 50)

    # Test 1: Empty board
    board = empty_board()
    action_mask = [1, 1, 1, 1, 1, 1, 1]
    action = agent.choose_action(observation=board, action_mask=action_mask)
    print(f"\nEmpty board - Chosen action: column {action}")
    assert 0 <= action <= 6, "Action should be valid column"

    # Test 2: Winning move available
    board = empty_board()
    for c in range(3):
        board[5, c, 0] = 1
    print("\nWinning move at column 3:")
    print_board(board)
    action = agent.choose_action(observation=board, action_mask=action_mask)
    print(f"Chosen action: column {action}")
    assert action == 3, "Should choose winning move"

    # Test 3: Block opponent
    board = empty_board()
    for c in range(3):
        board[5, c, 1] = 1
    print("\nMust block at column 3:")
    print_board(board)
    action = agent.choose_action(observation=board, action_mask=action_mask)
    print(f"Chosen action: column {action}")
    assert action == 3, "Should block opponent's winning move"

    print("✓ Test passed!")


def test_performance(agent):
    """Test algorithm performance"""
    print("\n" + "=" * 50)
    print("TEST 7: Performance Test")
    print("=" * 50)

    import time

    board = empty_board()
    # Add some pieces
    for i in range(5):
        col = i % 7
        channel = i % 2
        board = agent._simulate_move(board, col, channel)

    print("\nTest board:")
    print_board(board)

    action_mask = [1] * 7
    start_time = time.time()
    action = agent.choose_action(observation=board, action_mask=action_mask)
    elapsed = time.time() - start_time

    print(f"\nChosen action: column {action}")
    print(f"Time taken: {elapsed:.3f} seconds")
    print(f"Depth: {agent.depth}")

    if elapsed < 1.0:
        print("✓ Performance acceptable!")
    else:
        print("⚠ Performance may be slow for real-time play")


# ----------------------------------------
# MAIN
# ----------------------------------------
if __name__ == "__main__":
    print("=" * 50)
    print("MINIMAX AGENT TEST SUITE")
    print("=" * 50)

    fake_env = FakeEnv()
    agent = MinimaxAgent(env=fake_env, depth=3)

    try:
        test_get_valid_moves(agent)
        test_simulate_move(agent)
        test_check_win(agent)
        test_evaluate(agent)
        test_minimax(agent)
        test_choose_action(agent)
        test_performance(agent)

        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50)

    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback

        traceback.print_exc()