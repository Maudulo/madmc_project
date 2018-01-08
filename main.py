from test_pareto_func import *
from MADMC_project import *
import numpy as np
import matplotlib.pyplot as plt


def printAllArray(arr):
	for line in arr:
		for k in line:
			print("[", end="")
			if k != None:
				for i,x in enumerate(k):
					print(":", x.sum,":",end="")
			else:
				print("None", end="")
			print("], ",end="")
		print()

np.set_printoptions(formatter={'float': '{: 0.2f}'.format})
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

# l = gaussian_vector_generator(5, 10)
# k = 3
# print("\nliste : \n", l)

# dp1 = dynamic_programming_2(l, k, I_dominance = False)
# # print("nombre d'éléments dans chaque case du tableau de prog dyn ",[[len(x) if x else 0 for x in y] for y in dp1])
# print("\nil y a ", len(dp1), " solutions")

# for i,x in enumerate(dp1):
# 	print("\nsolution : ", i)
# 	print("p opt de taille ", k," ", x.sum)
# 	print("somme composée de ", x.elements)

# printAllArray(dynamic_programming_2(l, k, I_dominance = True, display_all_array = True))
# dp2 = dynamic_programming_2(l, k, I_dominance = True)
# #print("nombre d'éléments dans chaque case du tableau de prog dyn ",[[len(x) if x else 0 for x in y] for y in dp2])
# print("\nil y a ", len(dp2), " solutions")
# for i,x in enumerate(dp2):
# 	print("\nsolution : ", i)
# 	print("p opt de taille ", k," ", x.sum)
# 	print("somme composée de ", x.elements)


# # minmax = minimax_value_2(dp1)
# # print("minimax avec pareto : ", minmax.sum, " composé de : " , minmax.elements)
# minmax = minimax_value_2(dp2)
# print("minimax avec I dominance : ", minmax.sum, " composé de : " , minmax.elements)



#TODO : MINMAX parmi les solutions opt


# alpha_min = 0.1
# alpha_max = 0.2
# print("meilleur minimax avec alpha_min = ", alpha_min, " alpha_max = ", alpha_max, "\n", minimax_dynamic_programming(l, k, alpha_min = 0, alpha_max = 1))

# test_all_pareto_functions([naive_pareto_dominants, pareto_dominants])
# 
def tests(n = 50):
	t1,t2 = 0,[0 for _ in range(20)]
	for i in range(n):
		print("test :",i)
		l = gaussian_vector_generator(50, 1000)
		k = 10
		start = time.time()
		dp1 = dynamic_programming_2(l, k, I_dominance = False)
		t1 += time.time() - start

		for i,a in enumerate(np.arange(0.025,0.525,0.025)):
			start = time.time()
			dp2 = dynamic_programming_2(l, k, I_dominance = True, alpha_min=0.5-a, alpha_max= 0.5+a)
			t2[i] += time.time() - start

	return t1/n,np.array(t2)/n


def display_result_tests(results):
	t1,t2 = results
	x = np.arange(0.025,0.525,0.025)
	t1 = [t1 for _ in range(len(t2))]
	plt.figure(1)
	plt.plot(x,t1)
	plt.plot(x,t2)
	plt.show()
	print(t1)
	print(t2)

display_result_tests(tests(50))