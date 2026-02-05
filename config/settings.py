"""
Configuración global del sistema Pixel-OS
"""
import os

# Rutas del proyecto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
FONTS_DIR = os.path.join(ASSETS_DIR, "fonts")
IMGS_DIR = os.path.join(ASSETS_DIR, "imgs")
MODS_DIR = os.path.join(BASE_DIR, "mods")
USER_DATA_DIR = os.path.join(BASE_DIR, "user_data")

# Configuración de pantalla
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Pixel-OS"

# Fuente principal
FONT_PATH = os.path.join(FONTS_DIR, "Monocraft.ttc")
FONT_SIZE_SMALL = 12
FONT_SIZE_MEDIUM = 16
FONT_SIZE_LARGE = 24

# Logo del sistema
SYSTEM_LOGO = os.path.join(IMGS_DIR, "System.png")
SETUP_FILE = os.path.join(USER_DATA_DIR, "setup.json")

# Paleta de colores pastel
class Colors:
    # Colores principales
    BLACK = (0, 0, 0)                # #000000
    PINK = (255, 179, 217)           # #FFB3D9
    BLUE = (179, 217, 255)           # #B3D9FF
    GREEN = (179, 255, 217)          # #B3FFD9
    YELLOW = (255, 229, 179)         # #FFE5B3
    PURPLE = (217, 179, 255)         # #D9B3FF
    PEACH = (255, 212, 179)          # #FFD4B3
    
    # Colores de UI
    BACKGROUND = (250, 245, 255)     # Fondo muy claro
    WINDOW_BG = (255, 255, 255)      # Fondo de ventanas
    TASKBAR_BG = (240, 235, 255)     # Barra de tareas
    BORDER = (200, 180, 220)         # Bordes
    SHADOW = (220, 210, 230, 128)    # Sombras (con alpha)
    
    # Estados
    HOVER = (255, 240, 250)          # Hover suave
    ACTIVE = (240, 220, 255)         # Elemento activo
    INACTIVE = (230, 230, 240)       # Elemento inactivo
    
    # Texto
    TEXT_PRIMARY = (80, 70, 100)     # Texto principal
    TEXT_SECONDARY = (140, 130, 160) # Texto secundario
    TEXT_DISABLED = (180, 170, 190)  # Texto deshabilitado
    
    # Acentos por app (para personalización)
    ACCENTS = [PINK, BLUE, GREEN, YELLOW, PURPLE, PEACH]

# Animaciones
ANIMATION_SPEED = 0.2  # Velocidad de las animaciones (0-1)
EASING = "ease_out"     # Tipo de easing

# Sistema de ventanas (inspirado en Windows 11)
WINDOW_BORDER_RADIUS = 12
WINDOW_SHADOW_SIZE = 8
WINDOW_TITLEBAR_HEIGHT = 40
WINDOW_MIN_WIDTH = 400
WINDOW_MIN_HEIGHT = 300

# Barra de tareas
TASKBAR_HEIGHT = 50
TASKBAR_ICON_SIZE = 32
TASKBAR_POSITION = "bottom"  # bottom, top, left, right

# Desktop
DESKTOP_ICON_SIZE = 48
DESKTOP_ICON_SPACING = 20
DESKTOP_GRID_SNAP = True
