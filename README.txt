Toutes ces fonctions sont présentes dans le fichier main.py
Décommentez la ligne que vous voulez lancer puis dans un terminal:
$ python main.py

#########################################################################################################
# créer n vecteurs avec tirage gaussien d'espérance m puis récupère les pareto non dominés selon 3 fonctions
# deux naives et une optimisée en commencant par un tri
#########################################################################################################
test_pareto_functions


#########################################################################################################
# compare la vitesse d'exécution des différentes fonctions trouvant les pareto non dominés (naive 1 et celle avec le tri)
#########################################################################################################
compare_and_plot_pareto_functions
 

#########################################################################################################
# compare la vitesse d'exécution des différentes fonctions trouvant les pareto non dominés (les fonctions sont données dans la fonction)
#########################################################################################################
test_all_pareto_functions


#########################################################################################################
# calcule et affiche les solutions de la programmation dynamique pour n vecteurs de génération gaussienne
# d'espérance m pour trouver les ensembles pareto non dominés de taille k (1<k<=n)
# soit par pareto soit par l'I_dominance (I_dominance = True)
# on peut aussi afficher la tableau complet de programmation dynamique (display_dynamic_array = True)
#########################################################################################################
compute_and_display_solution_of_dynamic_programming


#########################################################################################################
# compare le temps d'exécution pour trouver les pareto non dominés avec la technique Pareto ou I_dominance
# avec tests le nombre de tests, n le nombre de vecteurs par tests, m l'espérance de génération gaussienne par vecteur
# et k le cardinal de l'ensemble de pareto non dominés à trouver
#########################################################################################################
display_result_tests