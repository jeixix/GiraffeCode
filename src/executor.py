import pygame
from src.sound import sound_manager

class Executor:
    def __init__(self, game_state, ui):
        self.game_state = game_state
        self.ui = ui
        self.is_running = False
        self.command_index = -1
        self.last_step_time = 0
        self.step_delay = 700 # milliseconds between steps
        
    def start(self):
        if not self.is_running and self.ui.commands:
            self.is_running = True
            self.command_index = 0
            self.last_step_time = pygame.time.get_ticks()
            self.game_state.reset() # Reset to start position before running
            self.game_state.state = "RUNNING"
            self.ui.set_running(True)
            self.loop_counters = {}
            
    def stop(self):
        self.is_running = False
        self.command_index = -1
        self.ui.set_running(False)
        if self.game_state.state == "RUNNING":
            self.game_state.state = "IDLE"
            
    def update(self):
        if self.is_running:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_step_time > self.step_delay:
                if self.command_index < len(self.ui.commands) and self.game_state.state == "RUNNING":
                    cmd = self.ui.commands[self.command_index]
                    
                    if cmd == "REPEAT":
                        # A REPEAT block jumps back to the beginning of the program.
                        # We allow each REPEAT block to jump back up to 2 times (3 total executions)
                        count = self.loop_counters.get(self.command_index, 0)
                        if count < 2:
                            self.loop_counters[self.command_index] = count + 1
                            self.command_index = 0
                            sound_manager.play_turn()
                        else:
                            # Reset counter so it works correctly if repeated by a later outer loop
                            self.loop_counters[self.command_index] = 0
                            self.command_index += 1
                    else:
                        self.game_state.update_giraffe(cmd)
                        if cmd == "FORWARD":
                            sound_manager.play_step()
                        elif cmd in ["LEFT", "RIGHT"]:
                            sound_manager.play_turn()
                        self.command_index += 1
                        
                    self.last_step_time = current_time
                else:
                    self.is_running = False
                    self.command_index = -1
                    self.ui.set_running(False)
                    if self.game_state.state == "RUNNING": # Finished commands but didn't win or crash
                        self.game_state.state = "IDLE"
