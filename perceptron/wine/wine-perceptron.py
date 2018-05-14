import random
import math
import numpy as np
import matplotlib.pyplot as plt

training_set_size = 150       # Percentage of dataset to be used for training
validate_set_size = 14       # Percentage of dataset to be used for validation
test_set_size = 14           # Percentage of dataset to be used for test

weights = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]  # Weights matrix
learning_rate = 0.5         # Learning rate
max_its = range(0,2000)    # Max iterations

show_error_by_it = False
show_zero_error_chart = False
show_accuracy_chart = True

# Reads the dataset file
def read_dataset_file():
    iris_data_file = open('wine.data', 'r')
    
    wines = []
    for line in iris_data_file: 
        data = line.split(',')
        wine = []
        for d in data:
            if data.index(d) == 0:
                wine.append(int(d))
            else:
                wine.append(float(d))
        wine.append(1.0) # bias
        wines.append(wine)
    return wines

# Gets the given amount of dataset elements randomly
def get_subset(wines, amount):
    subset = []
    counter = 0
    while counter < amount:
        index = random.randint(0, len(wines)-1)
        flower = wines[index]
        subset.append(flower)
        wines.remove(flower)
        counter += 1
    return subset

def perceptron(wine, w):
    sum_array = []
    for wi in w:
        sum_in =  wine[1]  *  wi[0]  # Alcohol
        sum_in += wine[2]  *  wi[1]  # Malic acid
        sum_in += wine[3]  *  wi[2]  # Ash
        sum_in += wine[4]  *  wi[3]  # Alcalinity of ash 
        sum_in += wine[5]  *  wi[4]  # Magnesium
        sum_in += wine[6]  *  wi[5]  # Total phenols
        sum_in += wine[7]  *  wi[6]  # Flavanoids
        sum_in += wine[8]  *  wi[7]  # Nonflavanoid phenols
        sum_in += wine[9]  *  wi[8]  # Proanthocyanins
        sum_in += wine[10] *  wi[9]  # Color intensity
        sum_in += wine[11] *  wi[10] # Hue
        sum_in += wine[12] *  wi[11] # OD280/OD315 of diluted wines
        sum_in += wine[13] *  wi[12] # Proline
        sum_in += wine[14] *  wi[13] # Bias
        sum_array.append(sum_in)
    return sum_array.index(max(sum_array)) + 1

def train(w, learning_rate):
    errors_array = []
    it = 0
    errors = 1                                                                               
    while it < len(max_its) and errors > 0:
        errors = 0
        for wine in training_set:
            expected = wine[0]
            result = perceptron(wine, w)
            if not result == expected:
                errors += 1
                for i in range(len(wine[1:])):
                    w[expected - 1][i] += wine[1:][i] * learning_rate
                    w[result - 1][i] -= wine[1:][i] * learning_rate
        errors_array.append(errors)
        zero_error_it = 0
        if errors == 0:
            zero_error_it = it
        it += 1
    zero_error_array.append(zero_error_it)
    if show_error_by_it:
        print errors_array
        plt.plot(range(len(errors_array)), errors_array)
        plt.ylabel('number of errors')
        plt.xlabel('iteration')
        plt.show()

def run_peceptron_for_set(w, run_set):
    correct_answers = 0 
    for wine in run_set:
        result = perceptron(wine, w)
        if result == wine[0]:
            correct_answers += 1
    accuracy = round((correct_answers/float(len(run_set))) * 100,2)
    return accuracy

def validate(w):
    run_peceptron_for_set(w, validate_set)

def test(w):
    return run_peceptron_for_set(w, test_set)

iterations = range(0,100)
accuracy_array = []
zero_error_array = []

print "\nInitial weights", weights
print "Learning rate", learning_rate
print "Max training iterations", len(max_its)

for i in iterations:
    wines = read_dataset_file()
    wines_len = len(wines)

    training_set = get_subset(wines, training_set_size)
    validate_set = get_subset(wines, validate_set_size)
    test_set = get_subset(wines, test_set_size)
    
    weights = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]

    train(weights, learning_rate)
    validate(weights)
    accuracy = test(weights)
    accuracy_array.append(accuracy)

if show_zero_error_chart:
    print zero_error_array
    plt.plot(iterations, zero_error_array)
    plt.ylabel('Zero error iteration')
    plt.show()

if show_accuracy_chart:
    print "\nAccuracy average", np.average(accuracy_array)

    plt.plot(iterations, accuracy_array)
    plt.ylabel('accuracy')
    plt.show()