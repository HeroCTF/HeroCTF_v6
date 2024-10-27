from engine.utils import Position, DIRECTIONS

class Ant:
    def __init__(self, pos, carrying=False):
        self.pos = Position(*pos)
        self.last_pos = Position(*pos)
        self.carrying = carrying
        self.last_carrying = carrying

    def move(self, direction):
        if direction in DIRECTIONS:
            delta = DIRECTIONS[direction]
            self.last_pos = self.pos
            self.pos = Position(self.pos.x + delta[0], self.pos.y + delta[1])

    def update_carrying(self, carrying):
        self.last_carrying = self.carrying
        self.carrying = carrying