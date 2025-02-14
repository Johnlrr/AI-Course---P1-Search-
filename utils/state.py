# utils/state.py
class State:
    def __init__(self, agent_pos, stones_pos, parent=None, action=None, cost=0):
        self.agent_pos = agent_pos
        self.stones_pos = stones_pos  # List of stone positions
        self.parent = parent
        self.action = action
        self.cost = cost
    
    def __eq__(self, other):
        return (self.agent_pos == other.agent_pos and 
                self.stones_pos == other.stones_pos)
    
    def __hash__(self):
        return hash((self.agent_pos, tuple(map(tuple, self.stones_pos))))
        # Generates a hash value based on the agent's position and the positions of the stones
    
    def __lt__(self, other):
        return (self.agent_pos, self.stones_pos) < (other.agent_pos, other.stones_pos)

    def get_path(self):
        path = []
        current = self
        while current.parent:
            path.append(current.action)
            current = current.parent
        return ''.join(reversed(path))