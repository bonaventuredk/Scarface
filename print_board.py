from pettingzoo.classic import connect_four_v3
import numpy as np

def print_board(observation):
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
        
# Test de la fonction
env = connect_four_v3.env()
env.reset(seed=42)

for agent in env.agent_iter():
    observation, reward, termination, truncation, info = env.last()

    if termination or truncation:
        break

    print(f"\nAgent: {agent}")
    print_board(observation['observation'])

    # Exemple de coup pour voir le plateau évoluer
    env.step(3)
    if agent == env.agents[0]:
        break
print("Affichage après quelques coups")
env.reset(seed=42)

# Jouons quelques coups avant d'afficher
env.step(5)  # premier coup
env.step(2)  # deuxième coup
env.step(3)  # troisième coup
env.step(1)  # quatrième coup
env.step(1)  # cinquième coup

# Récupérer l'état actuel
observation, reward, termination, truncation, info = env.last()
print_board(observation['observation'])
env.close()

