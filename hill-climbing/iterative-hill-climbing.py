import math
import random

print "\n Iterative Hill Climbing method to maximize g(x) = 2 ** (-2*((x-0.1)/0.9)**2) * (sin(5 * pi * x)) ** 6 \n"

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

def hillClimbing(maxit, x, evaluation):
    counter = 0
    while counter < maxit :
        x1 = disturb(x)
        evaluationx1 = evaluate(x1)
        if evaluationx1 > evaluation:
            x = x1
            evaluation = evaluationx1
        counter += 1;
    return [x, evaluation]

bestResult = 0
bestEvaluation = 0
executions = [0, 0.25, 0.75, 1]
max_it = 1000

for x in executions:
    print " Hill Climbing execution :", executions.index(x) + 1
    evaluation = evaluate(x)
    print "\t x =", x, " first evaluation result :",evaluation
    partial = hillClimbing(max_it, x, bestEvaluation)
    print "\t Execution result x = ", partial[0], " evaluation =", partial[1]
    if partial[1] > bestEvaluation :
        print "\t New best result!"
        bestResult = partial[0]
        bestEvaluation = partial[1]

print "\n Final result =",bestResult, "evaluated with",bestEvaluation