import math
import random

print "\n Stochastic Hill Climbing method to maximize g(x) = 2 ** (-2*((x-0.1)/0.9)**2) * (sin(5 * pi * x)) ** 6 \n"

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

    
x = 1
print " Initial parameter x =",x

evaluation = evaluate(x)
print " Evaluation result :",evaluation

max_it = 1000
print " Max number of executions :",max_it
print "\n"

counter = 0
while counter < max_it :
    print "\t Iteration ", counter + 1
    x1 = disturb(x)
    print "\t\t Disturbed x = x1 =", x1
    evaluationx1 = evaluate(x1)
    print "\t\t Disturbed evaluation =", evaluationx1
    randomNumber = random.random()
    print "\t\t Comparing random [0.0, 1.0) =",randomNumber
    accTestResult = acceptanceTest(evaluation, evaluationx1)
    print "\t\t with result of acceptance test =",accTestResult
    if randomNumber < accTestResult:
        print "\t\t x1 accepted"
        x = x1
        evaluation = evaluationx1
    counter += 1;

print "\n Result =",x, "evaluated with",evaluation