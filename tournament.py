[file name]: tournament.py
[file content begin]
"""
Tournament System for Connect Four Agents

This module implements a comprehensive tournament system to compare
different agents against each other and analyze their performance.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Any
import time
import json
import os
from datetime import datetime
from collections import defaultdict

# Import agents
from random_agent import RandomAgent
from smart_agent import SmartAgent
from smart_agent_ameliore import SmartAgentAmeliore
from WeightedRandomAgent import WeightedRandomAgent

# Import environment
from pettingzoo.classic import connect_four_v3


class TournamentStats:
    """Statistics collector for tournament games"""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset all statistics"""
        self.games_played = 0
        self.wins = defaultdict(int)
        self.losses = defaultdict(int)
        self.draws = defaultdict(int)
        self.total_moves = defaultdict(list)
        self.decision_times = defaultdict(list)
        self.win_streaks = defaultdict(int)
        self.max_win_streaks = defaultdict(int)
        self.last_winner = None
        
    def record_game(self, agent1: str, agent2: str, winner: Optional[str], 
                   moves: int, decision_times: Dict[str, float]):
        """Record results of a single game"""
        self.games_played += 1
        
        # Update win/loss/draw counts
        if winner == agent1:
            self.wins[agent1] += 1
            self.losses[agent2] += 1
            self._update_streak(agent1, agent2)
        elif winner == agent2:
            self.wins[agent2] += 1
            self.losses[agent1] += 1
            self._update_streak(agent2, agent1)
        else:  # Draw
            self.draws[agent1] += 1
            self.draws[agent2] += 1
            self.win_streaks[agent1] = 0
            self.win_streaks[agent2] = 0
        
        # Record moves and decision times
        self.total_moves[agent1].append(moves)
        self.total_moves[agent2].append(moves)
        
        for agent, dt in decision_times.items():
            self.decision_times[agent].append(dt)
    
    def _update_streak(self, winner: str, loser: str):
        """Update win streaks"""
        self.win_streaks[winner] += 1
        self.win_streaks[loser] = 0
        
        # Update max win streak
        if self.win_streaks[winner] > self.max_win_streaks[winner]:
            self.max_win_streaks[winner] = self.win_streaks[winner]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of statistics"""
        summary = {
            'games_played': self.games_played,
            'agents': {},
            'overall': {}
        }
        
        all_agents = set(list(self.wins.keys()) + list(self.losses.keys()) + list(self.draws.keys()))
        
        for agent in all_agents:
            total_games = (self.wins[agent] + self.losses[agent] + self.draws[agent])
            if total_games > 0:
                win_rate = self.wins[agent] / total_games
                draw_rate = self.draws[agent] / total_games
                avg_moves = np.mean(self.total_moves[agent]) if self.total_moves[agent] else 0
                avg_decision_time = np.mean(self.decision_times[agent]) if self.decision_times[agent] else 0
                
                summary['agents'][agent] = {
                    'wins': self.wins[agent],
                    'losses': self.losses[agent],
                    'draws': self.draws[agent],
                    'total_games': total_games,
                    'win_rate': win_rate,
                    'draw_rate': draw_rate,
                    'avg_moves': avg_moves,
                    'avg_decision_time_ms': avg_decision_time * 1000,
                    'max_win_streak': self.max_win_streaks[agent]
                }
        
        # Calculate overall metrics
        if all_agents:
            summary['overall'] = {
                'total_games': self.games_played,
                'unique_agents': len(all_agents),
                'avg_moves_per_game': np.mean([np.mean(moves) for moves in self.total_moves.values() if moves]),
                'avg_decision_time_ms': np.mean([np.mean(times) * 1000 for times in self.decision_times.values() if times])
            }
        
        return summary
    
    def save_to_file(self, filename: str):
        """Save statistics to JSON file"""
        summary = self.get_summary()
        
        # Add timestamp
        summary['timestamp'] = datetime.now().isoformat()
        summary['metadata'] = {
            'description': 'Connect Four Tournament Results',
            'version': '1.0'
        }
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"Statistics saved to {filename}")


class Tournament:
    """Main tournament class"""
    
    def __init__(self, agents: Dict[str, Any], num_games_per_matchup: int = 10):
        """
        Initialize tournament
        
        Args:
            agents: Dictionary of agent names to agent instances
            num_games_per_matchup: Number of games to play for each matchup
        """
        self.agents = agents
        self.num_games_per_matchup = num_games_per_matchup
        self.stats = TournamentStats()
        self.results_dir = "tournament_results"
        
        # Create results directory if it doesn't exist
        os.makedirs(self.results_dir, exist_ok=True)
    
    def _create_env(self):
        """Create a new environment instance"""
        return connect_four_v3.env(render_mode=None)
    
    def play_game(self, agent1_name: str, agent2_name: str, 
                  agent1_instance: Any, agent2_instance: Any,
                  seed: Optional[int] = None) -> Tuple[Optional[str], int, Dict[str, float]]:
        """
        Play a single game between two agents
        
        Returns:
            Tuple of (winner_name, total_moves, decision_times)
        """
        env = self._create_env()
        if seed is not None:
            env.reset(seed=seed)
        else:
            env.reset()
        
        agents = {
            "player_0": (agent1_name, agent1_instance),
            "player_1": (agent2_name, agent2_instance)
        }
        
        move_count = 0
        decision_times = {agent1_name: [], agent2_name: []}
        winner = None
        
        for agent_name in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            
            if termination or truncation:
                # Determine winner
                if reward == 1:  # player_0 wins
                    winner = agent1_name
                elif reward == -1:  # player_1 wins
                    winner = agent2_name
                else:  # Draw
                    winner = None
                break
            
            # Get current agent
            current_agent_name, current_agent = agents[agent_name]
            
            # Time the decision
            start_time = time.perf_counter()
            action = current_agent.choose_action(
                observation=observation["observation"],
                action_mask=observation["action_mask"]
            )
            decision_time = time.perf_counter() - start_time
            
            # Record decision time
            decision_times[current_agent_name].append(decision_time)
            
            # Make the move
            env.step(action)
            move_count += 1
        
        env.close()
        
        # Calculate average decision times
        avg_decision_times = {
            agent1_name: np.mean(decision_times[agent1_name]) if decision_times[agent1_name] else 0,
            agent2_name: np.mean(decision_times[agent2_name]) if decision_times[agent2_name] else 0
        }
        
        return winner, move_count, avg_decision_times
    
    def run_matchup(self, agent1_name: str, agent2_name: str) -> Dict[str, Any]:
        """Run multiple games between two agents"""
        print(f"\n{'='*60}")
        print(f"MATCHUP: {agent1_name} vs {agent2_name}")
        print(f"{'='*60}")
        
        agent1 = self.agents[agent1_name]
        agent2 = self.agents[agent2_name]
        
        matchup_stats = {
            'wins': {agent1_name: 0, agent2_name: 0},
            'draws': 0,
            'total_moves': [],
            'decision_times': {agent1_name: [], agent2_name: []}
        }
        
        for game in range(self.num_games_per_matchup):
            # Use different seeds for each game
            seed = 42 + game * 100
            
            winner, moves, decision_times = self.play_game(
                agent1_name, agent2_name, agent1, agent2, seed
            )
            
            # Update stats
            if winner == agent1_name:
                matchup_stats['wins'][agent1_name] += 1
            elif winner == agent2_name:
                matchup_stats['wins'][agent2_name] += 1
            else:
                matchup_stats['draws'] += 1
            
            matchup_stats['total_moves'].append(moves)
            matchup_stats['decision_times'][agent1_name].append(decision_times[agent1_name])
            matchup_stats['decision_times'][agent2_name].append(decision_times[agent2_name])
            
            # Record in global stats
            self.stats.record_game(agent1_name, agent2_name, winner, moves, decision_times)
            
            # Progress indicator
            if (game + 1) % max(1, self.num_games_per_matchup // 10) == 0:
                print(f"  Game {game + 1}/{self.num_games_per_matchup} completed")
        
        # Calculate percentages
        total_games = self.num_games_per_matchup
        matchup_stats['win_rates'] = {
            agent1_name: matchup_stats['wins'][agent1_name] / total_games,
            agent2_name: matchup_stats['wins'][agent2_name] / total_games
        }
        matchup_stats['draw_rate'] = matchup_stats['draws'] / total_games
        matchup_stats['avg_moves'] = np.mean(matchup_stats['total_moves'])
        matchup_stats['avg_decision_times'] = {
            agent1_name: np.mean(matchup_stats['decision_times'][agent1_name]),
            agent2_name: np.mean(matchup_stats['decision_times'][agent2_name])
        }
        
        # Print matchup summary
        print(f"\nMatchup Summary:")
        print(f"  {agent1_name}: {matchup_stats['wins'][agent1_name]} wins ({matchup_stats['win_rates'][agent1_name]:.1%})")
        print(f"  {agent2_name}: {matchup_stats['wins'][agent2_name]} wins ({matchup_stats['win_rates'][agent2_name]:.1%})")
        print(f"  Draws: {matchup_stats['draws']} ({matchup_stats['draw_rate']:.1%})")
        print(f"  Average moves per game: {matchup_stats['avg_moves']:.1f}")
        print(f"  Average decision times:")
        print(f"    {agent1_name}: {matchup_stats['avg_decision_times'][agent1_name]*1000:.2f} ms")
        print(f"    {agent2_name}: {matchup_stats['avg_decision_times'][agent2_name]*1000:.2f} ms")
        
        return matchup_stats
    
    def run_round_robin(self):
        """Run a round-robin tournament between all agents"""
        print("\n" + "="*70)
        print("CONNECT FOUR ROUND-ROBIN TOURNAMENT")
        print("="*70)
        
        agent_names = list(self.agents.keys())
        num_agents = len(agent_names)
        
        print(f"Participants ({num_agents} agents):")
        for i, name in enumerate(agent_names, 1):
            print(f"  {i}. {name}")
        
        matchup_results = {}
        
        # Play each pair (including self-play for some agents)
        for i in range(num_agents):
            for j in range(i, num_agents):  # Include self-play for testing
                agent1 = agent_names[i]
                agent2 = agent_names[j]
                
                # Skip self-play for different agent types
                if i == j:
                    # Only do self-play for learning agents
                    if "Random" not in agent1:  # Skip random agent self-play
                        matchup_key = f"{agent1}_vs_{agent1}"
                        matchup_results[matchup_key] = self.run_matchup(agent1, agent2)
                else:
                    matchup_key = f"{agent1}_vs_{agent2}"
                    matchup_results[matchup_key] = self.run_matchup(agent1, agent2)
        
        return matchup_results
    
    def generate_rankings(self) -> pd.DataFrame:
        """Generate rankings based on tournament results"""
        summary = self.stats.get_summary()
        
        rankings_data = []
        for agent_name, agent_stats in summary['agents'].items():
            rankings_data.append({
                'Agent': agent_name,
                'Wins': agent_stats['wins'],
                'Losses': agent_stats['losses'],
                'Draws': agent_stats['draws'],
                'Win Rate': agent_stats['win_rate'],
                'Draw Rate': agent_stats['draw_rate'],
                'Avg Moves': agent_stats['avg_moves'],
                'Avg Decision Time (ms)': agent_stats['avg_decision_time_ms'],
                'Max Win Streak': agent_stats['max_win_streak']
            })
        
        df = pd.DataFrame(rankings_data)
        
        # Sort by win rate (descending)
        df = df.sort_values('Win Rate', ascending=False).reset_index(drop=True)
        df['Rank'] = df.index + 1
        
        return df
    
    def visualize_results(self, rankings_df: pd.DataFrame):
        """Create visualizations of tournament results"""
        # Set style
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
        
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Connect Four Tournament Analysis', fontsize=16, fontweight='bold')
        
        # 1. Win Rates (Bar Plot)
        ax1 = axes[0, 0]
        bars = ax1.bar(rankings_df['Agent'], rankings_df['Win Rate'] * 100)
        ax1.set_title('Win Rates by Agent', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Win Rate (%)', fontsize=10)
        ax1.set_xlabel('Agent', fontsize=10)
        ax1.tick_params(axis='x', rotation=45)
        
        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                    f'{height:.1f}%', ha='center', va='bottom', fontsize=9)
        
        # 2. Performance Heatmap
        ax2 = axes[0, 1]
        agents = rankings_df['Agent'].tolist()
        win_matrix = np.zeros((len(agents), len(agents)))
        
        # Create win matrix (simplified - would need actual matchup data)
        for i, agent1 in enumerate(agents):
            for j, agent2 in enumerate(agents):
                if i == j:
                    win_matrix[i, j] = 0.5  # Self-play
                else:
                    # Simplified: use win rate difference
                    win_matrix[i, j] = rankings_df.loc[rankings_df['Agent'] == agent1, 'Win Rate'].values[0]
        
        im = ax2.imshow(win_matrix, cmap='RdYlGn', vmin=0, vmax=1)
        ax2.set_title('Performance Matrix', fontsize=12, fontweight='bold')
        ax2.set_xticks(range(len(agents)))
        ax2.set_yticks(range(len(agents)))
        ax2.set_xticklabels(agents, rotation=45)
        ax2.set_yticklabels(agents)
        plt.colorbar(im, ax=ax2, label='Expected Win Rate')
        
        # 3. Decision Time vs Win Rate (Scatter Plot)
        ax3 = axes[1, 0]
        scatter = ax3.scatter(rankings_df['Avg Decision Time (ms)'], 
                             rankings_df['Win Rate'] * 100,
                             s=rankings_df['Avg Moves'] * 10,  # Size by avg moves
                             alpha=0.7)
        ax3.set_title('Decision Time vs Win Rate', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Average Decision Time (ms)', fontsize=10)
        ax3.set_ylabel('Win Rate (%)', fontsize=10)
        
        # Add agent labels
        for i, row in rankings_df.iterrows():
            ax3.annotate(row['Agent'], 
                        (row['Avg Decision Time (ms)'], row['Win Rate'] * 100),
                        textcoords="offset points", xytext=(0, 5),
                        ha='center', fontsize=8)
        
        # 4. Game Length Distribution
        ax4 = axes[1, 1]
        all_moves = []
        for agent_moves in self.stats.total_moves.values():
            all_moves.extend(agent_moves)
        
        ax4.hist(all_moves, bins=20, edgecolor='black', alpha=0.7)
        ax4.set_title('Distribution of Game Lengths', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Number of Moves', fontsize=10)
        ax4.set_ylabel('Frequency', fontsize=10)
        ax4.axvline(np.mean(all_moves), color='red', linestyle='--', 
                   label=f'Mean: {np.mean(all_moves):.1f}')
        ax4.legend()
        
        # Adjust layout
        plt.tight_layout()
        
        # Save figure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(self.results_dir, f"tournament_results_{timestamp}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nVisualization saved to {filename}")
        
        plt.show()
    
    def save_detailed_report(self, rankings_df: pd.DataFrame):
        """Save detailed tournament report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save rankings to CSV
        csv_file = os.path.join(self.results_dir, f"rankings_{timestamp}.csv")
        rankings_df.to_csv(csv_file, index=False)
        print(f"Rankings saved to {csv_file}")
        
        # Save detailed statistics
        stats_file = os.path.join(self.results_dir, f"detailed_stats_{timestamp}.json")
        self.stats.save_to_file(stats_file)
        
        # Generate text report
        report_file = os.path.join(self.results_dir, f"tournament_report_{timestamp}.txt")
        with open(report_file, 'w') as f:
            f.write("="*70 + "\n")
            f.write("CONNECT FOUR TOURNAMENT REPORT\n")
            f.write("="*70 + "\n\n")
            
            f.write(f"Tournament Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total Games Played: {self.stats.games_played}\n")
            f.write(f"Number of Agents: {len(self.agents)}\n\n")
            
            f.write("FINAL RANKINGS:\n")
            f.write("-"*70 + "\n")
            
            for _, row in rankings_df.iterrows():
                f.write(f"\nRank {row['Rank']}: {row['Agent']}\n")
                f.write(f"  Win Rate: {row['Win Rate']:.1%} ({row['Wins']}W/{row['Losses']}L/{row['Draws']}D)\n")
                f.write(f"  Avg Moves: {row['Avg Moves']:.1f}\n")
                f.write(f"  Avg Decision Time: {row['Avg Decision Time (ms)']:.2f} ms\n")
                f.write(f"  Max Win Streak: {row['Max Win Streak']}\n")
            
            f.write("\n" + "="*70 + "\n")
            f.write("PERFORMANCE ANALYSIS\n")
            f.write("="*70 + "\n\n")
            
            # Best performer
            best = rankings_df.iloc[0]
            f.write(f"🏆 BEST PERFORMER: {best['Agent']}\n")
            f.write(f"   Win Rate: {best['Win Rate']:.1%}\n")
            f.write(f"   Key Strength: ", end="")
            
            if best['Avg Decision Time (ms)'] < 10:
                f.write("Fast decision making\n")
            elif best['Win Rate'] > 0.8:
                f.write("High strategic capability\n")
            else:
                f.write("Balanced performance\n")
            
            # Most efficient
            fastest = rankings_df.loc[rankings_df['Avg Decision Time (ms)'].idxmin()]
            f.write(f"\n⚡ FASTEST AGENT: {fastest['Agent']}\n")
            f.write(f"   Avg Decision Time: {fastest['Avg Decision Time (ms)']:.2f} ms\n")
            
            # Most draws
            most_draws = rankings_df.loc[rankings_df['Draws'].idxmax()]
            f.write(f"\n🤝 MOST DRAWS: {most_draws['Agent']}\n")
            f.write(f"   Draws: {most_draws['Draws']} ({most_draws['Draw Rate']:.1%})\n")
        
        print(f"Detailed report saved to {report_file}")
    
    def run_complete_tournament(self):
        """Run complete tournament with all features"""
        print("\n" + "="*70)
        print("STARTING COMPLETE TOURNAMENT")
        print("="*70)
        
        start_time = time.time()
        
        # Run round-robin
        matchup_results = self.run_round_robin()
        
        # Generate rankings
        rankings_df = self.generate_rankings()
        
        # Display rankings
        print("\n" + "="*70)
        print("FINAL RANKINGS")
        print("="*70)
        print(rankings_df.to_string(index=False))
        
        # Create visualizations
        try:
            self.visualize_results(rankings_df)
        except Exception as e:
            print(f"\n⚠️  Visualization failed: {e}")
            print("Continuing without visualizations...")
        
        # Save reports
        self.save_detailed_report(rankings_df)
        
        # Calculate tournament duration
        duration = time.time() - start_time
        print(f"\n⏱️  Tournament completed in {duration:.1f} seconds")
        print(f"   Average time per game: {duration/self.stats.games_played:.2f} seconds")
        
        return rankings_df


def create_standard_tournament(num_games: int = 20):
    """Create a standard tournament with all available agents"""
    # Create environment for agents
    env = connect_four_v3.env()
    
    # Define agents
    agents = {
        "RandomAgent": RandomAgent(env),
        "WeightedRandomAgent": WeightedRandomAgent(env),
        "SmartAgent": SmartAgent(env),
        "SmartAgentAmeliore": SmartAgentAmeliore(env),
    }
    
    # Create and run tournament
    tournament = Tournament(agents, num_games_per_matchup=num_games)
    rankings = tournament.run_complete_tournament()
    
    return rankings


def run_quick_test():
    """Run a quick test tournament"""
    print("Running quick test tournament...")
    
    env = connect_four_v3.env()
    
    # Use fewer agents and games for quick test
    agents = {
        "RandomAgent": RandomAgent(env),
        "SmartAgent": SmartAgent(env),
    }
    
    tournament = Tournament(agents, num_games_per_matchup=5)
    rankings = tournament.run_complete_tournament()
    
    return rankings


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Connect Four Tournament System")
    parser.add_argument("--mode", choices=["quick", "standard", "full"], 
                       default="standard", help="Tournament mode")
    parser.add_argument("--games", type=int, default=20,
                       help="Number of games per matchup")
    parser.add_argument("--agents", nargs="+", 
                       default=["RandomAgent", "SmartAgent", "SmartAgentAmeliore"],
                       help="List of agents to include")
    
    args = parser.parse_args()
    
    if args.mode == "quick":
        rankings = run_quick_test()
    else:
        rankings = create_standard_tournament(num_games=args.games)
    
    # Exit with success code
    exit(0)
[file content end]