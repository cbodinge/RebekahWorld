import numpy as np


def pair_distance(cluster1, cluster2):
    """
    Input: List cluster_list of clusters, integers idx1, idx2

    Output: Tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2].

    Notes: Returned tuple always has idx1 < idx2.
    """

    vert_dist = cluster1.avg_x() - cluster2.avg_x()
    horiz_dist = cluster1.avg_y() - cluster2.avg_y()

    return (vert_dist ** 2 + horiz_dist ** 2) ** 0.5


def slow_closest_pair(cluster_list):
    """
    Input: List cluster_list of clusters

    Output: Tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.

    Notes: Returned tuple always has idx1 < idx2. Implements O(n^2) time algorithm.
    """

    tup = (0, 0, 0)

    size = len(cluster_list)
    for ind1 in range(size - 1):
        c1 = cluster_list[ind1]
        for ind2 in range(ind1 + 1, size):
            c2 = cluster_list[ind2]
            dist = pair_distance(c1, c2)[0]
            if tup == (0, 0, 0):
                tup = (dist, ind1, ind2)
            elif dist < tup[0]:
                tup = (dist, ind1, ind2)

    return tup


def fast_closest_pair(sorted_cluster_list):
    """
    Input: List sorted_cluster_list of clusters SORTED SUCH THAT THE HORIZONTAL POSIIONS
    OF THEIR CENTERS ARE IN ASCENDING ORDER

    Output: Tuple of the form (dist, idx1, idx2) where the centers of the clusters
    sorted_cluster_list[idx1] and sorted_cluster_list[idx2] have minimum distance dist.

    Note: Returned tuple always has idx1 < idx2. Implements O(n log(n)^2) algorithm
    """

    size = len(sorted_cluster_list)

    if size <= 3:
        return slow_closest_pair(sorted_cluster_list)

    half = size // 2
    lst1 = sorted_cluster_list[:half]
    lst2 = sorted_cluster_list[half:]

    tup1 = fast_closest_pair(lst1)
    tup2 = fast_closest_pair(lst2)
    if tup1[0] <= tup2[0]:
        tup = tup1
    else:
        tup = (tup2[0], tup2[1] + half, tup2[2] + half)

    mid = (sorted_cluster_list[half - 1].avg_x() +
           sorted_cluster_list[half].avg_x()) / 2

    across = closest_pair_strip(sorted_cluster_list, mid, tup[0])

    if tup[0] < across[0]:
        return tup

    return across


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Input: List cluster_list of clusters,
    float horiz_center is the horizontal position of the strip's vertical center line
    float half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: Tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.

    NOTE: Returned tuple always has idx1 < idx2. Implements O(n log(n)) algorithm.
    """

    indices = [ind for ind in range(len(cluster_list))
               if abs(cluster_list[ind].avg_x() - horiz_center) <= half_width]

    indices.sort(key=lambda ind: cluster_list[ind].avg_y())
    size = len(indices)

    tup = (10 ** 10, 0, 0)

    for in1 in range(size - 1):
        for in2 in range(in1 + 1, min(in1 + 4, size)):
            new_tup = pair_distance(cluster_list[indices[in1]], cluster_list[indices[in2]])
            if new_tup[0] < tup[0]:
                tup = new_tup

    return tup


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Input: List cluster_list of clusters, interger num_clusters

    Output: List of clusters whose length is num_clusters

    NOTE: Function should mutate cluster_list to improve efficiency
    """

    while len(cluster_list) > num_clusters:
        cluster_list.sort(key=lambda cluster: cluster.avg_x())
        dij = fast_closest_pair(cluster_list)
        c_2 = cluster_list.pop(dij[2])
        cluster_list[dij[1]].merge_clusters(c_2)

    print(len(cluster_list))

    return cluster_list


class Cluster:
    def __init__(self, x, y, intensity):
        self.x = [x]
        self.y = [y]
        self.intensity = [intensity]

    def avg_x(self):
        return np.average(self.x)

    def avg_y(self):
        return np.average(self.y)

    def avg_intensity(self):
        return np.average(self.intensity)

    def copy(self):
        """
        Return a copy of a cluster
        """
        return Cluster(self.x, self.y, self.intensity)

    def merge(self, other_cluster):
        self.x += other_cluster.x
        self.y += other_cluster.y
        self.intensity += other_cluster.intesity
