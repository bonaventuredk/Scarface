"""
Minimax agent with alpha-beta pruning for Connect Four
"""

import numpy as np
import random


class MinimaxAgent:
    """
    Agent using minimax algorithm with alpha-beta pruning
    """

    def __init__(self, env, depth=4, player_name=None):
        """
        Initialize minimax agent

        Parameters:
            env: PettingZoo environment
            depth: How many moves to look ahead
            player_name: Optional name
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.depth = depth
        self.player_name = player_name or f"Minimax(d={depth})"

    def _get_valid_moves(self, board):
        """
        Get list of valid column indices where a piece can be placed

        Parameters:
            board: numpy array of shape (rows, cols, 2)

        Returns:
            list of valid column indices
        """
        valid = []
        for col in range(board.shape[1]):
            # Column is valid if top row is empty
            if board[0, col, 0] == 0 and board[0, col, 1] == 0:
                valid.append(col)
        return valid

    def _check_win(self, board, channel):
        """
        Check if player at given channel has won (4 in a row)

        Parameters:
            board: numpy array of shape (rows, cols, 2)
            channel: 0 for player 1, 1 for player 2

        Returns:
            True if player has won, False otherwise
        """
        rows, cols = board.shape[0], board.shape[1]

        # Create a grid representation (0=empty, 1=player1, 2=player2)
        grid = np.zeros((rows, cols), dtype=int)
        grid[board[:, :, 0] == 1] = 1
        grid[board[:, :, 1] == 1] = 2

        player = 1 if channel == 0 else 2

        # Check horizontal
        for r in range(rows):
            for c in range(cols - 3):
                if all(grid[r, c + i] == player for i in range(4)):
                    return True

        # Check vertical
        for c in range(cols):
            for r in range(rows - 3):
                if all(grid[r + i, c] == player for i in range(4)):
                    return True

        # Check diagonal (positive slope)
        for r in range(rows - 3):
            for c in range(cols - 3):
                if all(grid[r + i, c + i] == player for i in range(4)):
                    return True

        # Check diagonal (negative slope)
        for r in range(3, rows):
            for c in range(cols - 3):
                if all(grid[r - i, c + i] == player for i in range(4)):
                    return True

        return False

    def _simulate_move(self, board, col, channel):
        """
        Simulate placing a piece in the given column

        Parameters:
            board: current board state
            col: column index to place piece
            channel: 0 for player 1, 1 for player 2

        Returns:
            new board state after move
        """
        # Copy board to avoid modifying original
        new_board = board.copy()

        # Find lowest available row in column (gravity)
        for row in range(new_board.shape[0] - 1, -1, -1):
            if new_board[row, col, 0] == 0 and new_board[row, col, 1] == 0:
                new_board[row, col, channel] = 1
                return new_board

        # Column is full (shouldn't happen with valid moves)
        return new_board

    def _evaluate(self, board):
        """
        Evaluate board position from perspective of player 1 (channel 0)
        Higher score = better for player 1
        Lower score = better for player 2

        Parameters:
            board: current board state

        Returns:
            evaluation score
        """
        rows = board.shape[0]
        cols = board.shape[1]

        # Create grid representation
        grid = np.zeros(shape=(rows, cols), dtype=int)
        grid[board[:, :, 0] == 1] = 1
        grid[board[:, :, 1] == 1] = 2

        def score_window(window, player):
            """Score a window of 4 positions"""
            opp = 1 if player == 2 else 2
            score = 0

            # Four in a row - winning position
            if window.count(player) == 4:
                score += 10000
            # Three in a row with empty space - strong threat
            elif window.count(player) == 3 and window.count(0) == 1:
                score += 50
            # Two in a row with two empty spaces - potential
            elif window.count(player) == 2 and window.count(0) == 2:
                score += 5

            # Opponent threat - block it
            if window.count(opp) == 3 and window.count(0) == 1:
                score -= 80

            return score

        score = 0
        player = 1  # Our agent (channel 0)

        # Favor center column positions
        center_col = cols // 2
        center_array = list(grid[:, center_col])
        score += center_array.count(player) * 3

        # Score all horizontal windows
        for r in range(rows):
            for c in range(cols - 3):
                window = list(grid[r, c:c + 4])
                score += score_window(window, player)

        # Score all vertical windows
        for c in range(cols):
            for r in range(rows - 3):
                window = list(grid[r:r + 4, c])
                score += score_window(window, player)

        # Score positive slope diagonals
        for r in range(rows - 3):
            for c in range(cols - 3):
                window = [grid[r + i, c + i] for i in range(4)]
                score += score_window(window, player)

        # Score negative slope diagonals
        for r in range(3, rows):
            for c in range(cols - 3):
                window = [grid[r - i, c + i] for i in range(4)]
                score += score_window(window, player)

        return score

    def _minimax(self, board, depth, alpha, beta, maximizing):
        """
        Minimax algorithm with alpha-beta pruning

        Parameters:
            board: current board state
            depth: remaining depth to search
            alpha: best value for maximizer
            beta: best value for minimizer
            maximizing: True if maximizing player's turn

        Returns:
            best evaluation score
        """
        valid_cols = self._get_valid_moves(board)

        # Terminal conditions
        # Player 1 (channel 0) wins - return high score
        if self._check_win(board, 0):
            return float('inf')

        # Player 2 (channel 1) wins - return low score
        if self._check_win(board, 1):
            return float('-inf')

        # Depth limit reached or no valid moves (draw)
        if depth == 0 or not valid_cols:
            return self._evaluate(board)

        if maximizing:
            # Maximizing player (our agent - channel 0)
            best_score = float('-inf')

            for col in valid_cols:
                # Simulate move for player 1
                child = self._simulate_move(board, col, channel=0)
                score = self._minimax(child, depth - 1, alpha, beta, False)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

            return best_score

        else:
            # Minimizing player (opponent - channel 1)
            best_score = float('inf')

            for col in valid_cols:
                # Simulate move for player 2
                child = self._simulate_move(board, col, channel=1)
                score = self._minimax(child, depth - 1, alpha, beta, True)
                best_score = min(best_score, score)
                beta = min(beta, best_score)

                # Alpha-beta pruning
                if beta <= alpha:
                    break

            return best_score

    def choose_action(self, observation, reward=0.0, terminated=False,
                      truncated=False, info=None, action_mask=None):
        """
        Choose best action using minimax algorithm

        Parameters:
            observation: current board state
            reward: reward from previous action (unused)
            terminated: whether game is terminated (unused)
            truncated: whether game is truncated (unused)
            info: additional info (unused)
            action_mask: mask indicating valid actions

        Returns:
            best action (column index)
        """
        # Get valid actions from mask
        valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]

        if not valid_actions:
            return 0  # Fallback (shouldn't happen)

        best_action = None
        best_value = float('-inf')

        # Evaluate each valid action
        for action in valid_actions:
            # Simulate our move
            new_board = self._simulate_move(observation, action, channel=0)

            # Evaluate position (opponent's turn next, so minimizing)
            value = self._minimax(new_board, self.depth - 1,
                                  float('-inf'), float('inf'), False)

            # Track best move
            if value > best_value:
                best_value = value
                best_action = action

        # Return best action or random if none found
        return best_action if best_action is not None else random.choice(valid_actions)