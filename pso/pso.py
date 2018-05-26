import matplotlib.pyplot as plt
import numpy as np
import random
import sys

class Particle:
    current_position = [0,0]
    current_velocity = 0
    best_fit = 0
    best_fit_position = [0,0]
    neighborhood = []

    def __init__(self, current_position, current_velocity, best_fit, best_fit_position, neighborhood):
        self.current_position = current_position
        self.current_velocity = current_velocity
        self.best_fit_position = best_fit_position
        self.best_fit = best_fit
        self.neighborhood = neighborhood

def update_velocity(p, best_neighbor):
    ac1 = 2.05
    ac2 = 2.05
    phi1 = np.random.uniform(0.0, ac1, 2)
    phi2 = np.random.uniform(0.0, ac2, 2)
    v_result = p.current_velocity + np.dot(phi1, np.subtract(p.best_fit_position, p.current_position)) + np.dot(phi2, np.subtract(best_neighbor.current_position, p.current_position))
    if v_result > vmax:
        return vmax
    if v_result < vmin:
        return vmin
    return v_result

def update_position(p):
    return [p.current_position[0] + p.current_velocity, p.current_position[1] + p.current_velocity]

def f(x, y):
    return (1 - x) ** 2 + 100 * (y - x ** 2) ** 2

def define_particles_neighborhood(particles):
    p_len = len(particles)
    if p_len == 2:
        particles[0].neighborhood = [particles[1]]
        particles[1].neighborhood = [particles[0]]
    else:
        for i in range(0, p_len):
            if i == 0:
                particles[i].neighborhood = [particles[i + 1], particles[p_len - 1]]
            elif i == p_len - 1:
                particles[i].neighborhood = [particles[0], particles[i - 1]]
            else:
                particles[i].neighborhood = [particles[i + 1], particles[i - 1]]

def init_particles(n):
    particles = []
    for i in range(0,n):
        current_position = [random.randint(-5,5),random.randint(-5,5)]
        current_velocity = random.randint(vmin, vmax)
        best_fit = f(current_position[0], current_position[1])
        p = Particle(current_position, current_velocity, best_fit, current_position, [])
        particles.append(p)
    define_particles_neighborhood(particles)
    return particles

def print_particles(particles, is_neighborhood_print=False):
    tab = ""
    if is_neighborhood_print: tab = "\t"
    for p in particles:
        print tab, "PARTICLE"
        print tab, "Current position", p.current_position
        print tab, "Current velocity", p.current_velocity
        print tab, "Best fit", p.best_fit
        print tab, "Best fit position", p.best_fit_position
        if len(p.neighborhood) > 0 and not is_neighborhood_print:
            print tab,"Neighbors :\n",print_particles(p.neighborhood, True)

def get_best_fits_array(particles):
    best_fits = []
    for p in particles:
        best_fits.append(p.best_fit)
    return best_fits

max_it = 50
vmax = 10
vmin = -10

particles = init_particles(3)
print_particles(particles)

iterations = range(0,max_it)
fit_avgs = []
fit_mins = []

for it in iterations:
    for p in particles:
        current_fit = f(p.current_position[0], p.current_position[1])
        if  current_fit < p.best_fit:
            p.best_fit_position = p.current_position
            p.best_fit = current_fit
        neighborhood_fit = sys.maxint
        for n in p.neighborhood:
            neighbor_fit = f(n.current_position[0], n.current_position[1])
            if neighbor_fit < neighborhood_fit:
                neighborhood_fit = neighbor_fit
                best_neighbor = n
        p.current_velocity = update_velocity(p, best_neighbor)
        p.current_position = update_position(p)
        fits_array = get_best_fits_array(particles)
    fit_avgs.append(np.average(fits_array))
    fit_mins.append(min(fits_array))

print "======= RESULT ======"
best_fits = get_best_fits_array(particles)
print "The best min was", min(best_fits)

plt.plot(iterations, fit_avgs, fit_mins)
plt.show()   