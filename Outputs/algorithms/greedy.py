import heapq
import time
import psutil
import os
from utils.state import State

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def calculate_heuristic(stones_pos, switches):
    if not stones_pos or not switches:
        return 0
    
    total_distance = 0
    unmatched_stones = list(stones_pos)
    unmatched_switches = list(switches)
    
    while unmatched_stones:
        min_distance = float('inf')
        best_stone_idx = 0
        best_switch_idx = 0
        
        for i, stone in enumerate(unmatched_stones):
            for j, switch in enumerate(unmatched_switches):
                dist = manhattan_distance(stone, switch)
                if dist < min_distance:
                    min_distance = dist
                    best_stone_idx = i
                    best_switch_idx = j
        
        total_distance += min_distance
        unmatched_stones.pop(best_stone_idx)
        unmatched_switches.pop(best_switch_idx)
    
    return total_distance

def Greedy(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    initial_state = State(maze.agent_pos, maze.stones)
    initial_h = calculate_heuristic(maze.stones, maze.switches)
    
    open_set = [(initial_h, initial_state)]
    closed_set = set()
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    
    while open_set:
        current_h, current_state = heapq.heappop(open_set)
        
        if hash(current_state) in closed_set:
            continue
            
        closed_set.add(hash(current_state))
        
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
            
            if hash(new_state) in closed_set:
                continue
            
            h_score = calculate_heuristic(new_stones, maze.switches)
            heapq.heappush(open_set, (h_score, new_state))
            nodes_generated += 1
    
    return None