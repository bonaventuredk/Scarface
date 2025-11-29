"""
Test d'intégration: SmartAgent vs RandomAgent
"""

import numpy as np
import random
from pettingzoo.classic import connect_four_v3
from smart_agent import SmartAgent


def run_comprehensive_integration_test(num_games=100):
    """
    Test d'intégration complet entre SmartAgent et RandomAgent
    """
    print("="*60)
    print("COMPREHENSIVE INTEGRATION TEST")
    print(f"SmartAgent vs RandomAgent - {num_games} games")
    print("="*60)
    
    env = connect_four_v3.env(render_mode=None)
    
    # Créer les agents
    smart_agent = SmartAgent(env, "SmartAgent")
    
    # Statistiques détaillées
    stats = {
        'smart_wins_as_first': 0,
        'smart_wins_as_second': 0,
        'random_wins_as_first': 0,
        'random_wins_as_second': 0,
        'draws': 0,
        'total_moves': 0,
        'games_completed': 0
    }
    
    for game in range(num_games):
        if game % 10 == 0:
            print(f"Playing game {game+1}/{num_games}...")
        
        env.reset()
        moves = 0
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            moves += 1
            
            if termination or truncation:
                # Fin de la partie
                stats['games_completed'] += 1
                stats['total_moves'] += moves
                
                if reward > 0:
                    # Victoire du joueur 0 (commence toujours)
                    if game % 2 == 0:  # SmartAgent est player_0
                        stats['smart_wins_as_first'] += 1
                    else:  # RandomAgent est player_0
                        stats['random_wins_as_first'] += 1
                elif reward < 0:
                    # Victoire du joueur 1
                    if game % 2 == 0:  # RandomAgent est player_1
                        stats['random_wins_as_second'] += 1
                    else:  # SmartAgent est player_1
                        stats['smart_wins_as_second'] += 1
                else:
                    stats['draws'] += 1
                break
            
            if (game % 2 == 0 and agent == "player_0") or (game % 2 == 1 and agent == "player_1"):
                # SmartAgent's turn
                action_mask = observation["action_mask"]
                action = smart_agent.choose_action(
                    observation["observation"], 
                    action_mask=action_mask
                )
            else:
                # RandomAgent's turn
                action_mask = observation["action_mask"]
                valid_actions = np.where(action_mask == 1)[0]
                action = random.choice(valid_actions)
            
            env.step(action)
    
    # Calcul des résultats finaux
    total_smart_wins = stats['smart_wins_as_first'] + stats['smart_wins_as_second']
    total_random_wins = stats['random_wins_as_first'] + stats['random_wins_as_second']
    total_games = stats['games_completed']
    
    smart_win_rate = total_smart_wins / total_games
    random_win_rate = total_random_wins / total_games
    draw_rate = stats['draws'] / total_games
    avg_moves = stats['total_moves'] / total_games
    
    # Affichage des résultats détaillés
    print("\n" + "="*60)
    print("FINAL RESULTS")
    print("="*60)
    print(f"Total games: {total_games}")
    print(f"SmartAgent wins: {total_smart_wins} ({smart_win_rate:.1%})")
    print(f"  - As first player: {stats['smart_wins_as_first']}")
    print(f"  - As second player: {stats['smart_wins_as_second']}")
    print(f"RandomAgent wins: {total_random_wins} ({random_win_rate:.1%})")
    print(f"  - As first player: {stats['random_wins_as_first']}")
    print(f"  - As second player: {stats['random_wins_as_second']}")
    print(f"Draws: {stats['draws']} ({draw_rate:.1%})")
    print(f"Average moves per game: {avg_moves:.1f}")
    
    # Évaluation de la performance
    print("\n" + "="*60)
    print("PERFORMANCE EVALUATION")
    print("="*60)
    
    if smart_win_rate > random_win_rate:
        advantage = smart_win_rate - random_win_rate
        print(f"✅ SUCCESS: SmartAgent outperforms RandomAgent by {advantage:.1%}")
        
        if smart_win_rate > 0.6:
            print("🎉 EXCELLENT: SmartAgent has strong winning rate (>60%)")
        elif smart_win_rate > 0.55:
            print("👍 GOOD: SmartAgent has decent winning rate (>55%)")
        else:
            print("⚠️  ACCEPTABLE: SmartAgent wins but could be improved")
    else:
        print("❌ FAIL: RandomAgent performs equally or better")
    
    return smart_win_rate > random_win_rate


if __name__ == "__main__":
    # Exécuter le test d'intégration complet
    success = run_comprehensive_integration_test(num_games=100)
    
    if success:
        print("\n🎊 INTEGRATION TEST PASSED! Your SmartAgent is competitive.")
    else:
        print("\n💡 Consider improving your SmartAgent's strategy.")