import time
import numpy as np
import matplotlib.pyplot as plt
from MADMC_project import *

def test_pareto_functions(func, nmin = 200, nmax = 10000, step = 200, m = 1000, n = 50, proper = False):
	"""
	This function returns a list of the average time taken by the function func
	@params : func : the function to test
			  argmin : the minimum size of the list of values
			  argmax : the maximum size of the list of values
			  step : the number of value added to the list between 2 iterations
			  n : the number of tests during an iteration
	"""
	time_measure = []
	index_time_measure = 0

	for i in range(nmin, nmax, step):
		print(i, "/ ", nmax)
		time_measure.append(0)
		for j in range(n):

			l = gaussian_vector_generator(i, m)
			proper_l = build_vector(l)
			if proper:
				a = time.time()
				pareto_dominants = func(proper_l)
				time_measure[index_time_measure] += time.time() - a
			else:
				a = time.time()
				pareto_dominants = func(l)
				time_measure[index_time_measure] += time.time() - a

		time_measure[index_time_measure] /= n
		index_time_measure += 1

	print("-------------------------------------")
	return time_measure

def plot_pareto_functions(func, nmin = 200, nmax = 10000, step = 200, n = 50, m = 1000, proper = False):
	"""
	This function displays a graph representing the time depending of the number of value into a list
	@params : func : the function to test
			  nmin : the minimum size of the list of values
			  nmax : the maximum size of the list of values
			  step : the number of value added to the list between 2 iterations
			  n : the number of tests during an iteration
	"""
	x = np.arange(nmin, nmax, step);
	y = test_pareto_functions(func, nmin, nmax, step, n, m, proper = proper)
	plt.plot(x, y)

def plot_pareto_compare_functions(func1, func2, nmin = 200, nmax = 10000, step = 200, m = 1000, n = 50, proper1 = False, proper2 = False):
	plot_pareto_functions(func1, nmin = nmin, nmax = nmax, step = step, m = m, n = n, proper = proper1)
	plot_pareto_functions(func2, nmin = nmin, nmax = nmax, step = step, m = m, n = n, proper = proper2)
	plt.show()
	
def test_all_pareto_functions(func_list, nmin = 200, nmax = 10000, step = 200, m = 1000, n = 100, proper = None):
	"""
	This function displays a graph representing the time depending of the number of value into a list
	@params : func_list : a list of functions to test
			  argmin : the minimum size of the list of values
			  argmax : the maximum size of the list of values
			  step : the number of value added to the list between 2 iterations
			  m : the expectation of the gaussian
			  n : the number of tests during an iteration
	"""
	assert(((nmax-nmin)/step).is_integer())
	func_nb = len(func_list)
	time_measure = np.zeros((func_nb, int((nmax-nmin)/step)), dtype= 'f')
	index_time_measure = 0

	if proper == None:
		proper = [False for _ in range(len(func_list))]

	for i in range(nmin, nmax, step):
		print(i, "/ ", nmax)
		for j in range(n):

			l = gaussian_vector_generator(i, m)

			for f in range(func_nb):
				if proper[f] == True:
					l = build_vector(l)
					a = time.time()
					pareto_dominants = func_list[f](l)
					time_measure[f,index_time_measure] += time.time() - a
				else:
					a = time.time()
					pareto_dominants = func_list[f](l)
					time_measure[f,index_time_measure] += time.time() - a

		time_measure[f] /= n
		index_time_measure += 1
	print("-------------------------------------")
	
	fig, ax = plt.subplots()
	for f in range(func_nb):
		x = np.arange(nmin, nmax, step);
		y = time_measure[f]
		ax.plot(x, y, label=func_list[f].__name__)
	ax.set_ylabel("Temps (ms)")
	ax.set_xlabel("Nombre de vecteurs")
	ax.margins(y=.1, x=.1)
	legend = ax.legend(loc='upper center', shadow=True)
	frame = legend.get_frame()
	frame.set_facecolor('0.90')
	plt.show()