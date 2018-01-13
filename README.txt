Toutes ces fonctions sont pr�sentes dans le fichier main.py
D�commentez la ligne que vous voulez lancer puis dans un terminal:
$ python main.py

#########################################################################################################
# cr�er n vecteurs avec tirage gaussien d'esp�rance m puis r�cup�re les pareto non domin�s selon 3 fonctions
# deux naives et une optimis�e en commencant par un tri
#########################################################################################################
test_pareto_functions


#########################################################################################################
# compare la vitesse d'ex�cution des diff�rentes fonctions trouvant les pareto non domin�s (naive 1 et celle avec le tri)
#########################################################################################################
compare_and_plot_pareto_functions
 

#########################################################################################################
# compare la vitesse d'ex�cution des diff�rentes fonctions trouvant les pareto non domin�s (les fonctions sont donn�es dans la fonction)
#########################################################################################################
test_all_pareto_functions


#########################################################################################################
# calcule et affiche les solutions de la programmation dynamique pour n vecteurs de g�n�ration gaussienne
# d'esp�rance m pour trouver les ensembles pareto non domin�s de taille k (1<k<=n)
# soit par pareto soit par l'I_dominance (I_dominance = True)
# on peut aussi afficher la tableau complet de programmation dynamique (display_dynamic_array = True)
#########################################################################################################
compute_and_display_solution_of_dynamic_programming


#########################################################################################################
# compare le temps d'ex�cution pour trouver les pareto non domin�s avec la technique Pareto ou I_dominance
# avec tests le nombre de tests, n le nombre de vecteurs par tests, m l'esp�rance de g�n�ration gaussienne par vecteur
# et k le cardinal de l'ensemble de pareto non domin�s � trouver
#########################################################################################################
display_result_tests