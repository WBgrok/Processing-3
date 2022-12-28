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

N_BOIDS = 100

flock = Flock()

def setup():
    size(800, 800)
    # Add an initial set of boids into the system
    for i in range(N_BOIDS):
        flock.addBoid(Boid(random(width),random(height)))
        # flock.addBoid(Boid((i*2), (i*2)))
        # flock.addBoid(Boid(width / 2, height / 2))


def draw():
    background(50)
    flock.run()

# Add a boid into the System
def mousePressed():
    flock.addBoid(Boid(mouseX, mouseY))
    
def keyPressed():
    if keyCode == UP:
        flock.sep_fac += 0.1
        print(flock.sep_fac)
    elif keyCode == DOWN:
        flock.sep_fac -= 0.1
        print(flock.sep_fac)
    elif keyCode == LEFT:
        flock.ali_fac -= 0.1
        print(flock.ali_fac)
    elif keyCode == RIGHT:
        flock.ali_fac += 0.1
        print(flock.ali_fac)
    elif keyCode == CONTROL:
        flock.coh_fac -= 0.1
        print(flock.coh_fac)
    elif keyCode == SHIFT:
        flock.coh_fac += 0.1
        print(flock.coh_fac)
        
        
