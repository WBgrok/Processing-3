# Particles
class Prtcl():
    # Class constants
    wall_repulsion = 1000
    part_repulsion = 100.0
    charge_effect = 100
    friction = 0.01
    vel_limit = 25
    
    
    lst = []
    max_energy = 1
    tot_mass = 0
    
    def __init__(self, x, y, radius, charge, vel0 = PVector(0,0)):
        self.pos = PVector(x,y)
        self.radius = radius # int/float
        self.mass = radius ** 2
        self.charge = charge # Float btw -1 and 1
        self.vel = vel0 # PVector
        self.acc = PVector(0,0)
        Prtcl.lst.append(self)
        Prtcl.tot_mass += self.mass

    def run(self):
        sumforce = PVector(0,0)
        x = self.pos.x
        y = self.pos.y
        
        #wall repulsion
        sumforce.add(PVector(1,0).mult(Prtcl.wall_repulsion / (x + EPSILON) ** 2 ))
        sumforce.add(PVector(-1,0).mult(Prtcl.wall_repulsion / (width - x + EPSILON) ** 2 ))
        sumforce.add(PVector(0,1).mult(Prtcl.wall_repulsion / (y + EPSILON) ** 2))
        sumforce.add(PVector(0,-1).mult(Prtcl.wall_repulsion / (height - y + EPSILON) ** 2 ))
        sumforce.mult(self.mass)                
        
        # Repulsion
        for other in [b for b in Prtcl.lst if b != self]:
            d = PVector.dist(self.pos, other.pos)
            force = PVector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
            # Close repulsion
            if d < 500:
                force.normalize()
                force.mult( Prtcl.part_repulsion * (self.mass + other.mass) / (d+EPSILON) ** 2)
                sumforce.add(force)
            # Charge interaction
            force.normalize()
            force.mult(Prtcl.charge_effect * self.charge * other.charge / (d+EPSILON))
            sumforce.add(force)
        
        

            
        
        
        self.move(sumforce)
        e = 0.5 * self.mass * self.vel.mag() ** 2
        self.render(e)
        # return energy
        return 0.5 * self.mass * self.vel.mag() ** 2
        
    def move(self, force = PVector(0,0)):
        self.acc = force.mult(1/self.mass)
        self.acc.add(self.vel.copy().mult(-Prtcl.friction))
        self.vel.add(self.acc)
        self.vel.limit(Prtcl.vel_limit)
        self.pos.add(self.vel)
        # self.vel.mult(1  - Prtcl.friction)
        
        # On Edge, bounce
        if self.pos.x < self.radius:
            # self.pos.x - self.radius 
            # self.vel.x *= -1
            self.pos.x = width
        elif width - self.radius < self.pos.x:
            # self.pos.x = width - self.radius
            # self.vel.x *= -1
            self.pos.x = 0
        if self.pos.y < self.radius:
            # self.pos.y = self.radius
            # self.vel.y *= -1
            self.pos.y = height
        elif height - self.radius < self.pos.y:
            # self.pos.y - height - self.radius
            # self.vel.y *= -1
            self.pos.y = 0
        
    def charge_to_colour(self):
        scaled = abs(self.charge) * 255
        if self.charge < 0:
            return(color(255-scaled, 255-scaled, 255))
        elif self.charge >= 0:
            return(color(255, 255-scaled, 255-scaled))
                        
    def render(self, energy):
        noStroke()
        fill(self.charge_to_colour())
        ellipse(self.pos.x, self.pos.y, self.radius, self.radius)
        
def mousePressed():
    Prtcl(mouseX, mouseY, random(3,10), 0, PVector(random(-1,1), random(-1,1)))
    
def keyPressed():
    Prtcl.lst.pop()


def setup():
    size(800, 800)
    ellipseMode(RADIUS)
    
def draw():
    background(127, 255, 127, 64)
    tot_e = 0
    Prtcl.max_energy = EPSILON
    avg_pos = PVector(0,0)
    for p in Prtcl.lst:
        avg_pos.add(p.pos.copy().mult(p.mass))
        e = p.run()
        tot_e =+ e
        if Prtcl.max_energy < e:
            Prtcl.max_energy = e
    avg_pos.mult(1 / ( EPSILON + Prtcl.tot_mass))

    stroke(255,0,0)
    noFill()
    circle(avg_pos.x, avg_pos.y, .5 +(tot_e / 100))
    # print(Prtcl.tot_mass)
    # print(avg_pos.x, avg_pos.y)
    # print("System Energy: " + str(tot_e))
