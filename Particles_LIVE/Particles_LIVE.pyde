
def get_color(val):
    # Clamp val between -1 and 1
    val = max(-1, min(val, 1))
    
    # Convert val to a value between 0 and 510
    val = (val + 1) * 255
    
    # Calculate the red, green, and blue values
    red = 255 if val > 255 else int(val)
    green = 255 if val < 255 else int(510 - val)
    blue = 0
    
    return color(red, green, blue)

class Prtcl():
    friction = 0.005
    wbl = 0.1 # Wall Bounce Loss
    prtcls = []
    prf = 10 # Particle Repulstion Factor
    cf = 3000 # Charge factor
    max_vel = EPSILON
    tot_mass = 0
    
    def __init__(self, x, y, radius, vel=PVector(0,0)):
        self.pos = PVector(x, y)
        self.radius = radius
        self.mass = radius ** 2
        self.charge = random(-1,1)
        self.vel = vel
        self.acc = PVector(0,0)
        Prtcl.prtcls.append(self)
        Prtcl.tot_mass += self.mass

    def move(self, f=PVector(0,0)):

        for other in [p for p in Prtcl.prtcls if p != self]:
            dist = PVector.dist(self.pos, other.pos)
            # Levity (reverse gravity)
            if dist < 200:
                v = PVector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
                v.normalize()
                v.mult(Prtcl.prf * self.mass * other.mass / (dist + EPSILON) ** 2)
                f.add(v)
            # Charge interactions
                v = PVector(self.pos.x - other.pos.x, self.pos.y - other.pos.y)
                v.normalize()
                v.mult(Prtcl.cf * self.charge * other.charge / (dist + EPSILON) ** 2)
                f.add(v)
        
        self.acc = f.div(self.mass)
        self.vel.add(self.acc)
        self.pos.add(self.vel)
        self.vel.mult(1 - Prtcl.friction)
        if Prtcl.max_vel < self.vel.mag():
            Prtcl.max_vel = self.vel.mag()
        
        if self.pos.x < self.radius:
            self.vel.x *= -(1 - Prtcl.wbl)
            self.pos.x = self.radius + 1 
        elif self.pos.x + self.radius > width:
            self.vel.x *= -(1 - Prtcl.wbl)
            self.pos.x = width - self.radius - 1
        if self.pos.y < self.radius:
            self.vel.y *= -(1 - Prtcl.wbl)
            self.pos.y = self.radius + 1
        elif self.pos.y + self.radius > height:
            self.vel.y *= -(1 - Prtcl.wbl)
            self.pos.y = height - self.radius - 1
            
    def render(self):
        noStroke()
        fill(get_color(self.charge))
        circle(self.pos.x, self.pos.y, self.radius)


def mousePressed():
    Prtcl(mouseX, mouseY, random(2,7), PVector(random(-3,3), random (-1,1)))

def setup():
    size(800, 800)
    ellipseMode(RADIUS)
    
def draw():
    background(200)
    
    gravity = PVector(0, 0.1)
    avg_pos = PVector(0,0)
    Prtcl.max_vel = EPSILON 
    for p in Prtcl.prtcls:
        p.move(gravity)
        avg_pos.add(p.pos.copy().mult(p.mass))
    for p in Prtcl.prtcls:
        p.render()
        
    if len(Prtcl.prtcls) > 0:
        avg_pos.div(Prtcl.tot_mass)
    noFill()
    stroke(255,0,0)
    circle(avg_pos.x, avg_pos.y,1)
