import numpy as np 

def gaussian_vector_generator(n, m):
	"""
	generates n random vectors with a gaussian distribution with 
	an expected value of m and a standard deviation of m/4
	"""

	return np.array([np.random.normal(m, m/4, 2) for _ in range(n)])


def naive_pareto_dominants(l):
	"""
	find all vectors that are not pareto dominated in l
	by comparing each vector by pairs
	O(n²) 
	"""
	pareto_dominants = []
	for i in range(len(l)):
		pareto_dominant = true
		for j in range(len(pareto_dominants)):
			if np.all(pareto_dominants[j] >= l[i]) and np.any(pareto_dominants[j] > l[i]):
				pareto_dominant = false
				break

		if pareto_dominant:
			for j in range(i, len(l)):
				if np.all(l[j] >= l[i]) and np.any(l[j] > l[i]):
					pareto_dominant = false
					break

		if pareto_dominant:
			pareto_dominants.append(i)

	return pareto_dominants


def is_pareto_dominant(a,b):
	return np.all(a >= b) and np.any(a > b)

def naive_pareto_dominants_2(l):
	"""
	deletes elements that are pareto diminated while searching
	still O(n²) but should be faster 
	"""
	pareto_dominants = []
	go_on = True
	to_delete=[]
	while(go_on):
		pareto_dominant = true

		for j in range(len(pareto_dominants)):
			if is_pareto_dominant(pareto_dominants[j], new_l[0]):
				pareto_dominant = false
				break

		if pareto_dominant:
			for j in range(i, len(new_l)):
				if is_pareto_dominant(new_l[0], new_l[j]):
					to_delete.append(new_l[j])
				if is_pareto_dominant(new_l[j], new_l[0]):
					pareto_dominant = false
					break

		if pareto_dominant:
			pareto_dominants.append(0)

		to_delete.append(0)

		if len(to_delete) >= len(new_l)-1:
			go_on = false

		new_l = [i for j, i in enumerate(new_l) if j not in to_delete]



def pareto_dominants(l):
	"""
	find all vectors that are not pareto dominated in l
	by sorting l in a lexicographic order then 
	O(nlog(n))
	"""

	l_sorted = sorted(l, key=itemgetter(0,1), reverse=True)
	v_2_max = l_sorted[0]
	pareto_dominants = [l_sorted[0]]
	for i in range(1,len(l_sorted)):
		if l_sorted[i][1] > v_2_max[1]:
			v_2_max = l_sorted[i]
			pareto_dominants.append(l_sorted[i])

	return pareto_dominants
