# Lion Hunting Optimization Algorithm (LHOA)
import matplotlib.pyplot as plt
import math
import random
import sys

_hunting_groups = 4          # Amount of hunting groups
_hunters_by_group = 7        # Amount of hunters in each hunting group
_max_iterations = 50         # Number of iterations
_dimensions = 2              # Amount of problem dimensions

class Lion:
    current_position = []
    best_position = []
    fitness = sys.maxint

    def __init__(self, current_position, best_position, fitness):
        self.current_position = current_position
        self.best_position = best_position
        self.fitness = fitness

class Prey:
    current_position = []

    def __init__(self, current_position):
        self.current_position = current_position

class HuntingGroup:
    lions = []
    prey = None

    def __init__(self, lions, prey):
        self.lions = lions
        self.prey = prey

# Fitness is defined by the function to be optimized.
def f(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

global_min = sys.maxint

# Initialize hunting groups
hunting_groups = []
for i in range(0,_hunting_groups):
    # Add some lions to the hunting group
    group_lions = []
    group_x = 0
    group_y = 0
    for j in range(0, _hunters_by_group):
        position = [random.randint(-5,5), random.randint(-5,5)]
        lion_fitness = f(position[0], position[1])
        if lion_fitness < global_min:
            global_min = lion_fitness
        lion = Lion(position, position, lion_fitness)
        group_x += position[0]
        group_y += position[1]
        group_lions.append(lion)
    # Add the hunting group prey
    prey_position = [group_x/_hunters_by_group, group_y/_hunters_by_group]
    prey = Prey(prey_position)
    hunting_groups.append(HuntingGroup(group_lions, prey))

for i in range(0, _max_iterations):
    for hg in hunting_groups:
        for lion in hg.lions:
            u = random.uniform(0,1)
            new_x = (1 - u) * lion.current_position[0] + u * hg.prey.current_position[0]
            new_y = (1 - u) * lion.current_position[1] + u * hg.prey.current_position[1]
            new_fitness = f(new_x, new_y)
            if new_fitness < lion.fitness:
                lion.current_position[0] = new_x
                lion.current_position[1] = new_y
            if new_fitness < global_min:
                global_min = new_fitness
        u_prey = random.uniform(0,1)
        hg.prey.current_position[0] = hg.prey.current_position[0] + u_prey
        hg.prey.current_position[1] = hg.prey.current_position[1] + u_prey

print global_min