"""
Window Manager - Gestiona todas las ventanas del sistema
Inspirado en Windows 11 con funcionalidad estilo Linux
"""
import pygame
from typing import List, Optional, Dict, Tuple, Any
from config.settings import *


class Window:
    """Representa una ventana del sistema"""
    
    def __init__(self, title: str, x: int, y: int, width: int, height: int, 
                 color: Optional[Tuple[int, int, int]] = None, app_ref: Any = None):
        """Inicializa una ventana
        
        Args:
            title: Título de la ventana
            x, y: Posición inicial
            width, height: Dimensiones
            color: Color de acento (usa un color pastel por defecto)
            app_ref: Referencia a la aplicación asociada
        """
        self.title = title
        self.rect = pygame.Rect(x, y, max(width, WINDOW_MIN_WIDTH), 
                                max(height, WINDOW_MIN_HEIGHT))
        self.color = color or Colors.BLUE
        self.app_ref = app_ref
        
        # Estado de la ventana
        self.is_focused = False
        self.is_maximized = False
        self.is_minimized = False
        self.prev_rect = None  # Para restaurar al desmaximizar
        
        # Interacción
        self.dragging = False
        self.drag_offset = (0, 0)
        self.resizing = False
        self.resize_edge = None
        
        # Animación
        self.animation_progress = 0.0
        self.target_alpha = 255
        self.current_alpha = 0
        
        # Áreas de la ventana
        self.titlebar_rect = pygame.Rect(x, y, width, WINDOW_TITLEBAR_HEIGHT)
        self.content_rect = pygame.Rect(x, y + WINDOW_TITLEBAR_HEIGHT, 
                                       width, height - WINDOW_TITLEBAR_HEIGHT)
        
        # Botones de control
        self._setup_control_buttons()
    
    def _setup_control_buttons(self):
        """Crea los botones de control (cerrar, minimizar, maximizar)"""
        button_size = 32
        button_margin = 8
        right_x = self.rect.right - button_margin
        
        self.close_button = pygame.Rect(
            right_x - button_size, 
            self.rect.top + (WINDOW_TITLEBAR_HEIGHT - button_size) // 2,
            button_size, button_size
        )
        
        self.maximize_button = pygame.Rect(
            right_x - button_size * 2 - button_margin,
            self.rect.top + (WINDOW_TITLEBAR_HEIGHT - button_size) // 2,
            button_size, button_size
        )
        
        self.minimize_button = pygame.Rect(
            right_x - button_size * 3 - button_margin * 2,
            self.rect.top + (WINDOW_TITLEBAR_HEIGHT - button_size) // 2,
            button_size, button_size
        )
    
    def update_rects(self):
        """Actualiza todos los rectángulos después de mover/redimensionar"""
        self.titlebar_rect = pygame.Rect(
            self.rect.x, self.rect.y, 
            self.rect.width, WINDOW_TITLEBAR_HEIGHT
        )
        self.content_rect = pygame.Rect(
            self.rect.x, self.rect.y + WINDOW_TITLEBAR_HEIGHT,
            self.rect.width, self.rect.height - WINDOW_TITLEBAR_HEIGHT
        )
        self._setup_control_buttons()
    
    def maximize(self, screen_width: int, screen_height: int):
        """Maximiza la ventana"""
        if not self.is_maximized:
            self.prev_rect = self.rect.copy()
            self.rect = pygame.Rect(0, 0, screen_width, 
                                   screen_height - TASKBAR_HEIGHT)
            self.is_maximized = True
            self.update_rects()
    
    def restore(self):
        """Restaura la ventana a su tamaño anterior"""
        if self.is_maximized and self.prev_rect:
            self.rect = self.prev_rect.copy()
            self.is_maximized = False
            self.update_rects()
    
    def minimize(self):
        """Minimiza la ventana"""
        self.is_minimized = True
    
    def unminimize(self):
        """Restaura la ventana minimizada"""
        self.is_minimized = False
    
    def update(self, dt: float):
        """Actualiza animaciones de la ventana
        
        Args:
            dt: Delta time en segundos
        """
        # Animación de aparición
        if self.current_alpha < self.target_alpha:
            self.current_alpha = min(255, self.current_alpha + 1000 * dt)
    
    def render(self, screen: pygame.Surface, theme_manager):
        """Renderiza la ventana
        
        Args:
            screen: Superficie donde renderizar
            theme_manager: Gestor de temas
        """
        if self.is_minimized:
            return
        
        # Sombra (efecto Windows 11)
        shadow_rect = self.rect.inflate(WINDOW_SHADOW_SIZE * 2, WINDOW_SHADOW_SIZE * 2)
        shadow_surf = pygame.Surface(shadow_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, Colors.SHADOW, shadow_surf.get_rect(), 
                        border_radius=WINDOW_BORDER_RADIUS)
        screen.blit(shadow_surf, shadow_rect)
        
        # Fondo de ventana con bordes redondeados
        window_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        window_surf.set_alpha(int(self.current_alpha))
        
        # Fondo principal
        pygame.draw.rect(window_surf, Colors.WINDOW_BG, window_surf.get_rect(),
                        border_radius=WINDOW_BORDER_RADIUS)
        
        # Barra de título con color de acento
        titlebar_local = pygame.Rect(0, 0, self.rect.width, WINDOW_TITLEBAR_HEIGHT)
        
        # Gradiente sutil en la barra de título
        title_color = self.color if self.is_focused else Colors.INACTIVE
        pygame.draw.rect(window_surf, title_color, titlebar_local,
                        border_top_left_radius=WINDOW_BORDER_RADIUS,
                        border_top_right_radius=WINDOW_BORDER_RADIUS)
        
        # Renderizar título
        try:
            font = theme_manager.get_font(FONT_SIZE_MEDIUM)
            title_text = font.render(self.title, True, Colors.TEXT_PRIMARY)
            window_surf.blit(title_text, (16, (WINDOW_TITLEBAR_HEIGHT - title_text.get_height()) // 2))
        except:
            pass
        
        # Botones de control
        self._render_control_buttons(window_surf, theme_manager)
        
        # Borde
        pygame.draw.rect(window_surf, Colors.BORDER, window_surf.get_rect(),
                        width=2, border_radius=WINDOW_BORDER_RADIUS)
        
        screen.blit(window_surf, self.rect)
    
    def _render_control_buttons(self, surface: pygame.Surface, theme_manager):
        """Renderiza los botones de control de la ventana"""
        mouse_pos = pygame.mouse.get_pos()
        
        # Ajustar posiciones a coordenadas locales
        close_local = self.close_button.move(-self.rect.x, -self.rect.y)
        max_local = self.maximize_button.move(-self.rect.x, -self.rect.y)
        min_local = self.minimize_button.move(-self.rect.x, -self.rect.y)
        
        # Botón minimizar
        min_hover = self.minimize_button.collidepoint(mouse_pos)
        pygame.draw.rect(surface, Colors.HOVER if min_hover else Colors.WINDOW_BG,
                        min_local, border_radius=6)
        pygame.draw.line(surface, Colors.TEXT_PRIMARY,
                        (min_local.centerx - 6, min_local.centery),
                        (min_local.centerx + 6, min_local.centery), 2)
        
        # Botón maximizar/restaurar
        max_hover = self.maximize_button.collidepoint(mouse_pos)
        pygame.draw.rect(surface, Colors.HOVER if max_hover else Colors.WINDOW_BG,
                        max_local, border_radius=6)
        if self.is_maximized:
            # Icono restaurar (dos cuadrados superpuestos)
            pygame.draw.rect(surface, Colors.TEXT_PRIMARY,
                           (max_local.centerx - 4, max_local.centery - 2, 8, 8), 2)
        else:
            # Icono maximizar (un cuadrado)
            pygame.draw.rect(surface, Colors.TEXT_PRIMARY,
                           (max_local.centerx - 6, max_local.centery - 6, 12, 12), 2)
        
        # Botón cerrar (con efecto hover rojo suave)
        close_hover = self.close_button.collidepoint(mouse_pos)
        close_color = (255, 150, 150) if close_hover else Colors.WINDOW_BG
        pygame.draw.rect(surface, close_color, close_local, border_radius=6)
        # X
        pygame.draw.line(surface, Colors.TEXT_PRIMARY,
                        (close_local.centerx - 6, close_local.centery - 6),
                        (close_local.centerx + 6, close_local.centery + 6), 2)
        pygame.draw.line(surface, Colors.TEXT_PRIMARY,
                        (close_local.centerx + 6, close_local.centery - 6),
                        (close_local.centerx - 6, close_local.centery + 6), 2)


class WindowManager:
    """Gestiona todas las ventanas del sistema"""
    
    def __init__(self, screen: pygame.Surface, theme_manager):
        """Inicializa el gestor de ventanas
        
        Args:
            screen: Superficie principal
            theme_manager: Gestor de temas
        """
        self.screen = screen
        self.theme_manager = theme_manager
        self.windows: List[Window] = []
        self.focused_window: Optional[Window] = None
    
    def create_window(self, title: str, width: int = 600, height: int = 400,
                     color: Optional[Tuple[int, int, int]] = None, app_ref: Any = None) -> Window:
        """Crea una nueva ventana
        
        Args:
            title: Título de la ventana
            width, height: Dimensiones
            color: Color de acento
            app_ref: Referencia a la aplicación
            
        Returns:
            La ventana creada
        """
        # Posición en cascada
        offset = len(self.windows) * 30
        x = 100 + offset
        y = 50 + offset
        
        window = Window(title, x, y, width, height, color, app_ref)
        self.windows.append(window)
        self.focus_window(window)
        
        return window
    
    def focus_window(self, window: Window):
        """Enfoca una ventana (la trae al frente)
        
        Args:
            window: Ventana a enfocar
        """
        if window in self.windows:
            # Desenfocar ventana anterior
            if self.focused_window:
                self.focused_window.is_focused = False
            
            # Mover al final (encima de todas)
            self.windows.remove(window)
            self.windows.append(window)
            
            # Enfocar nueva ventana
            window.is_focused = True
            window.unminimize()
            self.focused_window = window
    
    def close_window(self, window: Window):
        """Cierra una ventana
        
        Args:
            window: Ventana a cerrar
        """
        if window in self.windows:
            # Notificar a la app y resetear estado
            if window.app_ref:
                try:
                    window.app_ref.on_close()
                except Exception:
                    pass
                window.app_ref.is_running = False
                window.app_ref.window = None
            self.windows.remove(window)
            
            if self.focused_window == window:
                self.focused_window = self.windows[-1] if self.windows else None
                if self.focused_window:
                    self.focused_window.is_focused = True
    
    def handle_event(self, event: pygame.event.Event):
        """Procesa eventos relacionados con ventanas
        
        Args:
            event: Evento de Pygame
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Iterar en orden inverso (de arriba hacia abajo)
            for window in reversed(self.windows):
                if window.is_minimized:
                    continue
                
                # Click en botones de control
                if window.close_button.collidepoint(mouse_pos):
                    self.close_window(window)
                    return
                
                if window.maximize_button.collidepoint(mouse_pos):
                    if window.is_maximized:
                        window.restore()
                    else:
                        window.maximize(SCREEN_WIDTH, SCREEN_HEIGHT)
                    return
                
                if window.minimize_button.collidepoint(mouse_pos):
                    window.minimize()
                    return
                
                # Click en barra de título para arrastrar
                if window.titlebar_rect.collidepoint(mouse_pos):
                    self.focus_window(window)
                    window.dragging = True
                    window.drag_offset = (
                        mouse_pos[0] - window.rect.x,
                        mouse_pos[1] - window.rect.y
                    )
                    return
                
                # Click en contenido
                if window.rect.collidepoint(mouse_pos):
                    self.focus_window(window)
                    return
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            # Detener arrastre
            for window in self.windows:
                window.dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            # Arrastrar ventana
            for window in self.windows:
                if window.dragging:
                    mouse_pos = event.pos
                    window.rect.x = mouse_pos[0] - window.drag_offset[0]
                    window.rect.y = mouse_pos[1] - window.drag_offset[1]
                    window.update_rects()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Doble click en barra de título para maximizar
            pass  # Implementar si se desea
    
    def update(self, dt: float):
        """Actualiza todas las ventanas
        
        Args:
            dt: Delta time en segundos
        """
        for window in self.windows:
            window.update(dt)
    
    def render(self):
        """Renderiza todas las ventanas"""
        for window in self.windows:
            window.render(self.screen, self.theme_manager)
    
    def get_windows(self) -> List[Window]:
        """Obtiene todas las ventanas
        
        Returns:
            Lista de ventanas
        """
        return self.windows
