
v0 = 3
friction = 0.005
gravity = 0.1


class Particle():
    lst = []
    
    def __init__(self, x, y, lifespan = 255, vel = PVector(0,0)):
        self.pos = PVector(x,y)
        self.vel = vel
        self.lifespan = lifespan
        Particle.lst.append(self)
    
    def move(self):
        self.pos.add(self.vel)
        self.vel.mult(1 - friction)
        self.vel.y += gravity
        self.lifespan -= 1
        if self.lifespan <= 0 or self.pos.x < 0 or self. pos.y < 0 or self.pos.x > width or self.pos.y > height:
            Particle.lst.remove(self)
        
    def render(self):
        stroke(self.vel.heading() + PI, TWO_PI, TWO_PI)
        strokeWeight(2)
        point(self.pos.x, self.pos.y)


    

def keyPressed():
    for _ in range(50):
        Particle(mouseX, mouseY, 255, PVector(random(-v0, v0), random(-v0, v0)))

def setup():
    size(600,600)
    colorMode(HSB,TWO_PI)
    
    
def draw():
    # print(len(Particle.lst))
    # background(0)
    # Particle(mouseX, mouseY, 255, PVector(random(-v0, v0), random(-v0, v0)))
    for p in Particle.lst:
        p.move()
        p.render()
