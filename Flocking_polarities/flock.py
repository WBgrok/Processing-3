# The Flock (a list of Boid objects)
class Flock(object):

    def __init__(self):
        self.boids = []  # Initialize a list for all the boids.
        self.sep_fac = 1.5
        self.ali_fac = 1.0
        self.coh_fac = 1.0

    def run(self):
        for b in self.boids:
            # Pass the entire list of boids to each boid individually.
            b.run(self.boids, self.sep_fac, self.ali_fac, self.coh_fac)

    def addBoid(self, b):
        self.boids.append(b)
