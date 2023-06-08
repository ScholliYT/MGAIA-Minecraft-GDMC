import numpy as np
import matplotlib.pyplot as plt
import random
from scipy.ndimage import gaussian_filter

# load map
slope = np.loadtxt('slope.txt', dtype=float)
map = np.loadtxt('map.txt', dtype=int)

plt.imshow(slope, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("slope")
plt.show()

plt.imshow(map, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("map")
plt.show()

NUM_paths = 3
babys = 2

MUTATION_RATE = 10
POP = 10

NUM_FOOD_SOURCES = 0
food_sources = []
for row_nr in range(len(map)):
    for col_nr in range(len(map)):
        if map[row_nr][col_nr] == 2:
            food_sources.append([row_nr, col_nr])
            NUM_FOOD_SOURCES += 1




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

    path.append((x0, y0))  # Add the endpoint to the path

    return path


paths = []
for food_from in food_sources:
    for i in range(NUM_paths):
        food_to = random.choice(food_sources)
        paths.append(find_straight_path(food_from, food_to))
    break

population = []
for i in range(POP):
    population.append(paths)


mapcopy = map.copy()
for p in paths:
    for block in p:
        mapcopy[block[0], block[1]] = 3

plt.imshow(mapcopy, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("mapcopy")
plt.show()


def mutate(path):
    try:
        mutated_path = path.copy()  # Create a copy of the original path

        # Randomly select a segment of the path to mutate
        start_index = random.randint(0, len(mutated_path) - 2)  # Exclude the endpoint
        end_index = random.randint(start_index + 1, len(mutated_path) - 1)
        old_middle = int(abs(start_index - end_index))
        new_middle = [path[old_middle][0] + int(random.randint(-MUTATION_RATE, MUTATION_RATE)),
                      path[old_middle][1] + int(random.randint(-MUTATION_RATE, MUTATION_RATE))]
        # Generate a new random subpath to replace the selected segment
        subpath = find_straight_path(mutated_path[start_index], new_middle)
        subpath += find_straight_path(new_middle, mutated_path[end_index])
        # Replace the selected segment with the new subpath
        mutated_path[start_index:end_index + 1] = subpath

        #mutated_path = [instance for instance in mutated_path if random.random() > 0.01]  # Adjust the probability as desired

        return mutated_path
    except:
        return path

def mutate_all(paths):
    for path_nr in range(len(paths)):
        paths[path_nr] = mutate(paths[path_nr])
    return paths

def fitness(paths):
    try:
        # LENGTH
        length = 0
        for p in paths:
            length += len(p)

        # OVERLAP HOUSE
        House_overlap = 0
        for p in paths:
            for b in p:
                if map[b[0],b[1]] != 0:
                    House_overlap += 1

        score = length * 0.1 + House_overlap
        return score
    except:
        return 100_000

def select(pop, scores):
    # Combine the array and scores into a list of tuples
    combined = list(zip(pop, scores))

    # Sort the combined list based on scores in descending order
    combined.sort(key=lambda x: x[1], reverse=False)

    # Calculate the index to split the array in half
    split_index = len(combined) // 2

    # Split the combined list into two halves
    sorted_arr, sorted_scores = zip(*combined[:split_index])

    # Return the sorted array and scores
    return sorted_arr, sorted_scores

old_fitness_scores = []
for sample in population:
    old_fitness_scores.append(fitness(sample))


#MAIN LOOP
for i in range(100_000):

    new_paths = []
    fitness_scores = []
    for sample in population:
        # add parents
        child = sample.copy()
        paths = mutate_all(child)
        new_paths.append(paths)
        fitness_score = fitness(paths)
        fitness_scores.append(fitness_score)

    new_paths += population
    fitness_scores += old_fitness_scores

    population, old_fitness_scores = select(new_paths, fitness_scores)




mapcopy = map.copy()
for p in population[0]:
    for block in p:
        mapcopy[block[0], block[1]] = 3

plt.imshow(mapcopy, cmap='hot', interpolation='nearest')
plt.colorbar()
plt.title("mapcopy")
plt.show()
