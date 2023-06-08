import random
import time

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# To integrate with our Minecraft project, we only need to adjust the slope(slope_scores)
# and map(build plan houses with doors)

# and then built a path on the x and z(and corresponding find y from heightmap)from the blocks named in the paths found
# (like done in the heatmap making code)
size = 100
HOUSE_AVOID_MULT = 4
SLOPE_AVOID_MULT = 0.2
NUM_paths = 2
Iterations = 70


def find_straight_path(start, end):
    path = []

    x0, y0 = start
    x1, y1 = end

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while x0 != x1 or y0 != y1:
        path.append((x0, y0))
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

    path.append((x0, y0))

    return path


def new_spot(path, indx, path_array):
    rows = len(path_array)
    cols = len(path_array[0])
    row = path[indx][0]
    col = path[indx][1]

    # Check if the given index is out of bounds
    if row < 0 or row >= rows or col < 0 or col >= cols:
        return None

    # Define the 8 neighbors' positions
    neighbors = [
        (row - 1, col - 1),
        (row - 1, col),
        (row - 1, col + 1),
        (row, col - 1),
        (row, col + 1),
        (row + 1, col - 1),
        (row + 1, col),
        (row + 1, col + 1),
    ]

    new_neighbors = []
    for n in neighbors:
        if (abs(n[0] - path[indx + 1][0]) + abs(n[1] - path[indx + 1][1])) > 0 and (
            abs(n[0] - path[indx - 1][0]) + abs(n[1] - path[indx - 1][1])
        ) > 0:
            new_neighbors.append(n)

    neighbors = new_neighbors
    max_value = float("-inf")
    max_index = None

    for neighbor_row, neighbor_col in neighbors:
        # Check if the neighbor index is within the array bounds
        if 0 <= neighbor_row < rows and neighbor_col >= 0 and neighbor_col < cols:
            neighbor_value = path_array[neighbor_row][neighbor_col]
            if neighbor_value > max_value:
                max_value = neighbor_value
                max_index = (neighbor_row, neighbor_col)

    return max_index


def alter_path(path, path_array):
    for path_indx in range(1, len(path) - 3):
        path[path_indx] = new_spot(path, path_indx, path_array)

    new_path = []
    for indx in range(0, len(path) - 1):
        new_path.append(path[indx])
        if (abs(path[indx][0] - path[indx + 1][0]) + abs(path[indx][1] - path[indx + 1][1])) > 2:
            new_path.append(
                (
                    int(path[indx][0] / 2 + path[indx + 1][0] / 2),
                    int(path[indx][1] / 2 + path[indx + 1][1] / 2),
                )
            )
    new_path = list(dict.fromkeys(new_path))
    return new_path


def fix_path_final(path):
    new_path = []
    for indx in range(0, len(path) - 1):
        new_path.append(path[indx])
        if (abs(path[indx][0] - path[indx + 1][0]) + abs(path[indx][1] - path[indx + 1][1])) > 1:
            new_path.append(
                (
                    int(path[indx][0] / 2 + path[indx + 1][0] / 2),
                    int(path[indx][1] / 2 + path[indx + 1][1] / 2),
                )
            )

    return new_path


def get_neighbour_paths(paths, map_avoid, slope):
    path_array = np.zeros((size, size))
    for i in range(len(paths)):
        for block in paths[i]:
            path_array[block[0], block[1]] = 1

    path_array = gaussian_filter(path_array, sigma=2, mode="constant")
    path_array -= map_avoid * HOUSE_AVOID_MULT
    path_array -= slope[:size, :size] * SLOPE_AVOID_MULT

    return path_array


def make_paths(slope, map):
    # load maps
    # slope = np.loadtxt('slope.txt', dtype=float)
    # map = np.loadtxt('map.txt', dtype=float)

    map_avoid = gaussian_filter(map, sigma=3, mode="constant")

    doors = []
    for row_nr in range(len(map)):
        for col_nr in range(len(map)):
            if map[row_nr][col_nr] == 2:
                doors.append([row_nr, col_nr])

    # make straight paths
    paths = []
    for food_from in doors:
        for i in range(NUM_paths):
            food_to = random.choice(doors)
            if food_to != food_from:
                paths.append(find_straight_path(food_from, food_to))

    for it in range(Iterations):
        for i in range(len(paths)):
            path_array = get_neighbour_paths(paths, map_avoid, slope)
            paths[i] = alter_path(paths[i], path_array)

    mapcopy = map.copy()
    final_paths = np.zeros((len(map), len(map)), dtype=int)
    for p in paths:
        p = fix_path_final(p)
        for block in p:
            mapcopy[block[0], block[1]] = 3
            final_paths[block[0], block[1]] = 1
    time.sleep(0.1)
    plt.imshow(mapcopy, cmap="hot", interpolation="nearest")
    plt.colorbar()
    plt.title("mapcopy")
    plt.show()

    return final_paths


final_paths = make_paths(slope, map)
