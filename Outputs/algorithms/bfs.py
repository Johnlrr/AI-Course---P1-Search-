# algorithms/bfs.py
from collections import deque
import time
import psutil
import os
from utils.state import State

def bfs(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024  # MB
    
    # Initial state
    initial_state = State(maze.agent_pos, maze.stones)
    
    # Queue for BFS
    queue = deque([initial_state])
    visited = {hash(initial_state)}
    
    # Directions: up, left, down, right
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    
    while queue:
        current_state = queue.popleft()
        
        # Check if all stones are on switches
        if all(pos in maze.switches for pos in current_state.stones_pos):
            end_time = time.time()
            memory_end = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            return {
                'solution': current_state.get_path(),
                'steps': len(current_state.get_path()),
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,  # Convert to ms
                'memory': memory_end - memory_start
            }
        
        # Try each direction
        for dir_idx, (dy, dx) in enumerate(directions):
            new_row = current_state.agent_pos[0] + dy
            new_col = current_state.agent_pos[1] + dx
            
            # Check if the move is valid
            if not maze.is_valid_move(new_row, new_col):
                continue
                
            # If there's a stone in the way
            stone_idx = -1
            for i, stone_pos in enumerate(current_state.stones_pos):
                if (new_row, new_col) == stone_pos:
                    stone_idx = i
                    break
            
            new_stones = current_state.stones_pos.copy()
            action = direction_names[dir_idx]
            
            if stone_idx >= 0:
                # Try to push the stone
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
                queue.append(new_state)
                nodes_generated += 1
    
    return None  # No solution found