#      RUN WITHOUT GUI (remember cd to folder Outputs)
#python main.py --input ..\Inputs\input-01.txt --output output-01.txt --algorithm bfs
#      RUN WITH GUI
#python main.py --input ..\Inputs\input-01.txt --gui


import tkinter as tk
from gui.visualizer import MazeVisualizer
from utils.maze import Maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs      
from algorithms.ucs import ucs
from algorithms.astar import astar  
from algorithms.greedy import Greedy
import time

def solve_maze(maze, algorithm):
    algorithms = {
        "bfs": bfs,
        "dfs": dfs,
        "ucs": ucs,
        "astar": astar,
        "greedy": Greedy
    }

    if algorithm not in algorithms:
        raise ValueError("Invalid algorithm")
    return algorithms[algorithm](maze)

def save_solution(result, output_file):
    if result is None:
        with open(output_file, 'w') as f:
            f.write("No solution found")
        return

    with open(output_file, 'w') as f:
        f.write(f"{result['algorithm'].upper()}\n")
        f.write(f"Steps: {result['steps']}, ")
        f.write(f"Nodes: {result['nodes']}, ")
        f.write(f"Time: {result['time']:.2f}ms, ")
        f.write(f"Memory: {result['memory']:.2f}MB\n")
        f.write(result['solution'])

def main():
    #parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="Maze solver")
    parser.add_argument('--input', type=str, default='input-01.txt',
                      help='Input file path')
    parser.add_argument('--output', type=str, default='output-01.txt',
                      help='Output file path')
    parser.add_argument('--algorithm', type=str, default='bfs',
                      choices=['bfs', 'dfs', 'ucs', 'astar', 'greedy'],
                      help='Search algorithm to use')
    parser.add_argument('--gui', action='store_true',
                      help='Show GUI visualization')
    args = parser.parse_args()
    
    # Load maze
    maze = Maze(args.input)
    
    if args.gui:
        # Start GUI
        root = tk.Tk()
        root.title("Ares's Adventure")
        app = MazeVisualizer(root, maze)
        root.mainloop()
    else:
        # Solve maze and save solution
        result = solve_maze(maze, args.algorithm)
        if result:
            result['algorithm'] = args.algorithm
        save_solution(result, args.output)

if __name__ == "__main__":
    main()