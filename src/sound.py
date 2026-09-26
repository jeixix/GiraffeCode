"""
Audio manager for SavannaCode / GiraffeCode.
Handles sound effect playback with graceful fallback when audio devices are absent.
"""
import os
import sys
import pygame

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

class SoundManager:
    def __init__(self):
        self.available = False
        self.sounds = {}
        self.enabled = True
        self._load_mute_pref()
        self._init_mixer()

    def _load_mute_pref(self):
        try:
            from src.i18n import load_settings
            settings = load_settings()
            if "sound_enabled" in settings:
                self.enabled = bool(settings["sound_enabled"])
        except Exception:
            pass

    def toggle_mute(self):
        self.enabled = not self.enabled
        try:
            from src.i18n import save_settings
            save_settings({"sound_enabled": self.enabled})
        except Exception:
            pass
        return self.enabled

    @property
    def is_muted(self):
        return not self.enabled

    def _init_mixer(self):
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            self.available = True
            self._load_sounds()
        except Exception as e:
            print(f"[SoundManager] Audio initialization skipped or failed: {e}")
            self.available = False

    def _load_sounds(self):
        sound_files = {
            "click": "assets/sound_click.wav",
            "step": "assets/sound_step.wav",
            "turn": "assets/sound_turn.wav",
            "win": "assets/sound_win.wav",
            "crash": "assets/sound_crash.wav",
            "error": "assets/sound_error.wav"
        }
        for name, rel_path in sound_files.items():
            full_path = get_resource_path(rel_path)
            if os.path.exists(full_path):
                try:
                    snd = pygame.mixer.Sound(full_path)
                    if name == "step":
                        snd.set_volume(0.45)
                    elif name == "turn":
                        snd.set_volume(0.5)
                    elif name == "click":
                        snd.set_volume(0.6)
                    elif name == "win":
                        snd.set_volume(0.7)
                    elif name == "crash":
                        snd.set_volume(0.65)
                    elif name == "error":
                        snd.set_volume(0.6)
                    self.sounds[name] = snd
                except Exception as e:
                    print(f"[SoundManager] Could not load {rel_path}: {e}")

    def play(self, name):
        if not self.available or not self.enabled:
            return
        snd = self.sounds.get(name)
        if snd:
            try:
                snd.play()
            except Exception:
                pass

    def play_click(self):
        self.play("click")

    def play_step(self):
        self.play("step")

    def play_turn(self):
        self.play("turn")

    def play_win(self):
        self.play("win")

    def play_crash(self):
        self.play("crash")

    def play_error(self):
        self.play("error")

# Global singleton instance for easy import across modules
sound_manager = SoundManager()
