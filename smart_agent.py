"""
My Smart Agent for Connect Four

This agent uses rule-based heuristics to play strategically.
"""

import random
import numpy as np

class SmartAgent:
    """
    A rule-based agent that plays strategically
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
        self.player_name = player_name or "SmartAgent"
        self.rows = 6
        self.column = 7

    def choose_action(self, observation, reward=0.0, terminated=False, truncated=False, info=None, action_mask=None):
        """
        Choose an action using rule-based strategy

        Strategy priority:
        1. Win if possible
        2. Block opponent from winning
        3. Play center if available
        4. Random valid move
        """
        # Get valid actions
        valid_actions = self._get_valid_actions(action_mask)

        # Rule 1: Try to win
        winning_move = self._find_winning_move(observation, valid_actions, channel=0)
        if winning_move is not None:
            return winning_move

        # Rule 2: Block opponent
        blocking_move = self._find_winning_move(observation, valid_actions, channel=1)
        if blocking_move is not None:
            return blocking_move

        # Rule 3: Prefer center
        if 3 in valid_actions:
            return 3

        # Rule 4: Random fallback
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
            return [col for col in range(self.column) if action_mask[col] == 1 ]
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
        for row in range(self.rows -1, -1, -1):  # Start from bottom (row 5)
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
        directions = [(0,1), (1,0), (1,1), (1,-1)]
        for a, b in directions:
            count = 1
            if row + a < self.rows and col + b < self.column:
                r1 = row + a 
                c1 = col + b 
                
                A = board[r1, c1, channel]
                if A == 1:
                    count += 1
                while 0 <= r1 < self.rows -1 and 0 <= c1 < self.column - 1 and A == 1:
                    r1 += a
                    c1 += b 
                    if A == board[r1, c1, channel]:
                        count += 1
                    A = board[r1, c1, channel]
            if   self.rows > row - a >= 0 and  self.column > col - b >= 0 :
                r2 = row - a 
                c2 = col - b 
                B = board[r2, c2, channel]
                if B == 1:
                    count += 1
                while 0 <= r2 < self.rows -1 and 0 <= c2 < self.column - 1  and B == 1:
                    r2 -= a
                    c2 -= b 
                    if B == board[r2, c2, channel]:
                        count += 1
                    B = board[r2, c2, channel]
                
            if count >= 4 :
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
                if self._check_win_from_position(observation, row, col, channel) == True:
                    return col
        return None


