from test_pareto_func import *
from MADMC_project import *



# vector_generated = gaussian_vector_generator(10, 50)

# print("valeurs générées : ", vector_generated)
# l = naive_pareto_dominants(vector_generated)
# print("p-dominants fonction 1 : ", l)
# l2 = pareto_dominants(vector_generated)
# print("p-dominants fonction 2 : ", l2)


# plot_pareto_compare_functions(naive_pareto_dominants, pareto_dominants, nmin = 20, nmax = 500, step = 25, n = 50)

l = gaussian_vector_generator(5, 10)
k = 2
print("liste : ", l)
print("p opt de taille k = ", k, " ", dynamic_programming(l, k))