"""
My Smart Agent for Connect Four

This agent uses advanced rule-based heuristics to play strategically.
"""

import random
import numpy as np

class SmartAgentAmeliore:
    """
    An enhanced rule-based agent that plays strategically
    """

    def __init__(self, env, player_name=None):
        """
        Initialize the smart agent

        Parameters:
            env: PettingZoo environment
            player_name: Optional name for the agent
        """
        self.env = env
        self.action_space = env.action_space(env.agents[0])
        self.player_name = player_name or "SmartAgentAmeliore"
        self.rows = 6
        self.column = 7

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose an action using advanced rule-based strategy

        Strategy priority:
        1. Win immediately
        2. Block opponent from winning
        3. Create double threat
        4. Block opponent double threat
        5. Create forks (multiple threats)
        6. Prefer center columns with strategic weighting
        7. Random valid move
        """
        # Get valid actions
        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Try to win immediately
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            return winning_move

        # Rule 2: Block opponent from winning
        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move

        # Rule 3: Create double threat (unbeatable if opponent can't win next)
        double_threat_move = self._find_double_threat_move(observation, valid_actions, channel=0)
        if double_threat_move is not None:
            return double_threat_move

        # Rule 4: Block opponent double threat
        block_double_threat = self._find_double_threat_move(observation, valid_actions, channel=1)
        if block_double_threat is not None:
            return block_double_threat

        # Rule 5: Create strategic forks
        fork_move = self._find_fork_move(observation, valid_actions, channel=0)
        if fork_move is not None:
            return fork_move

        # Rule 6: Block opponent forks
        block_fork = self._find_fork_move(observation, valid_actions, channel=1)
        if block_fork is not None:
            return block_fork

        # Rule 7: Strategic center preference with scoring
        scored_moves = []
        for col in valid_actions:
            score = self._evaluate_position_score(observation, col, channel=0)
            scored_moves.append((col, score))
        
        # Choose the move with highest score
        if scored_moves:
            scored_moves.sort(key=lambda x: x[1], reverse=True)
            return scored_moves[0][0]

        # Rule 8: Random fallback
        return random.choice(valid_actions)

    def _get_valid_actions(self, action_mask):
        """
        Get list of valid column indices

        Parameters:
            action_mask: numpy array (7,) with 1 for valid, 0 for invalid

        Returns:
            list of valid column indices
        """
        if action_mask is not None:
            # Convert action_mask to list of valid column indices
            return [col for col in range(self.column) if action_mask[col] == 1]
        else:
            # If not, we assume that all columns are valid
            return list(range(self.column))

    def _get_next_row(self, board, col):
        """
        Find which row a piece would land in if dropped in column col

        Parameters:
            board: numpy array (6, 7, 2)
            col: column index (0-6)

        Returns:
            row index (0-5) if space available, None if column full
        """
        for row in range(self.rows - 1, -1, -1):  # Start from bottom (row 5)
            if board[row, col, 0] == 0 and board[row, col, 1] == 0:
                return row  # This position is empty
        return None  # Column is full

    def _check_win_from_position(self, board, row, col, channel):
        """
        Check if placing a piece at (row, col) would create 4 in a row

        Parameters:
            board: numpy array (6, 7, 2)
            row: row index (0-5)
            col: column index (0-6)
            channel: 0 or 1 (which player's pieces to check)

        Returns:
            True if this position creates 4 in a row/col/diag, False otherwise
        """
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]  # horizontal, vertical, diagonal
        for dr, dc in directions:
            count = 1  # Count the current position
            
            # Check positive direction
            r, c = row + dr, col + dc
            while 0 <= r < self.rows and 0 <= c < self.column and board[r, c, channel] == 1:
                count += 1
                r += dr
                c += dc
            
            # Check negative direction  
            r, c = row - dr, col - dc
            while 0 <= r < self.rows and 0 <= c < self.column and board[r, c, channel] == 1:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 4:
                return True
        return False

    def _find_winning_move(self, observation, valid_actions, channel):
        """
        Find a move that creates 4 in a row for the specified player

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if winning move found, None otherwise
        """
        for col in valid_actions:
            # Find where the piece would land in this column
            row = self._get_next_row(observation, col)
            if row is not None:
                # Check if this move would create a winning position
                if self._check_win_from_position(observation, row, col, channel):
                    return col
        return None

    def _find_double_threat_move(self, observation, valid_actions, channel):
        """
        Find a move that creates two separate winning threats

        Parameters:
            observation: numpy array (6, 7, 2) - current board state
            valid_actions: list of valid column indices
            channel: 0 for current player, 1 for opponent

        Returns:
            column index (int) if double threat move found, None otherwise
        """
        for col in valid_actions:
            if self._creates_double_threat(observation, col, channel):
                return col
        return None

    def _creates_double_threat(self, board, col, channel):
        """
        Check if playing column col creates two separate winning threats

        A double threat is unbeatable because opponent can only block one.

        Returns:
            True if move creates double threat, False otherwise
        """
        # Create a copy of the board to simulate the move
        board_copy = board.copy()
        row = self._get_next_row(board_copy, col)
        if row is None:
            return False
            
        # Place the piece on the copied board
        board_copy[row, col, channel] = 1
        
        # Count how many winning moves are available after this move
        winning_threats = 0
        
        # Check all columns for winning moves in the next turn
        for next_col in range(self.column):
            next_row = self._get_next_row(board_copy, next_col)
            if next_row is not None:
                # Create a temporary copy to check win without modifying the main copy
                temp_board = board_copy.copy()
                if self._check_win_from_position(temp_board, next_row, next_col, channel):
                    winning_threats += 1
                    # If we found 2 threats, we can return early
                    if winning_threats >= 2:
                        return True
        
        return winning_threats >= 2

    def _find_fork_move(self, observation, valid_actions, channel):
        """
        Find moves that create multiple potential winning lines (forks)
        
        A fork creates multiple ways to win in future moves
        """
        best_fork_score = -1
        best_fork_move = None
        
        for col in valid_actions:
            fork_score = self._evaluate_fork_potential(observation, col, channel)
            if fork_score > best_fork_score:
                best_fork_score = fork_score
                best_fork_move = col
        
        # Only return if we found a good fork opportunity
        if best_fork_score >= 2:  # At least 2 potential winning lines
            return best_fork_move
        return None

    def _evaluate_fork_potential(self, board, col, channel):
        """
        Evaluate how many potential winning lines this move creates
        """
        board_copy = board.copy()
        row = self._get_next_row(board_copy, col)
        if row is None:
            return 0
            
        # Place the piece
        board_copy[row, col, channel] = 1
        
        # Count potential winning lines in different directions
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        potential_lines = 0
        
        for dr, dc in directions:
            # Check if this direction has potential for a winning line
            line_potential = self._check_line_potential(board_copy, row, col, channel, dr, dc)
            if line_potential:
                potential_lines += 1
        
        return potential_lines

    def _check_line_potential(self, board, row, col, channel, dr, dc):
        """
        Check if a line in given direction has potential to become a winning line
        """
        count = 1  # Current position
        
        # Check positive direction
        r, c = row + dr, col + dc
        consecutive_empty = 0
        while 0 <= r < self.rows and 0 <= c < self.column and consecutive_empty < 2:
            if board[r, c, channel] == 1:
                count += 1
            elif board[r, c, 0] == 0 and board[r, c, 1] == 0:
                consecutive_empty += 1
            else:
                break  # Opponent piece blocking
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        consecutive_empty = 0
        while 0 <= r < self.rows and 0 <= c < self.column and consecutive_empty < 2:
            if board[r, c, channel] == 1:
                count += 1
            elif board[r, c, 0] == 0 and board[r, c, 1] == 0:
                consecutive_empty += 1
            else:
                break  # Opponent piece blocking
            r -= dr
            c -= dc
        
        return count >= 3  # At least 3 in a row with potential to extend

    def _evaluate_position_score(self, board, col, channel):
        """
        Evaluate the strategic value of a position
        
        Higher scores for:
        - Center columns
        - Creating potential winning lines
        - Blocking opponent
        - Building from existing pieces
        """
        row = self._get_next_row(board, col)
        if row is None:
            return -1000  # Invalid move
            
        score = 0
        
        # Center preference (highest in center, decreasing towards edges)
        center_scores = [1, 2, 3, 4, 3, 2, 1]  # Columns 0-6
        score += center_scores[col]
        
        # Check if this connects with existing pieces
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            # Check for connections with friendly pieces
            connections = self._count_connections(board, row, col, channel, dr, dc)
            score += connections * 2  # Bonus for connecting pieces
            
            # Check for blocking opponent
            opponent_connections = self._count_connections(board, row, col, 1 - channel, dr, dc)
            if opponent_connections >= 2:  # If opponent has 2+ in a row
                score += opponent_connections * 3  # Big bonus for blocking
        
        # Bonus for creating potential winning setups
        if self._creates_potential_win(board, row, col, channel):
            score += 5
        
        return score

    def _count_connections(self, board, row, col, channel, dr, dc):
        """
        Count how many friendly pieces are connected in a line
        """
        count = 0
        
        # Check positive direction
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.column and board[r, c, channel] == 1:
            count += 1
            r += dr
            c += dc
        
        # Check negative direction
        r, c = row - dr, col - dc
        while 0 <= r < self.rows and 0 <= c < self.column and board[r, c, channel] == 1:
            count += 1
            r -= dr
            c -= dc
        
        return count

    def _creates_potential_win(self, board, row, col, channel):
        """
        Check if this move creates a strong potential winning position
        """
        # Check all directions for potential wins
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            # Simulate the move and check for strong positions
            if self._has_strong_potential(board, row, col, channel, dr, dc):
                return True
        
        return False

    def _has_strong_potential(self, board, row, col, channel, dr, dc):
        """
        Check if this position creates a strong potential in a specific direction
        """
        # Count consecutive pieces and empty spaces in this direction
        consecutive = 1  # Current piece
        empty_spaces = 0
        
        # Positive direction
        r, c = row + dr, col + dc
        while 0 <= r < self.rows and 0 <= c < self.column and empty_spaces < 2:
            if board[r, c, channel] == 1:
                consecutive += 1
            elif board[r, c, 0] == 0 and board[r, c, 1] == 0:
                empty_spaces += 1
            else:
                break
            r += dr
            c += dc
        
        # Negative direction
        r, c = row - dr, col - dc
        empty_spaces = 0
        while 0 <= r < self.rows and 0 <= c < self.column and empty_spaces < 2:
            if board[r, c, channel] == 1:
                consecutive += 1
            elif board[r, c, 0] == 0 and board[r, c, 1] == 0:
                empty_spaces += 1
            else:
                break
            r -= dr
            c -= dc
        
        # If we have 3+ consecutive with at least 1 empty space to complete
        return consecutive >= 3