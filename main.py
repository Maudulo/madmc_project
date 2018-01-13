import matplotlib.pyplot as plt
import numpy as np

from test_pareto_func import *
from MADMC_project import *

np.set_printoptions(formatter={'float': '{: 0.2f}'.format})

def printAllArray(arr):
	print("\nTableau de programmation dynamique :\n")
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


def test_pareto_functions(n = 10, m = 50):
	vector_generated = gaussian_vector_generator(n, m)
	proper_vector = build_vector(vector_generated)
	print("valeurs générées : ", vector_generated)

	start = time.time()
	l = naive_pareto_dominants(vector_generated)
	end = time.time() - start
	print("pareto_dominants version naive 1 : temps d'éxcution - ",end, " solution: ", l)

	start = time.time()
	l = naive_pareto_dominants_2(vector_generated)
	end = time.time() - start
	print("pareto_dominants version naive 2 : temps d'éxcution - ",end, " solution: ", l)

	start = time.time()
	l2 = pareto_dominants(proper_vector)
	end = time.time() - start
	print("pareto_dominants fonction 2 avec elements : temps d'éxcution - ",end, " solution: ", [x.elements for x in l2])


def compare_and_plot_pareto_functions(nmin = 20, nmax = 500, step = 25, n = 50):
	plot_pareto_compare_functions(naive_pareto_dominants, pareto_dominants, nmin = nmin, nmax = nmax, step = step, n = n, proper2 = True)


def compute_and_display_solution_of_dynamic_programming(n=5,m=10, k=3, I_dominance = False, display_dynamic_array = False):
	l = gaussian_vector_generator(n, m)
	print("\nwith I_dominance = ",I_dominance,"\nliste : \n", l)

	dp = dynamic_programming(l, k, I_dominance = I_dominance)

	if display_dynamic_array:
		printAllArray(dynamic_programming(l, k, I_dominance = True, display_all_array = True))

	print("\nil y a ", len(dp), " solutions")

	for i,x in enumerate(dp):
		print("\nsolution : ", i+1)
		print("solution pareto optimale de taille ", k," avec pour somme totale ", x.sum)
		print("solution composée de :\n", x.elements)

	minmax = minimax_value(dp)
	print("\nminimax de la solution : ", minmax.sum, " composé de : " , minmax.elements)



def tests(n = 50):
	t1,t2 = 0,[0 for _ in range(20)]
	for i in range(n):
		print("test :",i)
		l = gaussian_vector_generator(50, 1000)
		k = 10
		start = time.time()
		dp1 = dynamic_programming(l, k, I_dominance = False)
		t1 += time.time() - start

		for i,a in enumerate(np.arange(0.025,0.525,0.025)):
			start = time.time()
			dp2 = dynamic_programming(l, k, I_dominance = True, alpha_min=0.5-a, alpha_max= 0.5+a)
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


# test_pareto_functions(n=10,m=50)
# compare_and_plot_pareto_functions(nmin = 20, nmax = 500, step = 25, n = 50)
# test_all_pareto_functions([naive_pareto_dominants, pareto_dominants], proper = [False,True])
# compute_and_display_solution_of_dynamic_programming(n=5,m=10,k=3,I_dominance=False,display_dynamic_array=True)
# display_result_tests(tests(50))