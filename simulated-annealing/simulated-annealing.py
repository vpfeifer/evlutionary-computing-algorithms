import random
import math

print "\n Simulated Annealing to maximize g(x) = 2 ** (-2*((x-0.1)/0.9)**2) * (sin(5 * pi * x)) ** 6 \n"

def evaluate(x):
    return 2 ** (-2 * ((x-0.1)/0.9) ** 2) * (math.sin(5 * math.pi * x)) ** 6

def disturb(x):
    disturbed = x + random.gauss(0, 0.01)
    while disturbed <= 0 or disturbed >= 1:
        disturbed = x + random.gauss(0, 0.1)
    return disturbed

def acceptanceTest(evaluationx, evaluationx1):
    t = 0.1
    return 1 / math.exp((evaluationx - evaluationx1)/t)

temperature = 0
x = 0
evaluation = evaluate(x)

counter = 0
max_it = 100

while counter < max_it:
    x1 = disturb(x)
    evaluationx1 = evaluate(x1)
    if evaluationx1 > evaluation:
        x = x1
        evaluationx = evaluationx1
    elif random.random() < acceptanceTest(evaluationx, evaluationx1):
        x = x1
        evaluationx = evaluationx1
    
        