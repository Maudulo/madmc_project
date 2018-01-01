from test_pareto_func import *
from MADMC_project import *



# vector_generated = gaussian_vector_generator(10, 50)

# print("valeurs générées : ", vector_generated)
# l = naive_pareto_dominants(vector_generated)
# print("p-dominants fonction 1 : ", l)
# l2 = pareto_dominants(vector_generated)
# print("p-dominants fonction 2 : ", l2)


# plot_pareto_compare_functions(naive_pareto_dominants, pareto_dominants, nmin = 20, nmax = 500, step = 25, n = 50)

l = gaussian_vector_generator(3, 10)
k = 2
print("\nliste : \n", l)
dp = dynamic_programming(l, k)
print("\n\np opt de taille ", k, "\n ", dp[0])
print("somme composée de ", dp[1])

alpha_min = 0.1
alpha_max = 0.2
print("meilleur minimax avec alpha_min = ", alpha_min, " alpha_max = ", alpha_max, "\n", minimax_dynamic_programming(l, k, alpha_min = 0, alpha_max = 1))