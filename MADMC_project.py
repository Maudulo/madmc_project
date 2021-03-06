import numpy as np 
from operator import itemgetter, attrgetter
import copy
import sys

def gaussian_vector_generator(n, m):
	"""
	generates n random vectors with a gaussian distribution with 
	an expected value of m and a standard deviation of m/4
	"""

	return np.array([np.random.normal(m, m/4, 2) for _ in range(n)])


def build_vector(L):
	"""
	convert all vectors generated by gaussian_vector_generator to be compatible for all computation's functions
	"""
	return [Element(l,[l]) for l in L]

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
	new_l = l
	while(go_on):
		to_delete = []
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


def pareto_dominants(l, ph1 = None, ph2 = None):
	"""
	find all vectors that are not pareto dominated in l
	by sorting l in a lexicographic order then 
	O(nlog(n))
	"""
	# l_sorted = sorted(l, key=attrgetter('sum'), reverse=False)
	l_sorted = sorted(l, key=lambda elem: (elem.sum[0], elem.sum[1]), reverse=False)
	v_2_max = l_sorted[0]
	pareto_dominants = [l_sorted[0]]
	for i in range(1,len(l_sorted)):
		if l_sorted[i].sum[1] < v_2_max.sum[1]:
			v_2_max = l_sorted[i]
			pareto_dominants.append(l_sorted[i])

	return pareto_dominants


def arg_pareto_dominants(l):
	"""
	@params l : la liste des objets dans laquelle trouver les Pareto-dominants
	@return p_dominants la liste des Pareto-dominants
			arg_list la liste des indices des Pareto-dominants dans l
	"""
	p_dominants = pareto_dominants(l)
	# arg_list = []
	# for x in p_dominants:
	# 	for y in range(len(l)):
	# 		if x[0] == l[y][0] and x[1] == l[y][1]:
	# 			arg_list.append(y)
	# return p_dominants, arg_list

	return p_dominants, [l.index(x) for x in p_dominants]



def construct_arg_list(l, arg_list):
	list_pareto = []
	for element in arg_list:
		list_pareto.append(l[element])
	return list_pareto


def dynamic_programming(L, K, I_dominance = False, display_all_array = False, alpha_min = 0, alpha_max = 1):
	if(K > len(L)):
		print("Il ne peut pas y avoir de solution avec ", K, " élements dans un ensemble de ", len(L), " éléments")
		sys.exit()
	
	get_Dominators  = pareto_dominants
	if I_dominance:
		get_Dominators = I_dominant

	tab = np.empty((len(L), K), dtype = object)

	#_______________________________________________
	#initialisation
	tab[0,0] = [Element(L[0],[L[0]])]

	for l in range(1,len(L)):
		tab[l,0] = get_Dominators(np.concatenate((copy.deepcopy(tab[l-1,0]), [Element(L[l],[L[l]])])), alpha_min, alpha_max)

	for l in range(1, len(L)):
		for k in range(1, K):
			if k == l + 1:
				break
			objs = copy.deepcopy(tab[l-1,k-1])
			for o in objs:
				o.sum = np.add(o.sum, L[l])
				o.elements = np.concatenate((o.elements,[L[l]]))
			if k != l: # si k == l, alors k>l-1 et la case du dessus n'est pas remplie
				objs = np.concatenate((objs, copy.deepcopy(tab[l-1,k])))
			tab[l,k] = get_Dominators(objs, alpha_min, alpha_max)

	# return (tab[len(L)-1,K-1].sum, tab[len(L)-1,K-1].elements)
	if display_all_array:
		return tab
	else:
		return tab[len(L)-1,K-1]


def minimax_value(l, alpha_min = 0, alpha_max = 1):
	"""
		@params l la liste des paretos-dominants
		Détermine la valeur minimax de chacun des points de l, et retourne leur valeur minimax
	"""
	alpha = alpha_min
	results = []

	for element in l:
		if(element.sum[0] > element.sum[1]):
			alpha = alpha_max
		results.append(element.sum[0] * alpha + element.sum[1] * (1 - alpha))

	return l[np.argmin(results)]


def I_dominant(l, alpha_min = 0, alpha_max = 1):

	not_I_dominated = []
	new_l = copy.deepcopy(l)

	while(len(new_l) != 0):
		# init the list where goes all elements that are not I_dominated
		to_delete = []
		# process the first element
		element = new_l[0]
		# it will be removed at the end and possibly added to the not_I_dominated list
		to_delete.append(0)

		i_dominant = True

		# pour tous les autres éléments
		for i in range(1,len(new_l)):
			element2 = new_l[i]

			if dominate(element.sum, element2.sum, alpha_min, alpha_max):
				to_delete.append(i)

			elif dominate(element2.sum, element.sum, alpha_min, alpha_max):
				i_dominant = False
				break

		if(i_dominant):
			not_I_dominated.append(copy.deepcopy(element))

		new_l = [i for (j, i) in enumerate(new_l) if (j not in to_delete)]

	return not_I_dominated


def dominate(e1,e2,alpha_min, alpha_max):
	cst1 = (e1[0]-e2[0])
	cst2 = (e2[1]-e1[1])
	return ((alpha_min*cst1) <= ((1-alpha_min)*cst2)) and ((alpha_max*cst1) <= ((1-alpha_max)* cst2)) and (((alpha_min*cst1) < ((1-alpha_min)*cst2)) or ((alpha_max*cst1) < ((1-alpha_max)* cst2)))

class Element:

	def __init__(self, sum_vector = 0, element = []):
		self.sum = sum_vector
		self.elements = element