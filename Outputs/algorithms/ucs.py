# algorithms/ucs.py
import heapq
import time
import psutil
import os
from utils.state import State

class PriorityState:
    def __init__(self, state, priority):
        self.state = state
        self.priority = priority
    
    def __lt__(self, other):
        return self.priority < other.priority

def ucs(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    initial_state = State(maze.agent_pos, maze.stones)
    pq = [PriorityState(initial_state, 0)]
    visited = {hash(initial_state): 0}
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    total_weight = 0
    
    while pq:
        current_priority_state = heapq.heappop(pq)
        current_state = current_priority_state.state
        current_cost = current_priority_state.priority
        
        if current_cost > visited[hash(current_state)]:
            continue
            
        if all(pos in maze.switches for pos in current_state.stones_pos):
            end_time = time.time()
            memory_end = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            return {
                'solution': current_state.get_path(),
                'steps': len(current_state.get_path()),
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,
                'memory': memory_end - memory_start,
                'total_weight': total_weight
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
            new_cost = current_cost + 1  # Base movement cost
            
            if stone_idx >= 0:
                new_stone_row = new_row + dy
                new_stone_col = new_col + dx
                
                if not maze.is_valid_move(new_stone_row, new_stone_col):
                    continue
                
                if (new_stone_row, new_stone_col) in new_stones:
                    continue
                
                new_stones[stone_idx] = (new_stone_row, new_stone_col)
                action = action.upper()
                new_cost += maze.weights[stone_idx]  # Add stone weight to cost
                total_weight += maze.weights[stone_idx]
            
            new_state = State((new_row, new_col), new_stones, 
                            current_state, action)
            
            if (hash(new_state) not in visited or 
                new_cost < visited[hash(new_state)]):
                visited[hash(new_state)] = new_cost
                heapq.heappush(pq, PriorityState(new_state, new_cost))
                nodes_generated += 1
    
    return None