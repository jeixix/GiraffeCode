import os
import sys
import pygame
from src.sound import sound_manager

def load_icon(name, size):
    try:
        base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        path = os.path.join(base, "assets", name)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
    except Exception:
        pass
    return None

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, action, icon=None, icon_pos="right"):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action = action
        self.font = pygame.font.Font(None, 32)
        self.icon = icon
        self.icon_pos = icon_pos
        
    def draw(self, surface, mouse_pos):
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)
        
        text_surf = self.font.render(self.text, True, (0, 0, 0))
        if self.icon:
            gap = 8
            total_w = text_surf.get_width() + self.icon.get_width() + (gap if self.text else 0)
            start_x = self.rect.centerx - total_w // 2
            if self.icon_pos == "left":
                icon_rect = self.icon.get_rect(midleft=(start_x, self.rect.centery))
                text_rect = text_surf.get_rect(midleft=(icon_rect.right + gap, self.rect.centery))
            else:
                text_rect = text_surf.get_rect(midleft=(start_x, self.rect.centery))
                icon_rect = self.icon.get_rect(midleft=(text_rect.right + gap, self.rect.centery))
            surface.blit(text_surf, text_rect)
            surface.blit(self.icon, icon_rect)
        else:
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
        self.icon_undo = load_icon("emoji_undo.png", (22, 22))
        self.icon_clear = load_icon("emoji_trash.png", (22, 22))
        self.icon_run = load_icon("emoji_play.png", (20, 20))
        self.icon_stop = load_icon("emoji_stop.png", (20, 20))
        self.icon_repeat = load_icon("emoji_repeat.png", (22, 22))
        
        self.btn_fwd = Button(20, btn_y, 110, btn_h, "FORWARD", (100, 255, 100), (150, 255, 150), "FORWARD")
        self.btn_lft = Button(140, btn_y, 90, btn_h, "LEFT", (100, 100, 255), (150, 150, 255), "LEFT")
        self.btn_rgt = Button(240, btn_y, 90, btn_h, "RIGHT", (255, 100, 100), (255, 150, 150), "RIGHT")
        self.btn_rep = Button(340, btn_y, 110, btn_h, "REPEAT", (220, 150, 255), (235, 180, 255), "REPEAT", icon=self.icon_repeat)
        self.btn_undo = Button(460, btn_y, 100, btn_h, "UNDO", (255, 175, 75), (255, 200, 115), "UNDO", icon=self.icon_undo)
        self.btn_clear = Button(570, btn_y, 100, btn_h, "CLEAR", (210, 210, 210), (230, 230, 230), "CLEAR", icon=self.icon_clear)
        self.btn_run = Button(680, btn_y, 110, btn_h, "RUN", (255, 200, 0), (255, 230, 100), "RUN", icon=self.icon_run)
        
        self.buttons = [
            self.btn_fwd,
            self.btn_lft,
            self.btn_rgt,
            self.btn_rep,
            self.btn_undo,
            self.btn_clear,
            self.btn_run
        ]
        self.hint_font = pygame.font.Font(None, 19)
        self.font = pygame.font.Font(None, 20)
        self.arrow_font = pygame.font.Font(None, 20)
        self.empty_font = pygame.font.Font(None, 24)
        self.tut_font = pygame.font.Font(None, 28)
        
    def set_running(self, running):
        self.is_running = running
        if running:
            self.btn_run.text = "STOP"
            self.btn_run.icon = self.icon_stop
            self.btn_run.color = (255, 80, 80)
            self.btn_run.hover_color = (255, 120, 120)
            self.btn_run.action = "STOP"
        else:
            self.btn_run.text = "RUN"
            self.btn_run.icon = self.icon_run
            self.btn_run.color = (255, 200, 0)
            self.btn_run.hover_color = (255, 230, 100)
            self.btn_run.action = "RUN"
            
    def add_command(self, cmd):
        if not self.is_running and len(self.commands) < 100:
            self.commands.append(cmd)
            sound_manager.play_click()
            
    def undo_command(self):
        if not self.is_running and self.commands:
            self.commands.pop()
            sound_manager.play_click()
            
    def clear_commands(self):
        if not self.is_running:
            self.commands = []
            sound_manager.play_click()

    def draw(self, surface, active_cmd_idx=None, tutorial_level=None):
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw UI area background
        pygame.draw.rect(surface, (245, 245, 245), (0, self.height - 150, self.width, 150))
        pygame.draw.line(surface, (180, 180, 180), (0, self.height - 150), (self.width, self.height - 150), 2)
        
        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface, mouse_pos)
            
        # Draw keyboard hint on the right
        hint_lines = [
            "Keyboard shortcuts:",
            "Up/W : Forward     Backspace : Undo",
            "Left/A : Left      Enter : Run/Stop",
            "Right/D : Right    C : Clear all",
            "R : Repeat         F11 : Fullscreen"
        ]
        for idx, line in enumerate(hint_lines):
            color = (80, 80, 80) if idx == 0 else (120, 120, 120)
            hint_surf = self.hint_font.render(line, True, color)
            surface.blit(hint_surf, (800, self.height - 85 + idx * 16))
            
        # Draw program queue pills
        short_names = {"FORWARD": "FWD", "LEFT": "LFT", "RIGHT": "RGT", "REPEAT": "REP"}
        
        if not self.commands:
            text_surf = self.empty_font.render("Your Code Queue: Click buttons below or use keyboard to build instructions!", True, (110, 110, 110))
            surface.blit(text_surf, (20, self.height - 138))
        else:
            cur_x = 20
            cur_y = self.height - 142
            pill_h = 20
            row_spacing = 24
            max_w = self.width - 25
            
            for i, cmd in enumerate(self.commands):
                label = short_names.get(cmd, cmd)
                text_w, text_h = self.font.size(label)
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
                    txt_surf = self.font.render(label, True, (0, 0, 0))
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
                    txt_surf = self.font.render(label, True, (20, 20, 20))
                    
                txt_rect = txt_surf.get_rect(center=rect.center)
                surface.blit(txt_surf, txt_rect)
                
                cur_x += pill_w
                
                # Arrow between code blocks
                if i < len(self.commands) - 1:
                    arr_x = cur_x + arrow_w // 2
                    arr_y = cur_y + pill_h // 2
                    pts = [(arr_x - 3, arr_y - 4), (arr_x + 3, arr_y), (arr_x - 3, arr_y + 4)]
                    pygame.draw.polygon(surface, (140, 140, 140), pts)
                    cur_x += arrow_w
                    
        self.draw_tutorial_hints(surface, tutorial_level)
        
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

    def draw_tutorial_hints(self, surface, tutorial_level):
        if self.is_running or tutorial_level is None:
            return
            
        import math
        import time
        bounce = math.sin(time.time() * 6) * 5
        tut_color = (255, 60, 60)
        
        def draw_hint(text_str, target_rect):
            text = self.tut_font.render(text_str, True, tut_color)
            # Add a white outline for readability
            outline = self.tut_font.render(text_str, True, (255, 255, 255))
            rect = text.get_rect(midbottom=(target_rect.centerx, target_rect.top - 15 + bounce))
            
            for dx, dy in [(-1,-1), (1,-1), (-1,1), (1,1), (0,-2), (0,2), (-2,0), (2,0)]:
                surface.blit(outline, (rect.x + dx, rect.y + dy))
            surface.blit(text, rect)
            
            pygame.draw.polygon(surface, tut_color, [
                (rect.centerx - 8, rect.bottom + 4),
                (rect.centerx + 8, rect.bottom + 4),
                (rect.centerx, rect.bottom + 12)
            ])
            pygame.draw.polygon(surface, (255, 255, 255), [
                (rect.centerx - 10, rect.bottom + 2),
                (rect.centerx + 10, rect.bottom + 2),
                (rect.centerx, rect.bottom + 14)
            ], 2)
            
        if tutorial_level == 0:
            if len(self.commands) == 0:
                draw_hint("Click FORWARD to move!", self.btn_fwd.rect)
            else:
                draw_hint("Click RUN to execute!", self.btn_run.rect)
        elif tutorial_level == 1:
            if len(self.commands) == 0:
                # Point roughly between LEFT and RIGHT
                fake_rect = self.btn_lft.rect.copy()
                fake_rect.width += self.btn_rgt.rect.width + 10
                draw_hint("Use LEFT or RIGHT to turn!", fake_rect)
        elif tutorial_level == 2:
            if len(self.commands) > 0 and "REPEAT" not in self.commands:
                draw_hint("Try REPEAT to do it again!", self.btn_rep.rect)
