import numpy as np 
from operator import itemgetter

import sys

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
		pareto_dominant = True
		for j in range(len(pareto_dominants)):
			if np.all(pareto_dominants[j] <= l[i]) and np.any(pareto_dominants[j] < l[i]):
				pareto_dominant = False
				break

		if pareto_dominant:
			for j in range(i, len(l)):
				if np.all(l[j] <= l[i]) and np.any(l[j] < l[i]):
					pareto_dominant = False
					break

		if pareto_dominant:
			pareto_dominants.append(l[i])

	return pareto_dominants


def is_pareto_dominant(a,b):
	return np.all(a <= b) and np.any(a < b)

def naive_pareto_dominants_2(l):
	"""
	deletes elements that are pareto diminated while searching
	still O(n²) but should be faster 
	"""
	pareto_dominants = []
	go_on = True
	to_delete=[]
	new_l = l
	while(go_on):
		pareto_dominant = True
		for j in range(len(pareto_dominants)):
			if is_pareto_dominant(pareto_dominants[j], new_l[0]):
				pareto_dominant = False
				break

		if pareto_dominant:
			for j in range(1, len(new_l)):
				if is_pareto_dominant(new_l[0], new_l[j]):
					to_delete.append(j)
				elif is_pareto_dominant(new_l[j], new_l[0]):
					pareto_dominant = False
					break

		if pareto_dominant:
			pareto_dominants.append(new_l[0])

		to_delete.append(0)

		new_l = [i for (j, i) in enumerate(new_l) if j not in to_delete]
		if not new_l:
			go_on = False

	return pareto_dominants


def pareto_dominants(l):
	"""
	find all vectors that are not pareto dominated in l
	by sorting l in a lexicographic order then 
	O(nlog(n))
	"""
	l_sorted = sorted(l, key=itemgetter(0,1), reverse=False)
	v_2_max = l_sorted[0]
	pareto_dominants = [l_sorted[0]]
	for i in range(1,len(l_sorted)):
		if l_sorted[i][1] < v_2_max[1]:
			v_2_max = l_sorted[i]
			pareto_dominants.append(l_sorted[i])

	return pareto_dominants


def arg_pareto_dominants(l):
	p_dominants = pareto_dominants(l)
	arg_list = []
	for x in p_dominants:
		for y in range(len(l)):
			if x[0] == l[y][0] and x[1] == l[y][1]:
				arg_list.append(y)
	return p_dominants, arg_list


def construct_arg_list(l, arg_list):
	list_pareto = []
	for element in arg_list:
		print("coucou", len(l))
		print("kbdns", element)
		list_pareto.append(l[element])
	return list_pareto


def dynamic_programming(list_obj, size_max):
	"""
		@params list_obj la liste des objets dont on veut trouver un sous ensemble
				size_max la taille du sous ensemble d'objets souhaité
		@return la liste des paretos dominants

		Cette fonction trouve l'ensemble des paretos optimaux par la programmation dymnamique

		Les fonctions de récurrence sont : 
		dp_list[0,0] = list_obj[0]
		dp_list[1,l] = p_l U dp_list[1,l-1]
		dp_list[k,l] = Pareto((dp_list[k-1, l-1] + p_l) U dp_list[k, l-1])

	"""
	if(size_max > len(list_obj)):
		print("Il ne peut pas y avoir de solution avec ", size_max, " élements dans un ensemble de ", len(list_obj), " éléments")
		sys.exit()

	dp_list = np.empty((len(list_obj), size_max), dtype = object)
	obj_list = np.empty((len(list_obj), size_max), dtype = object)

	dp_list[0][0] = np.array([list_obj[0]])
	obj_list[0][0] = np.array([list_obj[0]])

	# pour chaque objet de la liste
	for l in range(1, len(list_obj)):

		dp_list[l][0], arg_pareto = arg_pareto_dominants(np.concatenate((np.array([list_obj[l]]), dp_list[l - 1][0])))
		obj_list[l][0] = construct_arg_list(np.concatenate((np.array([list_obj[l]]), obj_list[l - 1][0])), arg_pareto)
		
		# pour chaque taille d'objet
		for k in range(1, size_max):

			if k == l + 1:
				break

			sum_objs = np.add(dp_list[l - 1][k - 1], list_obj[l])
			objs = np.add(obj_list[l - 1][k - 1], list_obj[l])

			if k != l: # si k == l, alors k>l-1 et la case du dessus n'est pas remplie
				sum_objs = np.concatenate((sum_objs, dp_list[l - 1][k]))

			dp_list[l][k], arg_pareto = arg_pareto_dominants(np.array(sum_objs))
			obj_list[l][k] = construct_arg_list(np.array(objs), arg_pareto)

	return arg_pareto_dominants(dp_list[len(list_obj)-1][size_max-1])

def minimax_value(l, alpha_min, alpha_max):
	"""
		@params l la liste des paretos-dominants
		Détermine la valeur minimax de chacun des points de l, et retourne leur valeur minimax
	"""
	alpha = alpha_min
	results = []

	for element in l:
		if(element[0] > element[1]):
			alpha = alpha_max
		results.append(element[0] * alpha + element[1] * (1 - alpha))

	return results

def minimax_dynamic_programming(l, k, alpha_min = 0, alpha_max = 1):
	pareto, list_element = dynamic_programming(l, k)
	return pareto[np.argmax(minimax_value(pareto, alpha_min, alpha_max))], list_element[np.argmax(minimax_value(pareto, alpha_min, alpha_max))]
