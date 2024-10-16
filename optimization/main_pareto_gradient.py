from lib_pareto_ga import find_pareto_frontier
from lib_func_pool import get_total_func_lost, get_num_of_input, input_range
import nlopt
from numpy import *
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
#import seaborn as sns

output = find_pareto_frontier(5)
print("ga pareto finished -----------------------")
print("minimal is: ", min([cost for (_, cost) in output]))

print("minimal is: ", output)

X = np.array([item[0] for item in output])


kmeans = KMeans(n_clusters=3)

# 执行聚类
kmeans.fit(X)

# 获取聚类中心和聚类标签
centers = kmeans.cluster_centers_
labels = kmeans.labels_



# 绘制聚类结果
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='viridis')
plt.scatter(centers[:, 0], centers[:, 1], c='red', s=200, alpha=0.75)

plt.title("K-means Clustering")
plt.show()

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
    opt.set_maxtime(2)

    final_x.append(opt.optimize(x))
    final_min.append(opt.last_optimum_value())

print("gradient decent finished ----------------------")
print("minimal is: ", min(final_min))
print("input are: ", final_x)
print("input are: ", final_x[final_min.index(min(final_min))])

from sklearn.metrics import silhouette_score
print("Silhouette Score: ", silhouette_score(X, kmeans.labels_))
