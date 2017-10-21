import time
import numpy as np
import matplotlib.pyplot as plt
from MADMC_project import *

def test_pareto_functions(func, nmin = 200, nmax = 10000, step = 200, n = 50):
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

			l = gaussian_vector_generator(i, 50)

			a = time.time()
			pareto_dominants = func(l)
			time_measure[index_time_measure] += time.time() - a

		time_measure[index_time_measure] /= n
		index_time_measure += 1

	print("-------------------------------------")
	return time_measure

def plot_pareto_functions(func, nmin = 200, nmax = 10000, step = 200, n = 50):
	"""
	This function displays a graph representing the time depending of the number of value into a list
	@params : func : the function to test
			  nmin : the minimum size of the list of values
			  nmax : the maximum size of the list of values
			  step : the number of value added to the list between 2 iterations
			  n : the number of tests during an iteration
	"""
	y = np.arange(nmin, nmax, step);
	x = test_pareto_functions(func, nmin, nmax, step, n)
	plt.plot(x, y)

def plot_pareto_compare_functions(func1, func2, nmin = 200, nmax = 10000, step = 200, n = 50):
	plot_pareto_functions(func1, nmin = nmin, nmax = nmax, step = step, n = n)
	plot_pareto_functions(func2, nmin = nmin, nmax = nmax, step = step, n = n)
	plt.show()
	