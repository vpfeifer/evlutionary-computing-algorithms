import random
import numpy as np

population_size = 8

target = [1,1,1,1,0,1,1,0,1,1,1,1]
targetSize = len(target)

crossover_rate = 0.6
mutation_rate = 0.02

print "Reconhecer o 0 representado por",target
print "Tamanho da populacao :",population_size
print "Taxa de crossover :", crossover_rate
print "Taxa de mutacao :", mutation_rate

# Retorna um bit aleatorio que representa um gene.
def gen():
    return random.randint(0,1)

def initialize_population():
    initial_population = []
    counter = 0
    while counter < population_size:
        individual = [gen(), gen(), gen(), gen(), gen(), gen(), gen(), gen(), gen(), gen(), gen(), gen()]
        initial_population.append(individual)
        counter += 1
    return initial_population

def print_population(population):
    print "\nPopulacao\n"
    i = 1
    for individual in population:
        print i, "-", individual
        i += 1

# Conta a quantidade de genes diferentes de um individuo em relacao ao alvo.
def count_diff_gens(individual):
    diff = 0
    for gen in individual:
        index = individual.index(gen)
        if target[index] != gen:
            diff += 1
    return diff

# Retorna o vetor das distancias de hamming da populacao
def calculate_hamming_distance(population):
    hammingDistanceArray = []
    for individual in population:
        diffBits = count_diff_gens(individual)
        hammingDistanceArray.append(diffBits)
    return hammingDistanceArray

# Avalia a populacao
def evaluate(population):
    h = calculate_hamming_distance(population)
    aptitudes = []
    for item in h:
        aptitudes.append(targetSize - item)
    return aptitudes

# Gera o vetor com as faixas em graus da roleta
def get_selection_range(aptitudes):
    generationAptitude = sum(aptitudes)
    init_range = 0
    selection_range = []
    for aptitude in aptitudes:
        individualRangeSize = float (360 * aptitude)/generationAptitude
        selection_range.append([init_range, individualRangeSize + init_range])
        init_range += individualRangeSize
    return selection_range

# Realiza a selecao dos individuos para proxima geracao
def selection(aptitudes, population):
    selection_ranges = get_selection_range(aptitudes)
    selection_randoms = np.random.randint(360, size=population_size)
    newGeneration = []
    for srand in selection_randoms:
        for srange in selection_ranges:
            if srand >= srange[0] and srand <= srange[1]:
                index = selection_ranges.index(srange)
                newGeneration.append(population[index])
    return newGeneration

# Faz o crossover e atualiza a populacao substituindo
# os pais pelos filhos
def make_crossover(population, couple_index):
    position = couple_index * 2
    parent1 = population[position]
    parent2 = population[position+1]
    crossover_point = random.randint(0, targetSize-1)
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
    r = [random.random(), random.random(), random.random(), random.random()]
    for item in r:
        if item < crossover_rate:
            couple_index = r.index(item)
            make_crossover(population, couple_index)

# Realiza as mutacoes na populacao baseado na taxa de mutacao
def mutation(population):
    for individual in population:
        for gen in individual:
            if random.random() < mutation_rate:
                genIndex = individual.index(gen)
                individual[genIndex] = -gen + 1

# Imprime os dados de uma geracao  
def print_generation_data(generationNumber, population, aptitudes):
    print "======== Geracao", generationNumber, " ========"
    print "\nAptidoes =",aptitudes
    print "\nAvaliacao media da geracao =", float(sum(aptitudes)/population_size)

# Condicao de parada
def population_contains_target(aptitudes):
    for aptitude in aptitudes:
        if aptitude == 0:
            return True
    return False

population = initialize_population()
aptitudes = evaluate(population)

generationsCounter = 1
while not population_contains_target(aptitudes):
    population = selection(aptitudes, population)
    reproduction(population)
    mutation(population)
    aptitudes = evaluate(population)
    generationsCounter += 1

print_generation_data(generationsCounter, population, aptitudes)