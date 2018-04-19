import math
import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plotter

population_size = 8

crossover_rate = 0.5
mutation_rate = 0.02

max_iterations = 1000

print "Maximizar o g(x)"
print "Tamanho da populacao :",population_size
print "Taxa de crossover :", crossover_rate
print "Taxa de mutacao :", mutation_rate
print "Numero de iteracoes", max_iterations

# Retorna um bit aleatorio que representa um gene.
def gene():
    return random.randint(0,1)

def random_population_init():
    initial_population = []
    counter = 0
    while counter < population_size:
        individual = [gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene()]
        initial_population.append(individual)
        counter += 1
    return initial_population
        

def print_list(list, list_name):
    print "\n", list_name, "\n"
    i = 1
    for item in list:
        print i, "- ", item, "-",convert(item)
        i += 1

def convert(individual): 
    bitstring = ''.join(str(e) for e in individual)
    decimalNumber = int(bitstring, 2)
    return decimalNumber/1000.0

# Avalia a populacao
def evaluate(population):
    evaluations = []
    for i in population:
        x = convert(i)
        evaluation = 2 ** (-2 * ((x-0.1)/0.9) ** 2) * (math.sin(5 * math.pi * x)) ** 6
        evaluations.append(evaluation)
    return evaluations


# Gera o vetor com as faixas em graus da roleta
def get_selection_ranges(aptitudes):
    init_range = 0
    selection_ranges = []
    generationAptitude = sum(aptitudes)
    for aptitude in aptitudes:
        individualRangeSize = 0
        if generationAptitude == 0:
            individualRangeSize = 360/population_size
        else:
            individualRangeSize = float (360 * aptitude)/generationAptitude
        selection_ranges.append([init_range, individualRangeSize + init_range])
        init_range += individualRangeSize
    return selection_ranges

# Realiza a selecao dos individuos para proxima geracao
def selection(aptitudes, population):
    selection_ranges = get_selection_ranges(aptitudes)
    selection_randoms = np.random.randint(360, size=population_size)
    newGeneration = []
    for srand in selection_randoms:
        i = 0
        for srange in selection_ranges:
            if srand >= srange[0] and srand <= srange[1]:
                newGeneration.append(population[i])
            i+=1
    return newGeneration

# Faz o crossover e atualiza a populacao substituindo
# os pais pelos filhos
def make_crossover(population, couple_index):
    position = couple_index * 2
    parent1 = population[position]
    parent2 = population[position+1]
    crossover_point = random.randint(0, len(parent1)-1)
    child1 = genetic_recombination(parent1, parent2, crossover_point)
    child2 = genetic_recombination(parent2, parent1, crossover_point)
    population[position] = child1
    population[position+1] = child2

# Faz a recombinacao genetica dos pais e gera o filho
def genetic_recombination(parent1, parent2, crossover_point):
    child = []
    child.extend(parent1[:crossover_point])
    child.extend(parent2[crossover_point:])
    return child

# Realiza a reproducao da populacao, podendo haver crossover
# ou nao, baseado na taxa de crossover 
def reproduction(population):
    couplesCount = population_size/2
    r = []
    i = 0
    while i < couplesCount:
        r.append(random.random())
        i += 1
        
    for item in r:
        j = 0
        if item < crossover_rate:
            make_crossover(population, j)
        j+=1

# Realiza as mutacoes na populacao baseado na taxa de mutacao
def mutation(population):
    mutation_points = []
    population_index = 0
    for individual in population:
        i = 0
        while i < len(individual):
            if random.random() < mutation_rate:
                mutation_points.append([population_index+1, i+1])
                individual[i] = -individual[i] + 1
            i+=1
        population_index+=1

it = 0
population = random_population_init()
print_list(population,"Populacao Inicial")
evaluations = evaluate(population)

while it < max_iterations:
    population = selection(evaluations, population)
    reproduction(population)
    mutation(population)
    evaluations = evaluate(population)
    it += 1

print_list(population,"Populacao Final")
best_evaluation = max(evaluations)
best_index = evaluations.index(best_evaluation)
print "\nResultado", convert(population[best_index]),"com avaliacao",best_evaluation