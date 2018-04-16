import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plotter

# 0 - Imprime somente a geracao resultante
# 1 - Imprime o resultado a cada geracao (populacao, aptidao de cada individuo, aptidao media)
# 2 - Imprime os passos do algoritmo (selecao, reproducao, mutacao, avaliacao)
# 3 - Imprime os detalhes da selecao dos individuos da proxima geracao
verbose_level = 0

population_size = 32

target = [1,1,1,1,0,1,1,0,1,1,1,1]
targetSize = len(target)

crossover_rate = 0.5
mutation_rate = 0.02

execution_times = 1000

print "Reconhecer o 0 representado por",target
print "Verbose level", verbose_level
print "Tamanho da populacao :",population_size
print "Taxa de crossover :", crossover_rate
print "Taxa de mutacao :", mutation_rate
print "Numero de execucoes",execution_times

# Retorna um bit aleatorio que representa um gene.
def gene():
    return random.randint(0,1)

def random_population_init():
    initial_population = []
    counter = 0
    while counter < population_size:
        individual = [gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene(), gene()]
        initial_population.append(individual)
        counter += 1
    return initial_population

def print_list(list, list_name):
    print "\n", list_name, "\n"
    i = 1
    for item in list:
        print i, "-   ", item
        i += 1

# Conta a quantidade de genes diferentes de um individuo em relacao ao alvo.
def count_diff_genes(individual):
    diff = 0
    i = 0
    while i < targetSize:
        if target[i] != individual[i]:
            diff += 1
        i+=1
    return diff

# Retorna o vetor das distancias de hamming da populacao
def calculate_hamming_distance(population):
    hammingDistanceArray = []
    for individual in population:
        diffBits = count_diff_genes(individual)
        hammingDistanceArray.append(diffBits)
    return hammingDistanceArray

# Avalia a populacao
def evaluate(population):
    h = calculate_hamming_distance(population)
    aptitudes = []
    for item in h:
        aptitudes.append(targetSize - item)
    if verbose_level > 1:        
        print "\n=== EVALUATION STEP ==="
        print "Target", target
        print_list(population, "Population")
        print "Target size", targetSize
        print "Hamming Array",h
        print "Aptitudes result", aptitudes
    return aptitudes

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
    if verbose_level > 2:
        print "\n\t=== GET SELECTION RANGES ==="
        print "\tAptitudes =", aptitudes
        print "\tSum aptitudes =",generationAptitude
        print_list(selection_ranges, "Selection Ranges")
    return selection_ranges

# Realiza a selecao dos individuos para proxima geracao
def selection(aptitudes, population):
    if verbose_level > 1:
        print "\n=== SELECTION STEP ==="
    selection_ranges = get_selection_ranges(aptitudes)
    selection_randoms = np.random.randint(360, size=population_size)
    if verbose_level > 1:
        print "Target", target
        print_list(population, "Population")
        print "Aptitudes", aptitudes
        print_list(selection_ranges,"Selection ranges")
        print "Random numbers", selection_randoms
    newGeneration = []
    for srand in selection_randoms:
        if verbose_level > 2:
            print "\n\tThe random number", srand
        i = 0
        for srange in selection_ranges:
            if srand >= srange[0] and srand <= srange[1]:
                if verbose_level > 2:
                    print "\tMatch with", srange
                    print "\tThen the individual",i, " - ",population[i],"from the population was selected"
                newGeneration.append(population[i])
            i+=1
    if verbose_level > 1:
        print_list(newGeneration, "New Generation Selected")
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
        i = 0
        if item < crossover_rate:
            make_crossover(population, i)
        i+=1
    if verbose_level > 1:
        print "\n=== REPRODUCTION STEP ==="
        print "Target", target
        print_list(population, "Population")
        print "Crossover rate =", crossover_rate
        print "Random numbers =",r
        print_list(population, "Population after reproduction")

# Realiza as mutacoes na populacao baseado na taxa de mutacao
def mutation(population):
    if verbose_level > 1:
        print "\n=== MUTATION STEP ==="
        print "Mutation rate =", mutation_rate
        print "Target", target
        print_list(population, "Population")
    mutation_points = []
    population_index = 0
    for individual in population:
        individual_index = 0
        while individual_index < targetSize:
            if random.random() < mutation_rate:
                mutation_points.append([population_index+1, individual_index+1])
                individual[individual_index] = -individual[individual_index] + 1
            individual_index+=1
        population_index+=1
    if verbose_level > 1:
        print "Tota mutations",len(mutation_points)
        print "Mutation points [Individual, Gene] =", mutation_points
        print_list(population, "Population after mutation")

# Imprime os dados de uma geracao  
def print_generation_data(generationNumber, population, aptitudes):
    print "\n======== Geracao", generationNumber, " ========"
    print print_list(population, "Population")
    print "\nAptidoes =",aptitudes
    print "\nAptidao media da geracao =", float(sum(aptitudes)/population_size)

# Condicao de parada
def population_contains_target(aptitudes):
    for aptitude in aptitudes:
        if aptitude == targetSize:
            return True
    return False

def execute_algorithm(generate_execution_chart):
    population = random_population_init()
    aptitudes = evaluate(population)

    # Dados para o grafico de uma execucao do algoritmo
    generations = []
    aptitude_averages = []
    max_aptitudes = []
    min_aptitudes = []

    generationsCounter = 1
    while not population_contains_target(aptitudes):
        # Passos do algoritmo
        population = selection(aptitudes, population)
        reproduction(population)
        mutation(population)
        aptitudes = evaluate(population)

        # Dados para o grafico
        generations.append(generationsCounter)
        aptitude_avg = float(sum(aptitudes)/population_size)
        aptitude_averages.append(aptitude_avg)
        max_aptitudes.append(max(aptitudes))
        min_aptitudes.append(min(aptitudes))
        
        if verbose_level > 0:
            print_generation_data(generationsCounter, population, aptitudes)
        generationsCounter += 1

    if generate_execution_chart:
        print_generation_data(generationsCounter, population, aptitudes)

        fig, ax = plotter.subplots()
        ax.plot(generations, aptitude_averages, label='Population Aptitude Average')
        ax.plot(generations, max_aptitudes, label='Max Aptitude')
        ax.plot(generations, min_aptitudes, label='Min Aptitude')

        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels)

        ax.set(xlabel='Generations', ylabel='Aptitude',title='')
        ax.grid()

        fig.savefig("test.png")
        plotter.show()
    return generationsCounter

executed = 0

# Dados para o grafico de todas as execucoes
generations_needed_array = []
avg_array = []
max_array = []
min_array = []
executions = []

while executed < execution_times:
    generations_needed = execute_algorithm(False)
    generations_needed_array.append(generations_needed)
    executions.append(executed + 1)
    executed += 1

a = 0
avg_generations = sum(generations_needed_array)/len(generations_needed_array)
max_val = max(generations_needed_array)
min_val = min(generations_needed_array)

while a < execution_times:
    max_array.append(max_val)
    min_array.append(min_val)
    avg_array.append(avg_generations)
    a+=1

fig, ax = plotter.subplots()
ax.plot(executions, generations_needed_array, label='Generations Needed')
ax.plot(executions, avg_array, label='Generations average')
ax.plot(executions, min_array, label='Min Generation')
ax.plot(executions, max_array, label='Max Generation')

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels)

ax.set(xlabel='Executions')
ax.grid()

fig.savefig("test.png")
plotter.show()