from engine.cube import Cube

class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [[None for _ in range(size)] for _ in range(size)]
        self.cubes = []

    def add_sugar(self, pos, sugar):
        cube = Cube(pos, sugar)
        self.cubes.append(cube)
        self.grid[pos[0]][pos[1]] = cube

    def get_cube_at(self, pos):
        for cube in self.cubes:
            if cube.pos == pos:
                return cube
        return 0

    def update_grid(self, ants):
        # Clear grid and re-place ants
        self.grid = [[None for _ in range(self.size)] for _ in range(self.size)]
        for ant in ants:
            self.grid[ant.pos.x][ant.pos.y] = ant