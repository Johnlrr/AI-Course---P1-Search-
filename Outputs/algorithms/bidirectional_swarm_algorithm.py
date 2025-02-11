import heapq
import time
import psutil
import os
from utils.state import State

def bidirectional_swarm_algorithm(maze):
    start_time = time.time()
    memory_start = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
    
    initial_state = State(maze.agent_pos, maze.stones)
    initial_h = calculate_heuristic(maze.stones, maze.switches)
    
    open_set_forward = [(initial_h, initial_state)]
    open_set_backward = [(initial_h, initial_state)]
    closed_set_forward = set()
    closed_set_backward = set()
    
    directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    direction_names = ['u', 'l', 'd', 'r']
    
    nodes_generated = 1
    
    while open_set_forward and open_set_backward:
        current_h_forward, current_state_forward = heapq.heappop(open_set_forward)
        current_h_backward, current_state_backward = heapq.heappop(open_set_backward)
        
        if hash(current_state_forward) in closed_set_backward or hash(current_state_backward) in closed_set_forward:
            end_time = time.time()
            memory_end = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
            
            return {
                'solution': current_state_forward.get_path() + current_state_backward.get_path(),
                'steps': len(current_state_forward.get_path()) + len(current_state_backward.get_path()),
                'nodes': nodes_generated,
                'time': (end_time - start_time) * 1000,
                'memory': memory_end - memory_start
            }
        
        closed_set_forward.add(hash(current_state_forward))
        closed_set_backward.add(hash(current_state_backward))
        
        for dir_idx, (dy, dx) in enumerate(directions):
            new_row_forward = current_state_forward.agent_pos[0] + dy
            new_col_forward = current_state_forward.agent_pos[1] + dx
            new_row_backward = current_state_backward.agent_pos[0] + dy
            new_col_backward = current_state_backward.agent_pos[1] + dx
            
            if not maze.is_valid_move(new_row_forward, new_col_forward) or not maze.is_valid_move(new_row_backward, new_col_backward):
                continue
            
            stone_idx_forward = -1
            stone_idx_backward = -1
            for i, stone_pos in enumerate(current_state_forward.stones_pos):
                if (new_row_forward, new_col_forward) == stone_pos:
                    stone_idx_forward = i
                    break
            for i, stone_pos in enumerate(current_state_backward.stones_pos):
                if (new_row_backward, new_col_backward) == stone_pos:
                    stone_idx_backward = i
                    break
            
            new_stones_forward = current_state_forward.stones_pos.copy()
            new_stones_backward = current_state_backward.stones_pos.copy()
            action_forward = direction_names[dir_idx]
            action_backward = direction_names[dir_idx]
            
            if stone_idx_forward >= 0:
                new_stone_row_forward = new_row_forward + dy
                new_stone_col_forward = new_col_forward
                
                if not maze.is_valid_move(new_stone_row_forward, new_stone_col_forward):
                    continue
                
                if (new_stone_row_forward, new_stone_col_forward) in new_stones_forward:
                    continue
                
                new_stones_forward[stone_idx_forward] = (new_stone_row_forward, new_stone_col_forward)
                action_forward = action_forward.upper()
            
            if stone_idx_backward >= 0:
                new_stone_row_backward = new_row_backward + dy
                new_stone_col_backward = new_col_backward
                
                if not maze.is_valid_move(new_stone_row_backward, new_stone_col_backward):
                    continue
                
                if (new_stone_row_backward, new_stone_col_backward) in new_stones_backward:
                    continue
                
                new_stones_backward[stone_idx_backward] = (new_stone_row_backward, new_stone_col_backward)
                action_backward = action_backward.upper()
            
            new_state_forward = State((new_row_forward, new_col_forward), new_stones_forward, 
                            current_state_forward, action_forward)
            new_state_backward = State((new_row_backward, new_col_backward), new_stones_backward, 
                            current_state_backward, action_backward)
            
            if hash(new_state_forward) in closed_set_forward or hash(new_state_backward) in closed_set_backward:
                continue
            
            h_score_forward = calculate_heuristic(new_stones_forward, maze.switches)
            h_score_backward = calculate_heuristic(new_stones_backward, maze.switches)
            heapq.heappush(open_set_forward, (h_score_forward, new_state_forward))
            heapq.heappush(open_set_backward, (h_score_backward, new_state_backward))
            nodes_generated += 1
    
    return None
