from pathlib import Path
from game.shared.color import Color
import pygame
pygame.mixer.init()

FRAME_RATE = 50
MAX_X = 950
MAX_Y = 600
FONT_SIZE = 20
PLAYER_SIZE = 15
MAX_PLAYER_X = 400
CENTER = "center"
COLS = 60
ROWS = 40
CAPTION = "GALAXIA"
WHITE = Color(255, 255, 255)

SPLASH_IMAGE = Path(__file__).parent.parent / "assets/images/splash.png" 
SPLASH_INSTRUCTION = Path(__file__).parent.parent / "assets/images/splash_inst.png"
ACTOR_IMAGE = Path(__file__).parent.parent / "assets/images/hero.png"
ENEMY_IMAGE = Path(__file__).parent.parent / "assets/images/enemy.png"
ENEMY_IMAGE1 = Path(__file__).parent.parent / "assets/images/enemy1.png"
ENEMY_IMAGE2 = Path(__file__).parent.parent / "assets/images/enemy2.png"
ENEMY_IMAGE3 = Path(__file__).parent.parent / "assets/images/enemy3.png"


BACKGROUND_IMAGE = Path(__file__).parent.parent /"assets/images/background.png"
LOGO_IMAGE = Path(__file__).parent.parent / "assets/images/logo.png"
BULLET_IMAGE = Path(__file__).parent.parent / "assets/images/bullet.png"
BULLET_ENEMY_IMAGE = Path(__file__).parent.parent / "assets/images/bullet_enemy.png"

# Sounds for the game
ACTOR_SOUND = Path(__file__).parent.parent / "assets/sounds/actor_shoot_sound.wav"
BACKGROUND_SOUND = Path(__file__).parent.parent / "assets/sounds/background_sound.wav"
TITLE_MUSIC = Path(__file__).parent.parent / "assets/sounds/title_music.wav"
ENEMY_SHOT = pygame.mixer.Sound(Path(__file__).parent.parent / "assets/sounds/shotdown.wav")
HERO_SHOT = pygame.mixer.Sound(Path(__file__).parent.parent / "assets/sounds/crash.wav")
