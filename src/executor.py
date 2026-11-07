import pygame
from src.sound import sound_manager

class Executor:
    def __init__(self, game_state, ui):
        self.game_state = game_state
        self.ui = ui
        self.is_running = False
        self.command_index = -1
        self.last_step_time = 0
        self.speed_mode = "NORMAL"  # "NORMAL" or "FAST"
        self.step_delay = 600       # 600ms (normal) or 250ms (fast)
        self.loop_counters = {}
        
    def set_speed(self, mode):
        self.speed_mode = mode
        if mode == "FAST":
            self.step_delay = 250
        else:
            self.step_delay = 600

    def toggle_speed(self):
        new_mode = "FAST" if self.speed_mode == "NORMAL" else "NORMAL"
        self.set_speed(new_mode)
        return new_mode

    def start(self):
        if not self.ui.commands:
            return
        if not self.is_running:
            # If we were stepping midway through, continue from command_index
            if self.command_index < 0 or self.game_state.state != "RUNNING":
                self.command_index = 0
                self.game_state.reset()
                self.game_state.state = "RUNNING"
                self.loop_counters = {}
            self.is_running = True
            self.last_step_time = pygame.time.get_ticks()
            self.ui.set_running(True)
            
    def stop(self):
        self.is_running = False
        self.command_index = -1
        self.loop_counters = {}
        self.ui.set_running(False)
        self.game_state.reset()

    def reset_state(self):
        self.is_running = False
        self.command_index = -1
        self.loop_counters = {}
        self.ui.set_running(False)
        self.game_state.reset()

    def step_once(self):
        """Single-step debugger: executes exactly one command and pauses."""
        if not self.ui.commands:
            return
        
        # If currently auto-running, pause
        if self.is_running:
            self.is_running = False
            self.ui.set_running(False)
            return

        # Start from beginning if idle
        if self.command_index < 0 or self.game_state.state != "RUNNING":
            self.game_state.reset()
            self.game_state.state = "RUNNING"
            self.command_index = 0
            self.loop_counters = {}

        if self.command_index < len(self.ui.commands) and self.game_state.state == "RUNNING":
            self._do_step()
            self.last_step_time = pygame.time.get_ticks()

        if self.game_state.state in ("SUCCESS", "CRASH"):
            self.is_running = False
            self.ui.set_running(False)
            if self.game_state.state == "SUCCESS":
                self.command_index = -1
        elif self.command_index >= len(self.ui.commands) and self.game_state.state == "RUNNING":
            self.game_state.state = "IDLE"
            self.command_index = -1
            self.ui.set_running(False)

    def _do_step(self):
        if self.command_index >= len(self.ui.commands):
            return
        cmd = self.ui.commands[self.command_index]
        if cmd == "REPEAT":
            if self.command_index == 0:
                self.command_index += 1
                return
            # Find loop start: index right after the previous REPEAT, or 0 if none
            loop_start = 0
            for i in range(self.command_index - 1, -1, -1):
                if self.ui.commands[i] == "REPEAT":
                    loop_start = i + 1
                    break
            if loop_start >= self.command_index:
                # Consecutive REPEATs or nothing in between
                self.command_index += 1
                return

            count = self.loop_counters.get(self.command_index, 0)
            if count < 2:
                self.loop_counters[self.command_index] = count + 1
                self.command_index = loop_start
                sound_manager.play_turn()
            else:
                self.loop_counters[self.command_index] = 0
                self.command_index += 1
        else:
            self.game_state.update_giraffe(cmd)
            if self.game_state.state != "CRASH":
                if cmd == "FORWARD":
                    sound_manager.play_step()
                elif cmd in ["LEFT", "RIGHT"]:
                    sound_manager.play_turn()
                self.command_index += 1

    def update(self):
        if self.is_running:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_step_time > self.step_delay:
                if self.command_index < len(self.ui.commands) and self.game_state.state == "RUNNING":
                    self._do_step()
                    self.last_step_time = current_time
                if self.game_state.state != "RUNNING" or self.command_index >= len(self.ui.commands):
                    self.is_running = False
                    self.ui.set_running(False)
                    if self.game_state.state != "CRASH":
                        self.command_index = -1
                    if self.game_state.state == "RUNNING":
                        self.game_state.state = "IDLE"
