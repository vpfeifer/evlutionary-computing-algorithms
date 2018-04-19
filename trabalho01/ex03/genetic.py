import math
import random
import matplotlib
import matplotlib.pyplot as plotter

population_size = 30

crossover_rate = 0.6
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
        individualx = [gene(), gene(), gene(), gene()]
        individualy = [gene(), gene(), gene(), gene()]
        initial_population.append([individualx, individualy])
        counter += 1
    return initial_population
        
def print_list(list, list_name):
    print "\n", list_name, "\n"
    i = 1
    for item in list:
        print i, "- ", item, "- (",convert(item[0]),",",convert(item[1]),")"
        i += 1

def convert(individual): 
    bitstring = ''.join(str(e) for e in individual[1:])
    decimalNumber = int(bitstring, 2)
    if individual[0] == 0:
        return decimalNumber * -1
    return decimalNumber

# Avalia a populacao
def evaluate(population):
    evaluations = []
    for i in population:
        x = convert(i[0])
        y = convert(i[1])
        evaluation = (1 - x) ** 2 + 100 * (y - x ** 2) ** 2
        evaluations.append(evaluation)
    return evaluations


# Realiza a selecao dos individuos para proxima geracao
def selection(aptitudes, population):
    newGeneration = []
    min_aptitude = min(aptitudes)
    best_index = aptitudes.index(min_aptitude)
    generation_best = population[best_index] 
    newGeneration.append(generation_best)

    while len(newGeneration) < population_size:
        r = [random.randint(0, population_size-1), random.randint(0, population_size-1), random.randint(0, population_size-1)]
        aps = [aptitudes[r[0]], aptitudes[r[1]], aptitudes[r[2]]]
        ap = min(aps)
        idx = aptitudes.index(ap)
        newGeneration.append(population[idx])

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
        while i < len(individual[0]):
            if random.random() < mutation_rate:
                mutation_points.append([population_index+1, i+1])
                individual[0][i] = -individual[0][i] + 1
            i+=1
        i = 0
        while i < len(individual[1]):
            if random.random() < mutation_rate:
                mutation_points.append([population_index+1, i+1])
                individual[1][i] = -individual[1][i] + 1
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
best_evaluation = min(evaluations)
best_index = evaluations.index(best_evaluation)
print "\nResultado", convert(population[best_index][0]),",",convert(population[best_index][1]),"com avaliacao",best_evaluation