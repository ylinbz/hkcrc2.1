from lib_ga import run_ga
import nlopt
from numpy import *

from lib_func_pool import get_total_func_lost, input_range, get_num_of_input

# output: [(input_1, loss_1), (input_2, loss_2) ....]
output = run_ga(30)

print("ga finished -----------------------")
print("minimal is: ", min([cost for (_, cost) in output]))
print(output)






final_min = []
final_x = []

def loss_func(x, grad):
    return get_total_func_lost(x)

for (x, _) in output:
    opt = nlopt.opt(nlopt.LN_COBYLA, get_num_of_input())
    x_min, x_max = [], []
    for x_mix_max in input_range:
        x_min.append(x_mix_max[0])
        x_max.append(x_mix_max[1])
    opt.set_upper_bounds(x_max)
    opt.set_lower_bounds(x_min)
    opt.set_min_objective(loss_func)
    opt.set_xtol_rel(1e-20)
    opt.set_maxtime(4)

    final_x.append(opt.optimize(x))
    final_min.append(opt.last_optimum_value())

print("gradient decent finished ----------------------")
print("minimal is: ", min(final_min))
print("input are: ", final_x[final_min.index(min(final_min))])
print("input are: ", final_x)
