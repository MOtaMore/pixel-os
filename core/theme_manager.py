"""
Theme Manager - Gestiona temas, fuentes y estilos visuales
"""
import pygame
from config.settings import *


class ThemeManager:
    """Gestiona el tema visual del sistema"""
    
    def __init__(self):
        """Inicializa el gestor de temas"""
        self.fonts = {}
        self._load_fonts()
    
    def _load_fonts(self):
        """Carga la fuente Monocraft en diferentes tamaños"""
        try:
            # Intentar cargar Monocraft
            self.fonts['small'] = pygame.font.Font(FONT_PATH, FONT_SIZE_SMALL)
            self.fonts['medium'] = pygame.font.Font(FONT_PATH, FONT_SIZE_MEDIUM)
            self.fonts['large'] = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
            print("✅ Fuente Monocraft cargada correctamente")
        except Exception as e:
            print(f"⚠️ No se pudo cargar Monocraft, usando fuente por defecto: {e}")
            # Fallback a fuente del sistema
            self.fonts['small'] = pygame.font.Font(None, FONT_SIZE_SMALL)
            self.fonts['medium'] = pygame.font.Font(None, FONT_SIZE_MEDIUM)
            self.fonts['large'] = pygame.font.Font(None, FONT_SIZE_LARGE)
    
    def get_font(self, size: int = FONT_SIZE_MEDIUM) -> pygame.font.Font:
        """Obtiene una fuente del tamaño especificado
        
        Args:
            size: Tamaño de la fuente
            
        Returns:
            Objeto Font de Pygame
        """
        if size <= FONT_SIZE_SMALL:
            return self.fonts['small']
        elif size <= FONT_SIZE_MEDIUM:
            return self.fonts['medium']
        else:
            return self.fonts['large']
    
    def get_color(self, color_name: str) -> tuple:
        """Obtiene un color de la paleta pastel
        
        Args:
            color_name: Nombre del color
            
        Returns:
            Tupla RGB del color
        """
        return getattr(Colors, color_name.upper(), Colors.PINK)
    
    def draw_rounded_rect(self, surface: pygame.Surface, color: tuple, 
                         rect: pygame.Rect, radius: int = 8):
        """Dibuja un rectángulo con esquinas redondeadas
        
        Args:
            surface: Superficie donde dibujar
            color: Color del rectángulo
            rect: Rectángulo a dibujar
            radius: Radio de las esquinas
        """
        pygame.draw.rect(surface, color, rect, border_radius=radius)
    
    def draw_button(self, surface: pygame.Surface, rect: pygame.Rect,
                   text: str, color: tuple = None, hover: bool = False,
                   font_size: int = FONT_SIZE_MEDIUM):
        """Dibuja un botón estilo pastel
        
        Args:
            surface: Superficie donde dibujar
            rect: Rectángulo del botón
            text: Texto del botón
            color: Color de acento (opcional)
            hover: Si está en hover
            font_size: Tamaño de fuente
        """
        btn_color = color or Colors.BLUE
        
        if hover:
            # Hacer más claro al hacer hover
            btn_color = tuple(min(255, c + 20) for c in btn_color[:3])
        
        # Dibujar botón
        pygame.draw.rect(surface, btn_color, rect, border_radius=8)
        
        # Dibujar texto
        font = self.get_font(font_size)
        text_surf = font.render(text, True, Colors.TEXT_PRIMARY)
        text_rect = text_surf.get_rect(center=rect.center)
        surface.blit(text_surf, text_rect)
