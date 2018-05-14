import random
import math
import numpy as np
import matplotlib.pyplot as plt

# Perceptron to recognize types of iris flowers

# Data representation
# Bias, Sepal Length, Sepal Width, Petal Length, Petal Width, Type
# Where Type = 0 -> setosa
#              1 -> versicolor
#              2 -> virginica

training_flowers_factor = 0.8       # Percentage of dataset to be used for training
validate_flowers_factor = 0.1       # Percentage of dataset to be used for validation
test_flowers_factor = 0.1           # Percentage of dataset to be used for test

weights = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]  # Weights matrix
learning_rate = 0.5       # Learning rate
max_its = range(0,400)    # Max iterations

show_error_by_it = False
show_zero_error_chart = False
show_accuracy_chart = False

# Convert type to number
def convert_type_to_number(iris_type):
    if iris_type == 'Iris-setosa':
        return 0
    elif iris_type == 'Iris-versicolor':
        return 1
    elif iris_type == 'Iris-virginica':
        return 2
    else: 
        return 999

# Convert number to type
def convert_number_to_type(iris_number):
    if iris_number == 0:
        return 'Iris-setosa'
    elif iris_number == 1:
        return 'Iris-versicolor'
    elif iris_number == 2:
        return 'Iris-virginica'
    else: 
        return 'None'

def perceptron(flower, w):
    sum_array = []
    for wi in w:
        sum_in =  flower[0] * wi[0] # bias
        sum_in += flower[1] * wi[1] # sepal length
        sum_in += flower[2] * wi[2] # sepal width
        sum_in += flower[3] * wi[3] # petal length
        sum_in += flower[4] * wi[4] # petal width
        sum_array.append(sum_in)
    return sum_array.index(max(sum_array))

def train_perceptron(w, learning_rate):
    errors_array = []
    it = 0
    errors = 1                                                                               
    while it < len(max_its) and errors > 0:
        errors = 0
        for flower in training_set:
            expected = flower[5]
            result = perceptron(flower, w)
            if not result == expected:
                errors += 1
                for i in range(len(flower[:5])):
                    w[expected][i] += flower[:5][i] * learning_rate
                    w[result][i] -= flower[:5][i] * learning_rate
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
    for flower in run_set:
        result = perceptron(flower, w)
        if result == flower[5]:
            correct_answers += 1
    accuracy = round((correct_answers/float(len(run_set))) * 100,2)
    return accuracy
    
def validate(w):
    run_peceptron_for_set(w, validate_set)

def test(w):
    return run_peceptron_for_set(w, test_set)

# Reads the dataset file
def read_dataset_file():
    iris_data_file = open('iris.data', 'r')
    
    all_flowers = []
    for line in iris_data_file: 
        data = line.split(',')
        iris_number = convert_type_to_number(data[4].replace('\n',''))
        iris_flower = [1.0, float(data[0]), float(data[1]), float(data[2]), float(data[3]), iris_number]
        all_flowers.append(iris_flower)
    return all_flowers

# Gets the given amount of dataset elements randomly
def get_flowers_subset(all_flowers, amount):
    subset = []
    counter = 0
    while counter < amount:
        index = random.randint(0, len(all_flowers)-1)
        flower = all_flowers[index]
        subset.append(flower)
        all_flowers.remove(flower)
        counter += 1
    return subset

def get_fixed_sets():
    for i in range(0, len(flowers)):
        if i <= 40 or (i > 50 and i <= 90) or (i > 100 and i < 140):
            training_set.append(flowers[i])
        else:
            test_set.append(flowers[i])
    for j in range(0,30):
        index = random.randint(0, len(training_set)-1)
        validate_set.append(training_set[index])

iterations = range(0,100)
accuracy_array = []
zero_error_array = []

print "\nInitial weights", weights
print "Learning rate", learning_rate
print "Max training iterations", len(max_its)

for i in iterations:
    flowers = read_dataset_file()
    flowers_len = len(flowers)

    training_set_size = flowers_len * training_flowers_factor
    training_set = get_flowers_subset(flowers, training_set_size)

    validate_set_size = flowers_len * validate_flowers_factor
    validate_set = get_flowers_subset(flowers, validate_set_size)

    test_set_size = flowers_len * test_flowers_factor
    test_set = get_flowers_subset(flowers, test_set_size)
    
    weights = [[0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0]]

    train_perceptron(weights, learning_rate)
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

one_of_best_weights =  [[12.0, 26.35000000000002, 50.65000000000003, -63.60000000000008, -34.949999999999946], [72.5, -2.050000000000124, 32.550000000000594, -6.499999999999974, -67.45000000000081], [-84.5, -24.2999999999997, -83.19999999999892, 70.10000000000007, 102.40000000000131]]
print one_of_best_weights
wrongs = 0
for train_flower in training_set:
    result = perceptron(train_flower, one_of_best_weights)
    if not result == train_flower[5]:
        wrongs += 1

for validate_flower in validate_set:
    result = perceptron(validate_flower, one_of_best_weights)
    if not result == validate_flower[5]:
        wrongs += 1

for test_flower in test_set:
    result = perceptron(test_flower, one_of_best_weights)
    if not result == test_flower[5]:
        wrongs += 1

print "Total errors",wrongs
print "Accuracy", 100 - float(wrongs / 150.0) * 100