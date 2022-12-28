"""
    Balls 
"""

class Ball():
    max_force = 0.5
    vel_limit = 50
    scale = 0.01
    spring = 0.0001
    friction = 0.001
    balls = []

    part_repulsion = 100
    wall_repulsion = 500
    
    
    def __init__(self, x, y, mass, vel0 = PVector(0, 0)):
        self.pos = PVector(x,y)
        self.mass = mass # float
        self.radius = int(sqrt(mass))
        self.vel = vel0 # PVector
        self.acc = PVector(0,0)
        Ball.balls.append(self)
    
    def move(self, force = PVector(0, 0)):
        # Apply force and integrate
        self.acc = force.mult(1/self.mass)
        self.vel.add(self.acc)
        # self.vel.limit(Ball.vel_limit)
        self.pos.add(self.vel)
        
        # On Edge, bounce
        if self.pos.x < self.radius:
            self.pos.x - self.radius 
            self.vel.x *= -1
        elif width - self.radius < self.pos.x:
            self.pos.x = width - self.radius
            self.vel.x *= -1
        
        if self.pos.y < self.radius:
            self.pos.y = self.radius
            self.vel.x *= -1
        elif height - self.radius < self.pos.y:
            self.pos.y - height - self.radius
            self.vel.y *= -1
            
        #Friction
        self.vel.mult(1 - Ball.friction)
        

        
    def render(self):
        
        fill(255 * sqrt((self.acc.mag() / self.mass) / Ball.max_force))
        ellipse(self.pos.x, self.pos.y, self.radius, self.radius)
        
        
    def run(self):
        sumforce = PVector(0,0)
        x = self.pos.x
        y = self.pos.y
        
        # left, right, top, bottom
        # sumforce.add(PVector(1,0).mult(Ball.wall_repulsion / x ))
        # sumforce.add(PVector(-1,0).mult(Ball.wall_repulsion / (width - x) ))
        # sumforce.add(PVector(0,1).mult(Ball.wall_repulsion / y ))
        # sumforce.add(PVector(0,-1).mult(Ball.wall_repulsion / (height - y) ))
        # sumforce.mult(self.mass)
        # print(sumforce)
        
        # Repulsion
        # for other in [b for b in Ball.balls if b != self]:
        #     d = PVector.dist(self.pos, other.pos)
        #     if d < 2000:
        #         force = PVector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
        #         force.normalize()
        #         force.mult( Ball.part_repulsion * (self.mass + other.mass) / d)
        #         sumforce.add(force)
           
            
             

        # # Gravity
        # for other in [b for b in Ball.balls if b != self]:
        #     d = PVector.dist(self.pos, other.pos)
        #     # if 0 < d < self. radius * 10:
        #     force = PVector.sub(other.pos, self.pos)
        #     force.normalize()
        #     force.mult(Ball.scale * (self.mass + other.mass) / d)
        #     sumforce.add(force)
        
        self.move(sumforce)
        # self.render()

def mousePressed():
    # Ball(mouseX, mouseY, random(10,50), PVector(random(-10, 10), random(-10, 10)))
    Ball(mouseX, mouseY, random(10,50))
def keyPressed():
    Ball.balls.pop()

def setup():
    size(800, 600)
    noStroke()
    ellipseMode(RADIUS)
    
def draw():
    background(127, 127, 255)

    for b in Ball.balls:
        b.run()
        b.render()
