import matplotlib.pyplot as plt
import math
import random
import sys

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
    pheromone = 0.0
    pheromone_track_probability = 0.0
    heuristic_desire = 0.0
    transition_probability = 0.0

    def __init__(self, from_city, to_city, pheromone):
        self.from_city = from_city
        self.to_city = to_city
        self.distance = calculate_distance(from_city, to_city)
        self.pheromone = pheromone

class Ant:
    current_edge = None
    visited_cities = []
    solution_distance = 0.0

    def __init__(self, current_edge):
        self.current_edge = current_edge
    
    def put_pheromone(self, edge):
        edge.pheromone += Q/edge.distance
    
    def sniff(self, edge):
        return edge.pheromone

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

def create_graph():
    edges = []
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                edges.append(Edge(city1, city2, 0.1))
    return edges

def get_neighbors_set(edges_set, current_city, visited_cities):
    neighbors_set = []
    for e in edges_set:
       if e.from_city == current_city and e.to_city not in visited_cities:
           neighbors_set.append(e)
    return neighbors_set

def calculate_probabilities(edges_set):
    pheromone_sum = 0.0
    for e in edges_set:
        pheromone_sum += e.pheromone
    for e in edges_set:
        e.pheromone_track_probability = e.pheromone / pheromone_sum
        e.heuristic_desire = 1 / e.distance

def apply_transition_rule(edges_set):
    transition_probability_sum = sum((e.pheromone_track_probability ** alfa) * (e.heuristic_desire ** beta) for e in edges_set)
    selected_edge = Edge(City('none',0,0),City('none',0,0),0)
    for e in edges_set:
        e.transition_probability = (e.pheromone_track_probability ** alfa) * (e.heuristic_desire ** beta) / transition_probability_sum
        if e.transition_probability > selected_edge.transition_probability:
            selected_edge = e
    return selected_edge
        
def print_city(city):
    print "{ Name :", city.name,", x:",city.x,", y:", city.y," }"

def print_edges(edges):
    i = 0
    for e in edges:
        i+=1
        print "Edge", i
        print "\tFrom city:", print_city(e.from_city)
        print "\tTo city:", print_city(e.to_city)
        print "\tDistance:", e.distance
        print "\tPheromone:", e.pheromone
        print "\tPheromone track probability:", e.pheromone_track_probability
        print "\tHeuristic desire:", e.heuristic_desire
        print "\tTransition probability:", e.transition_probability

x_axis = []
y_axis = []

alfa = 1
beta = 5
peta = 0.5
Q = 100
b = 5

max_it = 1
best_solution = sys.maxint
amount_of_ants = 1

cities = read_file()
edges = create_graph()

# Put ants on random edges to start
ants = []
for j in range(0,amount_of_ants):
    edge_index = random.randint(0, len(edges) - 1)
    start_edge = edges[edge_index]
    ant = Ant(start_edge)
    ants.append(ant)    

for t in range(0, max_it):
    for ant in ants:
        print print_edges([ant.current_edge])
        for j in range(0,len(cities)):
            neighbors_set = get_neighbors_set(edges, ant.current_edge.to_city, ant.visited_cities)
            calculate_probabilities(neighbors_set)
            print "Length:", len(neighbors_set)
            selected_edge = apply_transition_rule(neighbors_set)
            #if selected_edge.from_city.name == 'none':
            #    for e in edges:
            #        if ant.visited_cities[0] == e.from_city and ant.visited_cities[len(ant.visited_cities)-1] == e.to_city:
            #            selected_edge = e
            print print_city(selected_edge.from_city)
            ant.visited_cities.append(selected_edge.from_city)
            ant.solution_distance += selected_edge.distance
            ant.current_edge = selected_edge

solution_x = []
solution_y = []

for city in ants[0].visited_cities:
    #print_city(city)
    solution_x.append(city.x)
    solution_y.append(city.y)

for ant in ants:
    if ant.solution_distance < best_solution:
        best_solution = ant.solution_distance

print "Best solution:", best_solution
plt.plot(x_axis, y_axis,'o')
plt.plot(solution_x, solution_y)
plt.show()