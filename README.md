# Flo_Bona
Projet python portant sur le jeu Puissance4.

#Partie 1:


##Tache 1.1 : Analyse des règles du jeu
1. Les dimensions d'un tableau de Puissance 4: 6 rangées sur la hauteur et 7 colonnes. Soit 42 emplacements.

2. Un joueur gagne la partie s'il arrive à aligner un 4 jetons consécutifs (au moins) suivant une ligne horizontale, verticale ou suivant les diagonales.

3. Si le plateau est complètement rempli sans gagnant, la partie se termine avec un MATCH NUL.

4. Non, un joueur ne peut pas placer un pion dans une colonne déjà pleine. Il doit choisir une colonne qui contient au moins une case vide.

5. Les résultats possibles. Soit le Joueur 1 gagne, soit le joueur 2 gagne, soit il y un Match Nul.


##Tache 1.2 : Analyse des conditions de victoire
1. Dessin des 4 motifs:
        ------------------------------------
        |  O |  O |  O |  O |    |    |  O |
        ------------------------------------
        |    |    |    |    |    |    |  O |
        ------------------------------------
        |    |    |    |  O |    |    |  O |
        ------------------------------------
        |    |    |  O |    |  O |    |  O |
        ------------------------------------
        |    |  O |    |    |    |  O |    |
        ------------------------------------
        |  O |    |    |    |    |    |  O |
        ------------------------------------

2. 4 directions au plus doivent être vérifiées pour une victoire. En particulier si la position donnée est au coin (du bas) , il n'y a plus que 3 directions à vérifier.

3. L'algorithme pour vérifier l'alignement de 4 points est :   f
