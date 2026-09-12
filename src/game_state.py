from .giraffe import Giraffe

class GameState:
    def __init__(self, level):
        self.level = level
        self.reset()
        
    def reset(self):
        self.giraffe = Giraffe(self.level.start_x, self.level.start_y, self.level.start_dir)
        self.state = "IDLE"  # IDLE, RUNNING, SUCCESS, CRASH
        
    def is_valid_pos(self, x, y):
        if x < 0 or x >= self.level.width:
            return False
        if y < 0 or y >= self.level.height:
            return False
        if (x, y) in self.level.obstacles:
            return False
        return True
        
    def update_giraffe(self, command):
        if command == "FORWARD":
            # Simulate forward move to check bounds
            sim_x, sim_y = self.giraffe.grid_x, self.giraffe.grid_y
            if self.giraffe.direction == 0: sim_y -= 1
            elif self.giraffe.direction == 1: sim_x += 1
            elif self.giraffe.direction == 2: sim_y += 1
            elif self.giraffe.direction == 3: sim_x -= 1
            
            if self.is_valid_pos(sim_x, sim_y):
                self.giraffe.move_forward()
            else:
                self.state = "CRASH"
        elif command == "LEFT":
            self.giraffe.turn_left()
        elif command == "RIGHT":
            self.giraffe.turn_right()
            
        # Check win condition
        if self.state != "CRASH" and self.giraffe.grid_x == self.level.goal_x and self.giraffe.grid_y == self.level.goal_y:
            self.state = "SUCCESS"
