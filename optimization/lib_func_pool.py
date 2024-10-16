import math
from cube import Cubic

def get_individual_func_lost_list_with_goal(input_list):
    f_list = get_individual_func(input_list)
    f_with_goal_list = []
    for i in range(len(f_list)):
        f_with_goal_list.append([f_list[i], goal[i]])
    return f_with_goal_list

def get_total_func_lost(input_list):
    total_lost = 0
    f_list = get_individual_func(input_list)
    for i in range(len(f_list)):
        total_lost += coefficient[i]*f_list[i]
    return total_lost

def get_num_of_input():
    return len(input_range)
        
# TODO edit here
# range of different vars
# [[x_1_min, x_1_max], ..., [x_n_min, x_n_max]]
input_range = [[600, 4500], [600, 12000], [600, 4900], [1, 300], [1, 100], [1, 100], [1, 500]]
target_loss = [-1000000000000000000000000, -100000000000000000000000000000, -100000000000000000000, -10000000000000000000000, -10000000000000000000, -10000000000000000,-100000000000000,-100000000000000000,-10000000000000000000]
goal = ['minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize', 'minimize']
coefficient = [10,10,1,1,1,1,1,1,1]



# [length, width, height, temp, humidity, density, ............]
def get_individual_func(input_list):
    return [Cubic.total_volume(input_list[0], input_list[1], input_list[2]), 
            Cubic.total_surface_area(input_list[0], input_list[1]), 
            Cubic.beam_cost(input_list[0], input_list[1], input_list[2], input_list[3], input_list[4], input_list[5], input_list[6]), 
            Cubic.product_cost(input_list[3], input_list[4], input_list[5], input_list[6]),
           Cubic.calculate_welding(input_list[3],input_list[4],  input_list[5], input_list[6]),
            Cubic.welding_time(input_list[3], input_list[4], input_list[5], input_list[6]),
            Cubic.calculate_weldingprice(input_list[3], input_list[4], input_list[5], input_list[6])  ,
            Cubic.deflection_x(input_list[1], input_list[3], input_list[4], input_list[5],input_list[6]),
            Cubic.deflection_y(input_list[0], input_list[3], input_list[4], input_list[5],input_list[6])                                   
            ]



