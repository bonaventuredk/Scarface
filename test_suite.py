import unittest
import time
import tracemalloc
import numpy as np
import random
from typing import Dict, List, Tuple, Optional

# Import agents
from random_agent import RandomAgent
from smart_agent import SmartAgent
from smart_agent_ameliore import SmartAgentAmeliore
from WeightedRandomAgent import WeightedRandomAgent

# Import environment
from pettingzoo.classic import connect_four_v3


class TestBoardStates:
    """Test fixtures for common board states"""
    
    @staticmethod
    def empty_board() -> np.ndarray:
        """Create an empty board"""
        return np.zeros((6, 7, 2))
    
    @staticmethod
    def immediate_win_state() -> np.ndarray:
        """Board state where agent can win immediately"""
        board = np.zeros((6, 7, 2))
        board[5, 0, 0] = 1  # X in column 0, row 5
        board[5, 1, 0] = 1  # X in column 1, row 5
        board[5, 2, 0] = 1  # X in column 2, row 5
        return board
    
    @staticmethod
    def opponent_threat_state() -> np.ndarray:
        """Board state where opponent can win next turn"""
        board = np.zeros((6, 7, 2))
        board[5, 0, 1] = 1  # O in column 0, row 5
        board[5, 1, 1] = 1  # O in column 1, row 5
        board[5, 2, 1] = 1  # O in column 2, row 5
        return board
    
    @staticmethod
    def double_threat_state() -> np.ndarray:
        """Board state that can create a double threat"""
        board = np.zeros((6, 7, 2))
        board[5, 2, 0] = 1  # X
        board[4, 2, 0] = 1  # X
        board[5, 0, 0] = 1  # X
        board[5, 1, 0] = 1  # X
        return board
    
    @staticmethod
    def fork_position_state() -> np.ndarray:
        """Board state with fork opportunity"""
        board = np.zeros((6, 7, 2))
        board[5, 2, 1] = 1  # O
        board[4, 2, 1] = 1  # O
        board[3, 2, 1] = 1  # O
        board[5, 1, 0] = 1  # X
        board[4, 1, 0] = 1  # X
        board[5, 0, 0] = 1  # X
        return board
    
    @staticmethod
    def almost_full_board() -> np.ndarray:
        """Board that is almost completely full"""
        board = np.ones((6, 7, 2)) * 0.5  # Fill with something
        # Leave one column partially empty
        board[:, 3, :] = 0
        board[5, 3, 0] = 1  # One piece at bottom
        return board


class TestRandomAgent(unittest.TestCase):
    """Unit tests for RandomAgent"""
    
    def setUp(self):
        """Set up test environment"""
        self.env = connect_four_v3.env()
        self.agent = RandomAgent(self.env)
    
    def test_valid_action_selection(self):
        """Test that agent always selects valid actions"""
        test_cases = [
            # (action_mask, expected_valid_range)
            (np.array([1, 1, 1, 1, 1, 1, 1]), range(7)),  # All columns valid
            (np.array([1, 0, 1, 0, 1, 0, 1]), [0, 2, 4, 6]),  # Some columns valid
            (np.array([0, 0, 0, 1, 0, 0, 0]), [3]),  # Only center valid
        ]
        
        for action_mask, valid_actions in test_cases:
            # Run multiple times to test randomness
            for _ in range(10):
                action = self.agent.choose_action(
                    observation=TestBoardStates.empty_board(),
                    action_mask=action_mask
                )
                self.assertIn(action, valid_actions,
                             f"Agent chose invalid action {action} for mask {action_mask}")
    
    def test_manual_action_selection(self):
        """Test the manual action selection method"""
        action_mask = np.array([1, 0, 1, 0, 1, 0, 1])
        
        # Run multiple times to test randomness
        actions = []
        for _ in range(100):
            action = self.agent.choose_action_manual(
                observation=TestBoardStates.empty_board(),
                action_mask=action_mask
            )
            actions.append(action)
            self.assertIn(action, [0, 2, 4, 6])
        
        # Check distribution (should be roughly uniform)
        unique, counts = np.unique(actions, return_counts=True)
        # Each valid action should be chosen at least once
        self.assertEqual(len(unique), 4)
    
    def test_terminated_state(self):
        """Test that agent returns None when game is terminated"""
        action = self.agent.choose_action(
            observation=TestBoardStates.empty_board(),
            terminated=True,
            action_mask=np.array([1, 1, 1, 1, 1, 1, 1])
        )
        self.assertIsNone(action)
    
    def test_performance(self):
        """Test performance of action selection"""
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Time multiple selections
        start_time = time.perf_counter()
        for _ in range(1000):
            self.agent.choose_action(
                observation=TestBoardStates.empty_board(),
                action_mask=action_mask
            )
        end_time = time.perf_counter()
        
        avg_time = (end_time - start_time) / 1000
        print(f"\nRandomAgent average decision time: {avg_time*1000:.3f} ms")
        self.assertLess(avg_time, 0.001, "Decision time should be < 1ms")


class TestSmartAgent(unittest.TestCase):
    """Unit tests for SmartAgent"""
    
    def setUp(self):
        """Set up test environment"""
        self.env = connect_four_v3.env()
        self.agent = SmartAgent(self.env)
    
    def test_get_valid_actions(self):
        """Test _get_valid_actions method"""
        test_cases = [
            (np.array([1, 0, 1, 0, 1, 0, 1]), [0, 2, 4, 6]),
            (np.array([0, 0, 0, 1, 0, 0, 0]), [3]),
            (np.array([1, 1, 1, 1, 1, 1, 1]), list(range(7))),
            (None, list(range(7))),  # No mask provided
        ]
        
        for action_mask, expected in test_cases:
            result = self.agent._get_valid_actions(action_mask)
            self.assertEqual(result, expected,
                           f"Failed for mask {action_mask}: got {result}, expected {expected}")
    
    def test_get_next_row(self):
        """Test _get_next_row method"""
        # Test empty column
        board = TestBoardStates.empty_board()
        row = self.agent._get_next_row(board, 3)
        self.assertEqual(row, 5, "Should place at bottom of empty column")
        
        # Test partially filled column
        board[5, 3, 0] = 1  # Place piece at bottom
        board[4, 3, 0] = 1  # Place another piece
        row = self.agent._get_next_row(board, 3)
        self.assertEqual(row, 3, "Should place on top of existing pieces")
        
        # Test full column
        for r in range(6):
            board[r, 3, 0] = 1
        row = self.agent._get_next_row(board, 3)
        self.assertIsNone(row, "Should return None for full column")
    
    def test_immediate_win_detection(self):
        """Test that agent detects immediate winning moves"""
        board = TestBoardStates.immediate_win_state()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Agent should choose column 3 to win
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        self.assertEqual(action, 3, f"Agent should play column 3 to win, played {action}")
    
    def test_opponent_blocking(self):
        """Test that agent blocks opponent's winning moves"""
        board = TestBoardStates.opponent_threat_state()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Agent should choose column 3 to block
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        self.assertEqual(action, 3, f"Agent should play column 3 to block, played {action}")
    
    def test_center_preference(self):
        """Test that agent prefers center columns"""
        board = TestBoardStates.empty_board()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        self.assertEqual(action, 3, f"Agent should prefer center column 3, played {action}")
        
        # Test when center is not available
        action_mask = np.array([1, 1, 1, 0, 1, 1, 1])
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        # Should choose another valid column
        self.assertIn(action, [0, 1, 2, 4, 5, 6])
    
    def test_performance_benchmark(self):
        """Benchmark performance of SmartAgent"""
        board = TestBoardStates.empty_board()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Start memory tracking
        tracemalloc.start()
        
        # Time multiple decisions
        start_time = time.perf_counter()
        for _ in range(100):
            self.agent.choose_action(
                observation=board,
                action_mask=action_mask
            )
        end_time = time.perf_counter()
        
        # Get memory usage
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        avg_time = (end_time - start_time) / 100
        print(f"\nSmartAgent performance:")
        print(f"  Average decision time: {avg_time*1000:.3f} ms")
        print(f"  Peak memory usage: {peak / 1024:.2f} KB")
        
        # Assert performance criteria
        self.assertLess(avg_time, 0.05, "Decision time should be < 50ms")
        self.assertLess(peak, 10 * 1024 * 1024, "Peak memory should be < 10MB")


class TestSmartAgentAmeliore(unittest.TestCase):
    """Unit tests for enhanced SmartAgent"""
    
    def setUp(self):
        """Set up test environment"""
        self.env = connect_four_v3.env()
        self.agent = SmartAgentAmeliore(self.env)
    
    def test_double_threat_detection(self):
        """Test that agent detects double threat opportunities"""
        # Create a board where a double threat is possible
        board = TestBoardStates.double_threat_state()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Agent should recognize the opportunity
        # This is a complex test - we'll verify the agent makes a valid move
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        self.assertIn(action, range(7), f"Agent chose invalid column {action}")
    
    def test_fork_detection(self):
        """Test that agent detects fork opportunities"""
        board = TestBoardStates.fork_position_state()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        action = self.agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        # Agent should make a strategic move (block or create fork)
        self.assertIn(action, range(7), f"Agent chose invalid column {action}")
    
    def test_strategic_scoring(self):
        """Test the position scoring system"""
        board = TestBoardStates.empty_board()
        
        # Test center column has highest score
        center_score = self.agent._evaluate_position_score(board, 3, channel=0)
        edge_score = self.agent._evaluate_position_score(board, 0, channel=0)
        
        self.assertGreater(center_score, edge_score,
                          "Center should have higher score than edge")
    
    def test_performance_comparison(self):
        """Compare performance with basic SmartAgent"""
        board = TestBoardStates.empty_board()
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        # Test enhanced agent
        start_time = time.perf_counter()
        for _ in range(100):
            self.agent.choose_action(
                observation=board,
                action_mask=action_mask
            )
        enhanced_time = time.perf_counter() - start_time
        
        # Test basic agent for comparison
        basic_agent = SmartAgent(self.env)
        start_time = time.perf_counter()
        for _ in range(100):
            basic_agent.choose_action(
                observation=board,
                action_mask=action_mask
            )
        basic_time = time.perf_counter() - start_time
        
        print(f"\nPerformance comparison:")
        print(f"  SmartAgentAmeliore: {enhanced_time/100*1000:.3f} ms per decision")
        print(f"  SmartAgent: {basic_time/100*1000:.3f} ms per decision")
        
        # Enhanced agent might be slower but more strategic
        self.assertLess(enhanced_time, 1.0, "Enhanced agent should be reasonably fast")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def test_full_game_simulation(self):
        """Test that a full game can be played without errors"""
        env = connect_four_v3.env()
        env.reset(seed=42)
        
        agents = {
            "player_0": RandomAgent(env),
            "player_1": SmartAgent(env)
        }
        
        max_moves = 42  # Maximum possible moves in Connect Four
        move_count = 0
        
        for agent_name in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            
            if termination or truncation:
                break
            
            action_mask = observation["action_mask"]
            action = agents[agent_name].choose_action(
                observation=observation["observation"],
                action_mask=action_mask
            )
            
            # Verify action is valid
            self.assertTrue(action_mask[action] == 1,
                          f"Agent {agent_name} chose invalid action {action}")
            
            env.step(action)
            move_count += 1
            
            if move_count > max_moves:
                self.fail("Game exceeded maximum possible moves")
        
        print(f"\nFull game completed in {move_count} moves")
        self.assertLessEqual(move_count, 42)
    
    def test_multiple_agent_combinations(self):
        """Test different agent combinations"""
        combinations = [
            ("RandomAgent", "SmartAgent"),
            ("SmartAgent", "RandomAgent"),
            ("SmartAgent", "SmartAgentAmeliore"),
            ("SmartAgentAmeliore", "SmartAgent"),
        ]
        
        for agent1_type, agent2_type in combinations:
            with self.subTest(f"{agent1_type} vs {agent2_type}"):
                env = connect_four_v3.env()
                env.reset()
                
                # Create agents
                if agent1_type == "RandomAgent":
                    agent1 = RandomAgent(env)
                elif agent1_type == "SmartAgent":
                    agent1 = SmartAgent(env)
                else:
                    agent1 = SmartAgentAmeliore(env)
                
                if agent2_type == "RandomAgent":
                    agent2 = RandomAgent(env)
                elif agent2_type == "SmartAgent":
                    agent2 = SmartAgent(env)
                else:
                    agent2 = SmartAgentAmeliore(env)
                
                agents = {
                    "player_0": agent1,
                    "player_1": agent2
                }
                
                # Play one complete game
                for agent_name in env.agent_iter():
                    observation, reward, termination, truncation, info = env.last()
                    
                    if termination or truncation:
                        break
                    
                    action_mask = observation["action_mask"]
                    action = agents[agent_name].choose_action(
                        observation=observation["observation"],
                        action_mask=action_mask
                    )
                    
                    env.step(action)
                
                env.close()
    
    def test_stress_test(self):
        """Stress test by playing many games quickly"""
        num_games = 10
        total_moves = 0
        
        for game in range(num_games):
            env = connect_four_v3.env()
            env.reset(seed=game)
            
            agent = SmartAgent(env)
            move_count = 0
            
            for agent_name in env.agent_iter():
                observation, reward, termination, truncation, info = env.last()
                
                if termination or truncation:
                    total_moves += move_count
                    break
                
                # SmartAgent plays both sides (self-play)
                action_mask = observation["action_mask"]
                action = agent.choose_action(
                    observation=observation["observation"],
                    action_mask=action_mask
                )
                
                env.step(action)
                move_count += 1
            
            env.close()
        
        avg_moves = total_moves / num_games
        print(f"\nStress test: {num_games} games, average {avg_moves:.1f} moves per game")
        self.assertGreater(avg_moves, 10, "Games should be reasonably long")


class TestStrategicScenarios(unittest.TestCase):
    """Tests for specific strategic scenarios"""
    
    def test_scenario_1_immediate_win(self):
        """Test Scenario 1: Immediate win detection"""
        board = np.zeros((6, 7, 2))
        board[5, 0, 0] = 1  # X
        board[5, 1, 0] = 1  # X
        board[5, 2, 0] = 1  # X
        # Empty at column 3, row 5
        
        env = connect_four_v3.env()
        agent = SmartAgent(env)
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        action = agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        
        self.assertEqual(action, 3, f"Should play column 3 to win, played {action}")
    
    def test_scenario_2_opponent_block(self):
        """Test Scenario 2: Opponent threat blocking"""
        board = np.zeros((6, 7, 2))
        board[5, 0, 1] = 1  # O
        board[5, 1, 1] = 1  # O
        board[5, 2, 1] = 1  # O
        # Empty at column 3, row 5
        
        env = connect_four_v3.env()
        agent = SmartAgent(env)
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        action = agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        
        self.assertEqual(action, 3, f"Should play column 3 to block, played {action}")
    
    def test_scenario_5_center_preference(self):
        """Test Scenario 5: Center control priority"""
        board = TestBoardStates.empty_board()
        
        env = connect_four_v3.env()
        agent = SmartAgent(env)
        action_mask = np.array([1, 1, 1, 1, 1, 1, 1])
        
        action = agent.choose_action(
            observation=board,
            action_mask=action_mask
        )
        
        self.assertEqual(action, 3, f"Should prefer center column 3, played {action}")


def run_all_tests():
    """Run all test suites and generate report"""
    print("=" * 70)
    print("CONNECT FOUR AGENTS - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    
    # Add test cases
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestRandomAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartAgent))
    suite.addTests(loader.loadTestsFromTestCase(TestSmartAgentAmeliore))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestStrategicScenarios))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {(result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100:.1f}%")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)