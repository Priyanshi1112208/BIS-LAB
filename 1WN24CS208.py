import random

# =========================================================
# 1. LOCATIONS
# =========================================================

locations = ['A', 'B', 'C', 'D', 'E']


# =========================================================
# 2. DISTANCE MATRIX
# =========================================================

distance = {
    'A': {'A': 0,  'B': 10, 'C': 15, 'D': 20, 'E': 25},
    'B': {'A': 10, 'B': 0,  'C': 35, 'D': 25, 'E': 30},
    'C': {'A': 15, 'B': 35, 'C': 0,  'D': 30, 'E': 20},
    'D': {'A': 20, 'B': 25, 'C': 30, 'D': 0,  'E': 15},
    'E': {'A': 25, 'B': 30, 'C': 20, 'D': 15, 'E': 0}
}


# =========================================================
# 3. CALCULATE TOTAL DISTANCE
# =========================================================

def calculate_distance(route):

    total_distance = 0

    # A -> first location
    total_distance += distance['A'][route[0]]

    # Between locations
    for i in range(len(route) - 1):
        total_distance += distance[route[i]][route[i + 1]]

    # Last location -> A
    total_distance += distance[route[-1]]['A']

    return total_distance


# =========================================================
# 4. FITNESS FUNCTION
# =========================================================

def fitness(route):

    total_distance = calculate_distance(route)

    return 1 / total_distance


# =========================================================
# 5. CREATE INITIAL POPULATION
# =========================================================

def create_population(population_size):

    population = []

    for i in range(population_size):

        route = locations[1:].copy()

        random.shuffle(route)

        population.append(route)

    return population


# =========================================================
# 6. DISPLAY POPULATION
# =========================================================

def display_population(population):

    for i, route in enumerate(population):

        route_text = "A -> " + " -> ".join(route) + " -> A"

        dist = calculate_distance(route)

        fit = fitness(route)

        print(
            f"Individual {i + 1}: "
            f"{route_text} | "
            f"Distance = {dist} | "
            f"Fitness = {fit:.6f}"
        )


# =========================================================
# 7. SELECTION
# =========================================================

def selection(population):

    sorted_population = sorted(
        population,
        key=fitness,
        reverse=True
    )

    selected = sorted_population[:4]

    print("\n--- SELECTED PARENTS ---")

    for i, route in enumerate(selected):

        print(
            f"Parent {i + 1}: "
            f"A -> {' -> '.join(route)} -> A | "
            f"Distance = {calculate_distance(route)}"
        )

    return selected


# =========================================================
# 8. CROSSOVER
# =========================================================

def crossover(parent1, parent2):

    size = len(parent1)

    start = random.randint(0, size - 2)
    end = random.randint(start + 1, size - 1)

    child = [None] * size

    # Copy section from parent 1
    child[start:end] = parent1[start:end]

    # Fill remaining positions from parent 2
    remaining = [
        x for x in parent2
        if x not in child
    ]

    index = 0

    for i in range(size):

        if child[i] is None:

            child[i] = remaining[index]

            index += 1

    print("\nCROSSOVER")

    print(
        "Parent 1: A -> "
        + " -> ".join(parent1)
        + " -> A"
    )

    print(
        "Parent 2: A -> "
        + " -> ".join(parent2)
        + " -> A"
    )

    print(
        f"Crossover points: {start} and {end}"
    )

    print(
        "Child:    A -> "
        + " -> ".join(child)
        + " -> A"
    )

    return child


# =========================================================
# 9. MUTATION
# =========================================================

def mutation(route):

    mutation_rate = 0.10

    original_route = route.copy()

    random_number = random.random()

    print("\nMUTATION CHECK")

    print(
        "Route before mutation: A -> "
        + " -> ".join(route)
        + " -> A"
    )

    print(
        f"Random number = {random_number:.4f}"
    )

    print(
        f"Mutation rate = {mutation_rate}"
    )

    if random_number < mutation_rate:

        i, j = random.sample(
            range(len(route)),
            2
        )

        route[i], route[j] = (
            route[j],
            route[i]
        )

        print("MUTATION OCCURRED!")

        print(
            f"Swapped positions {i} and {j}"
        )

        print(
            "Route after mutation:  A -> "
            + " -> ".join(route)
            + " -> A"
        )

    else:

        print("No mutation.")

    return route


# =========================================================
# 10. GENETIC ALGORITHM
# =========================================================

def genetic_algorithm():

    population_size = 20

    generations = 10

    population = create_population(
        population_size
    )

    best_route = None

    best_distance = float('inf')


    # -----------------------------------------------------
    # INITIAL POPULATION
    # -----------------------------------------------------

    print("=" * 70)

    print("INITIAL POPULATION")

    print("=" * 70)

    display_population(population)


    # -----------------------------------------------------
    # GENERATIONS
    # -----------------------------------------------------

    for generation in range(1, generations + 1):

        print("\n")
        print("=" * 70)

        print(f"GENERATION {generation}")

        print("=" * 70)


        # -------------------------------------------------
        # FIND BEST ROUTE
        # -------------------------------------------------

        current_best = min(
            population,
            key=calculate_distance
        )

        current_distance = calculate_distance(
            current_best
        )


        print("\nCURRENT BEST ROUTE")

        print(
            "A -> "
            + " -> ".join(current_best)
            + " -> A"
        )

        print(
            "Distance =",
            current_distance
        )


        # -------------------------------------------------
        # UPDATE GLOBAL BEST
        # -------------------------------------------------

        if current_distance < best_distance:

            best_distance = current_distance

            best_route = current_best.copy()

            print("\nNEW GLOBAL BEST!")

            print(
                "Best Route = A -> "
                + " -> ".join(best_route)
                + " -> A"
            )

            print(
                "Best Distance =",
                best_distance
            )


        # -------------------------------------------------
        # SELECTION
        # -------------------------------------------------

        selected = selection(population)


        # -------------------------------------------------
        # CREATE NEW POPULATION
        # -------------------------------------------------

        new_population = selected.copy()

        print("\n--- CREATING NEW CHILDREN ---")


        while len(new_population) < population_size:

            # Choose two parents
            parent1, parent2 = random.sample(
                selected,
                2
            )

            # Crossover
            child = crossover(
                parent1,
                parent2
            )

            # Mutation
            child = mutation(child)

            new_population.append(child)

            print(
                "\nChild added to population:"
            )

            print(
                "A -> "
                + " -> ".join(child)
                + " -> A"
            )

            print(
                "Distance =",
                calculate_distance(child)
            )


        population = new_population


        # -------------------------------------------------
        # END OF GENERATION
        # -------------------------------------------------

        print("\n--- END OF GENERATION ---")

        generation_best = min(
            population,
            key=calculate_distance
        )

        print(
            "Generation Best Route: A -> "
            + " -> ".join(generation_best)
            + " -> A"
        )

        print(
            "Generation Best Distance:",
            calculate_distance(generation_best)
        )


    # =====================================================
    # FINAL RESULT
    # =====================================================

    print("\n")

    print("=" * 70)

    print("FINAL RESULT")

    print("=" * 70)

    print(
        "\nBEST ROUTE FOUND:"
    )

    print(
        "A -> "
        + " -> ".join(best_route)
        + " -> A"
    )

    print(
        "\nMINIMUM TOTAL DISTANCE:",
        best_distance
    )

    print(
        "\nFITNESS:",
        fitness(best_route)
    )

    return best_route, best_distance


# =========================================================
# 11. RUN PROGRAM
# =========================================================

best_route, best_distance = genetic_algorithm()
