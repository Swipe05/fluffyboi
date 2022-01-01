# ENEMY USEFULL FUNCTION UwU


"""
Ce qui serai bien de faire apres l'ajout des fonctions spawn chez ennemi et chez allié: 
il faudrai affecter une team "allié" a chaque unité crée par la fonction de spawn_ally_unit et une team "ennemi" a chaque unité crée par spawn_enemy_unit

Ce qu'il faut faire pour l'IA en pseudo code et francais  :

Routine du BOT :

Construction premier batiment:
Conditions:

si il y a moins que un certain nombre de ce batiment
et que l'on a les ressource pour en construire
=> effectuer les constructions

Formation de villageois:
Conditions:

si il y en a moins qu'un certains nombre
et que l'on a les ressources disponibles
=> former des villageois

Objecitf principal du bot ,  passer à l'age suivant :

definir % de villageois a la Recherche de nourritures(Baies) et a la recolte de bois on va dire pour l'instant 60% sur la nourriture et 40% sur le bois
Condition: 2 batiments(a definir lequels) construit et au moins 500 de nourriture dans les stocks

Ainsi en code   Si (age_actuel==1ere age):
                    villageois sur la nourriture 60%
                    villageois sur le bois 40%
                    villageois sur la pierre  0%
                    villageois sur l'or 0%

Possibilité d'envoyer un soldat en exploration de maniere aleatoire


"""

