import pygame
import sys
import os
from src.levels import LEVELS
from src.game_state import GameState
from src.ui import UI, Button
from src.executor import Executor
TILE_SIZE = 80
UI_HEIGHT = 150
MARGIN = 40

LOGICAL_WIDTH = 1024
LOGICAL_HEIGHT = 768
IS_FULLSCREEN = True

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
def get_resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)
def draw_grid(surface, level, offset_x, offset_y, assets, target_sprite="tree"):
    # Draw background grid
    for y in range(level.height):
        for x in range(level.width):
            rect = pygame.Rect(offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            # Grass variations
            grass_type = (x * 7 + y * 3) % 3
            grass_img = assets.get("grass")
            if grass_type == 1 and assets.get("grass_dry"):
                grass_img = assets.get("grass_dry")
            elif grass_type == 2 and assets.get("grass_dirt"):
                grass_img = assets.get("grass_dirt")
            if grass_img:
                surface.blit(grass_img, rect)
            else:
                pygame.draw.rect(surface, (200, 255, 200), rect)
            # Obstacles
            if (x, y) in level.obstacles:
                is_water = ((x * 13 + y * 17) % 3) == 0 # 1/3 chance for water
                if is_water and assets.get("water"):
                    surface.blit(assets["water"], rect)
                elif not is_water and assets.get("rock"):
                    rock_rect = assets["rock"].get_rect(center=rect.center)
                    surface.blit(assets["rock"], rock_rect)
                else:
                    color = (50, 100, 200) if is_water else (150, 150, 150)
                    pygame.draw.rect(surface, color, rect)
            # Goal
            elif x == level.goal_x and y == level.goal_y:
                target_img = assets.get(target_sprite) or assets.get("tree")
                if target_img:
                    target_rect = target_img.get_rect(center=rect.center)
                    surface.blit(target_img, target_rect)
                else:
                    pygame.draw.circle(surface, (50, 200, 50), rect.center, TILE_SIZE // 3)
            pygame.draw.rect(surface, (150, 200, 150), rect, 2) # Grid lines
def character_select_menu(screen, assets):
    """Start menu screen to choose between Giraffe and Cheetah"""
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
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                IS_FULLSCREEN = not IS_FULLSCREEN; get_screen()
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
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 140))
            screen.blit(overlay, (0, 0))
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
        t1 = font_card_title.render("🦒 Giraffe", True, (0, 120, 0))
        screen.blit(t1, (card1_rect.centerx - t1.get_width() // 2, card1_rect.y + 20))
        if preview_giraffe and preview_tree:
            screen.blit(preview_giraffe, (card1_rect.x + 35, card1_rect.y + 75))
            arrow1 = font_card_title.render("➜", True, (0, 160, 0))
            screen.blit(arrow1, (card1_rect.x + 145, card1_rect.y + 115))
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
        t2 = font_card_title.render("🐆 Cheetah", True, (200, 80, 0))
        screen.blit(t2, (card2_rect.centerx - t2.get_width() // 2, card2_rect.y + 20))
        if preview_cheetah and preview_gazelle:
            screen.blit(preview_cheetah, (card2_rect.x + 35, card2_rect.y + 75))
            arrow2 = font_card_title.render("➜", True, (220, 100, 0))
            screen.blit(arrow2, (card2_rect.x + 145, card2_rect.y + 115))
            screen.blit(preview_gazelle, (card2_rect.x + 185, card2_rect.y + 85))
        desc2_a = font_card_desc.render("Goal: Catch the Speedy Gazelle", True, (120, 50, 0))
        desc2_b = font_card_desc.render("Fastest runner on the savanna!", True, (80, 80, 80))
        screen.blit(desc2_a, (card2_rect.centerx - desc2_a.get_width() // 2, card2_rect.y + 225))
        screen.blit(desc2_b, (card2_rect.centerx - desc2_b.get_width() // 2, card2_rect.y + 255))
        btn2.draw(screen, mouse_pos)
        pygame.display.flip()
        clock.tick(60)
def main_menu(screen, selected_char, assets):
    global IS_FULLSCREEN
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
    for i, level in enumerate(LEVELS):
        btn = Button(screen.get_width() // 2 - 300, 0, 600, 60, level.name_giraffe if selected_char == "giraffe" else level.name_cheetah, btn_color, btn_hover, i)
        buttons.append(btn)
    btn_fs = Button(screen.get_width() - 210, 70, 190, 42, "Windowed" if IS_FULLSCREEN else "Fullscreen", (100, 150, 255), (150, 200, 255), "TOGGLE_FS")
    btn_change_hero = Button(screen.get_width() - 210, 20, 190, 42, 
                             f"Switch Hero 🔄", (255, 235, 59), (255, 249, 196), "SWITCH_HERO")
    clock = pygame.time.Clock()
    scroll_y = 0
    max_scroll = max(0, len(LEVELS) * 80 - screen.get_height() + 250)
    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                IS_FULLSCREEN = not IS_FULLSCREEN; get_screen()
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
                return hero_act
            fs_act = btn_fs.handle_event(event)
            if fs_act:
                
                IS_FULLSCREEN = not IS_FULLSCREEN
                get_screen()
                btn_fs.text = "Windowed" if IS_FULLSCREEN else "Fullscreen"
                
            for btn in buttons:
                action = btn.handle_event(event)
                if action is not None:
                    return action
        # Update button positions based on scroll
        start_y = 170 + scroll_y
        for i, btn in enumerate(buttons):
            btn.rect.y = start_y + i * 80
        if bg_image:
            screen.blit(bg_image, (0, 0))
            overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 255, 255, 140))
            screen.blit(overlay, (0, 0))
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
        # Hero status badge
        hero_tag = f"Playing as {char_info['emoji']} {char_info['name']}  |  Goal: {char_info['target_name']}"
        tag_surf = font_sub.render(hero_tag, True, char_info["theme_color"])
        screen.blit(tag_surf, (35, 92))
        # Switch Hero button
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
    assets["giraffe"] = load_image("giraffe.png", (TILE_SIZE, TILE_SIZE))
    assets["giraffe_walk"] = [
        load_image("giraffe_walk1.png", (TILE_SIZE, TILE_SIZE)) or assets["giraffe"],
        load_image("giraffe_walk2.png", (TILE_SIZE, TILE_SIZE)) or assets["giraffe"]
    ]
    assets["cheetah"] = load_image("cheetah.png", (TILE_SIZE, TILE_SIZE))
    assets["cheetah_walk"] = [
        load_image("cheetah_walk1.png", (TILE_SIZE, TILE_SIZE)) or assets["cheetah"],
        load_image("cheetah_walk2.png", (TILE_SIZE, TILE_SIZE)) or assets["cheetah"]
    ]
    assets["tree"] = load_image("tree.png", (TILE_SIZE, TILE_SIZE))
    assets["gazelle"] = load_image("gazelle.png", (TILE_SIZE, TILE_SIZE))
    assets["rock"] = load_image("rock.png", (TILE_SIZE, TILE_SIZE))
    assets["grass"] = load_image("grass.jpg", (TILE_SIZE, TILE_SIZE))
    assets["grass_dry"] = load_image("grass_dry.jpg", (TILE_SIZE, TILE_SIZE))
    assets["grass_dirt"] = load_image("grass_dirt.jpg", (TILE_SIZE, TILE_SIZE))
    assets["water"] = load_image("water.jpg", (TILE_SIZE, TILE_SIZE))
    assets["menu_bg_raw"] = load_image("menu_bg.jpg")
    state = "CHAR_SELECT"
    selected_character = "giraffe"
    current_level_idx = 0
    def load_level(idx):
        level = LEVELS[idx]
        # Use fixed logical resolution
        screen_w = LOGICAL_WIDTH
        screen_h = LOGICAL_HEIGHT
        scr = screen  # Reuse existing screen
        char_info = CHARACTERS[selected_character]
        pygame.display.set_caption(f"SavannaCode - {char_info['name']} Level {idx + 1}")
        game_state = GameState(level)
        ui = UI(screen_w, screen_h)
        executor = Executor(game_state, ui)
        offset_x = (screen_w - (level.width * TILE_SIZE)) // 2
        offset_y = max(MARGIN, (screen_h - UI_HEIGHT - (level.height * TILE_SIZE)) // 2)
        return scr, level, game_state, ui, executor, offset_x, offset_y
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 40)
    small_font = pygame.font.Font(None, 34)
    # Level variables
    level = game_state = ui = executor = offset_x = offset_y = None
    while True:
        if state == "CHAR_SELECT":
            
            selected_character = character_select_menu(screen, assets)
            state = "MENU"
            continue
        elif state == "MENU":
            
            menu_action = main_menu(screen, selected_character, assets)
            if menu_action == "SWITCH_HERO":
                state = "CHAR_SELECT"
                continue
            else:
                current_level_idx = menu_action
                state = "PLAYING"
                screen, level, game_state, ui, executor, offset_x, offset_y = load_level(current_level_idx)
                continue
        elif state == "PLAYING":
            char_info = CHARACTERS[selected_character]
            transitioned = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                    IS_FULLSCREEN = not IS_FULLSCREEN; get_screen()
                if not executor.is_running:
                    action = ui.handle_event(event)
                    if action in ["FORWARD", "LEFT", "RIGHT"]:
                        ui.add_command(action)
                    elif action == "RUN":
                        executor.start()
                    elif action == "CLEAR":
                        ui.clear_commands()
                        game_state.reset()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and game_state.state == "SUCCESS":
                        if current_level_idx < len(LEVELS) - 1:
                            current_level_idx += 1
                            screen, level, game_state, ui, executor, offset_x, offset_y = load_level(current_level_idx)
                        else:
                            state = "MENU"
                        transitioned = True
                        break
                    elif event.key == pygame.K_SPACE and game_state.state == "CRASH":
                        game_state.reset()
                        ui.clear_commands()
                    elif event.key == pygame.K_ESCAPE:
                        state = "MENU"
                        transitioned = True
                        break
            if transitioned:
                continue
            # Update
            executor.update()
            # Draw
            screen.fill((135, 206, 235))
            # Header info
            title_str = f"{(level.name_giraffe if selected_character == 'giraffe' else level.name_cheetah)}  [{char_info['emoji']} {char_info['name']}]  (ESC: Menu)"
            title_surf = small_font.render(title_str, True, (0, 0, 0))
            screen.blit(title_surf, (MARGIN, 10))
            # Grid with target sprite
            draw_grid(screen, level, offset_x, offset_y, assets, target_sprite=char_info["target_sprite"])
            # Player sprite
            gx, gy = game_state.giraffe.grid_x, game_state.giraffe.grid_y
            walk_key = char_info["character_sprite"] + "_walk"
            player_sprites = assets.get(walk_key) or assets.get(char_info["character_sprite"])
            game_state.giraffe.draw(screen, offset_x + gx * TILE_SIZE, offset_y + gy * TILE_SIZE, TILE_SIZE, player_sprites)
            # Command buttons & code queue
            ui.draw(screen)
            # Success Overlay
            if game_state.state == "SUCCESS":
                overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                overlay.fill((0, 255, 0, 50))
                screen.blit(overlay, (0, 0))
                prompt = "Next Level" if current_level_idx < len(LEVELS) - 1 else "Menu"
                text = font.render(f"{char_info['win_text']} (Press SPACE for {prompt})", True, (255, 255, 255))
                text_rect = text.get_rect(center=(screen.get_width() // 2, (screen.get_height() - UI_HEIGHT) // 2))
                bg_rect = text_rect.inflate(24, 20)
                pygame.draw.rect(screen, (0, 140, 0), bg_rect, border_radius=10)
                screen.blit(text, text_rect)
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
        with open("crash.log", "w") as f:
            traceback.print_exc(file=f)
        raise
if __name__ == "__main__":
    main_wrapper()
