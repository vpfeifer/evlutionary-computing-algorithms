import matplotlib.pyplot as plt
import math
import random
import sys

# Ant Colony Optimization Algorithm to find the smaller path
alfa = 1
beta = 5
peta = 0.5
Q = 100
b = 5

max_it = 10
best_solution = sys.maxint
best_solution_path = []
best_solution_index = 0
amount_of_ants = 52

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
    name = "none"
    current_edge = None
    visited_cities = []
    solution_distance = 0.0
    visited_edges = []

    def __init__(self, name, current_edge, visited_cities, visited_edges, solution_distance):
        self.name = name
        self.current_edge = current_edge
        self.visited_cities = visited_cities
        self.visited_edges = visited_edges
        self.solution_distance = solution_distance
    
    def put_pheromone(self,edge):
        return Q/edge.distance

# Reads a file
def read_file():
    file = open('berlin_coordinates_only.tsp', 'r')
    cities = []
    for line in file:
        data = line.split(' ')
        city = City(data[0], float(data[1]), float(data[2]))
        cities_x.append(float(data[1]))
        cities_y.append(float(data[2]))
        cities.append(city)
    return cities

def calculate_distance(from_city, to_city):
    return math.sqrt((to_city.x - from_city.x) ** 2 + (to_city.y - from_city.y) ** 2)

def create_graph():
    edges = []
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                edges.append(Edge(city1, city2, 10 ** -6))
    return edges

def get_neighbors_set(edges_set, current_city, visited_cities):
    neighbors_set = []
    for e in edges_set:
        if e.from_city.name == current_city.name and e.to_city not in visited_cities:
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

def update_edges_pheromone_track(edges):
    for e in edges:
        pheromone_sum = 0
        for k in range(0,len(ants)):
            ak = ants[k]
            if e in ant.visited_edges:
                pheromone_sum += ak.put_pheromone(e)
                if k == best_solution_index:
                    e.pheromone += b * ak.put_pheromone(e)
        e.pheromone = (1 - peta) * e.pheromone + pheromone_sum

cities_x = []
cities_y = []
cities = read_file()
edges = create_graph()

# Put ants on random edges to start
ants = []
for j in range(0,amount_of_ants):
    edge_index = random.randint(0, len(edges) - 1)
    start_edge = edges[edge_index]
    ant = Ant(j, start_edge, [], [], 0)
    ants.append(ant)    

for t in range(0, max_it):
    # apply the transition rule for each ant
    for ant in ants:
        ant.visited_cities.append(ant.current_edge.from_city)
        for j in range(0,len(cities)-1):
            if len(ant.visited_cities) == 51:
                ant.visited_cities.append(ant.current_edge.to_city)
                for e in edges:
                    if ant.visited_cities[0] == e.to_city and ant.visited_cities[len(ant.visited_cities)-1] == e.from_city:
                        selected_edge = e
                ant.visited_cities.append(selected_edge.to_city)
            else:
                neighbors_set = get_neighbors_set(edges, ant.current_edge.to_city, ant.visited_cities)
                calculate_probabilities(neighbors_set)
                selected_edge = apply_transition_rule(neighbors_set)
                ant.visited_cities.append(selected_edge.from_city)
            ant.solution_distance += selected_edge.distance
            ant.current_edge = selected_edge
            ant.visited_edges.append(selected_edge)
    #update best solution
    for ant in ants:
        if ant.solution_distance < best_solution:
            print "New best solution :", ant.solution_distance
            best_solution_index = ants.index(ant)
            best_solution_path = ant.visited_cities
            best_solution = ant.solution_distance
    update_edges_pheromone_track(edges)
    for ant in ants:
        ant.current_edge = ant.visited_edges[0]
        ant.visited_cities = []
        ant.visited_edges = []
        ant.solution_distance = 0
             
solution_x = []
solution_y = []

for city in best_solution_path:
    solution_x.append(city.x)
    solution_y.append(city.y)

print len(solution_x)

print "Best solution:", best_solution
plt.plot(cities_x, cities_y,'o')
plt.plot(solution_x, solution_y)
plt.show()