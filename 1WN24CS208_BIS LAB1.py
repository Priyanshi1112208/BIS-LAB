import random

# ---------------------------------------------------------
# 1. LOCATIONS
# ---------------------------------------------------------

locations = ['A', 'B', 'C', 'D', 'E']


# ---------------------------------------------------------
# 2. DISTANCE MATRIX
# ---------------------------------------------------------
# Distance between each pair of locations

distance = {
    'A': {'A': 0,  'B': 10, 'C': 15, 'D': 20, 'E': 25},
    'B': {'A': 10, 'B': 0,  'C': 35, 'D': 25, 'E': 30},
    'C': {'A': 15, 'B': 35, 'C': 0,  'D': 30, 'E': 20},
    'D': {'A': 20, 'B': 25, 'C': 30, 'D': 0,  'E': 15},
    'E': {'A': 25, 'B': 30, 'C': 20, 'D': 15, 'E': 0}
}


# ---------------------------------------------------------
# 3. CALCULATE TOTAL ROUTE DISTANCE
# ---------------------------------------------------------

def calculate_distance(route):

    total_distance = 0

    # Distance from starting point to first location
    total_distance += distance['A'][route[0]]

    # Distance between locations
    for i in range(len(route) - 1):
        total_distance += distance[route[i]][route[i + 1]]

    # Return to starting point A
    total_distance += distance[route[-1]]['A']

    return total_distance


# ---------------------------------------------------------
# 4. CREATE INITIAL POPULATION
# ---------------------------------------------------------

def create_population(population_size):

    population = []

    for _ in range(population_size):

        route = locations.copy()

        # A is the fixed starting point,
        # so we shuffle only B, C, D, E
        middle = route[1:]
        random.shuffle(middle)

        route = middle

        population.append(route)

    return population


# ---------------------------------------------------------
# 5. FITNESS FUNCTION
# ---------------------------------------------------------

def fitness(route):

    total_distance = calculate_distance(route)

    # Smaller distance = better fitness
    return 1 / total_distance


# ---------------------------------------------------------
# 6. SELECTION
# ---------------------------------------------------------

def selection(population):

    # Sort routes according to fitness
    population.sort(key=fitness, reverse=True)

    # Keep the best routes
    return population[:4]


# ---------------------------------------------------------
# 7. ORDER CROSSOVER
# ---------------------------------------------------------

def crossover(parent1, parent2):

    size = len(parent1)

    # Select two random crossover points
    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    # Copy part of parent 1
    child = [None] * size

    child[start:end] = parent1[start:end]

    # Fill remaining positions using parent 2
    remaining = [x for x in parent2 if x not in child]

    index = 0

    for i in range(size):

        if child[i] is None:

            child[i] = remaining[index]
            index += 1

    return child


# ---------------------------------------------------------
# 8. MUTATION
# ---------------------------------------------------------

def mutation(route):

    # Mutation probability
    mutation_rate = 0.10

    if random.random() < mutation_rate:

        # Select two locations
        i, j = random.sample(range(len(route)), 2)

        # Swap them
        route[i], route[j] = route[j], route[i]

    return route


# ---------------------------------------------------------
# 9. GENETIC ALGORITHM
# ---------------------------------------------------------

def genetic_algorithm():

    population_size = 20
    generations = 100

    population = create_population(population_size)

    best_route = None
    best_distance = float('inf')

    for generation in range(generations):

        # Find current best route
        current_best = min(
            population,
            key=calculate_distance
        )

        current_distance = calculate_distance(current_best)

        # Update global best
        if current_distance < best_distance:

            best_distance = current_distance
            best_route = current_best.copy()

        # Selection
        selected = selection(population)

        # Create new population
        new_population = selected.copy()

        while len(new_population) < population_size:

            # Select two parents
            parent1, parent2 = random.sample(selected, 2)

            # Crossover
            child = crossover(parent1, parent2)

            # Mutation
            child = mutation(child)

            new_population.append(child)

        population = new_population

    return best_route, best_distance


# ---------------------------------------------------------
# 10. RUN THE ALGORITHM
# ---------------------------------------------------------

best_route, best_distance = genetic_algorithm()


# ---------------------------------------------------------
# 11. DISPLAY RESULT
# ---------------------------------------------------------

print("Best Route:")

print("A → " + " → ".join(best_route) + " → A")

print("Total Distance:", best_distance)
