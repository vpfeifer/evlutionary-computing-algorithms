import matplotlib.pyplot as plt
import math

# Ant Colony Optimization Algorithm to find the smaller path

class City:
    name = ""
    x = 0.0
    y = 0.0

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y

class Edge:
    from_city = None
    to_city = None
    distance = 0.0

    def __init__(self, from_city, to_city):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = calculate_distance(from_city, to_city)

x_axis = []
y_axis = []

# Reads a file
def read_file():
    file = open('berlin_coordinates_only.tsp', 'r')
    cities = []
    for line in file:
        data = line.split(' ')
        city = City(data[0], float(data[1]), float(data[2]))
        x_axis.append(float(data[1]))
        y_axis.append(float(data[2]))
        cities.append(city)
    return cities

def calculate_distance(from_city, to_city):
    return math.sqrt((to_city.x - from_city.x) ** 2 + (to_city.y - from_city.y) ** 2)

cities = read_file()

print cities[0].x
print cities[0].y
print cities[1].x
print cities[1].y
print calculate_distance(cities[0], cities[1])

#plt.plot(x_axis, y_axis,'o')
#plt.show()