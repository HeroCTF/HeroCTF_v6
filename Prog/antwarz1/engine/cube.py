from engine.utils import Position

class Cube:
    def __init__(self, pos, sugar):
        self.pos = Position(*pos)
        self.sugar = sugar
        self.discovered = False

    def collect_sugar(self):
        if self.sugar >= 1:
            self.sugar -= 1
            return 1
        return 0