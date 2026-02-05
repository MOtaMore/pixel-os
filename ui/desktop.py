"""
Desktop - Escritorio del sistema con iconos y fondos
"""
import os
import pygame
from typing import List, Optional, Tuple, Any
from config.i18n import tr
from config.settings import *


class DesktopIcon:
    """Representa un icono en el escritorio"""
    
    def __init__(self, name: str, x: int, y: int, app_ref: Any = None,
                 color: Optional[Tuple[int, int, int]] = None, app_id: Optional[str] = None):
        """Inicializa un icono de escritorio
        
        Args:
            name: Nombre del icono
            x, y: Posición
            app_ref: Referencia a la aplicación asociada
            color: Color de acento
            app_id: ID de la aplicación para cargar el icono correcto
        """
        self.name = name
        self.x = x
        self.y = y
        self.app_ref = app_ref
        self.color = color or Colors.BLUE
        self.app_id = app_id
        
        # Rectángulos
        self.icon_rect = pygame.Rect(x, y, DESKTOP_ICON_SIZE, DESKTOP_ICON_SIZE)
        self.label_rect = pygame.Rect(
            x - 20, y + DESKTOP_ICON_SIZE + 4,
            DESKTOP_ICON_SIZE + 40, 30
        )
        
        # Estado
        self.selected = False
        self.hover = False
        
        # Cargar imagen del icono
        self.icon_image = self._load_icon_image()
    
    def _load_icon_image(self) -> Optional[pygame.Surface]:
        """Carga la imagen del icono desde archivo
        
        Returns:
            Superficie con la imagen escalada, o None si no se encuentra
        """
        if not self.app_id:
            return None
        
        icon_path = os.path.join("assets", "imgs", f"icon_{self.app_id}.png")
        try:
            if os.path.exists(icon_path):
                img = pygame.image.load(icon_path)
                # Escalar a tamaño del icono
                return pygame.transform.scale(img, (DESKTOP_ICON_SIZE - 8, DESKTOP_ICON_SIZE - 8))
        except Exception:
            pass
        return None
    
    def update(self, mouse_pos):
        """Actualiza el estado del icono
        
        Args:
            mouse_pos: Posición del mouse
        """
        self.hover = (self.icon_rect.collidepoint(mouse_pos) or 
                     self.label_rect.collidepoint(mouse_pos))
    
    def render(self, surface: pygame.Surface, theme_manager):
        """Renderiza el icono
        
        Args:
            surface: Superficie donde renderizar
            theme_manager: Gestor de temas
        """
        # Fondo si está seleccionado o en hover
        if self.selected or self.hover:
            bg_color = Colors.ACTIVE if self.selected else Colors.HOVER
            full_rect = self.icon_rect.union(self.label_rect)
            full_rect.inflate_ip(8, 8)
            pygame.draw.rect(surface, bg_color, full_rect, border_radius=8)
        
        # Icono: mostrar imagen o fallback a color
        if self.icon_image:
            # Mostrar imagen del icono
            img_rect = self.icon_image.get_rect(center=self.icon_rect.center)
            surface.blit(self.icon_image, img_rect)
        else:
            # Fallback: cuadrado de color
            pygame.draw.rect(surface, self.color, self.icon_rect, border_radius=8)
        
        # Borde del icono
        pygame.draw.rect(surface, Colors.BORDER, self.icon_rect, width=2, border_radius=8)
        
        # Label
        font = theme_manager.get_font(FONT_SIZE_SMALL)
        text = font.render(self.name, True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=(self.label_rect.centerx, self.label_rect.centery))
        
        # Fondo del texto para mejor legibilidad
        text_bg = text_rect.inflate(8, 4)
        pygame.draw.rect(surface, Colors.WINDOW_BG, text_bg, border_radius=4)
        
        surface.blit(text, text_rect)


class Desktop:
    """Gestiona el escritorio del sistema"""
    
    def __init__(self, screen: pygame.Surface, theme_manager):
        """Inicializa el escritorio
        
        Args:
            screen: Superficie principal
            theme_manager: Gestor de temas
        """
        self.screen = screen
        self.theme_manager = theme_manager
        self.icons: List[DesktopIcon] = []
        
        # Crear algunos iconos de ejemplo
        self._create_default_icons()
    
    def _create_default_icons(self):
        """Crea iconos por defecto del sistema"""
        # Distribuir iconos en grid
        start_x = 30
        start_y = 30
        spacing = DESKTOP_ICON_SIZE + DESKTOP_ICON_SPACING
        
        default_apps = [
            (tr("app.terminal"), Colors.GREEN),
            (tr("app.text_editor"), Colors.BLUE),
            (tr("app.file_manager"), Colors.YELLOW),
            (tr("app.settings"), Colors.PURPLE),
        ]
        
        for i, (name, color) in enumerate(default_apps):
            y = start_y + (i * spacing)
            icon = DesktopIcon(name, start_x, y, color=color)
            self.icons.append(icon)
    
    def add_icon(self, name: str, app_ref: Any = None,
                 color: Optional[Tuple[int, int, int]] = None):
        """Añade un icono al escritorio
        
        Args:
            name: Nombre del icono
            app_ref: Referencia a la aplicación
            color: Color de acento
        """
        # Calcular posición automáticamente
        start_x = 30
        start_y = 30
        spacing = DESKTOP_ICON_SIZE + DESKTOP_ICON_SPACING
        
        y = start_y + (len(self.icons) * spacing)
        
        # Obtener app_id desde la referencia de la aplicación
        app_id = getattr(app_ref, 'app_id', None) if app_ref else None
        
        icon = DesktopIcon(name, start_x, y, app_ref, color, app_id=app_id)
        self.icons.append(icon)
    
    def update(self, dt: float):
        """Actualiza el escritorio
        
        Args:
            dt: Delta time en segundos
        """
        mouse_pos = pygame.mouse.get_pos()
        for icon in self.icons:
            icon.update(mouse_pos)
    
    def render(self):
        """Renderiza el escritorio"""
        # Los iconos se renderizan sobre el fondo
        for icon in self.icons:
            icon.render(self.screen, self.theme_manager)
    
    def handle_click(self, pos: Tuple[int, int]) -> Optional[DesktopIcon]:
        """Maneja clicks en el escritorio
        
        Args:
            pos: Posición del click
            
        Returns:
            Icono clickeado o None
        """
        for icon in self.icons:
            if icon.icon_rect.collidepoint(pos) or icon.label_rect.collidepoint(pos):
                return icon
        return None
