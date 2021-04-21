import numpy as np
import random
import math


class Kmeans:
    def __init__(self, X, n_clusters, max_iter):
        self.X = X
        self.K = n_clusters
        self.max_iter = max_iter
        self.cluster_centers_ = self.init_centroids()
        self.labels_ = None

    def init_centroids(self):
        u, n = np.unique(self.X, return_index=True, axis=0)
        np.random.shuffle(n)
        ind = n[0:self.K]
        ret = self.X[ind]
        return ret

    def closest_centroids(self):
        n = self.X.shape[0]
        c_ind = []

        for i in range(n):
            dist = np.inf
            closest = 0
            x = self.X[i]

            for c in range(len(self.cluster_centers_)):
                d = np.sqrt(np.sum((x- self.cluster_centers_[c])**2))
                if d < dist:
                    closest = c
                    dist = d

            c_ind.append(closest)
        c_ind = np.array(c_ind)

        self.labels_ = c_ind
        return c_ind


    def update_centroids(self, centroid_indices):
        clusters = {}
        for i in range(self.K):
            clusters[i] = []

        centers = []
        old_centers = self.cluster_centers_

        for (x, ind) in zip(self.X, centroid_indices):
            spec_clus = clusters[ind]
            spec_clus.append(x)

        for c in range(len(clusters)):
            m = np.mean(clusters[c], axis=0)
            centers.append(m)

        centers = np.array(centers)

        if (not np.array_equal(old_centers, centers)):
            self.cluster_centers_ = centers
            return False
        return True


    def fit(self):
        foo = False
        for i in range(self.max_iter):
            if (not foo):
                foo = self.update_centroids(self.closest_centroids())
            else:
                break
        self.labels_ = np.array(self.closest_centroids())
