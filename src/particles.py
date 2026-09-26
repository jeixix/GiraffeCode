"""
Particle effects system for SavannaCode / GiraffeCode.
Provides cheerful, non-distracting visual feedback for movements,
collisions, leaf eating celebrations, and level completion confetti.
"""
import random
import pygame

class Particle:
    __slots__ = ("x", "y", "vx", "vy", "color", "radius", "life", "max_life", "gravity", "shape", "angle", "v_angle")

    def __init__(self, x, y, vx, vy, color, radius, life, gravity=0.15, shape="circle"):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)
        self.color = color
        self.radius = float(radius)
        self.life = int(life)
        self.max_life = int(life)
        self.gravity = float(gravity)
        self.shape = shape
        self.angle = random.uniform(0, 360)
        self.v_angle = random.uniform(-6, 6)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += self.gravity
        self.vx *= 0.96
        self.angle += self.v_angle
        self.life -= 1
        return self.life > 0

    def draw(self, surface):
        if self.life <= 0:
            return
        alpha = int(255 * (self.life / self.max_life))
        cur_rad = max(1, int(self.radius * (self.life / self.max_life)))
        
        if self.shape == "leaf":
            # Small fluttering diamond / leaf shape
            s = cur_rad * 2 + 2
            leaf_surf = pygame.Surface((s, s), pygame.SRCALPHA)
            pts = [(s // 2, 0), (s, s // 2), (s // 2, s), (0, s // 2)]
            pygame.draw.polygon(leaf_surf, (*self.color, alpha), pts)
            surface.blit(leaf_surf, (int(self.x - s // 2), int(self.y - s // 2)))
        elif self.shape == "confetti":
            # Rectangular spinning paper flake
            w = max(2, cur_rad * 2)
            h = max(2, int(cur_rad * 1.4))
            c_surf = pygame.Surface((w, h), pygame.SRCALPHA)
            c_surf.fill((*self.color, alpha))
            surface.blit(c_surf, (int(self.x - w // 2), int(self.y - h // 2)))
        else:
            # Circle with alpha
            s = cur_rad * 2 + 2
            circ_surf = pygame.Surface((s, s), pygame.SRCALPHA)
            pygame.draw.circle(circ_surf, (*self.color, alpha), (s // 2, s // 2), cur_rad)
            surface.blit(circ_surf, (int(self.x - s // 2), int(self.y - s // 2)))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def clear(self):
        self.particles.clear()

    def add_leaf_burst(self, center_x, center_y, count=24):
        """Celebrate reaching acacia tree with fluttering leaves"""
        leaf_colors = [
            (34, 139, 34),   # Forest Green
            (50, 205, 50),   # Lime Green
            (107, 142, 35),  # Olive Drab
            (154, 205, 50),  # Yellow Green
            (0, 100, 0)      # Dark Green
        ]
        for _ in range(count):
            vx = random.uniform(-3.5, 3.5)
            vy = random.uniform(-5.0, -1.0)
            color = random.choice(leaf_colors)
            rad = random.uniform(3, 6)
            life = random.randint(35, 55)
            self.particles.append(Particle(center_x, center_y, vx, vy, color, rad, life, gravity=0.12, shape="leaf"))

    def add_cheetah_catch(self, center_x, center_y, count=24):
        """Speed bursts when cheetah catches the gazelle"""
        star_colors = [
            (255, 215, 0),   # Gold
            (255, 140, 0),   # Dark Orange
            (255, 235, 59),  # Yellow
            (255, 255, 255)  # Sparkle
        ]
        for _ in range(count):
            vx = random.uniform(-4.0, 4.0)
            vy = random.uniform(-4.0, 2.0)
            color = random.choice(star_colors)
            rad = random.uniform(2, 5)
            life = random.randint(30, 45)
            self.particles.append(Particle(center_x, center_y, vx, vy, color, rad, life, gravity=0.15, shape="circle"))

    def add_dust_puff(self, x, y, direction=1):
        """Small dust puffs under feet when running"""
        dust_colors = [(210, 180, 140), (222, 184, 135), (245, 222, 179)]
        # Offset behind direction
        opp_dx = [-0, -1, 0, 1][direction]
        opp_dy = [1, 0, -1, 0][direction]
        px = x + opp_dx * 12 + random.uniform(-5, 5)
        py = y + opp_dy * 12 + random.uniform(-5, 5)
        for _ in range(4):
            vx = random.uniform(-1.0, 1.0) + opp_dx * 0.5
            vy = random.uniform(-1.5, 0.2) + opp_dy * 0.5
            color = random.choice(dust_colors)
            rad = random.uniform(2, 4)
            life = random.randint(15, 25)
            self.particles.append(Particle(px, py, vx, vy, color, rad, life, gravity=-0.02, shape="circle"))

    def add_water_splash(self, center_x, center_y, count=18):
        """Droplets splashing upward when falling in water"""
        water_colors = [(65, 105, 225), (100, 149, 237), (135, 206, 250), (255, 255, 255)]
        for _ in range(count):
            vx = random.uniform(-3.5, 3.5)
            vy = random.uniform(-4.5, -1.0)
            color = random.choice(water_colors)
            rad = random.uniform(2, 4.5)
            life = random.randint(25, 40)
            self.particles.append(Particle(center_x, center_y, vx, vy, color, rad, life, gravity=0.22, shape="circle"))

    def add_rock_bump(self, center_x, center_y, count=14):
        """Pebbles scattering when colliding with a rock"""
        rock_colors = [(105, 105, 105), (128, 128, 128), (169, 169, 169), (139, 69, 19)]
        for _ in range(count):
            vx = random.uniform(-3.0, 3.0)
            vy = random.uniform(-3.5, 0.5)
            color = random.choice(rock_colors)
            rad = random.uniform(2, 4)
            life = random.randint(20, 35)
            self.particles.append(Particle(center_x, center_y, vx, vy, color, rad, life, gravity=0.18, shape="circle"))

    def add_win_confetti(self, screen_w, screen_h, count=45):
        """Raining celebratory confetti on success"""
        confetti_colors = [
            (255, 99, 71),   # Tomato
            (255, 215, 0),   # Gold
            (50, 205, 50),   # Lime
            (30, 144, 255),  # Dodger Blue
            (255, 105, 180), # Hot Pink
            (147, 112, 219)  # Medium Purple
        ]
        for _ in range(count):
            x = random.uniform(50, screen_w - 50)
            y = random.uniform(10, screen_h // 3)
            vx = random.uniform(-2.0, 2.0)
            vy = random.uniform(1.0, 3.5)
            color = random.choice(confetti_colors)
            rad = random.uniform(3, 5)
            life = random.randint(50, 85)
            self.particles.append(Particle(x, y, vx, vy, color, rad, life, gravity=0.04, shape="confetti"))

    def update(self):
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)

# Global singleton
particles = ParticleSystem()
