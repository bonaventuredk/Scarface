# Plan de test – Agents de jeu (Puissance 4)

## 1. Objectifs du plan de test

L’objectif de ce plan de test est de vérifier que les agents implémentés :
- respectent strictement les règles du jeu,
- prennent uniquement des décisions valides,
- présentent de bonnes performances en temps et en mémoire,
- adoptent une stratégie cohérente et efficace face à différents adversaires,
- restent robustes face à des situations limites.

---

## 2. Portée des tests

Les tests concernent :
- la sélection des coups,
- la gestion des fins de partie,
- la performance algorithmique,
- la qualité stratégique,
- la robustesse sur des états spécifiques du plateau.

Les agents testés incluent :
- RandomAgent
- SmartAgent
- SmartAgentAmeliore
- MinimaxAgent
---

## 3. Stratégie de test

### 3.1 Tests fonctionnels – Que tester ?

Objectif : vérifier que l’agent fonctionne correctement selon les règles du jeu.

#### Catégories de tests :
- Sélection d’un coup valide
- Respect du masque d’action (colonnes non pleines)
- Gestion correcte de la fin de partie (victoire, défaite, match nul)
- Absence d’erreurs ou d’exceptions durant le jeu
- Stabilité sur des parties complètes

---

### 3.2 Tests de performance

Objectif : mesurer l’efficacité computationnelle des agents.

#### Indicateurs mesurés :
- Temps moyen de calcul par coup
- Temps total par partie
- Utilisation maximale de la mémoire
- Scalabilité du temps de calcul avec profondeur de recherche

---

### 3.3 Tests stratégiques

Objectif : vérifier la qualité du jeu produit par l’agent.

#### Éléments évalués :
- Capacité à gagner contre RandomAgent
- Capacité à bloquer des menaces évidentes
- Capacité à détecter une victoire immédiate
- Performance dans un tournoi multi-agents
- Stabilité du taux de victoire sur plusieurs parties

---

## 4. Méthodes de test – Comment tester ?

### 4.1 Tests fonctionnels

- Création d’états de plateau prédéfinis
- Vérification systématique que l’action renvoyée est légale
- Utilisation de tests unitaires`
- Vérification de la terminaison correcte du jeu

---

### 4.2 Tests stratégiques

- Lancer N parties (ex : N = 100 ou 50)
- Alterner le joueur qui commence
- Calculer les taux de victoire, défaite et match nul
- Comparer les agents entre eux dans un tournoi round-robin

---

### 4.3 Tests de performance

- Mesurer le temps avec `time.time()`
- Mesurer l’usage mémoire avec `tracemalloc`
- Calculer des moyennes et des maximums
- Comparer les performances entre agents

---

## 5. Critères de succès

Un agent est considéré comme valide s’il respecte les critères suivants :

### Fonctionnel
- 100% des coups joués sont légaux
- 0 exception non gérée sur ≥ 500 parties
- Détection correcte des fins de partie

### Stratégique
- > 80% de victoires contre RandomAgent
- >= 60% de victoires contre SmartAgent
- Taux de match nul cohérent sur adversaires forts
- Blocage correct des menaces immédiates

### Performance
- Temps moyen par coup < 0.1 seconde
- Temps maximal par coup < 0.5 seconde
- Utilisation mémoire < 10 MB

---

## 6. Conception de cas de test spécifiques

### Scénario 1 : Victoire immédiate détectée

État du plateau :

. . . . . . . 
. . . . . . . 
. . . . . . . 
. . . . . . . 
. . . . . . . 
X X X . . . . 

Attendu : L’agent joue la colonne 3 et gagne immédiatement.

---

### Scénario 2 : Blocage d’une victoire adverse

État du plateau :

. . . . . . . 
. . . . . . . 
. . . . . . . 
. . . . . . . 
. . . . . . . 
O O O . . . . 

Attendu : L’agent joue la colonne 3 pour bloquer la victoire.

---

### Scénario 3 : Colonne pleine

État du plateau :

. . . X . . . 
. . . X . . . 
. . . X . . . 
. . . X . . . 
. . . X . . . 
O O O X X . .

Attendu : 
- La colonne 3 est interdite
- L’agent choisit une autre colonne valide

---

### Scénario 4 : Double menace adverse

État du plateau :

. . . . . . . 
. . . . . . . 
. . . . . . . 
. X O X . . . 
X O X O . . . 
O X O X O . . 

Attendu : 
- L’agent choisit le coup minimisant les risques immédiats
- Priorité au blocage plutôt qu’à l’attaque (normalement l'agent doit jouer soit dans la colonne 3 ou 5). 

---

### Scénario 5 : Fin de partie – Match nul

État du plateau :

Plateau entièrement rempli sans alignement de 4

Attendu :
- L’agent reconnaît correctement un match nul
- Aucun coup supplémentaire n’est joué

