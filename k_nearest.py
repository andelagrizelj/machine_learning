import matplotlib.pyplot as plt
import math

"""
Group 1 = marker='o', c='red'
Group 2 = marker='x', c='blue'
"""

def classify_point_k_nearest(training_data, point_coord, k):
    e_distances = []
    for group in training_data:
        for tr_point in training_data[group]:
            euclidean_distance = math.sqrt((tr_point[0] - point_coord[0]) ** 2 + (tr_point[1] - point_coord[1]) ** 2)
            e_distances.append((euclidean_distance, group))

    k_neighbors = sorted(e_distances)[:k]
    group1_freq = 0
    group2_freq = 0

    for neighbor in k_neighbors:
        if neighbor[1] == 1:
            group1_freq += 1
        elif neighbor[1] == 2:
            group2_freq += 1

    if group1_freq > group2_freq:
        return 1
    else:
        return 2

def classify_points_k_nearest(training_data, points, k, ax):
    for point in points:
        point_group = classify_point_k_nearest(training_data, point, k)
        if point_group == 1:
            ax.scatter(point[0], point[1], marker='o', c='red', s=7)
        elif point_group == 2:
            ax.scatter(point[0], point[1], marker='x', c='blue', s=7)


if __name__ == '__main__':

    """ Load data """
    with open('spiral.txt', 'r') as file:
        file_contents = file.read()

    coords_tuple = file_contents.split('\n')
    spiral1 = []
    spiral2 = []
    all_points = []

    for coord_tuple in coords_tuple:
        coord = coord_tuple.split(';')
        all_points.append([float(coord[0]), float(coord[1])])
        if int(coord[2]) == 1:
            spiral1.append([float(coord[0]), float(coord[1])])
        elif int(coord[2]) == -1:
            spiral2.append([float(coord[0]), float(coord[1])])

    spiral1_x = [coord[0] for coord in spiral1]
    spiral1_y = [coord[1] for coord in spiral1]
    spiral2_x = [coord[0] for coord in spiral2]
    spiral2_y = [coord[1] for coord in spiral2]

    """ Plot data """
    fig, ((ax1, ax2), (ax3, ax4))= plt.subplots(nrows=2, ncols=2)
    fig.suptitle('K-Nearest Neighbor', fontsize=16)

    ax1.scatter(spiral1_x, spiral1_y, marker='o', c='red', s=7)
    ax1.scatter(spiral2_x, spiral2_y, marker='x', c='blue', s=7)
    ax1.set_title("Training data")

    training_data = {1: spiral1, 2: spiral2}

    """ K-Nearest Neigbor for k=1 """
    classify_points_k_nearest(training_data, all_points, 1, ax2)
    ax2.set_title("k=1")

    """ K-Nearest Neigbor for k=3 """
    classify_points_k_nearest(training_data, all_points, 3, ax3)
    ax3.set_title("k=3")

    """ K-Nearest Neigbor for k=5 """
    classify_points_k_nearest(training_data, all_points, 5, ax4)
    ax4.set_title("k=5")

    plt.tight_layout()
    plt.show()






