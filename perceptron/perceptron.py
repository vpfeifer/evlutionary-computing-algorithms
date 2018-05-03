import random

# Perceptron to recognize types of iris flowers

training_flowers_factor = 0.8       # Percentage of dataset to be used for training
validate_flowers_factor = 0.1       # Percentage of dataset to be used for validation
test_flowers_factor = 0.1           # Percentage of dataset to be used for test

# Class to represent the flower
class IrisFlower(object):
    sepal_length = 0.0
    sepal_width = 0.0
    petal_length = 0.0
    petal_width = 0.0
    name = "none"

    def __init__(self, sepal_length, sepal_width, petal_length, petal_width, name):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.name = name

# Print a flower on console
def print_flower(flower):
    print "Sepal length:", flower.sepal_length
    print "Sepal width:", flower.sepal_width
    print "Petal length:", flower.petal_length
    print "Petal width:", flower.petal_width
    print "Type:", flower.name

# Reads the dataset file
def read_dataset_file():
    iris_data_file = open('iris.data', 'r')
    
    all_flowers = []
    for line in iris_data_file: 
        data = line.split(',')
        iris_flower = IrisFlower(float(data[0]), float(data[1]), float(data[2]), float(data[3]), data[4])
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

flowers = read_dataset_file()
flowers_len = len(flowers)

training_set_size = flowers_len * training_flowers_factor
training_set = get_flowers_subset(flowers, training_set_size)

validate_set_size = flowers_len * validate_flowers_factor
validate_set = get_flowers_subset(flowers, validate_set_size)

test_set_size = flowers_len * test_flowers_factor
test_set = get_flowers_subset(flowers, test_set_size)


def perceptron(flower, w, b):
    print "Received flower \n", print_flower(flower)
    print w
    print b
    y = 0
    for ws in w:
        sum_in = 0.0
        sum_in =  flower.sepal_length * ws[0] 
        sum_in += flower.sepal_width  * ws[1]
        sum_in += flower.petal_length * ws[2]
        sum_in += flower.petal_width  * ws[3]
        sum_in += b
        print "n", y, "outs", sum_in
        y+=1

def train_perceptron():
    w = [[0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]    # Weights matrix
    b = 0.0                                                                   # Bias
    max_it = 1000                                                             # Max iterations
    it = 0                                                                    # Current iteration
    error = 1                                                                 # Calculated error

    while it < max_it and error > 0:
        error = 0
        for flower in training_set:
            perceptron(flower, w, b)
        it += 1

train_perceptron()