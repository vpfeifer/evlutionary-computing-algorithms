import random

class IrisFlower(object):
    sepal_length = 0
    sepal_width = 0
    petal_length = 0
    petal_width = 0
    name = "none"

    def __init__(self, sepal_length, sepal_width, petal_length, petal_width, name):
        self.sepal_length = sepal_length
        self.sepal_width = sepal_width
        self.petal_length = petal_length
        self.petal_width = petal_width
        self.name = name

def print_flower(flower):
    print "Iris Flower"
    print "Sepal length:", flower.sepal_length
    print "Sepal width:", flower.sepal_width
    print "Petal length:", flower.petal_length
    print "Petal width:", flower.petal_width
    print "Type:", flower.name

def get_flowers_subset(all_flowers, factor):
    subset = []
    all_flowers_len = len(all_flowers)
    counter = 0
    while counter < all_flowers_len * factor:
        index = random.randint(0, all_flowers_len-1)
        subset.append(all_flowers[index])
        counter += 1
    return subset

iris_data_file = open('iris.data', 'r')

all_flowers = []
for line in iris_data_file: 
    data = line.split(',')
    iris_flower = IrisFlower(data[0], data[1], data[2], data[3], data[4])
    all_flowers.append(iris_flower)

training_flowers_factor = 0.8
validate_flowers_factor = 0.1
test_flowers_factor = 0.1

training_set = get_flowers_subset(all_flowers, training_flowers_factor)

print len(training_set)