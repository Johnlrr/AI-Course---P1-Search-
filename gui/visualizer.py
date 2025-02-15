import tkinter as tk
from tkinter import ttk
import time

class MazeVisualizer:
    def __init__(self, root, maze, maze_file, cell_size=30):  #can change cell size
        self.root = root
        self.maze = maze
        self.maze_file = maze_file
        self.cell_size = cell_size
        
        # Calculate canvas dimensions
        self.width = len(maze.grid[0]) * cell_size
        self.height = len(maze.grid) * cell_size
        
        # Create main frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create control panel
        self.control_frame = ttk.Frame(self.main_frame)
        self.control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Create algorithm selection
        self.algorithm_var = tk.StringVar(value="bfs")
        algorithms = [("BFS", "bfs"), ("DFS", "dfs"), ("UCS", "ucs"), 
                     ("A*", "astar"), ("Greedy", "greedy")]
        
        for text, value in algorithms:
            ttk.Radiobutton(self.control_frame, text=text, value=value,
                          variable=self.algorithm_var).pack(side=tk.LEFT, padx=5)
        
        # Create buttons
        self.start_button = ttk.Button(self.control_frame, text="Start",
                                     command=self.start_visualization)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.reset_button = ttk.Button(self.control_frame, text="Reset",
                                     command=self.reset_visualization)
        self.reset_button.pack(side=tk.LEFT, padx=5)
        
        # Create status frame
        self.status_frame = ttk.Frame(self.main_frame)
        self.status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(self.status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Create canvas
        self.canvas = tk.Canvas(self.main_frame, width=self.width, 
                              height=self.height, bg='white')
        self.canvas.pack()
        
        # Initialize visualization state
        self.current_state = None
        self.animation_speed = 500  # milliseconds
        self.is_running = False
        
        # Draw initial state
        self.draw_maze()
    
    def draw_maze(self):
        self.canvas.delete("all")
        
        # Draw grid
        for i in range(len(self.maze.grid)):
            for j in range(len(self.maze.grid[0])):
                # Debugging: Print grid indices
                #print(f"Accessing grid[{i}][{j}]")
                
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                # Draw cell
                if self.maze.grid[i][j] == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='gray')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')
                
                # Draw switch
                if (i, j) in self.maze.switches:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill='yellow', outline='darkgoldenrod')  # Adjusted padding
                
                # Draw stone
                if (i, j) in self.maze.stones:
                    stone_idx = self.maze.stones.index((i, j))
                    padding = self.cell_size * 0.1
                    self.canvas.create_rectangle(x1+padding, y1+padding, x2-padding, y2-padding, fill='brown', outline='darkred')  # Adjusted padding
                    font_size = max(8,min(int(self.cell_size*0.4),12))
                    self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(self.maze.weights[stone_idx]),font=('Arial', font_size), fill='white')
                
                # Draw agent
                if (i, j) == self.maze.agent_pos:
                    self.canvas.create_oval(x1+10, y1+10, x2-10, y2-10, fill='red', outline='darkred')  # Adjusted padding
    
    def update_visualization(self, state):
        self.current_state = state
        self.draw_maze()
        self.root.update()
    
    def animate_solution(self, solution_path):
        if not solution_path:
            self.status_label["text"] = "No solution found!"
            return
        
        self.is_running = True
        current_pos = self.maze.agent_pos
        current_stones = self.maze.stones.copy()
        
        for move in solution_path:
            if not self.is_running:
                break
                
            # Calculate new positions
            dy = -1 if move.lower() == 'u' else 1 if move.lower() == 'd' else 0
            dx = -1 if move.lower() == 'l' else 1 if move.lower() == 'r' else 0
            
            new_pos = (current_pos[0] + dy, current_pos[1] + dx)
            
            # If pushing stone
            if move.isupper():
                stone_idx = current_stones.index(new_pos)
                current_stones[stone_idx] = (new_pos[0] + dy, new_pos[1] + dx)
            
            current_pos = new_pos
            
            # Update visualization
            self.maze.agent_pos = current_pos
            self.maze.stones = current_stones
            self.draw_maze()
            
            self.root.update()
            time.sleep(self.animation_speed / 1000)
    
    def start_visualization(self):
        from main import solve_maze  # Import here to avoid circular import
        
        algorithm = self.algorithm_var.get()
        result = solve_maze(self.maze, algorithm)
        
        if result:
            self.status_label["text"] = (
                f"Steps: {result['steps']}, "
                f"Nodes: {result['nodes']}, "
                f"Time: {result['time']:.2f}ms"
            )
            self.animate_solution(result['solution'])
        else:
            self.status_label["text"] = "No solution found!"
    
    def reset_visualization(self):
        self.is_running = False
        self.maze.reset_maze(self.maze_file)
        self.draw_maze()
        self.status_label["text"] = "Ready"