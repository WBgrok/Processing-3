class Victor:
    def __init__(self, vel, acc):
        self.vel = vel
        self.acc = acc
        
    def render(self):
        with pushMatrix():
            translate(width / 2, height / 2)
            rotate(self.vel.heading2D()+ + radians(90))
            fill(0)
            stroke(200)
            with beginShape(TRIANGLES):
                vertex(0, -10 * 2)
                vertex(-10, 10 * 2)
                vertex(10, 10 * 2)
            rotate(self.acc.heading2D()+ radians(90))
            noFill()
            stroke(255)
            with beginShape(TRIANGLES):
                vertex(0, -5 * 2)
                vertex(-5, 5 * 2)
                vertex(5, 5 * 2)





# The Flock (a list of Boid objects)
class Flock(object):

    def __init__(self):
        self.boids = []  # Initialize a list for all the boids.

    def run(self, mousePressed):

        av_acc = PVector()
        av_vel = PVector()
        for b in self.boids:
            # Pass the entire list of boids to each boid individually.
            b.run(self.boids, mousePressed)

            av_acc += b.acc
            av_vel += b.velocity
        
        # We don't need to scale as we initially want the angle
        # av_acc /= len(self.boids)
        # av_vel /= len(self.boids)
        vec = Victor(av_vel, av_acc)
        vec.render()

    def addBoid(self, b):
        self.boids.append(b)
