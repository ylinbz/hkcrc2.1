import math
import npga as ga
import matplotlib.pyplot as plt
import numpy as np

from lib_func_pool import get_num_of_input, input_range, get_individual_func_lost_list_with_goal, target_loss, get_total_func_lost


def scaleMinMax(x, xmin, xmax, mindesired, maxdesired):
	return ((x - xmin) / (xmax - xmin) * (maxdesired - mindesired) + mindesired)

def graytodec(bin_list):
	"""
	Convert from Gray coding to binary coding.
	We assume big endian encoding.
	"""
	b = bin_list[0]
	d = int(b) * (2**(len(bin_list)-1))
	for i, e in enumerate(range(len(bin_list) - 2, -1, -1)):
		b = str(int(b != bin_list[i + 1]))
		d += int(b) * (2**e)
	return d

def decodechromosome(bits, BitsForEachNumber, vector_size):
	x = np.zeros((vector_size,), dtype = np.float64)
	for i in range(vector_size):
		dec = graytodec(bits[(i * BitsForEachNumber) : (i * BitsForEachNumber + BitsForEachNumber)])
		max_current = math.pow(2, BitsForEachNumber) - 1
		x[i] = scaleMinMax(dec, 0, max_current, input_range[i][0], input_range[i][1])
	return x


def getfitness(candidate, BitsForEachNumber, vector_size):
    x = decodechromosome(candidate, BitsForEachNumber, vector_size)

    return get_individual_func_lost_list_with_goal(x)


def find_pareto_frontier(itr_num):
    gene_set = '01'
    bits_foreach_number = 16
    vector_size = get_num_of_input()
    gene_len = [bits_foreach_number * vector_size]

    def fnGetFitness(genes): return getfitness(genes, bits_foreach_number, vector_size)

    algorithm = ga.Algorithm(fnGetFitness, target_loss, 
                    gene_len,
                    chromosome_set = gene_set,
                    population_size = 20,
                    max_generation = itr_num, crossover_rate = 0.65,
                    mutation_rate = 1/170, niche_radius = 0.02,
                    candidate_size = 10, prc_tournament_size = 0.13,
                    multithread_mode = True)

    solution = algorithm.run()

    output = []
    for gene in solution:
        x = decodechromosome(gene.genes, bits_foreach_number, vector_size)
        output.append((x, get_total_func_lost(x)))

    return output
