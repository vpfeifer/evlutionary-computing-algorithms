# Lion Hunting Optimization Algorithm (LHOA)
import random

_hunting_groups = 1          # Amount of hunting groups
_hunters_by_group = 3        # Amount of hunters in each hunting group
_dimensions = 2              # Amount of problem dimensions

class Lion:
    current_position = []
    best_position = []

    def __init__(self, current_position, best_position):
        self.current_position = current_position
        self.best_position = best_position

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

# Initialize hunting groups
hunting_groups = []
for i in range(0,_hunting_groups):
    # Add some lions to the hunting group
    group_lions = []
    group_x = 0
    group_y = 0
    for j in range(0, _hunters_by_group):
        position = [random.randint(-5,5), random.randint(-5,5)]
        lion = Lion(position, position)
        group_x += position[0]
        group_y += position[1]
        group_lions.append(lion)
    # Add the hunting group prey
    prey_position = [group_x/_hunters_by_group, group_y/_hunters_by_group]
    prey = Prey(prey_position)
    hunting_groups.append(HuntingGroup(group_lions, prey))