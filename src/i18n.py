"""
Internationalization (i18n) module for SavannaCode / GiraffeCode.
Provides bilingual support (English and Spanish) for UI commands, tutorials,
character dialogues, and menu navigation.
"""
import os
import sys
import json
import locale

def get_base_data_dir():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _detect_default_language():
    try:
        loc = locale.getdefaultlocale()[0]
        if loc and loc.lower().startswith("es"):
            return "ES"
    except Exception:
        pass
    return "EN"

STRINGS = {
    "EN": {
        "lang_name": "English",
        "lang_flag": "🇬🇧 EN",
        "windowed": "Windowed",
        "fullscreen": "Fullscreen",
        "switch_hero": "Switch Hero",
        "level_editor": "Level Editor",
        "play_custom": "Play Custom",
        "menu": "Menu",
        "back_to_menu": "Back to Menu",
        "playing_as": "Playing as: ",
        "goal": "Goal: ",
        "completed": "Completed: ",
        "sound_on": "Sound: ON",
        "sound_off": "Sound: OFF",
        "speed_label": "Speed: ",
        "speed_normal": "Normal",
        "speed_fast": "Turbo",
        "cmd_forward": "FORWARD",
        "cmd_left": "LEFT",
        "cmd_right": "RIGHT",
        "cmd_repeat": "REPEAT",
        "cmd_undo": "UNDO",
        "cmd_clear": "CLEAR",
        "cmd_run": "RUN",
        "cmd_stop": "STOP",
        "cmd_step": "STEP",
        "pill_forward": "FWD",
        "pill_left": "LFT",
        "pill_right": "RGT",
        "pill_repeat": "REP",
        "hint_title": "Keyboard shortcuts:",
        "hint_fwd": "Up/W : Forward     Backspace : Undo",
        "hint_turn": "Left/A : Left      Enter : Run/Stop",
        "hint_step": "Right/D : Right    S : Step",
        "hint_rep": "R : Repeat         C : Clear all",
        "hint_fs": "F11 : Fullscreen   M : Mute",
        "hint_speed": "T : Speed (1x/2x)  L : Language",
        "win_giraffe": "YAY! You got the leaves!",
        "win_cheetah": "SPEEDY! You caught the gazelle!",
        "press_space_next": "   (Press SPACE for Next Level)",
        "press_space_menu": "   (Press SPACE for Menu)",
        "press_space_editor": "   (Press SPACE for Editor)",
        "crash_text": "Oh no! {name} hit an obstacle! (Press SPACE to retry)",
        "chapter": "Chapter",
        "prev_chapter": "< Prev",
        "next_chapter": "Next >",
        "empty_queue_hint": "Click command buttons below or use W/A/D to code!",
        "tut_step1": "Click FORWARD to move your animal!",
        "tut_step2": "Now click RUN to execute your code!",
        "tut_turn": "Use LEFT or RIGHT to turn towards your goal!",
        "tut_repeat": "Use REPEAT to loop your commands and write shorter code!",
        "choose_hero_title": "Choose Your Savanna Hero!",
        "choose_hero_sub": "Who would you like to guide today?",
        "hero_giraffe": "Giraffe",
        "hero_cheetah": "Cheetah",
        "card_goal_giraffe": "Goal: Reach the Acacia Tree",
        "card_desc_giraffe": "Get the tasty leaves!",
        "card_btn_giraffe": "Play as Giraffe",
        "card_goal_cheetah": "Goal: Catch the Speedy Gazelle",
        "card_desc_cheetah": "Fastest runner on the savanna!",
        "card_btn_cheetah": "Play as Cheetah",
        "level_title": "Level",
        "world_1": "1. Sunny Meadow",
        "world_2": "2. Waterhole Oasis",
        "world_3": "3. Acacia Grove",
        "world_4": "4. Rocky Ridge",
        "world_5": "5. River Crossing",
        "world_6": "6. Savanna Labyrinth",
        "world_7": "7. Muddy Trails",
        "world_8": "8. Deep Savanna",
        "world_9": "9. Expert Paths",
        "world_10": "10. Savanna Master",
        "menu_nav_hint": "Click any level to play! Use Left/Right keys or chapter pills below to browse."
    },
    "ES": {
        "lang_name": "Español",
        "lang_flag": "ES",
        "windowed": "Ventana",
        "fullscreen": "Pantalla",
        "switch_hero": "Cambiar Héroe",
        "level_editor": "Editor",
        "play_custom": "Mis Niveles",
        "menu": "Menú",
        "back_to_menu": "Volver al Menú",
        "playing_as": "Jugando como: ",
        "goal": "Objetivo: ",
        "completed": "Completados: ",
        "sound_on": "Sonido: SÍ",
        "sound_off": "Sonido: NO",
        "speed_label": "Velocidad: ",
        "speed_normal": "Normal",
        "speed_fast": "Rápido",
        "cmd_forward": "AVANZAR",
        "cmd_left": "IZQUIERDA",
        "cmd_right": "DERECHA",
        "cmd_repeat": "REPETIR",
        "cmd_undo": "DESHACER",
        "cmd_clear": "BORRAR",
        "cmd_run": "EJECUTAR",
        "cmd_stop": "PARAR",
        "cmd_step": "PASO",
        "pill_forward": "AVZ",
        "pill_left": "IZQ",
        "pill_right": "DER",
        "pill_repeat": "REP",
        "hint_title": "Atajos de teclado:",
        "hint_fwd": "Arriba/W : Avanzar    Borrar : Deshacer",
        "hint_turn": "Izq/A : Girar Izq    Enter : Ejecutar/Parar",
        "hint_step": "Der/D : Girar Der    S : Paso a paso",
        "hint_rep": "R : Repetir          C : Borrar todo",
        "hint_fs": "F11 : Pantalla       M : Silenciar",
        "hint_speed": "T : Velocidad        L : Idioma",
        "win_giraffe": "¡GENIAL! ¡Alcanzaste las hojas!",
        "win_cheetah": "¡VELOZ! ¡Atrapaste a la gacela!",
        "press_space_next": "   (Presiona ESPACIO para Siguiente Nivel)",
        "press_space_menu": "   (Presiona ESPACIO para el Menú)",
        "press_space_editor": "   (Presiona ESPACIO para el Editor)",
        "crash_text": "¡Oh no! ¡{name} chocó con un obstáculo! (ESPACIO para reintentar)",
        "chapter": "Capítulo",
        "prev_chapter": "< Ant.",
        "next_chapter": "Sig. >",
        "empty_queue_hint": "¡Usa los botones de abajo o W/A/D para programar!",
        "tut_step1": "¡Presiona AVANZAR para mover tu animal!",
        "tut_step2": "¡Ahora presiona EJECUTAR para ver tu código!",
        "tut_turn": "¡Usa IZQUIERDA o DERECHA para girar hacia tu objetivo!",
        "tut_repeat": "¡Usa REPETIR para crear bucles y escribir menos código!",
        "choose_hero_title": "¡Elige tu Héroe de la Sabana!",
        "choose_hero_sub": "¿A quién te gustaría guiar hoy?",
        "hero_giraffe": "Jirafa",
        "hero_cheetah": "Guepardo",
        "card_goal_giraffe": "Objetivo: Alcanzar la Acacia",
        "card_desc_giraffe": "¡Consigue las ricas hojas!",
        "card_btn_giraffe": "Jugar como Jirafa",
        "card_goal_cheetah": "Objetivo: Atrapar la Gacela",
        "card_desc_cheetah": "¡El más veloz de la sabana!",
        "card_btn_cheetah": "Jugar como Guepardo",
        "level_title": "Nivel",
        "world_1": "1. Pradera Soleada",
        "world_2": "2. Oasis del Río",
        "world_3": "3. Bosque de Acacias",
        "world_4": "4. Cordillera Rocosa",
        "world_5": "5. Cruce del Río",
        "world_6": "6. Laberinto Sabana",
        "world_7": "7. Senderos de Fango",
        "world_8": "8. Sabana Profunda",
        "world_9": "9. Rutas de Expertos",
        "world_10": "10. Maestro Sabana",
        "menu_nav_hint": "¡Elige un nivel para jugar! Usa las flechas o botones de abajo para explorar."
    }
}

CURRENT_LANG = _detect_default_language()

def _get_settings_path():
    try:
        return os.path.join(get_base_data_dir(), "settings.json")
    except Exception:
        return "settings.json"

def load_settings():
    global CURRENT_LANG
    try:
        path = _get_settings_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                lang = data.get("language")
                if lang in STRINGS:
                    CURRENT_LANG = lang
                return data
    except Exception:
        pass
    return {"language": CURRENT_LANG}

def save_settings(extra_data=None):
    try:
        path = _get_settings_path()
        data = {"language": CURRENT_LANG}
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception:
                pass
        data["language"] = CURRENT_LANG
        if extra_data:
            data.update(extra_data)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to save settings: {e}")

# Load saved settings at startup
load_settings()

def get_lang():
    return CURRENT_LANG

def set_lang(lang):
    global CURRENT_LANG
    if lang in STRINGS:
        CURRENT_LANG = lang
        save_settings()

def toggle_lang():
    new_lang = "ES" if CURRENT_LANG == "EN" else "EN"
    set_lang(new_lang)
    return new_lang

def t(key, default=None):
    """Retrieve translated string for the current active language."""
    lang_dict = STRINGS.get(CURRENT_LANG, STRINGS["EN"])
    if key in lang_dict:
        return lang_dict[key]
    # Fallback to English if missing in target
    if key in STRINGS["EN"]:
        return STRINGS["EN"][key]
    return default if default is not None else key
