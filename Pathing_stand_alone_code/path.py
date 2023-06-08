import random

# Constants
WIDTH = 10
HEIGHT = 10
NUM_DOORS = 5
NUM_ANTS = 10
EVAPORATION_RATE = 0.01 # Rate at which pheromones evaporate
STEPS_PER_PHEROMONE = 10  # Number of steps per pheromone deposition


# Create the pheromone grid
pheromones = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Place doors (food sources) randomly on the map
doors = []
for _ in range(NUM_DOORS):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    doors.append((x, y))

# Place ant homes randomly on the map
ant_homes = []
for _ in range(NUM_DOORS):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    ant_homes.append((x, y))


# Define Ant class
class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited_doors = set()
        self.steps = 0

    def move(self):
        # Get neighboring cells' pheromone levels
        neighboring_pheromones = []
        for dx in [-1,0, 1]:
            for dy in [-1,0, 1]:
                new_x = self.x + dx
                new_y = self.y + dy
                if new_x >= 0 and new_x < WIDTH and new_y >= 0 and new_y < HEIGHT:
                    neighboring_pheromones.append(pheromones[new_y][new_x])
                else:
                    neighboring_pheromones.append(0)


        if random.randint(0,1) == 1:
            max_pheromone = max(neighboring_pheromones)
            max_indices = [i for i, pheromone in enumerate(neighboring_pheromones) if pheromone == max_pheromone]
            index = random.choice(max_indices)
        else:
            max_pheromone = random.choice(neighboring_pheromones)
            indeces = [i for i, pheromone in enumerate(neighboring_pheromones) if pheromone == max_pheromone]
            index = random.choice(indeces)

        dx = [-1, 0, 1][index % 3]
        dy = [-1, 0, 1][index // 3]

        # Update the ant's position
        new_x = self.x + dx
        new_y = self.y + dy
        if new_x >= 0 and new_x < WIDTH and new_y >= 0 and new_y < HEIGHT:
            self.x = new_x
            self.y = new_y

    def get_position(self):
        return self.x, self.y

    def leave_pheromone(self):
        pheromones[self.y][self.x] += 1

    def found_food(self):
        door = (self.x, self.y)
        if door not in self.visited_doors:
            self.visited_doors.add(door)
        self.steps = 0

    def found_home(self):
        door = (self.x, self.y)
        if door not in self.visited_doors:
            self.visited_doors.add(door)
        self.steps = 0


# Create ants
ants = []
for _ in range(NUM_ANTS):
    x = random.randint(0, WIDTH - 1)
    y = random.randint(0, HEIGHT - 1)
    ants.append(Ant(x, y))

# Simulate ant movement
for _ in range(1000):  # Number of simulation steps
    for ant in ants:
        ant.move()

        # Check if the ant found food or home
        if (ant.x, ant.y) in doors:
            ant.found_food()
        elif (ant.x, ant.y) in ant_homes:
            ant.found_home()

        # Check if the ant needs to leave pheromones
        if ant.steps < STEPS_PER_PHEROMONE:
            ant.leave_pheromone()
            ant.steps += 1

    # Evaporate pheromones and decay existing pheromones
    for i in range(HEIGHT):
        for j in range(WIDTH):
            pheromones[i][j] *= (1 - EVAPORATION_RATE)

    # Update the map with ant positions and pheromone levels

    for i in range(HEIGHT):
        for j in range(WIDTH):
            print(pheromones[i][j], end=' ')
        print()
    print('----')