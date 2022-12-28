
def setup():
    size(800,800)


def draw():
    background(200)
    stroke(0)
    bezier(0, height, mouseX, mouseY, mouseX, mouseY, width, height)
