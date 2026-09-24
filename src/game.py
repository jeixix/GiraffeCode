import pygame
import sys
import os
import json
import random
import math
from src.levels import LEVELS, Level
from src.game_state import GameState
from src.ui import UI, Button
from src.executor import Executor
from src.sound import sound_manager
from src.editor import level_editor_screen, custom_dict_to_level, load_custom_levels
TILE_SIZE = 80
UI_HEIGHT = 150
MARGIN = 40

LOGICAL_WIDTH = 1024
LOGICAL_HEIGHT = 768
IS_FULLSCREEN = True

def set_fullscreen(val):
    global IS_FULLSCREEN
    IS_FULLSCREEN = val

def get_screen():
    
    flags = pygame.SCALED | pygame.FULLSCREEN if IS_FULLSCREEN else pygame.SCALED
    return pygame.display.set_mode((LOGICAL_WIDTH, LOGICAL_HEIGHT), flags)

CHARACTERS = {
    "giraffe": {
        "name": "Giraffe",
        "emoji": "🦒",
        "character_sprite": "giraffe",
        "target_sprite": "tree",
        "target_name": "Acacia Tree",
        "win_text": "YAY! You got the leaves!",
        "btn_color": (100, 230, 100),
        "btn_hover": (150, 255, 150),
        "theme_color": (34, 139, 34),
        "desc": "Guide the giraffe to the acacia leaves!"
    },
    "cheetah": {
        "name": "Cheetah",
        "emoji": "🐆",
        "character_sprite": "cheetah",
        "target_sprite": "gazelle",
        "target_name": "Gazelle",
        "win_text": "YAY! You caught the gazelle!",
        "btn_color": (255, 170, 50),
        "btn_hover": (255, 200, 100),
        "theme_color": (204, 102, 0),
        "desc": "Guide the fast cheetah to the gazelle!"
    }
}
def get_base_data_dir():
    """Returns directory where user data/saves should persist (binary dir if frozen, project root if dev)"""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_save_file_path():
    try:
        return os.path.join(get_base_data_dir(), "progress.json")
    except Exception:
        return "progress.json"

def load_progress():
    path = get_save_file_path()
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                return set(data.get("completed_levels", []))
    except Exception as e:
        print(f"Failed to load progress: {e}")
    return set()

def save_progress(completed_levels):
    path = get_save_file_path()
    try:
        with open(path, "w") as f:
            json.dump({"completed_levels": sorted(list(completed_levels))}, f, indent=2)
    except Exception as e:
        print(f"Failed to save progress: {e}")

def generate_terrain(level, level_idx):
    """
    Deterministically generates a realistic savanna terrain distribution:
    - Water obstacles cluster into natural ponds / riverbeds.
    - Mud / dirt clusters around water banks and forms subtle animal trails.
    - Golden dry savanna grass forms natural sunlit patches.
    - Lush green grass forms the dominant background.
    """
    seed = (level_idx + 1) * 7919 + level.width * 313 + level.height * 1009 + level.start_x * 47 + level.goal_y * 89
    rng = random.Random(seed)

    # 1. Obstacle types: cluster water together into natural ponds / creeks
    obstacle_types = {}
    if level.obstacles:
        name_lower = level.name.lower()
        has_water_theme = any(w in name_lower for w in ["river", "creek", "pool", "water", "splash", "crossing", "hippo", "crocodile"])
        has_water = has_water_theme or (rng.random() < 0.55)

        if has_water and len(level.obstacles) > 0:
            water_anchor = rng.choice(level.obstacles)
            water_radius = rng.uniform(1.2, 2.6)
            for (ox, oy) in level.obstacles:
                d = math.hypot(ox - water_anchor[0], oy - water_anchor[1])
                if d <= water_radius:
                    obstacle_types[(ox, oy)] = "water"
                else:
                    obstacle_types[(ox, oy)] = "rock"
        else:
            for o in level.obstacles:
                obstacle_types[o] = "rock"

    water_tiles = [pos for pos, t in obstacle_types.items() if t == "water"]

    # 2. Ground biome features
    dry_cx = rng.uniform(0, level.width)
    dry_cy = rng.uniform(0, level.height)
    dry_radius = rng.uniform(1.8, 3.4)

    trail_cx = rng.uniform(0, level.width)
    trail_cy = rng.uniform(0, level.height)

    ground_types = {}
    for y in range(level.height):
        for x in range(level.width):
            if (x, y) in obstacle_types:
                continue

            # Proximity to water (muddy banks)
            if water_tiles:
                min_water_dist = min(math.hypot(x - wx, y - wy) for (wx, wy) in water_tiles)
            else:
                min_water_dist = 999.0

            # Muddy shorelines around water
            if min_water_dist <= 1.05:
                ground_types[(x, y)] = "dirt" if rng.random() < 0.85 else "grass"
                continue
            elif min_water_dist <= 1.6:
                if rng.random() < 0.45:
                    ground_types[(x, y)] = "dirt"
                    continue

            # Dry savanna patch with organic noise
            dist_dry = math.hypot(x - dry_cx, y - dry_cy)
            noise = (math.sin(x * 1.5 + seed) * math.cos(y * 1.5 + seed * 0.5)) * 0.6
            effective_dry_dist = dist_dry + noise

            if effective_dry_dist < dry_radius:
                prob = 1.0 - (effective_dry_dist / dry_radius) * 0.5
                ground_types[(x, y)] = "dry" if rng.random() < prob else "grass"
            else:
                # Small animal trail / dirt patch
                dist_trail = math.hypot(x - trail_cx, y - trail_cy)
                if dist_trail < 1.3 and rng.random() < 0.4:
                    ground_types[(x, y)] = "dirt"
                elif rng.random() < 0.06:
                    ground_types[(x, y)] = "dry"
                else:
                    ground_types[(x, y)] = "grass"

    return obstacle_types, ground_types

def draw_grid(surface, level, offset_x, offset_y, tile_size, assets, obstacle_types, ground_types, target_sprite="tree"):
    # Draw background grid
    for y in range(level.height):
        for x in range(level.width):
            rect = pygame.Rect(offset_x + x * tile_size, offset_y + y * tile_size, tile_size, tile_size)

            # Ground texture
            g_type = ground_types.get((x, y), "grass")
            if g_type == "dry" and assets.get("grass_dry"):
                grass_img = assets["grass_dry"]
            elif g_type == "dirt" and assets.get("grass_dirt"):
                grass_img = assets["grass_dirt"]
            else:
                grass_img = assets.get("grass")

            if grass_img:
                surface.blit(grass_img, rect)
            else:
                pygame.draw.rect(surface, (200, 255, 200), rect)

            # Obstacles
            if (x, y) in level.obstacles:
                obs_type = obstacle_types.get((x, y), "rock")
                if obs_type == "water" and assets.get("water"):
                    surface.blit(assets["water"], rect)
                elif assets.get("rock"):
                    rock_rect = assets["rock"].get_rect(center=rect.center)
                    surface.blit(assets["rock"], rock_rect)
                else:
                    color = (50, 100, 200) if obs_type == "water" else (150, 150, 150)
                    pygame.draw.rect(surface, color, rect)

            # Goal
            elif x == level.goal_x and y == level.goal_y:
                target_img = assets.get(target_sprite) or assets.get("tree")
                if target_img:
                    target_rect = target_img.get_rect(center=rect.center)
                    surface.blit(target_img, target_rect)
                else:
                    pygame.draw.circle(surface, (50, 200, 50), rect.center, tile_size // 3)

            pygame.draw.rect(surface, (150, 200, 150), rect, 2) # Grid lines
def character_select_menu(screen, assets):
    """Start menu screen to choose between Giraffe and Cheetah"""
    global IS_FULLSCREEN
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 62)
    font_sub = pygame.font.Font(None, 32)
    font_card_title = pygame.font.Font(None, 42)
    font_card_desc = pygame.font.Font(None, 24)
    bg_image = None
    try:
        raw_bg = assets.get("menu_bg_raw")
        if raw_bg:
            bg_image = pygame.transform.scale(raw_bg, screen.get_size())
    except Exception:
        pass
    card_w, card_h = 320, 390
    card1_rect = pygame.Rect(60, 145, card_w, card_h)
    card2_rect = pygame.Rect(420, 145, card_w, card_h)
    btn1 = Button(card1_rect.x + 30, card1_rect.bottom - 65, card_w - 60, 48, 
                  "Play as Giraffe", (100, 230, 100), (160, 255, 160), "giraffe")
    btn2 = Button(card2_rect.x + 30, card2_rect.bottom - 65, card_w - 60, 48, 
                  "Play as Cheetah", (255, 170, 50), (255, 210, 110), "cheetah")
    preview_giraffe = pygame.transform.scale(assets["giraffe"], (110, 110)) if assets.get("giraffe") else None
    preview_tree = pygame.transform.scale(assets["tree"], (90, 90)) if assets.get("tree") else None
    preview_cheetah = pygame.transform.scale(assets["cheetah"], (110, 110)) if assets.get("cheetah") else None
    preview_gazelle = pygame.transform.scale(assets["gazelle"], (90, 90)) if assets.get("gazelle") else None
    menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    menu_overlay.fill((255, 255, 255, 140))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                IS_FULLSCREEN = not IS_FULLSCREEN
                screen = get_screen()
                menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                menu_overlay.fill((255, 255, 255, 140))
                if assets.get("menu_bg_raw"):
                    bg_image = pygame.transform.scale(assets["menu_bg_raw"], screen.get_size())
            action1 = btn1.handle_event(event)
            if action1:
                return action1
            action2 = btn2.handle_event(event)
            if action2:
                return action2
            # Allow clicking anywhere on the cards
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if card1_rect.collidepoint(event.pos):
                    return "giraffe"
                elif card2_rect.collidepoint(event.pos):
                    return "cheetah"
        # Background
        if bg_image:
            screen.blit(bg_image, (0, 0))
            screen.blit(menu_overlay, (0, 0))
        else:
            screen.fill((135, 206, 235))
        # Header
        title = font_title.render("Choose Your Savanna Hero!", True, (0, 90, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
        pygame.draw.rect(screen, (255, 255, 255), title_rect.inflate(40, 20), border_radius=12)
        pygame.draw.rect(screen, (0, 110, 0), title_rect.inflate(40, 20), 4, border_radius=12)
        screen.blit(title, title_rect)
        subtitle = font_sub.render("Who would you like to guide today?", True, (40, 40, 40))
        sub_rect = subtitle.get_rect(center=(screen.get_width() // 2, 112))
        screen.blit(subtitle, sub_rect)
        # Draw Card 1: Giraffe
        hover1 = card1_rect.collidepoint(mouse_pos)
        c1_bg = (240, 255, 240) if hover1 else (255, 255, 255)
        c1_border = (40, 160, 40) if hover1 else (180, 210, 180)
        pygame.draw.rect(screen, c1_bg, card1_rect, border_radius=16)
        pygame.draw.rect(screen, c1_border, card1_rect, 4 if hover1 else 2, border_radius=16)
        t1 = font_card_title.render("Giraffe", True, (0, 120, 0))
        emoji_g = assets.get("emoji_giraffe")
        if emoji_g:
            e1 = pygame.transform.scale(emoji_g, (32, 32))
            tot_w = t1.get_width() + e1.get_width() + 8
            sx = card1_rect.centerx - tot_w // 2
            screen.blit(e1, (sx, card1_rect.y + 20))
            screen.blit(t1, (sx + e1.get_width() + 8, card1_rect.y + 22))
        else:
            screen.blit(t1, (card1_rect.centerx - t1.get_width() // 2, card1_rect.y + 20))
        if preview_giraffe and preview_tree:
            screen.blit(preview_giraffe, (card1_rect.x + 35, card1_rect.y + 75))
            arr_x = card1_rect.x + 155
            arr_y = card1_rect.y + 130
            pygame.draw.polygon(screen, (0, 160, 0), [(arr_x - 8, arr_y - 10), (arr_x + 8, arr_y), (arr_x - 8, arr_y + 10)])
            screen.blit(preview_tree, (card1_rect.x + 185, card1_rect.y + 85))
        desc1_a = font_card_desc.render("Goal: Reach the Acacia Tree", True, (40, 80, 40))
        desc1_b = font_card_desc.render("Get the tasty leaves!", True, (80, 80, 80))
        screen.blit(desc1_a, (card1_rect.centerx - desc1_a.get_width() // 2, card1_rect.y + 225))
        screen.blit(desc1_b, (card1_rect.centerx - desc1_b.get_width() // 2, card1_rect.y + 255))
        btn1.draw(screen, mouse_pos)
        # Draw Card 2: Cheetah
        hover2 = card2_rect.collidepoint(mouse_pos)
        c2_bg = (255, 248, 235) if hover2 else (255, 255, 255)
        c2_border = (230, 120, 0) if hover2 else (230, 200, 170)
        pygame.draw.rect(screen, c2_bg, card2_rect, border_radius=16)
        pygame.draw.rect(screen, c2_border, card2_rect, 4 if hover2 else 2, border_radius=16)
        t2 = font_card_title.render("Cheetah", True, (200, 80, 0))
        emoji_c = assets.get("emoji_cheetah")
        if emoji_c:
            e2 = pygame.transform.scale(emoji_c, (32, 32))
            tot_w = t2.get_width() + e2.get_width() + 8
            sx = card2_rect.centerx - tot_w // 2
            screen.blit(e2, (sx, card2_rect.y + 20))
            screen.blit(t2, (sx + e2.get_width() + 8, card2_rect.y + 22))
        else:
            screen.blit(t2, (card2_rect.centerx - t2.get_width() // 2, card2_rect.y + 20))
        if preview_cheetah and preview_gazelle:
            screen.blit(preview_cheetah, (card2_rect.x + 35, card2_rect.y + 75))
            arr_x = card2_rect.x + 155
            arr_y = card2_rect.y + 130
            pygame.draw.polygon(screen, (220, 100, 0), [(arr_x - 8, arr_y - 10), (arr_x + 8, arr_y), (arr_x - 8, arr_y + 10)])
            screen.blit(preview_gazelle, (card2_rect.x + 185, card2_rect.y + 85))
        desc2_a = font_card_desc.render("Goal: Catch the Speedy Gazelle", True, (120, 50, 0))
        desc2_b = font_card_desc.render("Fastest runner on the savanna!", True, (80, 80, 80))
        screen.blit(desc2_a, (card2_rect.centerx - desc2_a.get_width() // 2, card2_rect.y + 225))
        screen.blit(desc2_b, (card2_rect.centerx - desc2_b.get_width() // 2, card2_rect.y + 255))
        btn2.draw(screen, mouse_pos)
        pygame.display.flip()
        clock.tick(60)
def main_menu(screen, selected_char, assets, completed_levels):
    global IS_FULLSCREEN
    
    char_info = CHARACTERS.get(selected_char, CHARACTERS["giraffe"])
    font_title = pygame.font.Font(None, 68)
    font_sub = pygame.font.Font(None, 28)
    bg_image = None
    try:
        raw_bg = assets.get("menu_bg_raw")
        if raw_bg:
            bg_image = pygame.transform.scale(raw_bg, screen.get_size())
    except Exception:
        pass
    buttons = []
    btn_color = char_info["btn_color"]
    btn_hover = char_info["btn_hover"]
    star_icon = pygame.transform.scale(assets["emoji_star"], (26, 26)) if assets.get("emoji_star") else None
    for i, level in enumerate(LEVELS):
        lvl_name = level.name_giraffe if selected_char == "giraffe" else level.name_cheetah
        is_done = i in completed_levels
        c_color = (255, 235, 140) if is_done else btn_color
        c_hover = (255, 245, 175) if is_done else btn_hover
        btn_icon = star_icon if is_done else None
        btn = Button(screen.get_width() // 2 - 300, 0, 600, 60, lvl_name, c_color, c_hover, i, icon=btn_icon, icon_pos="left")
        buttons.append(btn)
    fs_w = 120
    hero_w = 145
    cust_w = 140
    ed_w = 140
    gap = 10
    top_y = 16
    btn_h = 36

    icon_switch = pygame.transform.scale(assets["emoji_switch"], (18, 18)) if assets.get("emoji_switch") else None

    btn_fs = Button(0, top_y, fs_w, btn_h, "Windowed" if IS_FULLSCREEN else "Fullscreen", (110, 160, 255), (160, 205, 255), "TOGGLE_FS", font_size=26)
    btn_change_hero = Button(0, top_y, hero_w, btn_h, "Switch Hero", (255, 235, 60), (255, 248, 170), "SWITCH_HERO", icon=icon_switch, icon_pos="right", font_size=26)
    btn_custom = Button(0, top_y, cust_w, btn_h, "Play Custom 🎮", (120, 220, 130), (160, 245, 170), "PLAY_CUSTOM_MENU", font_size=26)
    btn_editor = Button(0, top_y, ed_w, btn_h, "Level Editor 🛠️", (255, 185, 60), (255, 215, 110), "LEVEL_EDITOR", font_size=26)

    def reposition_header_buttons(scr_w):
        btn_fs.rect.x = scr_w - 20 - fs_w
        btn_change_hero.rect.x = btn_fs.rect.left - gap - hero_w
        btn_custom.rect.x = btn_change_hero.rect.left - gap - cust_w
        btn_editor.rect.x = btn_custom.rect.left - gap - ed_w

    reposition_header_buttons(screen.get_width())

    clock = pygame.time.Clock()
    scroll_y = 0
    max_scroll = max(0, len(LEVELS) * 80 - screen.get_height() + 250)
    menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    menu_overlay.fill((255, 255, 255, 140))
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                IS_FULLSCREEN = not IS_FULLSCREEN
                screen = get_screen()
                menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                menu_overlay.fill((255, 255, 255, 140))
                if assets.get("menu_bg_raw"):
                    bg_image = pygame.transform.scale(assets["menu_bg_raw"], screen.get_size())
                reposition_header_buttons(screen.get_width())
            if event.type == pygame.MOUSEWHEEL:
                scroll_y += event.y * 45
                scroll_y = max(-max_scroll, min(0, scroll_y))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    scroll_y += 90
                    scroll_y = max(-max_scroll, min(0, scroll_y))
                elif event.key == pygame.K_DOWN:
                    scroll_y -= 90
                    scroll_y = max(-max_scroll, min(0, scroll_y))
            hero_act = btn_change_hero.handle_event(event)
            if hero_act:
                sound_manager.play_click()
                return hero_act
            ed_act = btn_editor.handle_event(event)
            if ed_act:
                sound_manager.play_click()
                return ed_act
            cust_act = btn_custom.handle_event(event)
            if cust_act:
                sound_manager.play_click()
                saved_levels = load_custom_levels()
                if saved_levels:
                    custom_lvl = custom_dict_to_level(saved_levels[0])
                    return ("PLAY_CUSTOM", custom_lvl)
                else:
                    return "LEVEL_EDITOR"
            fs_act = btn_fs.handle_event(event)
            if fs_act:
                IS_FULLSCREEN = not IS_FULLSCREEN
                screen = get_screen()
                menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                menu_overlay.fill((255, 255, 255, 140))
                if assets.get("menu_bg_raw"):
                    bg_image = pygame.transform.scale(assets["menu_bg_raw"], screen.get_size())
                btn_fs.text = "Windowed" if IS_FULLSCREEN else "Fullscreen"
                reposition_header_buttons(screen.get_width())
                
            for btn in buttons:
                action = btn.handle_event(event)
                if action is not None:
                    sound_manager.play_click()
                    return action
        # Update button positions based on scroll
        start_y = 170 + scroll_y
        for i, btn in enumerate(buttons):
            btn.rect.x = screen.get_width() // 2 - 300
            btn.rect.y = start_y + i * 80
        if bg_image:
            screen.blit(bg_image, (0, 0))
            screen.blit(menu_overlay, (0, 0))
        else:
            screen.fill((135, 206, 235))
        # Draw buttons
        for btn in buttons:
            if -80 <= btn.rect.y <= screen.get_height() + 20:
                btn.draw(screen, mouse_pos)
        # Sticky Top Header Bar
        header_bar = pygame.Surface((screen.get_width(), 150))
        header_bar.fill((255, 255, 255))
        pygame.draw.line(header_bar, (180, 180, 180), (0, 149), (screen.get_width(), 149), 2)
        screen.blit(header_bar, (0, 0))
        # Title
        title = font_title.render("SavannaCode!", True, (0, 100, 0))
        screen.blit(title, (30, 20))
        # Hero status badge & progress stars with real emoji images
        badge_y = 92
        cx = 35
        s1 = font_sub.render("Playing as: ", True, (70, 70, 70))
        screen.blit(s1, (cx, badge_y))
        cx += s1.get_width() + 4
        
        hero_emoji_img = assets.get(f"emoji_{selected_char}")
        if hero_emoji_img:
            mini_hero = pygame.transform.scale(hero_emoji_img, (24, 24))
            screen.blit(mini_hero, (cx, badge_y - 2))
            cx += mini_hero.get_width() + 6
            
        s2 = font_sub.render(f"{char_info['name']}   |   Goal: ", True, char_info["theme_color"])
        screen.blit(s2, (cx, badge_y))
        cx += s2.get_width() + 4
        
        target_emoji_key = "emoji_leaf" if selected_char == "giraffe" else "emoji_gazelle"
        target_emoji_img = assets.get(target_emoji_key)
        if target_emoji_img:
            mini_target = pygame.transform.scale(target_emoji_img, (24, 24))
            screen.blit(mini_target, (cx, badge_y - 2))
            cx += mini_target.get_width() + 6
            
        s3 = font_sub.render(f"{char_info['target_name']}   |   Completed: {len(completed_levels)}/{len(LEVELS)} ", True, (70, 70, 70))
        screen.blit(s3, (cx, badge_y))
        cx += s3.get_width() + 4
        
        if assets.get("emoji_star"):
            mini_star = pygame.transform.scale(assets["emoji_star"], (22, 22))
            screen.blit(mini_star, (cx, badge_y - 1))
        # Header action buttons
        btn_editor.draw(screen, mouse_pos)
        btn_custom.draw(screen, mouse_pos)
        btn_change_hero.draw(screen, mouse_pos)
        btn_fs.draw(screen, mouse_pos)
        pygame.display.flip()
        clock.tick(60)
def main():
    global IS_FULLSCREEN
    
    pygame.init()
    # Initialize display FIRST so we can use .convert() on images
    
    screen = get_screen()
    pygame.display.set_caption("SavannaCode: Giraffe & Cheetah")
    try:
        icon_path = get_resource_path(os.path.join("assets", "icon.png"))
        app_icon = pygame.image.load(icon_path)
        pygame.display.set_icon(app_icon)
    except Exception as e:
        print(f"Failed to load app icon: {e}")
    # Load game assets
    assets = {}
    def load_image(filename, size=None):
        try:
            path = get_resource_path(os.path.join("assets", filename))
            if filename.endswith(".png"):
                img = pygame.image.load(path).convert_alpha()
            else:
                img = pygame.image.load(path).convert()
            if size:
                return pygame.transform.scale(img, size)
            return img
        except Exception as e:
            print(f"Failed to load {filename}: {e}")
            return None
    assets["giraffe"] = load_image("giraffe.png")
    assets["giraffe_walk"] = [
        load_image("giraffe_walk1.png") or assets["giraffe"],
        load_image("giraffe_walk2.png") or assets["giraffe"]
    ]
    assets["cheetah"] = load_image("cheetah.png")
    assets["cheetah_walk"] = [
        load_image("cheetah_walk1.png") or assets["cheetah"],
        load_image("cheetah_walk2.png") or assets["cheetah"]
    ]
    assets["tree"] = load_image("tree.png")
    assets["gazelle"] = load_image("gazelle.png")
    assets["rock"] = load_image("rock.png")
    assets["grass"] = load_image("grass.jpg")
    assets["grass_dry"] = load_image("grass_dry.jpg")
    assets["grass_dirt"] = load_image("grass_dirt.jpg")
    assets["water"] = load_image("water.jpg")
    assets["menu_bg_raw"] = load_image("menu_bg.jpg")
    assets["emoji_giraffe"] = load_image("emoji_giraffe.png")
    assets["emoji_cheetah"] = load_image("emoji_cheetah.png")
    assets["emoji_star"] = load_image("emoji_star.png")
    assets["emoji_switch"] = load_image("emoji_switch.png")
    assets["emoji_leaf"] = load_image("emoji_leaf.png")
    assets["emoji_gazelle"] = load_image("emoji_gazelle.png")

    assets_cache = {}
    def get_scaled_assets(tile_size):
        if tile_size not in assets_cache:
            scaled = {}
            for k, v in assets.items():
                if k.startswith("emoji_") or k.endswith("_raw") or v is None:
                    scaled[k] = v
                elif isinstance(v, list):
                    scaled[k] = [pygame.transform.scale(f, (tile_size, tile_size)) if f else None for f in v]
                elif isinstance(v, pygame.Surface):
                    scaled[k] = pygame.transform.scale(v, (tile_size, tile_size))
                else:
                    scaled[k] = v
            assets_cache[tile_size] = scaled
        return assets_cache[tile_size]

    state = "CHAR_SELECT"
    selected_character = "giraffe"
    current_level_idx = 0

    playing_custom = False
    custom_level_obj = None

    def load_level(idx_or_level):
        nonlocal current_level_idx, playing_custom, custom_level_obj
        if isinstance(idx_or_level, Level):
            level = idx_or_level
            custom_level_obj = level
            playing_custom = True
            idx = 0
        else:
            idx = idx_or_level
            level = LEVELS[idx]
            playing_custom = False
            custom_level_obj = None

        screen_w = LOGICAL_WIDTH
        screen_h = LOGICAL_HEIGHT
        scr = screen  # Reuse existing screen
        char_info = CHARACTERS[selected_character]
        pygame.display.set_caption(f"SavannaCode - {char_info['name']} - {level.name}")
        game_state = GameState(level)
        ui = UI(screen_w, screen_h)
        executor = Executor(game_state, ui)

        # Dynamic layout: ensure bottom row and all borders are 100% visible above UI
        header_height = 48
        ui_top = LOGICAL_HEIGHT - UI_HEIGHT  # 618
        pad_top = 16
        pad_bottom = 16
        pad_x = 24

        board_top = header_height + pad_top  # 64
        board_bottom = ui_top - pad_bottom   # 602
        avail_h = board_bottom - board_top   # 538
        avail_w = LOGICAL_WIDTH - 2 * pad_x  # 976

        max_w_tile = avail_w // level.width
        max_h_tile = avail_h // level.height
        tile_size = max(1, min(80, max_w_tile, max_h_tile))

        grid_w = level.width * tile_size
        grid_h = level.height * tile_size

        offset_x = (LOGICAL_WIDTH - grid_w) // 2
        offset_y = board_top + (avail_h - grid_h) // 2

        if playing_custom and getattr(level, 'obstacle_types', None):
            obstacle_types = {}
            for k, v in level.obstacle_types.items():
                if isinstance(k, str) and "," in k:
                    parts = k.split(",")
                    obstacle_types[(int(parts[0]), int(parts[1]))] = v
                elif isinstance(k, tuple):
                    obstacle_types[k] = v
            for o in level.obstacles:
                if tuple(o) not in obstacle_types:
                    obstacle_types[tuple(o)] = "rock"
            ground_types = {}
        else:
            obstacle_types, ground_types = generate_terrain(level, idx)

        level_assets = get_scaled_assets(tile_size)
        return scr, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 34)
    completed_levels = load_progress()
    # Level variables
    level = game_state = ui = executor = offset_x = offset_y = tile_size = level_assets = obstacle_types = ground_types = None
    last_game_state = "IDLE"
    while True:
        screen = pygame.display.get_surface()
        if state == "CHAR_SELECT":
            selected_character = character_select_menu(screen, assets)
            state = "MENU"
            continue
        elif state == "MENU":
            menu_action = main_menu(screen, selected_character, assets, completed_levels)
            if menu_action == "SWITCH_HERO":
                state = "CHAR_SELECT"
                continue
            elif menu_action == "LEVEL_EDITOR":
                state = "EDITOR"
                continue
            elif isinstance(menu_action, tuple) and menu_action[0] == "PLAY_CUSTOM":
                state = "PLAYING"
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types = load_level(menu_action[1])
                last_game_state = "IDLE"
                continue
            else:
                current_level_idx = menu_action
                state = "PLAYING"
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types = load_level(current_level_idx)
                last_game_state = "IDLE"
                continue
        elif state == "EDITOR":
            editor_action, custom_lvl = level_editor_screen(
                screen, assets, selected_character,
                get_screen_fn=get_screen,
                is_fullscreen_getter=lambda: IS_FULLSCREEN,
                is_fullscreen_setter=set_fullscreen
            )
            if editor_action == "PLAY_CUSTOM" and custom_lvl:
                state = "PLAYING"
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types = load_level(custom_lvl)
                last_game_state = "IDLE"
                continue
            else:
                state = "MENU"
                continue
        elif state == "PLAYING":
            char_info = CHARACTERS[selected_character]
            transitioned = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    IS_FULLSCREEN = not IS_FULLSCREEN; screen = get_screen()
                
                # UI button actions (including STOP when running)
                action = ui.handle_event(event)
                if action in ["FORWARD", "LEFT", "RIGHT", "REPEAT"]:
                    ui.add_command(action)
                elif action == "UNDO":
                    ui.undo_command()
                elif action == "RUN":
                    executor.start()
                    last_game_state = "RUNNING"
                elif action == "STOP":
                    executor.stop()
                    last_game_state = "IDLE"
                elif action == "CLEAR":
                    ui.clear_commands()
                    game_state.reset()
                    last_game_state = "IDLE"
                
                # Keyboard shortcuts for coding & controls
                if event.type == pygame.KEYDOWN:
                    if not executor.is_running:
                        if event.key in (pygame.K_w, pygame.K_UP):
                            ui.add_command("FORWARD")
                        elif event.key in (pygame.K_a, pygame.K_LEFT):
                            ui.add_command("LEFT")
                        elif event.key in (pygame.K_d, pygame.K_RIGHT):
                            ui.add_command("RIGHT")
                        elif event.key == pygame.K_r:
                            ui.add_command("REPEAT")
                        elif event.key == pygame.K_BACKSPACE:
                            ui.undo_command()
                        elif event.key == pygame.K_c:
                            ui.clear_commands()
                            game_state.reset()
                            last_game_state = "IDLE"
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            executor.start()
                            last_game_state = "RUNNING"
                    else:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            executor.stop()
                            last_game_state = "IDLE"

                    if event.key == pygame.K_SPACE and game_state.state == "SUCCESS":
                        if playing_custom:
                            state = "EDITOR"
                        elif current_level_idx < len(LEVELS) - 1:
                            current_level_idx += 1
                            screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types = load_level(current_level_idx)
                        else:
                            state = "MENU"
                        last_game_state = "IDLE"
                        transitioned = True
                        break
                    elif event.key == pygame.K_SPACE and game_state.state == "CRASH":
                        game_state.reset()
                        ui.clear_commands()
                        last_game_state = "IDLE"
                    elif event.key == pygame.K_ESCAPE:
                        state = "EDITOR" if playing_custom else "MENU"
                        last_game_state = "IDLE"
                        transitioned = True
                        break
            if transitioned:
                continue
            # Update
            executor.update()
            
            # Sound triggers on state changes
            if game_state.state != last_game_state:
                if game_state.state == "SUCCESS":
                    sound_manager.play_win()
                elif game_state.state == "CRASH":
                    sound_manager.play_crash()
                last_game_state = game_state.state

            # Save progress when player successfully reaches the goal in campaign
            if game_state.state == "SUCCESS" and not playing_custom and current_level_idx not in completed_levels:
                completed_levels.add(current_level_idx)
                save_progress(completed_levels)
                
            # Draw
            screen.fill((135, 206, 235))
            # Header info with real hero emoji image
            lvl_name = getattr(level, "name_giraffe", level.name) if selected_character == 'giraffe' else getattr(level, "name_cheetah", level.name)
            part1 = small_font.render(f"{lvl_name}   |   ", True, (0, 0, 0))
            hx = MARGIN
            screen.blit(part1, (hx, 10))
            hx += part1.get_width()
            hero_emoji_img = level_assets.get(f"emoji_{selected_character}")
            if hero_emoji_img:
                h_icon = pygame.transform.scale(hero_emoji_img, (26, 26))
                screen.blit(h_icon, (hx, 8))
                hx += h_icon.get_width() + 6
            esc_target = "Editor" if playing_custom else "Menu"
            part2 = small_font.render(f"{char_info['name']}  (ESC: {esc_target})", True, (0, 0, 0))
            screen.blit(part2, (hx, 10))
            # Grid with target sprite
            draw_grid(screen, level, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, target_sprite=char_info["target_sprite"])
            # Player sprite
            gx, gy = game_state.giraffe.grid_x, game_state.giraffe.grid_y
            walk_key = char_info["character_sprite"] + "_walk"
            player_sprites = level_assets.get(walk_key) or level_assets.get(char_info["character_sprite"])
            if player_sprites:
                game_state.giraffe.draw(screen, offset_x + gx * tile_size, offset_y + gy * tile_size, tile_size, player_sprites)
            # Command buttons & code queue with active execution highlight
            active_cmd = executor.command_index if executor.is_running else None
            tut_idx = None if playing_custom else current_level_idx
            ui.draw(screen, active_cmd_idx=active_cmd, tutorial_level=tut_idx)
            # Success Overlay
            if game_state.state == "SUCCESS":
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 255, 0, 50))
                screen.blit(overlay, (0, 0))
                if playing_custom:
                    prompt = "Editor"
                else:
                    prompt = "Next Level" if current_level_idx < len(LEVELS) - 1 else "Menu"
                win_str1 = f"{char_info['win_text']}   "
                win_str2 = f"   (Press SPACE for {prompt})"
                surf1 = font.render(win_str1, True, (255, 255, 255))
                surf2 = font.render(win_str2, True, (255, 255, 255))
                star_img = level_assets.get("emoji_star")
                if star_img:
                    star_surf = pygame.transform.scale(star_img, (32, 32))
                    tot_w = surf1.get_width() + star_surf.get_width() + surf2.get_width()
                    tot_h = max(surf1.get_height(), star_surf.get_height())
                    win_surf = pygame.Surface((tot_w, tot_h), pygame.SRCALPHA)
                    win_surf.blit(surf1, (0, (tot_h - surf1.get_height()) // 2))
                    win_surf.blit(star_surf, (surf1.get_width(), (tot_h - star_surf.get_height()) // 2))
                    win_surf.blit(surf2, (surf1.get_width() + star_surf.get_width(), (tot_h - surf2.get_height()) // 2))
                else:
                    win_surf = font.render(f"{char_info['win_text']} (Press SPACE for {prompt})", True, (255, 255, 255))
                text_rect = win_surf.get_rect(center=(screen.get_width() // 2, (screen.get_height() - UI_HEIGHT) // 2))
                bg_rect = text_rect.inflate(28, 20)
                pygame.draw.rect(screen, (0, 140, 0), bg_rect, border_radius=10)
                screen.blit(win_surf, text_rect)
            # Crash Overlay
            elif game_state.state == "CRASH":
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((255, 0, 0, 50))
                screen.blit(overlay, (0, 0))
                text = font.render(f"Oh no! {char_info['name']} hit an obstacle! (Press SPACE to retry)", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, (screen.get_height() - UI_HEIGHT) // 2))
                bg_rect = text_rect.inflate(24, 20)
                pygame.draw.rect(screen, (160, 0, 0), bg_rect, border_radius=10)
                screen.blit(text, text_rect)
            pygame.display.flip()
            clock.tick(60)
def main_wrapper():
    try:
        main()
    except Exception as e:
        import traceback
        try:
            crash_path = os.path.join(get_base_data_dir(), "crash.log")
            with open(crash_path, "w") as f:
                traceback.print_exc(file=f)
        except Exception:
            traceback.print_exc()
        raise
if __name__ == "__main__":
    main_wrapper()
