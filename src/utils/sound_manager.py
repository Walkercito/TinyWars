from os.path import join

import pygame


class SoundManager:
    def __init__(self):
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        self._sfx_cache: dict[str, pygame.mixer.Sound] = {}
        self.sfx_volume: float = 1.0
        self.music_volume: float = 0.5

    def play_sfx(self, filename: str, subfolder: str = "SFX") -> None:
        """Loads (if necessary) and plays a sound effect."""
        if filename not in self._sfx_cache:
            try:
                path = join("src", "assets", "Audio", subfolder, filename)
                self._sfx_cache[filename] = pygame.mixer.Sound(path)
            except FileNotFoundError:
                print(f"Warning: Sound file '{filename}' not found at {path}")
                return

        sound = self._sfx_cache[filename]
        sound.set_volume(self.sfx_volume)
        sound.play()

    def play_music(self, filename: str, loop: int = -1) -> None:
        """Loads and plays background music."""
        try:
            path = join("src", "assets", "Audio", "Music", filename)
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(loop)
        except FileNotFoundError:
            print(f"Warning: Music file '{filename}' not found at {path}")

    def set_sfx_volume(self, volume: float) -> None:
        self.sfx_volume = max(0.0, min(volume, 1.0))

    def set_music_volume(self, volume: float) -> None:
        self.music_volume = max(0.0, min(volume, 1.0))
        pygame.mixer.music.set_volume(self.music_volume)


sound_manager = SoundManager()
