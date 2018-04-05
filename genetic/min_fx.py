import math
import random

print("Min of f(x) = x ** 2 - 4 * x + 4")

def evaluate(x) :
    return  x ** 2 - 4 * x + 4

def convertToDecimal(bits) :
    index = 0
    result = 0
    while index < 4 :
        bit = bits[index]
        result += bit * 2 ** index
        index += 1
    if bits[4] == 1 :
        result = result * -1
    return result

def getProportionRanges(evaluations) :
    sumEvaluations = sum(evaluations)
    degreesProp = [0,0,0,0]
    for e in evaluations:
        degrees = 360 * e / sumEvaluations
        pos = evaluations.index(e)
        degreesProp[pos] = degrees
    degreesProp.sort(reverse=True)
    ranges = []
    for d in degreesProp:
        x = 0
        
        ranges.append()

init = [[0,0,0,0,0], [1,1,1,1,1], [0,1,0,1,0], [1,0,1,0,1]]
evaluations = [0,0,0,0]

for i in init:
    print(i)
    decimalValue = convertToDecimal(i)
    evaluation = evaluate(decimalValue)
    position = init.index(i)
    print(evaluation)
    evaluations[position] = evaluation

print(evaluations)
getProportionRanges(evaluations)