import numpy as np
import random

def generate_values(n=100, a=0.1, b=2):
    """
    :param n: Anzahl von Geschenke
    :param a: Min Gewicht
    :param b: Max Gewicht
    :return: Array von n Geschenken mit zufälligen Gewichten zwischen a und b
    """
    return [random.uniform(a, b) for _ in range(n)]


def generate_population_0(n=1000, a=100):
    return [generate_solution(a) for _ in range(n)]

def generate_solution(n):
    return [random.randint(0,1) for _ in range(n)]

def get_fitness(population, values, weight_limit):
    """
    :param population: Array mit allen Solutions aus der Population 0
    :param values: Werte, die für die Berechnung des Gewichtes verwendet werden sollen
    :param weight_limit: Max Gewicht für ein Solution
    :return: Array mit berechneten Fitnesses
    """
    fitness = []
    for i in np.arange(0, len(population)):
        weight_sum = sum(values[j] for j in population[i] if population[i][j] == 1)

        # Wenn weight_limit nicht überschritten werden darf:
        """if weight_sum <= weight_limit:
            f = np.exp(-0.001*(weight_limit-weight_sum)**2)
            fitness.append(f)
        else:
            fitness.append(0)"""

        # Wenn weight_limit überschritten werden darf:
        f = np.exp(-0.001 * (weight_limit - weight_sum) ** 2)
        fitness.append(f)

    return fitness


# Calculate fitness for one individual (solution) based on values (weight of presents) and weight_limit
def calc_fitness(solution, values, weight_limit):
    weight_sum = sum(values[i] for i in solution if solution[i] == 1)
    return np.exp(-0.001 * (weight_limit - weight_sum) ** 2)

def get_probability(fitness):
    fitness_sum = sum(fitness)
    return [f / fitness_sum for f in fitness]

def selection(population, probability, r, values, weight_limit):
    selected_ind = [select_solution_random(population, values, weight_limit) for _ in range(int(round((1-r)*len(population))))]
    new_population = [population[index] for index in selected_ind]
    return new_population


""" Selektion mit Wahrscheinlichkeit Pr(hi) = fitness(hi)/sum(all fitness) """
def select_solution(probability):
    randNum = random.uniform(0,1)
    summe = 0
    index = random.randint(0, len(probability))
    while summe < randNum:
        index = index + 1
        index = index % len(probability)
        summe = summe + probability[index]

    return index

""" Selektion: Zufällig zwei Individuen auswählen, und die, die bessere fitness hat, zurückgeben """
def select_solution_random(population, values, weight_limit):
    solution1 = population[random.randint(0, len(population) - 1)]
    solution2 = population[random.randint(0, len(population) - 1)]
    fitness1 = calc_fitness(solution1, values, weight_limit)
    fitness2 = calc_fitness(solution2, values, weight_limit)

    if fitness1 > fitness2:
        index = population.index(solution1)
        return index
    else:
        index = population.index(solution2)
        return index

def crossover(population, probability, r, values, weight_limit):
    children = []
    break_point = int(r * 100)
    for _ in range(int(round(r*len(population)/2))):
        parent1 = population[select_solution_random(population, values, weight_limit)]
        parent2 = population[select_solution_random(population, values, weight_limit)]
        child1 = parent1[:break_point] + parent2[break_point:]
        child2 = parent2[:break_point] + parent1[break_point:]

        children.append(child1)
        children.append(child2)
    return children


def mutation(population, m):
    selected_indices = random.sample(range(len(population) - 1), m)
    num_genes = len(population[0])
    for index in selected_indices:
        random_gene = random.randint(0, num_genes-1)
        if population[index][random_gene] == 1:
            population[index][random_gene] = 0
        else:
            population[index][random_gene] = 1
    return population


def runGenerativeAlg(values, population_0, r, m, num_gen, weight_limit):
    max_fitness = 0
    max_solution_index = -1
    for _ in range(num_gen-1):
        fitness = get_fitness(population_0, values, weight_limit)
        probability = get_probability(fitness)

        # Selektion
        population_s = selection(population_0, probability, r, values, weight_limit)

        # Crossover
        children = crossover(population_0, probability, r, values, weight_limit)
        population_s = population_s + children

        # Mutation
        population_s_mut = mutation(population_s, m)

        fitness_new = get_fitness(population_s_mut, values, weight_limit)
        max_fitness = max(fitness_new)
        print(max_fitness)
        population_0 = population_s_mut
        max_solution_index = fitness_new.index(max_fitness)

    best_solution = population_0[max_solution_index]
    print("\nMax fitness:")
    print(max_fitness)
    return population_0, best_solution
    





if __name__ == '__main__':
    print("Knapsack Problem")
    weight_limit = 100
    n = 100
    p = 100
    r = 0.5
    m = 80

    values = generate_values(n)
    population_0 = generate_population_0(n, p)

    ps, best_solution = runGenerativeAlg(values, population_0, r, m, 500, weight_limit)
    print("Für Individuum:")
    print(best_solution)

    knapsack_weight = sum(values[i] for i in best_solution if best_solution[i] == 1)
    print("Knapsack Gewicht:")
    print(knapsack_weight)






