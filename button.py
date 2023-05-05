class Button(object):
    # Buttons on screen
    def __init__(self, text, size, colour, y):
        self.text = text
        self.size = size
        self.colour = colour
        self.y = y
        self.toggle = False
