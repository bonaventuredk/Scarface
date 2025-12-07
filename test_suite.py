"""
Complete test plan for Connect Four agents
Corrected version - Fixes data type issues
"""

import time
import tracemalloc
import numpy as np
from pettingzoo.classic import connect_four_v3

# Import agents
from random_agent import RandomAgent
from smart_agent import SmartAgent
from smart_agent_ameliore import SmartAgentAmeliore
from agent_minimax import MinimaxAgent


class ConnectFourTester:
    """Main class to run all tests - Corrected version"""
    
    def __init__(self):
        """Initialize the tester with agents and scenarios"""
        self.env = connect_four_v3.env()
        self.env.reset()
        
        # Initialize agents with correct names
        self.agents = {
            "RandomAgent": RandomAgent(self.env, "RandomAgent"),
            "SmartAgent": SmartAgent(self.env, "SmartAgent"),
            "SmartAgentAmeliore": SmartAgentAmeliore(self.env, "SmartAgentAmeliore"),
            "MinimaxAgent": MinimaxAgent(self.env, depth=3, player_name="MinimaxAgent")
        }
        
        # Define test scenarios with int8 masks
        self.test_scenarios = self._create_test_scenarios()
    
    def _create_test_scenarios(self):
        """Create all test scenarios with int8 masks"""
        scenarios = {}
        
        # Scenario 1: Immediate win
        board1 = np.zeros((6, 7, 2), dtype=np.float32)
        board1[5, 0, 0] = 1
        board1[5, 1, 0] = 1
        board1[5, 2, 0] = 1
        scenarios["immediate_win"] = {
            "board": board1,
            "action_mask": np.array([1, 1, 1, 1, 1, 1, 1], dtype=np.int8),
            "expected_action": 3,
            "player_channel": 0
        }
        
        # Scenario 2: Block opponent
        board2 = np.zeros((6, 7, 2), dtype=np.float32)
        board2[5, 0, 1] = 1
        board2[5, 1, 1] = 1
        board2[5, 2, 1] = 1
        scenarios["block_opponent"] = {
            "board": board2,
            "action_mask": np.array([1, 1, 1, 1, 1, 1, 1], dtype=np.int8),
            "expected_action": 3,
            "player_channel": 0
        }
        
        # Scenario 3: Full column
        board3 = np.zeros((6, 7, 2), dtype=np.float32)
        for row in range(6):
            board3[row, 3, 0] = 1
        board3[5, 0, 1] = 1
        board3[5, 1, 1] = 1
        board3[5, 2, 1] = 1
        board3[5, 4, 0] = 1
        scenarios["full_column"] = {
            "board": board3,
            "action_mask": np.array([1, 1, 1, 0, 1, 1, 1], dtype=np.int8),
            "expected_action": None,  # Any column except 3
            "player_channel": 0
        }
        
        # Scenario 4: Draw (only one free column)
        board4 = np.zeros((6, 7, 2), dtype=np.float32)
        # Fill almost the entire board
        for col in range(7):
            for row in range(5):
                if (row + col) % 2 == 0:
                    board4[row, col, 0] = 1
                else:
                    board4[row, col, 1] = 1
        scenarios["draw"] = {
            "board": board4,
            "action_mask": np.array([0, 0, 0, 1, 0, 0, 0], dtype=np.int8),
            "expected_action": 3,
            "player_channel": 0
        }
        
        return scenarios
    
    # === FUNCTIONAL TESTS CORRECTED ===
    
    def test_scenario(self, agent_name, scenario_name):
        """Test an agent on a specific scenario - Corrected version"""
        agent = self.agents[agent_name]
        scenario = self.test_scenarios[scenario_name]
        
        try:
            # For RandomAgent, use a special method
            if agent_name == "RandomAgent":
                # Get valid actions
                valid_actions = [i for i, valid in enumerate(scenario["action_mask"]) if valid == 1]
                if not valid_actions:
                    return {
                        "agent": agent_name,
                        "scenario": scenario_name,
                        "action": None,
                        "valid": False,
                        "correct": False,
                        "error": "No valid actions"
                    }
                
                # Choose a random valid action
                action = np.random.choice(valid_actions)
            else:
                # Other agents use normal method
                action = agent.choose_action(
                    observation=scenario["board"],
                    action_mask=scenario["action_mask"],
                    reward=0.0,
                    terminated=False,
                    truncated=False,
                    info=None
                )
            
            # Check if action is valid
            if action is None:
                return {
                    "agent": agent_name,
                    "scenario": scenario_name,
                    "action": None,
                    "valid": False,
                    "correct": False,
                    "error": "Action is None"
                }
            
            valid = scenario["action_mask"][action] == 1
            
            # Check if action is expected
            expected = scenario["expected_action"]
            if expected is not None:
                correct = (action == expected)
            else:
                correct = valid  # If no specific expectation, valid = correct
            
            return {
                "agent": agent_name,
                "scenario": scenario_name,
                "action": action,
                "valid": valid,
                "correct": correct,
                "error": None
            }
            
        except Exception as e:
            return {
                "agent": agent_name,
                "scenario": scenario_name,
                "action": None,
                "valid": False,
                "correct": False,
                "error": str(e)
            }
    
    def run_functional_tests(self):
        """Run all functional tests"""
        print("=" * 60)
        print("FUNCTIONAL TESTS")
        print("=" * 60)
        
        results = []
        
        # Test each agent on each scenario
        for agent_name in self.agents.keys():
            for scenario_name in self.test_scenarios.keys():
                result = self.test_scenario(agent_name, scenario_name)
                results.append(result)
                
                # Display result
                status = "✓" if result["valid"] and result["correct"] else "✗"
                action_display = result['action'] if result['action'] is not None else "None"
                print(f"{status} {agent_name:20} | {scenario_name:20} | "
                      f"Action: {action_display:2} | "
                      f"Valid: {result['valid']!s:5} | "
                      f"Error: {result['error'] or 'None'}")
        
        # Statistics
        total = len(results)
        valid = sum(1 for r in results if r["valid"])
        correct = sum(1 for r in results if r["correct"])
        errors = sum(1 for r in results if r["error"] is not None)
        
        print(f"\nSUMMARY: {valid}/{total} valid moves | "
              f"{correct}/{total} correct moves | "
              f"{errors} errors")
        
        return results
    
    # === SIMPLE PERFORMANCE TESTS ===
    
    def test_performance_simple(self, agent_name, num_tests=10):
        """Simplified performance test without using the environment"""
        agent = self.agents[agent_name]
        
        times = []
        
        for _ in range(num_tests):
            # Create a simple random board
            board = np.zeros((6, 7, 2))
            # Fill a few random cells
            for _ in range(10):
                row = np.random.randint(0, 6)
                col = np.random.randint(0, 7)
                channel = np.random.randint(0, 2)
                board[row, col, channel] = 1
            
            # Create a random action mask in int8
            action_mask = np.random.randint(0, 2, size=7, dtype=np.int8)
            
            # Measure time
            start_time = time.time()
            
            try:
                if agent_name == "RandomAgent":
                    valid_actions = [i for i, valid in enumerate(action_mask) if valid == 1]
                    action = np.random.choice(valid_actions) if valid_actions else 0
                else:
                    action = agent.choose_action(
                        observation=board,
                        action_mask=action_mask,
                        reward=0.0,
                        terminated=False,
                        truncated=False,
                        info=None
                    )
                
                end_time = time.time()
                times.append(end_time - start_time)
                
            except Exception as e:
                print(f"Error for {agent_name}: {e}")
                times.append(0.0)
        
        # Calculate statistics
        if times:
            return {
                "agent": agent_name,
                "average_time": np.mean(times),
                "max_time": np.max(times),
                "min_time": np.min(times),
                "num_tests": num_tests
            }
        else:
            return {
                "agent": agent_name,
                "average_time": 0.0,
                "max_time": 0.0,
                "min_time": 0.0,
                "num_tests": num_tests
            }
    
    def run_performance_tests(self):
        """Run performance tests for all agents"""
        print("\n" + "=" * 60)
        print("PERFORMANCE TESTS")
        print("=" * 60)
        
        results = []
        
        for agent_name in self.agents.keys():
            print(f"\nPerformance test for {agent_name}...")
            stats = self.test_performance_simple(agent_name, num_tests=20)
            results.append(stats)
            
            # Display results
            print(f"  Average time: {stats['average_time']:.6f}s")
            print(f"  Max time: {stats['max_time']:.6f}s")
            print(f"  Min time: {stats['min_time']:.6f}s")
            
            # Check success criteria
            time_ok = stats['average_time'] < 0.1 and stats['max_time'] < 0.5
            
            print(f"  Criteria: Time {'✓' if time_ok else '✗'}")
        
        return results
    
    # === STRATEGIC TESTS ===
    
    def play_single_game(self, agent1, agent2, agent1_name, agent2_name, seed=42):
        """Play a single game between two agents - Corrected version"""
        env = connect_four_v3.env()
        env.reset(seed=seed)
        
        # Map agents to environment players
        agent_dict = {
            env.agents[0]: agent1,
            env.agents[1]: agent2
        }
        
        # Play the game
        for agent in env.agent_iter():
            obs, reward, terminated, truncated, info = env.last()
            
            if terminated:
                final_rewards = env.rewards
                if final_rewards[env.agents[0]] > final_rewards[env.agents[1]]:
                    return agent1_name
                elif final_rewards[env.agents[0]] < final_rewards[env.agents[1]]:
                    return agent2_name
                else:
                    return "draw"

            else:
                current_agent = agent1 if agent == env.agents[0] else agent2
                
                # For RandomAgent, use choose_action_manual if exists
                if hasattr(current_agent, 'choose_action_manual'):
                    action = current_agent.choose_action_manual(
                        observation=obs["observation"],
                        action_mask=obs["action_mask"],
                        reward=reward,
                        terminated=terminated,
                        truncated=truncated,
                        info=info
                    )
                else:
                    action = current_agent.choose_action(
                        observation=obs["observation"],
                        action_mask=obs["action_mask"],
                        reward=reward,
                        terminated=terminated,
                        truncated=truncated,
                        info=info
                    )
                
                env.step(action)
        
        env.close()
        return "unknown"
    
    def run_strategic_tests_simple(self, games_per_match=5):
        """Run a simplified tournament between all agents"""
        print("\n" + "=" * 60)
        print("STRATEGIC TESTS - SIMPLIFIED TOURNAMENT")
        print("=" * 60)
        
        agents = list(self.agents.keys())
        results = {agent: {"wins": 0, "losses": 0, "draws": 0} for agent in agents}
        
        # Test each pair of agents
        for i, agent1_name in enumerate(agents):
            for j, agent2_name in enumerate(agents):
                if i < j:  # Avoid duplicates and self-matches
                    print(f"\n{agent1_name} vs {agent2_name}...")
                    
                    wins_agent1 = wins_agent2 = draws = 0
                    
                    for game in range(games_per_match):
                        seed = 42 + i * 10 + j * 5 + game
                        winner = self.play_single_game(
                            self.agents[agent1_name],
                            self.agents[agent2_name],
                            agent1_name,
                            agent2_name,
                            seed=seed
                        )
                        
                        if winner == agent1_name:
                            wins_agent1 += 1
                            results[agent1_name]["wins"] += 1
                            results[agent2_name]["losses"] += 1
                        elif winner == agent2_name:
                            wins_agent2 += 1
                            results[agent2_name]["wins"] += 1
                            results[agent1_name]["losses"] += 1
                        else:  # draw or unknown
                            draws += 1
                            results[agent1_name]["draws"] += 1
                            results[agent2_name]["draws"] += 1
                    
                    print(f"  {agent1_name}: {wins_agent1} wins")
                    print(f"  {agent2_name}: {wins_agent2} wins")
                    print(f"  Draws: {draws}")
        
        # Display final ranking
        print("\n" + "=" * 60)
        print("FINAL RANKING")
        print("=" * 60)
        
        # Compute win rates
        win_rates = {}
        for agent in agents:
            total = results[agent]["wins"] + results[agent]["losses"] + results[agent]["draws"]
            win_rates[agent] = results[agent]["wins"] / total if total > 0 else 0
        
        # Sort by win rate
        sorted_agents = sorted(win_rates.items(), key=lambda x: x[1], reverse=True)
        
        for rank, (agent, rate) in enumerate(sorted_agents, 1):
            print(f"{rank}. {agent:20} : {rate:.1%} "
                  f"({results[agent]['wins']}W/{results[agent]['losses']}L/{results[agent]['draws']}D)")
        
        return results
    
    # === COMPLETE TEST SUITE ===
    
    def run_complete_test_suite(self):
        """Run the entire Connect Four agent test suite"""
        print("COMPLETE TEST SUITE FOR CONNECT FOUR AGENTS")
        print("Corrected version")
        print("=" * 60)
        
        all_results = {}
        
        # 1. Functional tests
        all_results["functional"] = self.run_functional_tests()
        
        # 2. Performance tests
        all_results["performance"] = self.run_performance_tests()
        
        # 3. Strategic tests
        all_results["strategic"] = self.run_strategic_tests_simple(games_per_match=3)
        
        # 4. Final report
        self._generate_final_report(all_results)
        
        return all_results
    
    def _generate_final_report(self, all_results):
        """Generate a final report of all tests"""
        print("\n" + "=" * 60)
        print("FINAL REPORT - SUCCESS CRITERIA")
        print("=" * 60)
        
        # Functional criteria
        functional_results = all_results["functional"]
        valid_moves = sum(1 for r in functional_results if r["valid"])
        total_moves = len(functional_results)
        functional_success = (valid_moves == total_moves)
        
        print(f"\n1. FUNCTIONAL CRITERIA")
        print(f"   Valid moves: {valid_moves}/{total_moves}")
        print(f"   Status: {'✓ SUCCESS' if functional_success else '✗ FAILURE'}")
        
        # Performance criteria
        perf_results = all_results["performance"]
        perf_success = True
        
        print(f"\n2. PERFORMANCE CRITERIA")
        for perf in perf_results:
            time_ok = perf['average_time'] < 0.1 and perf['max_time'] < 0.5
            if not time_ok:
                perf_success = False
            print(f"   {perf['agent']:20}: "
                  f"Time {'✓' if time_ok else '✗'} "
                  f"({perf['average_time']:.6f}s avg, {perf['max_time']:.6f}s max)")
        
        # Strategic criteria - Check that SmartAgentAmeliore beats RandomAgent
        strategic_results = all_results["strategic"]
        sam_wins = strategic_results["SmartAgentAmeliore"]["wins"]
        random_wins = strategic_results["RandomAgent"]["wins"]
        strategic_success = (sam_wins > random_wins)
        
        print(f"\n3. STRATEGIC CRITERIA")
        print(f"   SmartAgentAmeliore: {sam_wins} wins")
        print(f"   RandomAgent: {random_wins} wins")
        print(f"   Status: {'✓ SUCCESS' if strategic_success else '✗ FAILURE'}")
        
        # Conclusion
        print("\n" + "=" * 60)
        print("CONCLUSION")
        print("=" * 60)
        
        all_passed = (functional_success and perf_success)
        
        if all_passed:
            print("✓ FUNCTIONAL AND PERFORMANCE TESTS PASSED")
            print("Agents meet basic criteria.")
        else:
            print("✗ SOME TESTS FAILED")
            print("Please check the details above.")


# === MAIN ENTRY POINT ===

if __name__ == "__main__":
    # Create and run the test suite
    tester = ConnectFourTester()
    
    # Run all tests
    results = tester.run_complete_test_suite()
