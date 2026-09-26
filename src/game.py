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
from src.i18n import t, get_lang, set_lang, toggle_lang
from src.particles import particles

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

def get_char_info(char_key):
    is_giraffe = (char_key == "giraffe")
    if is_giraffe:
        return {
            "name": "Giraffe" if get_lang() == "EN" else "Jirafa",
            "emoji": "🦒",
            "character_sprite": "giraffe",
            "target_sprite": "tree",
            "target_name": "Acacia Tree" if get_lang() == "EN" else "Árbol de Acacia",
            "win_text": t("win_giraffe"),
            "btn_color": (100, 230, 100),
            "btn_hover": (150, 255, 150),
            "theme_color": (34, 139, 34),
            "desc": "Guide the giraffe to the acacia leaves!" if get_lang() == "EN" else "¡Guía a la jirafa hacia las hojas!"
        }
    else:
        return {
            "name": "Cheetah" if get_lang() == "EN" else "Guepardo",
            "emoji": "🐆",
            "character_sprite": "cheetah",
            "target_sprite": "gazelle",
            "target_name": "Gazelle" if get_lang() == "EN" else "Gacela",
            "win_text": t("win_cheetah"),
            "btn_color": (255, 170, 50),
            "btn_hover": (255, 200, 100),
            "theme_color": (204, 102, 0),
            "desc": "Guide the fast cheetah to the gazelle!" if get_lang() == "EN" else "¡Guía al veloz guepardo hacia la gacela!"
        }

class CharacterDict(dict):
    def __getitem__(self, key):
        return get_char_info(key)
    def get(self, key, default=None):
        if key in ("giraffe", "cheetah"):
            return get_char_info(key)
        return default

CHARACTERS = CharacterDict({"giraffe": None, "cheetah": None})
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
    btn_lang = Button(screen.get_width() - 85, 20, 65, 36, get_lang(), (190, 225, 255), (220, 240, 255), "TOGGLE_LANG", font_size=24)
    btn1 = Button(card1_rect.x + 30, card1_rect.bottom - 65, card_w - 60, 48, 
                  t("card_btn_giraffe"), (100, 230, 100), (160, 255, 160), "giraffe")
    btn2 = Button(card2_rect.x + 30, card2_rect.bottom - 65, card_w - 60, 48, 
                  t("card_btn_cheetah"), (255, 170, 50), (255, 210, 110), "cheetah")
    preview_giraffe = pygame.transform.scale(assets["giraffe"], (110, 110)) if assets.get("giraffe") else None
    preview_tree = pygame.transform.scale(assets["tree"], (90, 90)) if assets.get("tree") else None
    preview_cheetah = pygame.transform.scale(assets["cheetah"], (110, 110)) if assets.get("cheetah") else None
    preview_gazelle = pygame.transform.scale(assets["gazelle"], (90, 90)) if assets.get("gazelle") else None
    menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    menu_overlay.fill((255, 255, 255, 140))

    def refresh_char_texts():
        btn_lang.text = get_lang()
        btn1.text = t("card_btn_giraffe")
        btn2.text = t("card_btn_cheetah")

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
                btn_lang.rect.x = screen.get_width() - 85
            if event.type == pygame.KEYDOWN and event.key == pygame.K_l:
                toggle_lang()
                refresh_char_texts()
            lang_act = btn_lang.handle_event(event)
            if lang_act:
                toggle_lang()
                refresh_char_texts()
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
        title = font_title.render(t("choose_hero_title"), True, (0, 90, 0))
        title_rect = title.get_rect(center=(screen.get_width() // 2, 60))
        pygame.draw.rect(screen, (255, 255, 255), title_rect.inflate(40, 20), border_radius=12)
        pygame.draw.rect(screen, (0, 110, 0), title_rect.inflate(40, 20), 4, border_radius=12)
        screen.blit(title, title_rect)
        subtitle = font_sub.render(t("choose_hero_sub"), True, (40, 40, 40))
        sub_rect = subtitle.get_rect(center=(screen.get_width() // 2, 112))
        screen.blit(subtitle, sub_rect)
        btn_lang.draw(screen, mouse_pos)
        # Draw Card 1: Giraffe
        hover1 = card1_rect.collidepoint(mouse_pos)
        c1_bg = (240, 255, 240) if hover1 else (255, 255, 255)
        c1_border = (40, 160, 40) if hover1 else (180, 210, 180)
        pygame.draw.rect(screen, c1_bg, card1_rect, border_radius=16)
        pygame.draw.rect(screen, c1_border, card1_rect, 4 if hover1 else 2, border_radius=16)
        t1 = font_card_title.render(t("hero_giraffe"), True, (0, 120, 0))
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
        desc1_a = font_card_desc.render(t("card_goal_giraffe"), True, (40, 80, 40))
        desc1_b = font_card_desc.render(t("card_desc_giraffe"), True, (80, 80, 80))
        screen.blit(desc1_a, (card1_rect.centerx - desc1_a.get_width() // 2, card1_rect.y + 225))
        screen.blit(desc1_b, (card1_rect.centerx - desc1_b.get_width() // 2, card1_rect.y + 255))
        btn1.draw(screen, mouse_pos)
        # Draw Card 2: Cheetah
        hover2 = card2_rect.collidepoint(mouse_pos)
        c2_bg = (255, 248, 235) if hover2 else (255, 255, 255)
        c2_border = (230, 120, 0) if hover2 else (230, 200, 170)
        pygame.draw.rect(screen, c2_bg, card2_rect, border_radius=16)
        pygame.draw.rect(screen, c2_border, card2_rect, 4 if hover2 else 2, border_radius=16)
        t2 = font_card_title.render(t("hero_cheetah"), True, (200, 80, 0))
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
        desc2_a = font_card_desc.render(t("card_goal_cheetah"), True, (120, 50, 0))
        desc2_b = font_card_desc.render(t("card_desc_cheetah"), True, (80, 80, 80))
        screen.blit(desc2_a, (card2_rect.centerx - desc2_a.get_width() // 2, card2_rect.y + 225))
        screen.blit(desc2_b, (card2_rect.centerx - desc2_b.get_width() // 2, card2_rect.y + 255))
        btn2.draw(screen, mouse_pos)
        pygame.display.flip()
        clock.tick(60)
def main_menu(screen, selected_char, assets, completed_levels):
    global IS_FULLSCREEN
    
    char_info = CHARACTERS.get(selected_char, CHARACTERS["giraffe"])
    font_title = pygame.font.Font(None, 52)
    font_sub = pygame.font.Font(None, 24)
    font_chap_title = pygame.font.Font(None, 28)
    font_card_num = pygame.font.Font(None, 24)
    font_card_name = pygame.font.Font(None, 20)
    font_hint = pygame.font.Font(None, 22)
    bg_image = None
    try:
        raw_bg = assets.get("menu_bg_raw")
        if raw_bg:
            bg_image = pygame.transform.scale(raw_bg, screen.get_size())
    except Exception:
        pass

    star_icon = pygame.transform.scale(assets["emoji_star"], (22, 22)) if assets.get("emoji_star") else None
    icon_switch = pygame.transform.scale(assets["emoji_switch"], (16, 16)) if assets.get("emoji_switch") else None
    icon_custom = pygame.transform.scale(assets["emoji_custom"], (16, 16)) if assets.get("emoji_custom") else None
    icon_editor = pygame.transform.scale(assets["emoji_editor"], (16, 16)) if assets.get("emoji_editor") else None

    # Header action buttons
    fs_w = 95
    lang_w = 48
    mute_w = 110
    hero_w = 130
    cust_w = 125
    ed_w = 115
    gap = 8
    top_y = 16
    btn_h = 36

    btn_fs = Button(0, top_y, fs_w, btn_h, t("windowed") if IS_FULLSCREEN else t("fullscreen"), (110, 160, 255), (160, 205, 255), "TOGGLE_FS", font_size=20)
    btn_lang = Button(0, top_y, lang_w, btn_h, get_lang(), (190, 225, 255), (220, 240, 255), "TOGGLE_LANG", font_size=20)
    btn_mute = Button(0, top_y, mute_w, btn_h, t("sound_off") if sound_manager.is_muted else t("sound_on"), (255, 180, 180) if sound_manager.is_muted else (210, 240, 210), (255, 205, 205) if sound_manager.is_muted else (230, 250, 230), "TOGGLE_MUTE", font_size=20)
    btn_change_hero = Button(0, top_y, hero_w, btn_h, t("switch_hero"), (255, 235, 60), (255, 248, 170), "SWITCH_HERO", icon=icon_switch, icon_pos="right", font_size=20)
    btn_custom = Button(0, top_y, cust_w, btn_h, t("play_custom"), (120, 220, 130), (160, 245, 170), "PLAY_CUSTOM_MENU", icon=icon_custom, icon_pos="right", font_size=20)
    btn_editor = Button(0, top_y, ed_w, btn_h, t("level_editor"), (255, 185, 60), (255, 215, 110), "LEVEL_EDITOR", icon=icon_editor, icon_pos="right", font_size=20)

    def reposition_header_buttons(scr_w):
        btn_fs.rect.x = scr_w - 18 - fs_w
        btn_lang.rect.x = btn_fs.rect.left - gap - lang_w
        btn_mute.rect.x = btn_lang.rect.left - gap - mute_w
        btn_change_hero.rect.x = btn_mute.rect.left - gap - hero_w
        btn_custom.rect.x = btn_change_hero.rect.left - gap - cust_w
        btn_editor.rect.x = btn_custom.rect.left - gap - ed_w

    reposition_header_buttons(screen.get_width())

    # Start at chapter of first uncompleted level
    current_chapter = 0
    for i in range(len(LEVELS)):
        if i not in completed_levels:
            current_chapter = i // 20
            break

    # Chapter nav buttons
    btn_prev = Button(50, 150, 100, 36, t("prev_chapter"), (200, 225, 255), (225, 240, 255), "PREV_CHAP", font_size=22)
    btn_next = Button(screen.get_width() - 150, 150, 100, 36, t("next_chapter"), (200, 225, 255), (225, 240, 255), "NEXT_CHAP", font_size=22)

    def refresh_menu_texts():
        btn_fs.text = t("windowed") if IS_FULLSCREEN else t("fullscreen")
        btn_lang.text = get_lang()
        btn_mute.text = t("sound_off") if sound_manager.is_muted else t("sound_on")
        btn_mute.color = (255, 180, 180) if sound_manager.is_muted else (210, 240, 210)
        btn_change_hero.text = t("switch_hero")
        btn_custom.text = t("play_custom")
        btn_editor.text = t("level_editor")
        btn_prev.text = t("prev_chapter")
        btn_next.text = t("next_chapter")

    clock = pygame.time.Clock()
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
                btn_next.rect.x = screen.get_width() - 150
                refresh_menu_texts()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_PAGEUP):
                    current_chapter = (current_chapter - 1) % 10
                    sound_manager.play_click()
                elif event.key in (pygame.K_RIGHT, pygame.K_PAGEDOWN):
                    current_chapter = (current_chapter + 1) % 10
                    sound_manager.play_click()
                elif event.key == pygame.K_m:
                    sound_manager.toggle_mute()
                    refresh_menu_texts()
                elif event.key == pygame.K_l:
                    toggle_lang()
                    refresh_menu_texts()

            # Handle header buttons
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
                reposition_header_buttons(screen.get_width())
                btn_next.rect.x = screen.get_width() - 150
                refresh_menu_texts()
            lang_act = btn_lang.handle_event(event)
            if lang_act:
                toggle_lang()
                refresh_menu_texts()
            mute_act = btn_mute.handle_event(event)
            if mute_act:
                sound_manager.toggle_mute()
                refresh_menu_texts()

            # Chapter navigation
            if btn_prev.handle_event(event):
                current_chapter = (current_chapter - 1) % 10
                sound_manager.play_click()
            if btn_next.handle_event(event):
                current_chapter = (current_chapter + 1) % 10
                sound_manager.play_click()

            # Chapter pill clicks and Level grid clicks
            pill_start_x = (screen.get_width() - (10 * 44 + 9 * 8)) // 2
            pill_y = 612
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Check chapter pills
                for ch in range(10):
                    p_rect = pygame.Rect(pill_start_x + ch * 52, pill_y, 44, 30)
                    if p_rect.collidepoint(event.pos):
                        current_chapter = ch
                        sound_manager.play_click()
                        break

                # Check level grid clicks
                grid_start_x = (screen.get_width() - (5 * 172 + 4 * 16)) // 2
                grid_start_y = 200
                for r in range(4):
                    for c in range(5):
                        card_rect = pygame.Rect(grid_start_x + c * 188, grid_start_y + r * 102, 172, 90)
                        if card_rect.collidepoint(event.pos):
                            slot_idx = r * 5 + c
                            lvl_idx = current_chapter * 20 + slot_idx
                            if lvl_idx < len(LEVELS):
                                sound_manager.play_click()
                                return lvl_idx

        # Background
        if bg_image:
            screen.blit(bg_image, (0, 0))
            screen.blit(menu_overlay, (0, 0))
        else:
            screen.fill((135, 206, 235))

        # Sticky Top Header Bar
        header_bar = pygame.Surface((screen.get_width(), 138))
        header_bar.fill((255, 255, 255))
        pygame.draw.line(header_bar, (180, 180, 180), (0, 137), (screen.get_width(), 137), 2)
        screen.blit(header_bar, (0, 0))

        # Title
        title = font_title.render("SavannaCode!", True, (0, 100, 0))
        screen.blit(title, (25, 18))

        # Hero status line
        badge_y = 86
        cx = 28
        s1 = font_sub.render(t("playing_as"), True, (70, 70, 70))
        screen.blit(s1, (cx, badge_y))
        cx += s1.get_width() + 4

        hero_emoji_img = assets.get(f"emoji_{selected_char}")
        if hero_emoji_img:
            mini_hero = pygame.transform.scale(hero_emoji_img, (22, 22))
            screen.blit(mini_hero, (cx, badge_y - 2))
            cx += mini_hero.get_width() + 6

        s2 = font_sub.render(f"{char_info['name']}   |   {t('goal')}", True, char_info["theme_color"])
        screen.blit(s2, (cx, badge_y))
        cx += s2.get_width() + 4

        target_emoji_key = "emoji_leaf" if selected_char == "giraffe" else "emoji_gazelle"
        target_emoji_img = assets.get(target_emoji_key)
        if target_emoji_img:
            mini_target = pygame.transform.scale(target_emoji_img, (22, 22))
            screen.blit(mini_target, (cx, badge_y - 2))
            cx += mini_target.get_width() + 6

        s3 = font_sub.render(f"{char_info['target_name']}   |   {t('completed')}{len(completed_levels)}/{len(LEVELS)} ", True, (70, 70, 70))
        screen.blit(s3, (cx, badge_y))
        cx += s3.get_width() + 4

        if star_icon:
            screen.blit(star_icon, (cx, badge_y - 2))

        # Header action buttons
        btn_editor.draw(screen, mouse_pos)
        btn_custom.draw(screen, mouse_pos)
        btn_change_hero.draw(screen, mouse_pos)
        btn_mute.draw(screen, mouse_pos)
        btn_lang.draw(screen, mouse_pos)
        btn_fs.draw(screen, mouse_pos)

        # Chapter Navigation Bar
        btn_prev.draw(screen, mouse_pos)
        btn_next.draw(screen, mouse_pos)

        chap_name = t(f"world_{current_chapter + 1}")
        chap_start = current_chapter * 20
        chap_done = sum(1 for lvl_i in range(chap_start, min(chap_start + 20, len(LEVELS))) if lvl_i in completed_levels)
        chap_title_str = f"{t('chapter')} {current_chapter + 1}: {chap_name}   ({chap_done}/20"
        title_surf = font_chap_title.render(chap_title_str, True, (0, 80, 0))
        star_w = star_icon.get_width() + 6 if star_icon else 10
        tot_w = title_surf.get_width() + star_w + 16
        chap_rect = pygame.Rect(screen.get_width() // 2 - tot_w // 2, 148, tot_w, 38)
        pygame.draw.rect(screen, (255, 255, 255), chap_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 160, 100), chap_rect, 2, border_radius=8)
        screen.blit(title_surf, (chap_rect.x + 10, chap_rect.y + 9))
        if star_icon:
            screen.blit(star_icon, (chap_rect.x + 10 + title_surf.get_width() + 4, chap_rect.y + 7))
            close_paren = font_chap_title.render(")", True, (0, 80, 0))
            screen.blit(close_paren, (chap_rect.x + 10 + title_surf.get_width() + 4 + star_icon.get_width(), chap_rect.y + 9))

        # Level Grid (5 columns x 4 rows)
        grid_start_x = (screen.get_width() - (5 * 172 + 4 * 16)) // 2
        grid_start_y = 200
        for r in range(4):
            for c in range(5):
                slot_idx = r * 5 + c
                lvl_idx = current_chapter * 20 + slot_idx
                if lvl_idx >= len(LEVELS):
                    continue
                lvl = LEVELS[lvl_idx]
                lvl_name = lvl.name_giraffe if selected_char == "giraffe" else lvl.name_cheetah
                is_done = lvl_idx in completed_levels

                card_rect = pygame.Rect(grid_start_x + c * 188, grid_start_y + r * 102, 172, 90)
                hover = card_rect.collidepoint(mouse_pos)

                if is_done:
                    c_bg = (255, 246, 175) if hover else (255, 238, 140)
                    c_border = (230, 160, 0) if hover else (210, 160, 20)
                else:
                    if hover:
                        c_bg = (240, 255, 240) if selected_char == "giraffe" else (255, 246, 235)
                        c_border = char_info["theme_color"]
                    else:
                        c_bg = (255, 255, 255)
                        c_border = (190, 210, 190)

                pygame.draw.rect(screen, c_bg, card_rect, border_radius=10)
                pygame.draw.rect(screen, c_border, card_rect, 3 if hover else 2, border_radius=10)

                # Number badge
                num_text = f"{t('level_title')} {lvl_idx + 1}"
                num_col = (0, 110, 0) if selected_char == "giraffe" else (190, 80, 0)
                num_surf = font_card_num.render(num_text, True, num_col)
                screen.blit(num_surf, (card_rect.x + 12, card_rect.y + 12))

                if is_done and star_icon:
                    screen.blit(star_icon, (card_rect.right - 30, card_rect.y + 10))

                # Level Name
                name_surf = font_card_name.render(lvl_name, True, (40, 40, 40))
                if name_surf.get_width() > 154:
                    short_name = lvl_name
                    while short_name and font_card_name.render(short_name + "...", True, (40, 40, 40)).get_width() > 154:
                        short_name = short_name[:-1]
                    name_surf = font_card_name.render(short_name + "...", True, (40, 40, 40))
                name_rect = name_surf.get_rect(center=(card_rect.centerx, card_rect.y + 58))
                screen.blit(name_surf, name_rect)

        # Chapter Jump Pills
        pill_start_x = (screen.get_width() - (10 * 44 + 9 * 8)) // 2
        pill_y = 612
        for ch in range(10):
            p_rect = pygame.Rect(pill_start_x + ch * 52, pill_y, 44, 30)
            is_cur = (ch == current_chapter)
            p_hover = p_rect.collidepoint(mouse_pos)
            if is_cur:
                p_bg = char_info["theme_color"]
                p_bd = (0, 60, 0) if selected_char == "giraffe" else (150, 50, 0)
                txt_col = (255, 255, 255)
            else:
                p_bg = (240, 245, 240) if p_hover else (255, 255, 255)
                p_bd = char_info["theme_color"] if p_hover else (180, 190, 180)
                txt_col = (40, 40, 40)
            pygame.draw.rect(screen, p_bg, p_rect, border_radius=6)
            pygame.draw.rect(screen, p_bd, p_rect, 2, border_radius=6)
            p_txt = font_card_num.render(str(ch + 1), True, txt_col)
            screen.blit(p_txt, p_txt.get_rect(center=p_rect.center))

        # Bottom Navigation Hint
        hint_surf = font_hint.render(t("menu_nav_hint"), True, (80, 80, 80))
        screen.blit(hint_surf, hint_surf.get_rect(center=(screen.get_width() // 2, 660)))

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
    assets["emoji_editor"] = load_image("emoji_editor.png")
    assets["emoji_custom"] = load_image("emoji_custom.png")
    assets["emoji_save"] = load_image("emoji_save.png")
    assets["emoji_play"] = load_image("emoji_play.png")

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

    # In-game top header action buttons
    btn_ingame_fs = Button(LOGICAL_WIDTH - 65, 8, 50, 32, "Win" if IS_FULLSCREEN else "Full", (110, 160, 255), (160, 205, 255), "TOGGLE_FS", font_size=18)
    btn_ingame_lang = Button(LOGICAL_WIDTH - 120, 8, 48, 32, get_lang(), (190, 225, 255), (220, 240, 255), "TOGGLE_LANG", font_size=18)
    btn_ingame_speed = Button(LOGICAL_WIDTH - 215, 8, 88, 32, "1x Normal", (255, 230, 140), (255, 245, 175), "SPEED", font_size=18)
    btn_ingame_mute = Button(LOGICAL_WIDTH - 325, 8, 102, 32, t("sound_off") if sound_manager.is_muted else t("sound_on"), (255, 180, 180) if sound_manager.is_muted else (210, 240, 210), (255, 205, 205) if sound_manager.is_muted else (230, 250, 230), "MUTE", font_size=18)

    def refresh_ingame_headers():
        btn_ingame_fs.text = "Win" if IS_FULLSCREEN else "Full"
        btn_ingame_lang.text = get_lang()
        btn_ingame_speed.text = f"1x {t('speed_normal')}" if (executor and executor.speed_mode == "NORMAL") else f"2x {t('speed_fast')}"
        btn_ingame_mute.text = t("sound_off") if sound_manager.is_muted else t("sound_on")
        btn_ingame_mute.color = (255, 180, 180) if sound_manager.is_muted else (210, 240, 210)

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
        particles.clear()
        last_player_pos = (game_state.giraffe.grid_x, game_state.giraffe.grid_y)
        return scr, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, last_player_pos

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 34)
    completed_levels = load_progress()
    # Level variables
    level = game_state = ui = executor = offset_x = offset_y = tile_size = level_assets = obstacle_types = ground_types = last_player_pos = None
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
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, last_player_pos = load_level(menu_action[1])
                refresh_ingame_headers()
                last_game_state = "IDLE"
                continue
            else:
                current_level_idx = menu_action
                state = "PLAYING"
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, last_player_pos = load_level(current_level_idx)
                refresh_ingame_headers()
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
                screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, last_player_pos = load_level(custom_lvl)
                refresh_ingame_headers()
                last_game_state = "IDLE"
                continue
            else:
                state = "MENU"
                continue
        elif state == "PLAYING":
            mouse_pos = pygame.mouse.get_pos()
            char_info = CHARACTERS[selected_character]
            transitioned = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    IS_FULLSCREEN = not IS_FULLSCREEN
                    screen = get_screen()
                    refresh_ingame_headers()

                # In-game top header buttons
                if btn_ingame_fs.handle_event(event):
                    IS_FULLSCREEN = not IS_FULLSCREEN
                    screen = get_screen()
                    refresh_ingame_headers()
                if btn_ingame_lang.handle_event(event):
                    toggle_lang()
                    ui.refresh_labels()
                    refresh_ingame_headers()
                if btn_ingame_speed.handle_event(event):
                    executor.toggle_speed()
                    refresh_ingame_headers()
                if btn_ingame_mute.handle_event(event):
                    sound_manager.toggle_mute()
                    refresh_ingame_headers()

                # UI bottom bar button actions
                action = ui.handle_event(event)
                if action in ["FORWARD", "LEFT", "RIGHT", "REPEAT"]:
                    ui.add_command(action)
                elif action == "UNDO":
                    ui.undo_command()
                elif action == "STEP":
                    executor.step_once()
                    last_game_state = "IDLE"
                elif action == "RUN":
                    executor.start()
                    last_game_state = "RUNNING"
                elif action == "STOP":
                    executor.stop()
                    last_game_state = "IDLE"
                elif action == "CLEAR":
                    ui.clear_commands()
                    game_state.reset()
                    particles.clear()
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
                            particles.clear()
                            last_game_state = "IDLE"
                        elif event.key == pygame.K_s:
                            executor.step_once()
                            last_game_state = "IDLE"
                        elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            executor.start()
                            last_game_state = "RUNNING"
                    else:
                        if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                            executor.stop()
                            last_game_state = "IDLE"

                    if event.key == pygame.K_t:
                        executor.toggle_speed()
                        refresh_ingame_headers()
                    elif event.key == pygame.K_m:
                        sound_manager.toggle_mute()
                        refresh_ingame_headers()
                    elif event.key == pygame.K_l:
                        toggle_lang()
                        ui.refresh_labels()
                        refresh_ingame_headers()

                    if event.key == pygame.K_SPACE and game_state.state == "SUCCESS":
                        particles.clear()
                        if playing_custom:
                            state = "EDITOR"
                        elif current_level_idx < len(LEVELS) - 1:
                            current_level_idx += 1
                            screen, level, game_state, ui, executor, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, last_player_pos = load_level(current_level_idx)
                            refresh_ingame_headers()
                        else:
                            state = "MENU"
                        last_game_state = "IDLE"
                        transitioned = True
                        break
                    elif event.key == pygame.K_SPACE and game_state.state == "CRASH":
                        particles.clear()
                        game_state.reset()
                        ui.clear_commands()
                        last_game_state = "IDLE"
                    elif event.key == pygame.K_ESCAPE:
                        particles.clear()
                        state = "EDITOR" if playing_custom else "MENU"
                        last_game_state = "IDLE"
                        transitioned = True
                        break
            if transitioned:
                continue

            # Update executor
            executor.update()

            # Dust particles when player moves to a new tile
            gx, gy = game_state.giraffe.grid_x, game_state.giraffe.grid_y
            if last_player_pos is not None and (gx, gy) != last_player_pos:
                px = offset_x + gx * tile_size + tile_size // 2
                py = offset_y + gy * tile_size + tile_size // 2
                particles.add_dust_puff(px, py, game_state.giraffe.direction)
                last_player_pos = (gx, gy)

            # State change triggers: sound & celebration / crash particles
            if game_state.state != last_game_state:
                if game_state.state == "SUCCESS":
                    sound_manager.play_win()
                    t_px = offset_x + level.goal_x * tile_size + tile_size // 2
                    t_py = offset_y + level.goal_y * tile_size + tile_size // 2
                    if selected_character == "giraffe":
                        particles.add_leaf_burst(t_px, t_py, 28)
                    else:
                        particles.add_cheetah_catch(t_px, t_py, 28)
                    particles.add_win_confetti(LOGICAL_WIDTH, LOGICAL_HEIGHT, 50)
                elif game_state.state == "CRASH":
                    sound_manager.play_crash()
                    c_px = offset_x + gx * tile_size + tile_size // 2
                    c_py = offset_y + gy * tile_size + tile_size // 2
                    obs_t = obstacle_types.get((gx, gy), "rock")
                    if obs_t == "water":
                        particles.add_water_splash(c_px, c_py, 24)
                    else:
                        particles.add_rock_bump(c_px, c_py, 20)
                last_game_state = game_state.state

            # Save progress when player successfully reaches the goal in campaign
            if game_state.state == "SUCCESS" and not playing_custom and current_level_idx not in completed_levels:
                completed_levels.add(current_level_idx)
                save_progress(completed_levels)

            # Draw background
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
            esc_target = t("level_editor") if playing_custom else t("menu")
            part2 = small_font.render(f"{char_info['name']}  (ESC: {esc_target})", True, (0, 0, 0))
            screen.blit(part2, (hx, 10))

            # Draw in-game header buttons
            btn_ingame_mute.draw(screen, mouse_pos)
            btn_ingame_speed.draw(screen, mouse_pos)
            btn_ingame_lang.draw(screen, mouse_pos)
            btn_ingame_fs.draw(screen, mouse_pos)

            # Grid with target sprite
            draw_grid(screen, level, offset_x, offset_y, tile_size, level_assets, obstacle_types, ground_types, target_sprite=char_info["target_sprite"])
            # Player sprite
            walk_key = char_info["character_sprite"] + "_walk"
            player_sprites = level_assets.get(walk_key) or level_assets.get(char_info["character_sprite"])
            if player_sprites:
                game_state.giraffe.draw(screen, offset_x + gx * tile_size, offset_y + gy * tile_size, tile_size, player_sprites)

            # Particles (bursts, dust, splashes, confetti)
            particles.update()
            particles.draw(screen)

            # Command buttons & code queue with active execution highlight
            active_cmd = executor.command_index if (executor.is_running or executor.command_index >= 0) else None
            tut_idx = None if playing_custom else current_level_idx
            ui.draw(screen, active_cmd_idx=active_cmd, tutorial_level=tut_idx)

            # Success Overlay
            if game_state.state == "SUCCESS":
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 255, 0, 50))
                screen.blit(overlay, (0, 0))
                if playing_custom:
                    prompt = t("press_space_editor")
                else:
                    prompt = t("press_space_next") if current_level_idx < len(LEVELS) - 1 else t("press_space_menu")
                win_str1 = f"{char_info['win_text']}   "
                win_str2 = prompt
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
                    win_surf = font.render(f"{char_info['win_text']} {prompt}", True, (255, 255, 255))
                text_rect = win_surf.get_rect(center=(screen.get_width() // 2, (screen.get_height() - UI_HEIGHT) // 2))
                bg_rect = text_rect.inflate(28, 20)
                pygame.draw.rect(screen, (0, 140, 0), bg_rect, border_radius=10)
                screen.blit(win_surf, text_rect)
            # Crash Overlay
            elif game_state.state == "CRASH":
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((255, 0, 0, 50))
                screen.blit(overlay, (0, 0))
                crash_msg = t("crash_text").format(name=char_info['name'])
                text = font.render(crash_msg, True, (255, 255, 255))
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
