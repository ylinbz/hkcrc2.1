import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs


# 生成数据
X, y_true = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)

# 绘制生成的数据
plt.scatter(X[:, 0], X[:, 1], s=50);
plt.title("Generated Data")
plt.show()


# 设置K-means聚类
kmeans = KMeans(n_clusters=4)

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