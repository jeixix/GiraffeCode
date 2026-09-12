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
        
        # Define buttons
        self.buttons = [
            Button(20, height - 80, 130, 50, "FORWARD", (100, 255, 100), (150, 255, 150), "FORWARD"),
            Button(160, height - 80, 110, 50, "LEFT", (100, 100, 255), (150, 150, 255), "LEFT"),
            Button(280, height - 80, 110, 50, "RIGHT", (255, 100, 100), (255, 150, 150), "RIGHT"),
            Button(420, height - 80, 110, 50, "RUN!", (255, 200, 0), (255, 230, 100), "RUN"),
            Button(540, height - 80, 100, 50, "CLEAR", (200, 200, 200), (230, 230, 230), "CLEAR"),
        ]
        
    def add_command(self, cmd):
        if len(self.commands) < 40: # limit queue size increased for harder levels
            self.commands.append(cmd)
            
    def clear_commands(self):
        self.commands = []

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw UI area background
        pygame.draw.rect(surface, (230, 230, 230), (0, self.height - 150, self.width, 150))
        pygame.draw.line(surface, (100, 100, 100), (0, self.height - 150), (self.width, self.height - 150), 3)
        
        # Draw buttons
        for btn in self.buttons:
            btn.draw(surface, mouse_pos)
            
        # Draw program queue
        font = pygame.font.Font(None, 24) # Slightly smaller font
        queue_abbrev = {"FORWARD": "FWD", "LEFT": "LFT", "RIGHT": "RGT"}
        short_cmds = [queue_abbrev.get(c, c) for c in self.commands]
        
        # Wrap into chunks of 15 commands per line
        chunk_size = 14
        chunks = [short_cmds[i:i + chunk_size] for i in range(0, len(short_cmds), chunk_size)]
        
        if not chunks:
            text_surf = font.render("Your Code: [ ]", True, (50, 50, 50))
            surface.blit(text_surf, (20, self.height - 140))
        else:
            for i, chunk in enumerate(chunks):
                prefix = "Your Code: [ " if i == 0 else "           "
                suffix = " ]" if i == len(chunks) - 1 else ""
                queue_text = prefix + " -> ".join(chunk) + suffix
                text_surf = font.render(queue_text, True, (50, 50, 50))
                surface.blit(text_surf, (20, self.height - 140 + i * 20))
        
    def handle_event(self, event):
        for btn in self.buttons:
            action = btn.handle_event(event)
            if action:
                return action
        return None
