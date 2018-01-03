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

def pareto_dominants_2(l):
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


def dynamic_programming_2(L, K, I_dominance = False):
	if(K > len(L)):
		print("Il ne peut pas y avoir de solution avec ", K, " élements dans un ensemble de ", len(L), " éléments")
		sys.exit()
	
	get_Dominators  = pareto_dominants_2
	if I_dominance:
		get_Dominators = I_dominant_2

	tab = np.empty((len(L), K), dtype = object)

	#_______________________________________________
	#initialisation
	tab[0,0] = [Element(L[0],[L[0]])]

	for l in range(1,len(L)):
		tab[l,0] = get_Dominators(np.concatenate((copy.deepcopy(tab[l-1,0]), [Element(L[l],[L[l]])])))

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
			tab[l,k] = get_Dominators(objs)

	# return (tab[len(L)-1,K-1].sum, tab[len(L)-1,K-1].elements)
	return tab[len(L)-1,K-1]


def dynamic_programming(list_obj, size_max, i_dominant = False, alpha_min = 0, alpha_max = 1):
    """
        @params list_obj la liste des objets dont on veut trouver un sous ensemble
                size_max la taille du sous ensemble d'objets souhaité
        @return la liste des paretos dominants

        Cette fonction trouve l'ensemble des paretos optimaux par la programmation dymnamique

        Les fonctions de récurrence sont : 
        dp_list[0,0] = list_obj[0]
        dp_list[1,l] = Pareto(p_l U dp_list[1,l-1])
        dp_list[k,l] = Pareto((dp_list[k-1, l-1] + p_l) U dp_list[k, l-1])

    """
    if(size_max > len(list_obj)):
        print("Il ne peut pas y avoir de solution avec ", size_max, " élements dans un ensemble de ", len(list_obj), " éléments")
        sys.exit()

    dp_list = np.empty((len(list_obj), size_max), dtype = object) # liste des P-opt (somme des objets)

    dp_list[0][0] = np.array([list_obj[0]])

    # pour chaque objet de la liste
    for l in range(1, len(list_obj)):
        if not I_dominant:
            dp_list[l][0], index_p_opt = arg_pareto_dominants(np.concatenate((np.array([list_obj[l]]), dp_list[l - 1][0])))
        else:
            dp_list[l][k] = I_dominant(np.concatenate((np.array([list_obj[l]]), dp_list[l - 1][0])), alpha_min, alpha_max)

        # pour chaque taille d'objet
        for k in range(1, size_max):

            if k == l + 1:
                break

            objs = np.add(dp_list[l - 1][k - 1], list_obj[l])

            if k != l: # si k == l, alors k>l-1 et la case du dessus n'est pas remplie
                objs = np.concatenate((objs, dp_list[l - 1][k]))

            if not I_dominant:
                dp_list[l][k], index_p_opt = arg_pareto_dominants(np.array(objs))
            else:
                dp_list[l][k] = I_dominant(np.array(objs), alpha_min, alpha_max)

    return dp_list[len(list_obj)-1][size_max-1], dp_obj[len(list_obj)-1][size_max-1]


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
	return pareto[np.argmin(minimax_value(pareto, alpha_min, alpha_max))], list_element[np.argmax(minimax_value(pareto, alpha_min, alpha_max))]


def minimax_value_2(l, alpha_min = 0, alpha_max = 1):
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

    I_dominator = []
    to_delete = []
    new_l = copy.deepcopy(l)

    while(len(new_l) != 0):
        element = l[0]
        i_dominant = True

        # pour tous les autres éléments
        for i in range(1,len(l)):
            element2 = l[i]

            if dominate(element, element2, alpha_min, alpha_max):
                to_delete.append(i)

            elif dominate(element2, element, alpha_min, alpha_max):
                i_dominant = False
                break

        if(i_dominant):
            I_dominator.append(element)
        to_delete.append(0)

        new_l = [i for (j, i) in enumerate(new_l) if (j not in to_delete)]

    return I_dominator

def I_dominant_2(l, alpha_min = 0, alpha_max = 1):

    I_dominator = []
    to_delete = []
    new_l = copy.deepcopy(l)

    while(len(new_l) != 0):
        element = l[0]
        i_dominant = True

        # pour tous les autres éléments
        for i in range(1,len(l)):
            element2 = l[i]

            if dominate(element.sum, element2.sum, alpha_min, alpha_max):
                to_delete.append(i)

            elif dominate(element2.sum, element.sum, alpha_min, alpha_max):
                i_dominant = False
                break

        if(i_dominant):
            I_dominator.append(copy.deepcopy(element))
        to_delete.append(0)

        new_l = [i for (j, i) in enumerate(new_l) if (j not in to_delete)]

    return I_dominator




def fi(element, alpha):
	return element[0] * alpha + element[1] * (1 - alpha)

def dominate(e1, e2, alpha_min, alpha_max):
	return fi(e1, alpha_min) <= fi(e2, alpha_min) and fi(e1, alpha_max) <= fi(e2, alpha_max) and (fi(e1, alpha_min) < fi(e2, alpha_min) or fi(e1, alpha_max) < fi(e2, alpha_max))


class Element:

	def __init__(self, sum_vector = 0, element = []):
		self.sum = sum_vector
		self.elements = element