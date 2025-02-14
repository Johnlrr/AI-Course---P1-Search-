import os

class Maze:
    def __init__(self, maze):
        self.weights = []
        self.grid = []
        self.stones = []
        self.switches = []
        self.agent_pos = None
        self.load_maze(maze)
    
    def load_maze(self, filename):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"No such file: '{filename}'")
        with open(filename, 'r') as f:
            self.weights = list(map(int, f.readline().strip().split()))
            temp_grid = []
            row = 0
            for line in f:
                col = 0
                row_list = []
                for char in line.strip():
                    if char == '$':
                        self.stones.append((row, col))
                    elif char == '.':
                        self.switches.append((row, col))
                    elif char == '@':
                        self.agent_pos = (row, col)
                    row_list.append(char)
                    col += 1
                temp_grid.append(row_list)
                row += 1
            self.grid = temp_grid

    def reset_maze(self, filename):
        self.weights = []
        self.grid = []
        self.stones = []
        self.switches = []
        self.agent_pos = None
        self.load_maze(filename)
    
    def is_valid_move(self, row, col):
        if row < 0 or row >= len(self.grid) or col < 0 or col >= len(self.grid[0]):
            return False
        return self.grid[row][col] != '#'
    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])