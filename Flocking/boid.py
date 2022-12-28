# The Boid class
class Boid(object):

    def __init__(self, x, y):
        self.acceleration = PVector(0, 0)
        self.acc = PVector(0,0)
        angle = random(TWO_PI)
        self.velocity = PVector(cos(angle), sin(angle))
        self.location = PVector(x, y)
        self.r = 5.0
        self.maxspeed = 3
        self.maxforce = 0.05
        self.sep_factor = random(1.25, 1.75)
        self.ali_factor = random(0.3, 1.1)
        self.coh_factor = random(0.9, 1.1)

    def run(self, boids, mousePressed):
        self.flock(boids, mousePressed)
        self.update()
        self.borders()
        self.render()

    def applyForce(self, force):
        # We could add mass here if we want A = F / M
        self.acceleration.add(force)

    # We accumulate acceleration each time based on three rules.
    def flock(self, boids, mousePressed):
        self.sep = self.separate(boids)  # Separation
        self.ali = self.align(boids)  # Alignment
        self.coh = self.cohesion(boids, mousePressed)  # Cohesion
        # Arbitrarily weight these forces.
        self.sep.mult(self.sep_factor)
        self.ali.mult(self.ali_factor)
        self.coh.mult(self.coh_factor)
        # Add the force vectors to acceleration.
        self.applyForce(self.sep)
        self.applyForce(self.ali)
        self.applyForce(self.coh)

    # Method to update location.
    def update(self):
        # Update velocity.
        self.acc = self.acceleration.copy()
        self.velocity.add(self.acceleration)
        # Limit speed.
        self.velocity.limit(self.maxspeed)
        self.location.add(self.velocity)
        # Reset accelertion to 0 each cycle.
        self.acceleration.mult(0)

    # A method that calculates and applies a steering force towards a target.
    # STEER = DESIRED MINUS VELOCITY
    def seek(self, target):
        # A vector pointing from the location to the target.
        desired = PVector.sub(target, self.location)
        # Scale to maximum speed.
        desired.normalize()
        desired.mult(self.maxspeed)
        # Above two lines of code below could be condensed with PVector setMag() method.
        # Not using this method until Processing.js catches up.
        # desired.setMag(maxspeed)
        # Steering = Desired minus Velocity
        steer = PVector.sub(desired, self.velocity)
        steer.limit(self.maxforce)  # Limit to maximum steering force.
        return steer

    def render(self):
        # Draw a triangle rotated in the direction of velocity.
        theta = self.velocity.heading2D() + radians(90)
        # heading2D() above is now heading() but leaving old syntax until
        # Processing.js catches up.

        # Render colour based on sep,ali,coh
        
        fill(
            255 * (self.sep.mag() / self.maxforce),
            255 * (self.ali.mag() / self.maxforce),
            255 * (self.coh.mag() / self.maxforce),
        )

        # Render colour based on sep, ali, coh FACTORS
        stroke(
            255 * ((self.sep_factor - 1.25) / 0.5),
            255 * ((self.ali_factor - 0.9) / 0.2),
            255 * ((self.coh_factor - 0.9) / 0.2),
        )
        strokeWeight(2)
        with pushMatrix():
            translate(self.location.x, self.location.y)
            rotate(theta)
            with beginShape(TRIANGLES):
                vertex(0, -self.r * 2)
                vertex(-self.r, self.r * 2)
                vertex(self.r, self.r * 2)

    # Wraparound
    def borders(self):
        if self.location.x < -self.r:
            self.location.x = width + self.r
        if self.location.y < -self.r:
            self.location.y = height + self.r
        if self.location.x > width + self.r:
            self.location.x = -self.r
        if self.location.y > height + self.r:
            self.location.y = -self.r

    # Separation
    # Method checks for nearby boids and steers away.
    def separate(self, boids):
        desiredseparation = 60.0
        steer = PVector(0, 0, 0)
        count = 0
        # For every boid in the system, check if it's too close.
        for other in boids:
            d = PVector.dist(self.location, other.location)
            # If the distance is greater than 0 and less than an arbitrary
            # amount (0 when you are yourself).
            if 0 < d < desiredseparation:
                # Calculate vector pointing away from neighbor.
                diff = PVector.sub(self.location, other.location)
                diff.normalize()
                diff.div(d)  # Weight by distance.
                steer.add(diff)
                count += 1  # Keep track of how many
        # Average -- divide by how many
        if count == 0:
            return PVector(0, 0)
        if count > 0:
            steer.div(float(count))
        # As long as the vector is greater than 0
        if steer.mag() > 0:
            # First two lines of code below could be condensed with PVector setMag() method.
            # Implement Reynolds: Steering = Desired - Velocity
            steer.normalize()
            steer.mult(self.maxspeed)
            steer.sub(self.velocity)
            steer.limit(self.maxforce)
        return steer

    # Alignment
    # For every nearby boid in the system, calculate the average velocity.
    def align(self, boids):
        neighbordist = 100
        sum = PVector(0, 0)
        count = 0
        for other in boids:
            d = PVector.dist(self.location, other.location)
            if 0 < d < neighbordist:
                sum.add(other.velocity)
                count += 1
        if count == 0:
            return PVector(0, 0)
        sum.div(float(count))
        # First two lines of code below could be condensed with PVector setMag() method.
        # Implement Reynolds: Steering = Desired - Velocity
        sum.normalize()
        sum.mult(self.maxspeed)
        steer = PVector.sub(sum, self.velocity)
        steer.limit(self.maxforce)
        return steer

    # Cohesion
    # For the average location (i.e. center) of all nearby boids, calculate
    # steering vector towards that location.
    def cohesion(self, boids, mousePressed):
        neighbordist = 100
        # Start with empty vector to accumulate all locations.
        sum = PVector(0, 0)
        count = 0
        if mousePressed:
            return self.seek(PVector(mouseX, mouseY))
        else:
            for other in boids:
                d = PVector.dist(self.location, other.location)
                if 0 < d < neighbordist:
                    sum.add(other.location)  # Add location.
                    count += 1
            if count > 0:
                sum.div(count)
                return self.seek(sum)  # Steer towards the location.
            else:
                return PVector(0, 0)
