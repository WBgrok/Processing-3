# import the Particle class
from particle import Particle

# create a list to store the particles
particles = []

N = 10
def setup():
    size(800, 800)
  
  
def draw():
    background(255)
    # create N new particle every frame
    for _ in range(N):
        particles.append(Particle(mouseX, mouseY, random(-2, 2), random(-2, 2), 255))
    # update and display all the particles
    Particle.run()
    
def keyPressed():
    global N
    if keyCode == UP:
        N +=1
    if keyCode == DOWN:
        N -= 1
    print(N)
