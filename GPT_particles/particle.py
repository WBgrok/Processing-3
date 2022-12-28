class Particle:
    particles = []
    
    @classmethod
    def run(cls):
        for p in cls.particles:
            p.update()
            p.display()
    
    def __init__(self, x, y, vx, vy, lifespan):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.lifespan = lifespan
        Particle.particles.append(self)
  
    def update(self):
        # update the position of the particle
        self.x += self.vx
        self.y += self.vy
        # reduce the lifespan of the particle
        self.lifespan -= 1
        if self.lifespan <=0 or self.x < 0 or self.x > width or self.y < 0 or self.y > height:
            # Outside bounds, delete
            Particle.particles.remove(self)
  
    def display(self):
        # draw the particle on the screen
        stroke(0, self.lifespan)
        strokeWeight(2)
        # stroke(255,0,0)
        point(self.x, self.y)
    
    def isDead(self):
        # check if the particle is still alive
        return self.lifespan < 0
