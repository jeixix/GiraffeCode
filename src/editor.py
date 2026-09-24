"""
SavannaCode / GiraffeCode Built-in Level Editor.
Allows players to build custom levels with mandatory solvability verification before playing.
"""
import os
import sys
import json
import math
from collections import deque
import pygame
from src.levels import Level
from src.sound import sound_manager
from src.ui import Button, load_icon

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_custom_levels_path():
    try:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, "custom_levels.json")
    except Exception:
        return "custom_levels.json"

def verify_level_solvable(width, height, start_x, start_y, start_dir, goal_x, goal_y, obstacles):
    """
    Mathematical Breadth-First Search solver.
    Returns (is_solvable: bool, message: str, steps: int)
    """
    if (start_x, start_y) == (goal_x, goal_y):
        return False, "Start and Goal cannot be on the exact same tile!", 0

    obs_set = set(tuple(o) for o in obstacles)
    if (start_x, start_y) in obs_set:
        return False, "The hero start tile cannot be placed on an obstacle!", 0

    if (goal_x, goal_y) in obs_set:
        return False, "The goal tile cannot be placed on an obstacle!", 0

    start_state = (start_x, start_y, start_dir)
    queue = deque([(start_state, 0)])
    visited = {start_state}

    while queue:
        (x, y, d), steps = queue.popleft()
        if (x, y) == (goal_x, goal_y):
            return True, f"Level is solvable! (Optimal path: {steps} steps)", steps

        # 1. Turn Left
        nl = (x, y, (d - 1) % 4)
        if nl not in visited:
            visited.add(nl)
            queue.append((nl, steps + 1))

        # 2. Turn Right
        nr = (x, y, (d + 1) % 4)
        if nr not in visited:
            visited.add(nr)
            queue.append((nr, steps + 1))

        # 3. Move Forward
        dx, dy = 0, 0
        if d == 0: dy = -1   # Up
        elif d == 1: dx = 1  # Right
        elif d == 2: dy = 1  # Down
        elif d == 3: dx = -1 # Left

        nx, ny = x + dx, y + dy
        if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in obs_set:
            nf = (nx, ny, d)
            if nf not in visited:
                visited.add(nf)
                queue.append((nf, steps + 1))

    return False, "Unsolvable level! No path exists from start to goal. Remove some obstacles.", 0

def load_custom_levels():
    path = get_custom_levels_path()
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        print(f"[LevelEditor] Error loading custom levels: {e}")
    return []

def save_custom_levels(levels_list):
    path = get_custom_levels_path()
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(levels_list, f, indent=2)
        return True
    except Exception as e:
        print(f"[LevelEditor] Error saving custom levels: {e}")
        return False

def custom_dict_to_level(data):
    """Converts a custom level dictionary into a playable Level object."""
    obstacles = [tuple(o) for o in data.get("obstacles", [])]
    lvl = Level(
        name=data.get("name", "Custom Level"),
        width=data.get("width", 7),
        height=data.get("height", 7),
        start_x=data.get("start_x", 0),
        start_y=data.get("start_y", 0),
        start_dir=data.get("start_dir", 1),
        goal_x=data.get("goal_x", 6),
        goal_y=data.get("goal_y", 6),
        obstacles=obstacles
    )
    lvl.name_giraffe = lvl.name
    lvl.name_cheetah = lvl.name
    lvl.is_custom = True
    lvl.obstacle_types = data.get("obstacle_types", {})
    return lvl

def level_editor_screen(screen, assets, selected_char, get_screen_fn, is_fullscreen_getter, is_fullscreen_setter):
    """
    Main interactive Level Editor loop.
    Returns:
      - ("MENU", None) -> Return to main menu
      - ("PLAY_CUSTOM", Level) -> Solvability verified, launch game loop with custom level!
    """
    clock = pygame.time.Clock()
    font_title = pygame.font.Font(None, 42)
    font_ui = pygame.font.Font(None, 24)
    font_ui_bold = pygame.font.Font(None, 28)
    font_toast = pygame.font.Font(None, 28)

    # Load background
    bg_image = None
    bg_path = get_resource_path("assets/menu_bg.jpg")
    if os.path.exists(bg_path):
        try:
            raw_bg = pygame.image.load(bg_path).convert()
            bg_image = pygame.transform.scale(raw_bg, screen.get_size())
        except Exception:
            pass

    menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    menu_overlay.fill((255, 255, 255, 140))

    # Saved levels list
    saved_levels = load_custom_levels()
    current_level_idx = 0 if saved_levels else -1

    # Current level state
    def get_default_level_state(idx=0):
        return {
            "name": f"My Level {idx + 1}",
            "width": 7,
            "height": 7,
            "start_x": 0,
            "start_y": 3,
            "start_dir": 1,  # 0: Up, 1: Right, 2: Down, 3: Left
            "goal_x": 6,
            "goal_y": 3,
            "obstacles": [(2, 2), (2, 3), (2, 4), (4, 1), (4, 2), (4, 3)],
            "obstacle_types": {
                "2,2": "rock", "2,3": "rock", "2,4": "rock",
                "4,1": "water", "4,2": "water", "4,3": "water"
            }
        }

    if saved_levels:
        state = dict(saved_levels[0])
        # ensure obstacle_types exists
        if "obstacle_types" not in state:
            state["obstacle_types"] = {f"{o[0]},{o[1]}": "rock" for o in state.get("obstacles", [])}
    else:
        state = get_default_level_state(0)

    # Editor tool: "START", "GOAL", "ROCK", "WATER", "ERASE"
    current_tool = "ROCK"

    # Feedback toast
    toast_msg = "Tip: Build your level, then click 'Test & Play'!"
    toast_color = (40, 100, 40)
    toast_bg = (220, 255, 220)
    toast_expiry = pygame.time.get_ticks() + 4000

    def show_toast(msg, is_error=False, duration_ms=4500):
        nonlocal toast_msg, toast_color, toast_bg, toast_expiry
        toast_msg = msg
        toast_color = (180, 20, 20) if is_error else (20, 120, 20)
        toast_bg = (255, 225, 225) if is_error else (225, 255, 225)
        toast_expiry = pygame.time.get_ticks() + duration_ms

    # Setup Buttons
    btn_menu = Button(20, 15, 140, 40, "Back to Menu", (220, 220, 220), (240, 240, 240), "MENU")
    btn_fs = Button(screen.get_width() - 170, 15, 150, 40,
                    "Windowed" if is_fullscreen_getter() else "Fullscreen",
                    (100, 150, 255), (150, 200, 255), "TOGGLE_FS")

    # Tool selection buttons
    tool_buttons = [
        Button(20, 140, 150, 46, "Hero Start", (255, 235, 140), (255, 245, 180), "TOOL_START"),
        Button(20, 195, 150, 46, "Goal Target", (140, 240, 140), (180, 255, 180), "TOOL_GOAL"),
        Button(20, 250, 150, 46, "Rock Obstacle", (210, 210, 210), (230, 230, 230), "TOOL_ROCK"),
        Button(20, 305, 150, 46, "Water Hazard", (160, 210, 255), (190, 230, 255), "TOOL_WATER"),
        Button(20, 360, 150, 46, "Eraser", (255, 190, 190), (255, 215, 215), "TOOL_ERASE"),
    ]

    # Grid size controls
    btn_w_minus = Button(20, 435, 36, 36, "-", (200, 200, 200), (220, 220, 220), "W_MINUS")
    btn_w_plus = Button(134, 435, 36, 36, "+", (200, 200, 200), (220, 220, 220), "W_PLUS")
    btn_h_minus = Button(20, 480, 36, 36, "-", (200, 200, 200), (220, 220, 220), "H_MINUS")
    btn_h_plus = Button(134, 480, 36, 36, "+", (200, 200, 200), (220, 220, 220), "H_PLUS")

    # Level Management Buttons
    btn_prev = Button(20, 545, 45, 36, "<", (210, 210, 210), (230, 230, 230), "PREV_LEVEL")
    btn_next = Button(125, 545, 45, 36, ">", (210, 210, 210), (230, 230, 230), "NEXT_LEVEL")
    btn_new = Button(20, 590, 150, 38, "+ New Level", (255, 220, 130), (255, 235, 170), "NEW_LEVEL")
    btn_clear = Button(20, 636, 150, 38, "Clear Grid", (230, 230, 230), (245, 245, 245), "CLEAR_GRID")
    btn_del = Button(20, 682, 150, 38, "Delete Level", (255, 160, 160), (255, 190, 190), "DEL_LEVEL")

    # Center Action Buttons (bottom bar)
    btn_test_play = Button(screen.get_width() // 2 - 210, screen.get_height() - 75, 200, 55,
                           "Test & Play ▶", (100, 230, 100), (140, 255, 140), "TEST_PLAY")
    btn_save = Button(screen.get_width() // 2 + 10, screen.get_height() - 75, 190, 55,
                      "Save Level 💾", (255, 200, 80), (255, 220, 120), "SAVE_LEVEL")

    all_ui_buttons = tool_buttons + [
        btn_menu, btn_fs,
        btn_w_minus, btn_w_plus, btn_h_minus, btn_h_plus,
        btn_prev, btn_next, btn_new, btn_clear, btn_del,
        btn_test_play, btn_save
    ]

    mouse_down = False
    hero_char_key = "giraffe" if selected_char == "giraffe" else "cheetah"
    target_char_key = "tree" if selected_char == "giraffe" else "gazelle"

    while True:
        mouse_pos = pygame.mouse.get_pos()
        now = pygame.time.get_ticks()

        # Dynamic Grid Dimensions & Placement
        grid_w_count = state["width"]
        grid_h_count = state["height"]
        avail_w = screen.get_width() - 250
        avail_h = screen.get_height() - 210
        tile_size = max(32, min(68, avail_w // grid_w_count, avail_h // grid_h_count))
        board_pixel_w = grid_w_count * tile_size
        board_pixel_h = grid_h_count * tile_size
        grid_start_x = 210 + (avail_w - board_pixel_w) // 2
        grid_start_y = 90 + (avail_h - board_pixel_h) // 2
        grid_rect = pygame.Rect(grid_start_x, grid_start_y, board_pixel_w, board_pixel_h)

        def screen_to_cell(pos):
            x, y = pos
            if grid_rect.collidepoint(x, y):
                col = (x - grid_start_x) // tile_size
                row = (y - grid_start_y) // tile_size
                return col, row
            return None

        def apply_tool(col, row):
            nonlocal current_tool
            # Obstacles list as sets for easy manipulation
            obs_map = state.get("obstacle_types", {})
            obs_set = set((int(o[0]), int(o[1])) for o in state.get("obstacles", []))
            key = f"{col},{row}"

            if current_tool == "START":
                if (col, row) == (state["goal_x"], state["goal_y"]):
                    return
                if (col, row) == (state["start_x"], state["start_y"]):
                    # Click again to rotate start direction!
                    state["start_dir"] = (state["start_dir"] + 1) % 4
                    sound_manager.play_turn()
                else:
                    state["start_x"] = col
                    state["start_y"] = row
                    # clear any obstacle on this tile
                    obs_set.discard((col, row))
                    obs_map.pop(key, None)
                    sound_manager.play_click()

            elif current_tool == "GOAL":
                if (col, row) == (state["start_x"], state["start_y"]):
                    return
                state["goal_x"] = col
                state["goal_y"] = row
                # clear any obstacle on this tile
                obs_set.discard((col, row))
                obs_map.pop(key, None)
                sound_manager.play_click()

            elif current_tool in ("ROCK", "WATER"):
                if (col, row) in ((state["start_x"], state["start_y"]), (state["goal_x"], state["goal_y"])):
                    return
                obs_set.add((col, row))
                obs_map[key] = "rock" if current_tool == "ROCK" else "water"
                sound_manager.play_click()

            elif current_tool == "ERASE":
                obs_set.discard((col, row))
                obs_map.pop(key, None)
                sound_manager.play_click()

            state["obstacles"] = [list(o) for o in obs_set]
            state["obstacle_types"] = obs_map

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                is_fullscreen_setter(not is_fullscreen_getter())
                screen = get_screen_fn()
                if bg_image:
                    bg_image = pygame.transform.scale(raw_bg, screen.get_size())
                menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                menu_overlay.fill((255, 255, 255, 140))
                btn_fs.text = "Windowed" if is_fullscreen_getter() else "Fullscreen"
                btn_fs.rect.x = screen.get_width() - 170
                btn_test_play.rect.x = screen.get_width() // 2 - 210
                btn_save.rect.x = screen.get_width() // 2 + 10

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click
                    mouse_down = True
                    cell = screen_to_cell(event.pos)
                    if cell:
                        apply_tool(cell[0], cell[1])
                elif event.button == 3: # Right click -> Quick eraser!
                    cell = screen_to_cell(event.pos)
                    if cell:
                        prev_tool = current_tool
                        current_tool = "ERASE"
                        apply_tool(cell[0], cell[1])
                        current_tool = prev_tool

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False

            elif event.type == pygame.MOUSEMOTION:
                if mouse_down and current_tool in ("ROCK", "WATER", "ERASE"):
                    cell = screen_to_cell(event.pos)
                    if cell:
                        apply_tool(cell[0], cell[1])

            # UI Button handling
            for btn in all_ui_buttons:
                act = btn.handle_event(event)
                if not act:
                    continue

                if act == "MENU":
                    sound_manager.play_click()
                    return "MENU", None

                elif act == "TOGGLE_FS":
                    is_fullscreen_setter(not is_fullscreen_getter())
                    screen = get_screen_fn()
                    if bg_image:
                        bg_image = pygame.transform.scale(raw_bg, screen.get_size())
                    menu_overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                    menu_overlay.fill((255, 255, 255, 140))
                    btn_fs.text = "Windowed" if is_fullscreen_getter() else "Fullscreen"
                    btn_fs.rect.x = screen.get_width() - 170
                    btn_test_play.rect.x = screen.get_width() // 2 - 210
                    btn_save.rect.x = screen.get_width() // 2 + 10

                elif act == "TOOL_START":
                    current_tool = "START"
                    sound_manager.play_click()
                elif act == "TOOL_GOAL":
                    current_tool = "GOAL"
                    sound_manager.play_click()
                elif act == "TOOL_ROCK":
                    current_tool = "ROCK"
                    sound_manager.play_click()
                elif act == "TOOL_WATER":
                    current_tool = "WATER"
                    sound_manager.play_click()
                elif act == "TOOL_ERASE":
                    current_tool = "ERASE"
                    sound_manager.play_click()

                elif act == "W_MINUS":
                    if state["width"] > 4:
                        state["width"] -= 1
                        # clamp start, goal, and obstacles
                        state["start_x"] = min(state["start_x"], state["width"] - 1)
                        state["goal_x"] = min(state["goal_x"], state["width"] - 1)
                        state["obstacles"] = [o for o in state["obstacles"] if o[0] < state["width"]]
                        sound_manager.play_click()
                elif act == "W_PLUS":
                    if state["width"] < 10:
                        state["width"] += 1
                        sound_manager.play_click()
                elif act == "H_MINUS":
                    if state["height"] > 4:
                        state["height"] -= 1
                        state["start_y"] = min(state["start_y"], state["height"] - 1)
                        state["goal_y"] = min(state["goal_y"], state["height"] - 1)
                        state["obstacles"] = [o for o in state["obstacles"] if o[1] < state["height"]]
                        sound_manager.play_click()
                elif act == "H_PLUS":
                    if state["height"] < 10:
                        state["height"] += 1
                        sound_manager.play_click()

                elif act == "CLEAR_GRID":
                    state["obstacles"] = []
                    state["obstacle_types"] = {}
                    state["start_x"], state["start_y"] = 0, 0
                    state["goal_x"], state["goal_y"] = state["width"] - 1, state["height"] - 1
                    sound_manager.play_click()
                    show_toast("Cleared all obstacles from grid.")

                elif act == "PREV_LEVEL":
                    if saved_levels and current_level_idx > 0:
                        current_level_idx -= 1
                        state = dict(saved_levels[current_level_idx])
                        sound_manager.play_click()
                        show_toast(f"Loaded '{state['name']}'")
                elif act == "NEXT_LEVEL":
                    if saved_levels and current_level_idx < len(saved_levels) - 1:
                        current_level_idx += 1
                        state = dict(saved_levels[current_level_idx])
                        sound_manager.play_click()
                        show_toast(f"Loaded '{state['name']}'")

                elif act == "NEW_LEVEL":
                    current_level_idx = len(saved_levels)
                    state = get_default_level_state(current_level_idx)
                    sound_manager.play_click()
                    show_toast("Created fresh new level draft!")

                elif act == "DEL_LEVEL":
                    if saved_levels and 0 <= current_level_idx < len(saved_levels):
                        del saved_levels[current_level_idx]
                        save_custom_levels(saved_levels)
                        sound_manager.play_click()
                        if saved_levels:
                            current_level_idx = max(0, min(current_level_idx, len(saved_levels) - 1))
                            state = dict(saved_levels[current_level_idx])
                        else:
                            current_level_idx = -1
                            state = get_default_level_state(0)
                        show_toast("Deleted custom level.")

                elif act in ("SAVE_LEVEL", "TEST_PLAY"):
                    # MANDATORY SOLVABILITY CHECK!
                    solvable, message, steps = verify_level_solvable(
                        state["width"], state["height"],
                        state["start_x"], state["start_y"], state["start_dir"],
                        state["goal_x"], state["goal_y"],
                        state["obstacles"]
                    )

                    if not solvable:
                        # PLAY CANNOT PROCEED IF UNSOLVABLE!
                        sound_manager.play_error()
                        show_toast(f"Cannot Play: {message}", is_error=True, duration_ms=5500)
                    else:
                        # SAVE LEVEL AND PERMIT PLAY
                        sound_manager.play_win()
                        # Update or append to saved_levels
                        level_dict = dict(state)
                        if saved_levels and 0 <= current_level_idx < len(saved_levels):
                            saved_levels[current_level_idx] = level_dict
                        else:
                            saved_levels.append(level_dict)
                            current_level_idx = len(saved_levels) - 1
                        save_custom_levels(saved_levels)

                        if act == "SAVE_LEVEL":
                            show_toast(f"Saved '{state['name']}'! {message}")
                        else:
                            # Launch custom level directly in gameplay!
                            lvl_obj = custom_dict_to_level(level_dict)
                            return "PLAY_CUSTOM", lvl_obj

        # ---------------- RENDER ----------------
        if bg_image:
            screen.blit(bg_image, (0, 0))
            screen.blit(menu_overlay, (0, 0))
        else:
            screen.fill((135, 206, 235))

        # Top Bar
        top_bar = pygame.Surface((screen.get_width(), 70))
        top_bar.fill((255, 255, 255))
        pygame.draw.line(top_bar, (190, 190, 190), (0, 69), (screen.get_width(), 69), 2)
        screen.blit(top_bar, (0, 0))

        title = font_title.render("🛠️ Level Editor", True, (0, 100, 0))
        screen.blit(title, (180, 16))

        # Level name badge in header
        level_display_name = state.get("name", "Custom Level")
        lvl_lbl = font_ui_bold.render(f"Editing: {level_display_name}", True, (50, 50, 50))
        screen.blit(lvl_lbl, (460, 24))

        # Left Sidebar Panel
        sidebar = pygame.Surface((190, screen.get_height() - 70))
        sidebar.fill((248, 248, 248))
        pygame.draw.line(sidebar, (200, 200, 200), (189, 0), (189, sidebar.get_height()), 2)
        screen.blit(sidebar, (0, 70))

        # Section Labels
        s_tool = font_ui_bold.render("1. Tools", True, (60, 60, 60))
        screen.blit(s_tool, (20, 110))

        s_size = font_ui_bold.render("2. Grid Size", True, (60, 60, 60))
        screen.blit(s_size, (20, 410))

        s_mgm = font_ui_bold.render("3. Levels", True, (60, 60, 60))
        screen.blit(s_mgm, (20, 520))

        # Width and Height values
        w_lbl = font_ui.render(f"W: {state['width']}", True, (30, 30, 30))
        h_lbl = font_ui.render(f"H: {state['height']}", True, (30, 30, 30))
        screen.blit(w_lbl, (68, 444))
        screen.blit(h_lbl, (68, 489))

        # Level index indicator
        idx_txt = f"{current_level_idx + 1}/{len(saved_levels)}" if saved_levels else "Draft"
        idx_lbl = font_ui.render(idx_txt, True, (40, 40, 40))
        screen.blit(idx_lbl, (75, 554))

        # Highlight currently selected tool button
        for btn in tool_buttons:
            is_active = (
                (btn.action == "TOOL_START" and current_tool == "START") or
                (btn.action == "TOOL_GOAL" and current_tool == "GOAL") or
                (btn.action == "TOOL_ROCK" and current_tool == "ROCK") or
                (btn.action == "TOOL_WATER" and current_tool == "WATER") or
                (btn.action == "TOOL_ERASE" and current_tool == "ERASE")
            )
            if is_active:
                pygame.draw.rect(screen, (255, 140, 0), btn.rect.inflate(6, 6), 3, border_radius=8)
            btn.draw(screen, mouse_pos)

        # Draw remaining buttons
        btn_menu.draw(screen, mouse_pos)
        btn_fs.draw(screen, mouse_pos)
        btn_w_minus.draw(screen, mouse_pos)
        btn_w_plus.draw(screen, mouse_pos)
        btn_h_minus.draw(screen, mouse_pos)
        btn_h_plus.draw(screen, mouse_pos)
        btn_prev.draw(screen, mouse_pos)
        btn_next.draw(screen, mouse_pos)
        btn_new.draw(screen, mouse_pos)
        btn_clear.draw(screen, mouse_pos)
        btn_del.draw(screen, mouse_pos)
        btn_test_play.draw(screen, mouse_pos)
        btn_save.draw(screen, mouse_pos)

        # ---------------- DRAW GRID ----------------
        # Grid frame shadow/background
        pygame.draw.rect(screen, (220, 230, 220), grid_rect.inflate(16, 16), border_radius=12)
        pygame.draw.rect(screen, (160, 180, 160), grid_rect.inflate(16, 16), 3, border_radius=12)

        # Fetch loaded sprites from assets
        grass_img = assets.get("grass")
        rock_img = assets.get("rock")
        water_img = assets.get("water")
        hero_img = assets.get(hero_char_key)
        target_img = assets.get(target_char_key)

        obs_set = set((int(o[0]), int(o[1])) for o in state.get("obstacles", []))
        obs_map = state.get("obstacle_types", {})

        hovered_cell = screen_to_cell(mouse_pos)

        for r in range(grid_h_count):
            for c in range(grid_w_count):
                cell_rect = pygame.Rect(grid_start_x + c * tile_size, grid_start_y + r * tile_size, tile_size, tile_size)

                # 1. Base grass
                if grass_img:
                    scaled_grass = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    screen.blit(scaled_grass, cell_rect)
                else:
                    pygame.draw.rect(screen, (130, 200, 120), cell_rect)

                # 2. Obstacle (Rock or Water)
                if (c, r) in obs_set:
                    t_type = obs_map.get(f"{c},{r}", "rock")
                    if t_type == "water":
                        if water_img:
                            scaled_water = pygame.transform.scale(water_img, (tile_size, tile_size))
                            screen.blit(scaled_water, cell_rect)
                        else:
                            pygame.draw.rect(screen, (50, 120, 230), cell_rect)
                    else:
                        if rock_img:
                            scaled_rock = pygame.transform.scale(rock_img, (tile_size, tile_size))
                            screen.blit(scaled_rock, cell_rect)
                        else:
                            pygame.draw.rect(screen, (120, 120, 120), cell_rect)

                # 3. Start Tile (Hero)
                if (c, r) == (state["start_x"], state["start_y"]):
                    # Golden start halo
                    pygame.draw.rect(screen, (255, 230, 80, 140), cell_rect, 4, border_radius=6)
                    if hero_img:
                        scaled_hero = pygame.transform.scale(hero_img, (tile_size - 8, tile_size - 8))
                        screen.blit(scaled_hero, (cell_rect.x + 4, cell_rect.y + 4))

                    # Direction indicator arrow
                    dir_arrows = ["⬆️", "➡️", "⬇️", "⬅️"]
                    arr_txt = font_ui_bold.render(dir_arrows[state["start_dir"]], True, (255, 0, 0))
                    screen.blit(arr_txt, (cell_rect.right - 24, cell_rect.top + 2))

                # 4. Goal Tile (Target)
                if (c, r) == (state["goal_x"], state["goal_y"]):
                    # Red target halo
                    pygame.draw.rect(screen, (255, 100, 100, 140), cell_rect, 4, border_radius=6)
                    if target_img:
                        scaled_target = pygame.transform.scale(target_img, (tile_size - 8, tile_size - 8))
                        screen.blit(scaled_target, (cell_rect.x + 4, cell_rect.y + 4))

                # Grid border
                pygame.draw.rect(screen, (160, 200, 160), cell_rect, 1)

                # Cell hover highlight
                if hovered_cell == (c, r):
                    pygame.draw.rect(screen, (255, 255, 255, 100), cell_rect, 3)

        # ---------------- DRAW TOAST NOTIFICATION ----------------
        if now < toast_expiry and toast_msg:
            lines = toast_msg.split("\n")
            line_surfs = [font_toast.render(l, True, toast_color) for l in lines]
            tw = max(s.get_width() for s in line_surfs) + 32
            th = sum(s.get_height() for s in line_surfs) + 16
            t_rect = pygame.Rect(screen.get_width() // 2 - tw // 2, 78, tw, th)

            pygame.draw.rect(screen, toast_bg, t_rect, border_radius=10)
            pygame.draw.rect(screen, toast_color, t_rect, 2, border_radius=10)

            cur_ty = t_rect.y + 8
            for s in line_surfs:
                screen.blit(s, (t_rect.centerx - s.get_width() // 2, cur_ty))
                cur_ty += s.get_height()

        pygame.display.flip()
        clock.tick(60)
