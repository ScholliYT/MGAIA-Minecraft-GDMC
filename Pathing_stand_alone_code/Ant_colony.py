import random

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# Constants
print_array = False

iterations = 10000
NUM_ANTS = 50
Food_amount = 100
PHEROMONE_EVAPORATION = 0.05
PHEROMONE_DECAY = 0.02
RANDOMNESS = 0.05
SAME_DIR_MULTIPLIER = 2
SLOPE_MODIFIER = 2

GRID_SIZE = 100
HOME_POSITION = (GRID_SIZE // 2, GRID_SIZE // 2)
# load map
slope = np.loadtxt("slope.txt", dtype=float)
map = np.loadtxt("map.txt", dtype=int)

# Initialize grid and pheromone array
grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
pheromone_array = np.zeros((GRID_SIZE, GRID_SIZE), dtype=float)
step_counts = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
last_paths_array = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
pheromone_history = np.zeros((GRID_SIZE, GRID_SIZE), dtype=float)
last_paths = []

# Place food sources randomly
# food_sources = np.random.randint(1, 6, size=(NUM_FOOD_SOURCES, 2))
NUM_FOOD_SOURCES = 0
food_sources = []
for row_nr in range(len(map)):
    for col_nr in range(len(map)):
        if map[row_nr][col_nr] == 2:
            food_sources.append([row_nr, col_nr])
            NUM_FOOD_SOURCES += 1


food_sources_left = [Food_amount] * NUM_FOOD_SOURCES
for food in food_sources:
    grid[food[0], food[1]] = -1

# Place ants at the home position

ants = [random.choice(food_sources)] * NUM_ANTS
ants_homes = [a for a in ants]

Ants_pheromones = [1] * NUM_ANTS
ant_paths = [[] for _ in range(NUM_ANTS)]
going_home = [False] * NUM_ANTS
ants_last_move = [[0, 0]] * NUM_ANTS


def move_ant(pheromone_array, ant_position, i):
    # Get the dimensions of the pheromone array
    rows = len(pheromone_array)
    cols = len(pheromone_array[0])

    # Define the neighboring positions
    potential_neighbors = [
        (ant_position[0] - 1, ant_position[1]),  # Up
        (ant_position[0] + 1, ant_position[1]),  # Down
        (ant_position[0], ant_position[1] - 1),  # Left
        (ant_position[0], ant_position[1] + 1),  # Right
        (ant_position[0] - 1, ant_position[1] + 1),  #
        (ant_position[0] - 1, ant_position[1] - 1),  #
        (ant_position[0] + 1, ant_position[1] + 1),  #
        (ant_position[0] + 1, ant_position[1] - 1),  #
    ]
    if ants_last_move[i] == [0, 0]:
        neighbors = potential_neighbors
        factor = [1] * len(neighbors)
    else:
        ant_next = [ant_position[0] + ants_last_move[i][0], ant_position[1] + ants_last_move[i][1]]
        factor = []
        neighbors = []
        for pot in potential_neighbors:
            dif = np.abs(ant_next[0] - pot[0]) + np.abs(ant_next[1] - pot[1])
            if dif < 2:
                neighbors.append(pot)
                if dif < 1:
                    factor.append(SAME_DIR_MULTIPLIER)
                else:
                    factor.append(1)

    # Calculate the pheromone levels of the neighboring positions
    pheromone_levels = []
    slope_levels = []
    for neighbor in neighbors:
        row, col = neighbor
        # Check if the neighbor is within the array bounds
        if 0 <= row < rows and 0 <= col < cols:
            pheromone_levels.append(pheromone_array[row][col])
            slope_levels.append(slope[row][col])
        else:
            # If the neighbor is out of bounds, assign a low pheromone level
            pheromone_levels.append(0.0)
            slope_levels.append(10_000)

    if sum(pheromone_levels) == 0:
        # Calculate the probabilities based on the pheromone levels
        probabilities = [1 for _ in pheromone_levels]
    else:
        # Calculate the probabilities based on the pheromone levels
        probabilities = [
            level + RANDOMNESS * sum(pheromone_levels) / sum(pheromone_levels)
            for level in pheromone_levels
        ]

    probabilities = [
        (p * f) / s * SLOPE_MODIFIER + 0.1 for p, f, s in zip(probabilities, factor, slope_levels)
    ]
    # Choose the next position based on the probabilities
    next_position = random.choices(neighbors, probabilities)[0]
    return next_position


def print_this():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    # Update grid with ants
    for ant in ants:
        grid[ant[0], ant[1]] = 1

    # Update grid with food sources
    for food in food_sources:
        if food[0] >= 0 and food[0] < GRID_SIZE and food[1] >= 0 and food[1] < GRID_SIZE:
            grid[food[0], food[1]] = -1

    grid[HOME_POSITION[0], HOME_POSITION[1]] = 2

    # Display the grid
    for row in grid:
        for cell in row:
            if cell == 1:
                print("A", end=" ")  # Ant
            elif cell == -1:
                print("F", end=" ")  # Food
            elif cell == 2:
                print("H", end=" ")
            else:
                print(".", end=" ")  # Empty cell
        print()


iteration = 0
# Main loop
while len(food_sources) > 0:
    iteration += 1
    if print_array:
        print_this()

    # Update ant positions
    for i, ant in enumerate(ants):
        # GOING HOME
        if going_home[i]:
            if len(ant_paths[i]) == 0:
                going_home[i] = False
                Ants_pheromones[i] = 1
                continue
            step_counts[ants[i][0], ants[i][1]] += 1
            next_step = ant_paths[i].pop(-1)  # Move along the stored path
            pheromone_array[ants[i][0], ants[i][1]] += Ants_pheromones[i]
            Ants_pheromones[i] = Ants_pheromones[i] * (1 - PHEROMONE_DECAY)
            ants[i] = next_step
        # EAT FOOD
        elif (
            any(abs(ant[0] - f[0]) + abs(ant[1] - f[1]) < 3 for f in food_sources)
            and [ant[0], ant[1]] != ants_homes[i]
        ):
            food_found = [f for f in food_sources if abs(ant[0] - f[0]) + abs(ant[1] - f[1]) < 3]
            index_food = food_sources.index([food_found[0][0], food_found[0][1]])
            food_sources_left[index_food] -= 1
            if food_sources_left[index_food] == 0:
                # add last path to dict
                last_paths.append(ant_paths[i])
                food_sources.remove([food_found[0][0], food_found[0][1]])
                food_sources_left.remove(0)
            going_home[i] = True
            if len(ant_paths[i]) == 0:
                going_home[i] = False
                Ants_pheromones[i] = 1
                continue

            next_step = ant_paths[i].pop(-1)  # Move along the stored path
            pheromone_array[ants[i][0], ants[i][1]] += Ants_pheromones[i]
            Ants_pheromones[i] = Ants_pheromones[i] * (1 - PHEROMONE_DECAY)
            ants[i] = next_step
        # WONDER
        else:
            new_position = move_ant(pheromone_array, ants[i], i)
            # direction = np.random.choice([-1, 0, 1], size=2)
            # new_position = (ant[0] + direction[0], ant[1] + direction[1])

            # Check if new position is within the boundaries of the grid
            if (
                0 <= new_position[0] < GRID_SIZE
                and 0 <= new_position[1] < GRID_SIZE
                and map[new_position[0], new_position[1]] != 1
            ):
                ants_last_move[i] = [new_position[0] - ants[i][0], new_position[1] - ants[i][1]]
                ants[i] = new_position
                ant_paths[i].append(new_position)
            else:
                ants_last_move[i] = [0, 0]

    # Evaporate pheromones
    if iteration % 10 == 0:
        pheromone_array = gaussian_filter(pheromone_array, sigma=2, mode="constant")
    pheromone_array *= 1.0 - PHEROMONE_EVAPORATION
    pheromone_history += pheromone_array

    if iteration % 10_000 == 0:
        pheromone_array = np.round(pheromone_array, 8)

        plt.imshow(step_counts, cmap="hot", interpolation="nearest")
        plt.title("steps")
        plt.colorbar()
        plt.show()

        plt.imshow(pheromone_history, cmap="hot", interpolation="nearest")
        plt.colorbar()
        plt.title("pheromone")
        plt.show()

        print_this()


pheromone_array = np.round(pheromone_array, 8)
plt.imshow(pheromone_history, cmap="hot", interpolation="nearest")
plt.colorbar()
plt.title("pheromone")
plt.show()

plt.imshow(step_counts, cmap="hot", interpolation="nearest")
plt.title("steps")
plt.colorbar()
plt.show()

plt.imshow(slope, cmap="hot", interpolation="nearest")
plt.title("slope")
plt.colorbar()
plt.show()

print_this()
