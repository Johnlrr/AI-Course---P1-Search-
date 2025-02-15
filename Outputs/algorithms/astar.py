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

def astar(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    initial_state = State(maze.agent_pos, maze.stones)
    initial_f = calculate_heuristic(maze.stones, maze.switches)
    
    open_set = [(initial_f, 0, initial_state)]  # f_score, g_score, state
    closed_set = set()
    g_scores = {hash(initial_state): 0}
    f_scores = {hash(initial_state): initial_f}
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    total_weight = 0
    
    while open_set:
        current_f, current_g, current_state = heapq.heappop(open_set)
        
        if current_f > f_scores[hash(current_state)]:
            continue
        
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
            tentative_g = current_g + 1
            
            if stone_idx >= 0:
                new_stone_row = new_row + dy
                new_stone_col = new_col + dx
                
                if not maze.is_valid_move(new_stone_row, new_stone_col):
                    continue
                
                if (new_stone_row, new_stone_col) in new_stones:
                    continue
                
                new_stones[stone_idx] = (new_stone_row, new_stone_col)
                action = action.upper()
                tentative_g += maze.weights[stone_idx]
                total_weight += maze.weights[stone_idx]
            
            new_state = State((new_row, new_col), new_stones, 
                            current_state, action)
            
            if hash(new_state) in closed_set:
                continue
            
            if (hash(new_state) not in g_scores or 
                tentative_g < g_scores[hash(new_state)]):
                g_scores[hash(new_state)] = tentative_g
                f_score = tentative_g + calculate_heuristic(new_stones, maze.switches)
                f_scores[hash(new_state)] = f_score
                heapq.heappush(open_set, (f_score, tentative_g, new_state))
                nodes_generated += 1
    
    return None