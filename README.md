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

3. L'algorithme pour vérifier l'alignement de 4 points est :
    Pseudo Code:
    # direction horizontale (vers la droite)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers la droite):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
        
    # direction horizontale (vers la gauche)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers la gauche):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
    # direction vertical (vers le haut)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers le haut ):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
    # direction verticale (vers le bas)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers le bas):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
        
    # direction oblique (montante)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers le haut):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
    # direction oblique (descendante)
        Entrées: Position initiale (row,col)
            On initialise compteur = 1;
            On parcourt la ligne (vers le bas):
                Tant que la case(courante) existe et contient un élément du joueur, 
                    compteur = compteur + 1
        Sorties: victoire, si compteur >=4  
        
##Partie 2
#Tache 2.1

1. Noms des deux agents: player_0 et player_1

2. La variable "action" représente la colonne où le joueur veut déposer son jeton.
   La variable "action" est de type: int.
   
3. env.agent_iter() : est un itérateur qui renvoi à chaque itération l'agent actif.
   env.step(action) : permet de jouer "action" sur l'agent actif, met à jour le jeu et passe au tour suivant.
   
4. env.last() renvoi un tuple avec les informations du tour actuel: observation, reward(récompense de l'agent), termination(booleen indiquant si la partie est terminée), truncation( booleen indiquant si la partie s'est arrêté pour une raison inconnue autre que celle définie), info(dictionnaires avec des infos supplémentaires).

5. obs['observation'] : une matrice 6x7 représentant le plateau (0 = vide, 1 = pion du joueur, 2 = pion adversaire)

obs['action_mask'] : un tableau de 7 booléens indiquant les colonnes où un jeton peut être joué (True = jouable, False = interdit)

6. "action mask" permet de savoir quelle actions sont légales à ce tour. C'est un tableau.

#Tache 2.2
1. Forme du tableau d'observation: 6 * 7 

2. Représentation des dimensions: (6: les lignes du plateau), (7: les colonnes du plateau)

3. Valeurs possibles dans le tableau d'observation: O pour case vide; 1 pion  du joueur actif; 2 pour pion de l'adversaire.

#Tache 2.3
Fait
#Tache 2.4
Fait

##Partie 3
#Tache 3.1



