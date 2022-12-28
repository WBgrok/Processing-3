"""
Flocking 
by Daniel Shiffman.    

An implementation of Craig Reynold's Boids program to simulate
the flocking behavior of birds. Each boid steers itself based on 
rules of avoidance, alignment, and coherence.

Click the mouse to add a boid.
"""

from boid import Boid
from flock import Flock

N_BOIDS = 80

flock = Flock()

def setup():
    size(1000, 1000)
    # Add an initial set of boids into the system
    for i in range(N_BOIDS):
        # flock.addBoid(Boid(random(width), random(height)))
        flock.addBoid(Boid(width / 2, height / 2))


def draw():
    background(50)
    flock.run(mousePressed)

# Add a boid into the System
def mousePressed():
    flock.addBoid(Boid(mouseX, mouseY))
