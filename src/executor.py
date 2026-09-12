import pygame

class Executor:
    def __init__(self, game_state, ui):
        self.game_state = game_state
        self.ui = ui
        self.is_running = False
        self.command_index = 0
        self.last_step_time = 0
        self.step_delay = 700 # milliseconds between steps
        
    def start(self):
        if not self.is_running and self.ui.commands:
            self.is_running = True
            self.command_index = 0
            self.last_step_time = pygame.time.get_ticks()
            self.game_state.reset() # Reset to start position before running
            self.game_state.state = "RUNNING"
            
    def update(self):
        if self.is_running:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_step_time > self.step_delay:
                if self.command_index < len(self.ui.commands) and self.game_state.state == "RUNNING":
                    cmd = self.ui.commands[self.command_index]
                    self.game_state.update_giraffe(cmd)
                    self.command_index += 1
                    self.last_step_time = current_time
                else:
                    self.is_running = False
                    if self.game_state.state == "RUNNING": # Finished commands but didn't win or crash
                        self.game_state.state = "IDLE"
