from test_pareto_func import *
from MADMC_project import *



# vector_generated = gaussian_vector_generator(10, 50)

# print("valeurs générées : ", vector_generated)
# # l = naive_pareto_dominants(vector_generated)
# # print("p-dominants fonction 1 : ", l)
# # l = naive_pareto_dominants_2(vector_generated)
# # print("p-dominants fonction 1.2 : ", l)
# l2 = pareto_dominants(vector_generated)
# print("p-dominants fonction 2 : ", l2)
# elements = [Element(x,[x]) for x in vector_generated]
# l2 = pareto_dominants_2(elements)
# print("p-dominants fonction 2 avec elements : ", [x.elements for x in l2])


# plot_pareto_compare_functions(naive_pareto_dominants, pareto_dominants, nmin = 20, nmax = 500, step = 25, n = 50)

l = gaussian_vector_generator(10, 10)
k = 5
print("\nliste : \n", l)

dp = dynamic_programming_2(l, k, I_dominance = False)
# print("nombre d'éléments dans chaque case du tableau de prog dyn ",[[len(x) if x else 0 for x in y] for y in dp])
print("\nil y a ", len(dp), " solutions")
i = 0
for x in dp:
	i+=1
	print("\nsolution : ", i)
	print("p opt de taille ", k," ", x.sum)
	print("somme composée de ", x.elements)

dp = dynamic_programming_2(l, k, I_dominance = True)
# print("nombre d'éléments dans chaque case du tableau de prog dyn ",[[len(x) if x else 0 for x in y] for y in dp])
print("\nil y a ", len(dp), " solutions")
i = 0
for x in dp:
	i+=1
	print("\nsolution : ", i)
	print("p opt de taille ", k," ", x.sum)
	print("somme composée de ", x.elements)



#TODO : MINMAX parmi les solutions opt


# alpha_min = 0.1
# alpha_max = 0.2
# print("meilleur minimax avec alpha_min = ", alpha_min, " alpha_max = ", alpha_max, "\n", minimax_dynamic_programming(l, k, alpha_min = 0, alpha_max = 1))

# test_all_pareto_functions([naive_pareto_dominants, pareto_dominants])