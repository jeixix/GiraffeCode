import pygame

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 32)
        
    def draw(self, surface, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.action
        return None

class UI:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.commands = []
        self.is_running = False
        
        btn_y = height - 64
        btn_h = 48
        self.btn_fwd = Button(20, btn_y, 130, btn_h, "FORWARD", (100, 255, 100), (150, 255, 150), "FORWARD")
        self.btn_lft = Button(160, btn_y, 110, btn_h, "LEFT", (100, 100, 255), (150, 150, 255), "LEFT")
        self.btn_rgt = Button(280, btn_y, 110, btn_h, "RIGHT", (255, 100, 100), (255, 150, 150), "RIGHT")
        self.btn_undo = Button(400, btn_y, 110, btn_h, "UNDO ⌫", (255, 175, 75), (255, 200, 115), "UNDO")
        self.btn_clear = Button(520, btn_y, 110, btn_h, "CLEAR 🗑", (210, 210, 210), (230, 230, 230), "CLEAR")
        self.btn_run = Button(640, btn_y, 125, btn_h, "RUN ▶", (255, 200, 0), (255, 230, 100), "RUN")
        
        self.buttons = [
            self.btn_fwd,
            self.btn_lft,
            self.btn_rgt,
            self.btn_undo,
            self.btn_clear,
            self.btn_run
        ]
        
    def set_running(self, running):
        self.is_running = running
        if running:
            self.btn_run.text = "STOP ⏹"
            self.btn_run.color = (255, 80, 80)
            self.btn_run.hover_color = (255, 120, 120)
            self.btn_run.action = "STOP"
        else:
            self.btn_run.text = "RUN ▶"
            self.btn_run.color = (255, 200, 0)
            self.btn_run.hover_color = (255, 230, 100)
            self.btn_run.action = "RUN"
            
    def add_command(self, cmd):
        if not self.is_running and len(self.commands) < 40:
            self.commands.append(cmd)
            
    def undo_command(self):
        if not self.is_running and self.commands:
            self.commands.pop()
            
    def clear_commands(self):
        if not self.is_running:
            self.commands = []

    def draw(self, surface, active_cmd_idx=None):
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw UI area background
        pygame.draw.rect(surface, (245, 245, 245), (0, self.height - 150, self.width, 150))
        pygame.draw.line(surface, (180, 180, 180), (0, self.height - 150), (self.width, self.height - 150), 2)
        
        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface, mouse_pos)
            
        # Draw keyboard hint on the right
        hint_font = pygame.font.Font(None, 19)
        hint_lines = [
            "Keyboard shortcuts:",
            "↑ / W : Forward     Backspace : Undo",
            "← / A : Turn Left   Enter : Run / Stop",
            "→ / D : Turn Right  C : Clear all"
        ]
        for idx, line in enumerate(hint_lines):
            color = (80, 80, 80) if idx == 0 else (120, 120, 120)
            hint_surf = hint_font.render(line, True, color)
            surface.blit(hint_surf, (780, self.height - 68 + idx * 16))
            
        # Draw program queue pills
        font = pygame.font.Font(None, 20)
        arrow_font = pygame.font.Font(None, 20)
        short_names = {"FORWARD": "FWD", "LEFT": "LFT", "RIGHT": "RGT"}
        
        if not self.commands:
            empty_font = pygame.font.Font(None, 24)
            text_surf = empty_font.render("Your Code Queue: [ Click buttons below or use keyboard to build instructions! ]", True, (110, 110, 110))
            surface.blit(text_surf, (20, self.height - 138))
        else:
            cur_x = 20
            cur_y = self.height - 142
            pill_h = 20
            row_spacing = 24
            max_w = self.width - 25
            
            for i, cmd in enumerate(self.commands):
                label = short_names.get(cmd, cmd)
                text_w, text_h = font.size(label)
                pill_w = text_w + 12
                arrow_w = 14
                needed = pill_w + (arrow_w if i < len(self.commands) - 1 else 0)
                
                if cur_x + needed > max_w:
                    cur_x = 20
                    cur_y += row_spacing
                    
                rect = pygame.Rect(cur_x, cur_y, pill_w, pill_h)
                
                # Active highlight vs regular pastel badge
                is_active = (active_cmd_idx is not None and i == active_cmd_idx)
                if is_active:
                    pygame.draw.rect(surface, (255, 255, 140), rect, border_radius=5)
                    pygame.draw.rect(surface, (230, 140, 0), rect, 3, border_radius=5)
                    txt_surf = font.render(label, True, (0, 0, 0))
                else:
                    if cmd == "FORWARD":
                        bg_col = (220, 255, 220)
                        bd_col = (80, 180, 80)
                    elif cmd == "LEFT":
                        bg_col = (220, 230, 255)
                        bd_col = (80, 110, 220)
                    else:
                        bg_col = (255, 220, 220)
                        bd_col = (220, 80, 80)
                    pygame.draw.rect(surface, bg_col, rect, border_radius=5)
                    pygame.draw.rect(surface, bd_col, rect, 1, border_radius=5)
                    txt_surf = font.render(label, True, (20, 20, 20))
                    
                txt_rect = txt_surf.get_rect(center=rect.center)
                surface.blit(txt_surf, txt_rect)
                
                cur_x += pill_w
                
                # Arrow between code blocks
                if i < len(self.commands) - 1:
                    arr_surf = arrow_font.render("➜", True, (150, 150, 150))
                    arr_rect = arr_surf.get_rect(center=(cur_x + arrow_w // 2, cur_y + pill_h // 2))
                    surface.blit(arr_surf, arr_rect)
                    cur_x += arrow_w
        
    def handle_event(self, event):
        if self.is_running:
            # When running, allow STOP button click
            action = self.btn_run.handle_event(event)
            if action:
                return action
            return None

        for btn in self.buttons:
            action = btn.handle_event(event)
            if action:
                return action
        return None
