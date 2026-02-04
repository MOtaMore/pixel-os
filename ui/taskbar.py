"""
TaskBar - Barra de tareas estilo Windows 11 con colores pastel
"""
import pygame
from typing import List
from config.settings import *


class TaskBarButton:
    """Botón en la barra de tareas"""
    
    def __init__(self, name: str, color: tuple, window_ref=None):
        """Inicializa un botón de la barra
        
        Args:
            name: Nombre de la aplicación
            color: Color de acento
            window_ref: Referencia a la ventana
        """
        self.name = name
        self.color = color
        self.window_ref = window_ref
        self.rect = pygame.Rect(0, 0, TASKBAR_ICON_SIZE + 20, TASKBAR_ICON_SIZE + 8)
        self.hover = False
    
    def render(self, surface: pygame.Surface, theme_manager):
        """Renderiza el botón
        
        Args:
            surface: Superficie donde renderizar
            theme_manager: Gestor de temas
        """
        # Fondo del botón
        if self.window_ref and not self.window_ref.is_minimized:
            bg_color = Colors.ACTIVE
        elif self.hover:
            bg_color = Colors.HOVER
        else:
            bg_color = Colors.TASKBAR_BG
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        
        # Icono (simple cuadrado de color)
        icon_size = TASKBAR_ICON_SIZE - 8
        icon_rect = pygame.Rect(
            self.rect.centerx - icon_size // 2,
            self.rect.centery - icon_size // 2,
            icon_size, icon_size
        )
        pygame.draw.rect(surface, self.color, icon_rect, border_radius=4)
        
        # Indicador si está abierto
        if self.window_ref and not self.window_ref.is_minimized:
            indicator_rect = pygame.Rect(
                self.rect.centerx - 15,
                self.rect.bottom - 3,
                30, 2
            )
            pygame.draw.rect(surface, self.color, indicator_rect, border_radius=1)


class TaskBar:
    """Barra de tareas del sistema"""
    
    def __init__(self, screen: pygame.Surface, theme_manager, window_manager):
        """Inicializa la barra de tareas
        
        Args:
            screen: Superficie principal
            theme_manager: Gestor de temas
            window_manager: Gestor de ventanas
        """
        self.screen = screen
        self.theme_manager = theme_manager
        self.window_manager = window_manager
        
        # Rectángulo de la barra
        self.rect = pygame.Rect(
            0, SCREEN_HEIGHT - TASKBAR_HEIGHT,
            SCREEN_WIDTH, TASKBAR_HEIGHT
        )
        
        # Botones
        self.buttons: List[TaskBarButton] = []
        self.start_button_rect = pygame.Rect(10, self.rect.y + 5, 180, 40)
        self.start_menu_open = False
    
    def update(self, dt: float):
        """Actualiza la barra de tareas
        
        Args:
            dt: Delta time en segundos
        """
        # Sincronizar botones con ventanas
        self._sync_buttons()
        
        # Actualizar hover de botones
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.hover = button.rect.collidepoint(mouse_pos)
    
    def _sync_buttons(self):
        """Sincroniza los botones con las ventanas abiertas"""
        windows = self.window_manager.get_windows()
        
        # Eliminar botones de ventanas cerradas
        self.buttons = [btn for btn in self.buttons if btn.window_ref in windows]
        
        # Añadir botones de ventanas nuevas
        for window in windows:
            if not any(btn.window_ref == window for btn in self.buttons):
                button = TaskBarButton(window.title, window.color, window)
                self.buttons.append(button)
        
        # Actualizar posiciones
        self._update_button_positions()
    
    def _update_button_positions(self):
        """Actualiza las posiciones de los botones"""
        # Centrar botones
        total_width = len(self.buttons) * (TASKBAR_ICON_SIZE + 20 + 8)
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i, button in enumerate(self.buttons):
            button.rect.x = start_x + i * (TASKBAR_ICON_SIZE + 20 + 8)
            button.rect.y = self.rect.y + (TASKBAR_HEIGHT - button.rect.height) // 2
    
    def render(self):
        """Renderiza la barra de tareas"""
        # Fondo de la barra con efecto blur/frosted glass (simulado)
        taskbar_surf = pygame.Surface((SCREEN_WIDTH, TASKBAR_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(taskbar_surf, (*Colors.TASKBAR_BG, 240), taskbar_surf.get_rect())
        self.screen.blit(taskbar_surf, self.rect)
        
        # Línea superior sutil
        pygame.draw.line(self.screen, Colors.BORDER, 
                        (0, self.rect.y), 
                        (SCREEN_WIDTH, self.rect.y), 1)
        
        # Botón de inicio (Start)
        self._render_start_button()
        
        # Botones de aplicaciones
        for button in self.buttons:
            button.render(self.screen, self.theme_manager)
        
        # Reloj
        self._render_clock()
    
    def _render_start_button(self):
        """Renderiza el botón de inicio"""
        mouse_pos = pygame.mouse.get_pos()
        hover = self.start_button_rect.collidepoint(mouse_pos)
        
        # Fondo del botón
        bg_color = Colors.HOVER if hover else Colors.TASKBAR_BG
        pygame.draw.rect(self.screen, bg_color, self.start_button_rect, border_radius=8)
        
        # Logo (simple por ahora)
        logo_rect = pygame.Rect(
            self.start_button_rect.x + 10,
            self.start_button_rect.centery - 12,
            24, 24
        )
        
        # Dibujar logo simple de cuatro cuadrados (estilo Windows)
        colors = [Colors.PINK, Colors.BLUE, Colors.GREEN, Colors.YELLOW]
        for i, color in enumerate(colors):
            x_offset = (i % 2) * 13
            y_offset = (i // 2) * 13
            square = pygame.Rect(
                logo_rect.x + x_offset,
                logo_rect.y + y_offset,
                10, 10
            )
            pygame.draw.rect(self.screen, color, square, border_radius=2)
        
        # Texto "Pixel-OS"
        font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        text = font.render("Pixel-OS", True, Colors.TEXT_PRIMARY)
        text_x = logo_rect.right + 10
        text_y = self.start_button_rect.centery - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))
    
    def _render_clock(self):
        """Renderiza el reloj del sistema"""
        import datetime
        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M")
        
        font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        text = font.render(time_str, True, Colors.TEXT_PRIMARY)
        
        # Posición en la esquina derecha
        x = SCREEN_WIDTH - text.get_width() - 20
        y = self.rect.centery - text.get_height() // 2
        
        self.screen.blit(text, (x, y))
    
    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos de la barra de tareas
        
        Args:
            event: Evento de Pygame
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Click en botón de inicio
            if self.start_button_rect.collidepoint(mouse_pos):
                self.start_menu_open = not self.start_menu_open
                return
            
            # Click en botones de aplicaciones
            for button in self.buttons:
                if button.rect.collidepoint(mouse_pos):
                    if button.window_ref:
                        if button.window_ref.is_minimized:
                            button.window_ref.unminimize()
                            self.window_manager.focus_window(button.window_ref)
                        elif button.window_ref == self.window_manager.focused_window:
                            button.window_ref.minimize()
                        else:
                            self.window_manager.focus_window(button.window_ref)
                    return
