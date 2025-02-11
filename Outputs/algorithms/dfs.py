from collections import deque
import time
import psutil
import os
from utils.state import State

def dfs(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    initial_state = State(maze.agent_pos, maze.stones)
    stack = [initial_state]
    visited = {hash(initial_state)}
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    
    while stack:
        current_state = stack.pop()
        
        if all(pos in maze.switches for pos in current_state.stones_pos):
            end_time = time.time()
            memory_end = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            return {
                'solution': current_state.get_path(),
                'steps': len(current_state.get_path()),
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,
                'memory': memory_end - memory_start
            }
        
        for dir_idx, (dy, dx) in enumerate(directions):
            new_row = current_state.agent_pos[0] + dy
            new_col = current_state.agent_pos[1] + dx
            
            if not maze.is_valid_move(new_row, new_col):
                continue
            
            stone_idx = -1
            for i, stone_pos in enumerate(current_state.stones_pos):
                if (new_row, new_col) == stone_pos:
                    stone_idx = i
                    break
            
            new_stones = current_state.stones_pos.copy()
            action = direction_names[dir_idx]
            
            if stone_idx >= 0:
                new_stone_row = new_row + dy
                new_stone_col = new_col + dx
                
                if not maze.is_valid_move(new_stone_row, new_stone_col):
                    continue
                
                if (new_stone_row, new_stone_col) in new_stones:
                    continue
                
                new_stones[stone_idx] = (new_stone_row, new_stone_col)
                action = action.upper()
            
            new_state = State((new_row, new_col), new_stones, 
                            current_state, action)
            
            if hash(new_state) not in visited:
                visited.add(hash(new_state))
                stack.append(new_state)
                nodes_generated += 1
    
    return None