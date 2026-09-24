import pygame
import math

class Giraffe:
    def __init__(self, x, y, direction):
        self.grid_x = x
        self.grid_y = y
        self.pixel_x = None
        self.pixel_y = None
        self.direction = direction  # 0: Up, 1: Right, 2: Down, 3: Left
        self.walk_frame = 0.0
        
    def move_forward(self):
        if self.direction == 0:
            self.grid_y -= 1
        elif self.direction == 1:
            self.grid_x += 1
        elif self.direction == 2:
            self.grid_y += 1
        elif self.direction == 3:
            self.grid_x -= 1
            
    def turn_left(self):
        self.direction = (self.direction - 1) % 4
        
    def turn_right(self):
        self.direction = (self.direction + 1) % 4

    def draw(self, surface, target_x_px, target_y_px, tile_size, images):
        if self.pixel_x is None:
            self.pixel_x = float(target_x_px)
            self.pixel_y = float(target_y_px)
            
        # Smooth interpolation towards target
        dx = target_x_px - self.pixel_x
        dy = target_y_px - self.pixel_y
        
        is_moving = abs(dx) > 1 or abs(dy) > 1
        if is_moving:
            # Interpolation speed
            self.pixel_x += dx * 0.15
            self.pixel_y += dy * 0.15
            # Animation speed
            self.walk_frame += 0.35
            
            # Waddle and Bob simulation
            wobble = math.sin(self.walk_frame * math.pi) * 12 # Wobble up to 12 degrees
            bob = abs(math.cos(self.walk_frame * math.pi)) * 6 # Bob up to 6 pixels
        else:
            self.pixel_x = float(target_x_px)
            self.pixel_y = float(target_y_px)
            self.walk_frame = 0.0
            wobble = 0
            bob = 0

        # Cycle through generated frame images
        if not images:
            return
        if isinstance(images, list):
            frame_idx = int(self.walk_frame) % len(images)
            image = images[frame_idx]
        else:
            image = images

        if image is None:
            return

        angle = wobble
        if self.direction == 0:
            angle += 90
        elif self.direction == 2:
            angle -= 90
        elif self.direction == 3:
            angle += 180
            
        rotated_image = pygame.transform.rotate(image, angle)
        
        # Center the rotated image in the tile (with vertical bobbing offset)
        center_x = int(self.pixel_x) + tile_size // 2
        center_y = int(self.pixel_y) + tile_size // 2 - int(bob)
        rect = rotated_image.get_rect(center=(center_x, center_y))
        surface.blit(rotated_image, rect)

# Aliases for multi-character support
Player = Giraffe
Animal = Giraffe
