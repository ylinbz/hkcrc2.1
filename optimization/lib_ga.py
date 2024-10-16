import numpy as np
from lib_func_pool import get_total_func_lost, input_range, get_num_of_input


# %%
from sko.GA import GA

def run_ga(itr_num):
    output = []
    for itr in range(itr_num):
        ga = GA(func=get_total_func_lost, n_dim=get_num_of_input(), size_pop=50, max_iter=10, prob_mut=0.001, lb=[x[0] for x in input_range], ub=[x[1] for x in input_range], precision=1e-7)
        best_x, best_y = ga.run()
        output.append((best_x, best_y[0]))
    return output
