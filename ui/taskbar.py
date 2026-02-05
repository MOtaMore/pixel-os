"""
TaskBar - Barra de tareas estilo Windows 11 con colores pastel
Incluye menú de inicio y soporte para iconos PNG
"""
import os
import pygame
from typing import List, Optional, Any
from config.i18n import tr
from config.settings import *


class StartMenu:
    """Menú de inicio que muestra todas las aplicaciones disponibles"""
    
    def __init__(self, screen: pygame.Surface, theme_manager, plugin_manager):
        """Inicializa el menú de inicio"""
        self.screen = screen
        self.theme_manager = theme_manager
        self.plugin_manager = plugin_manager
        self.visible = False
        
        # Dimensiones del menú
        self.menu_width = 350
        self.menu_height = 500
        self.menu_rect = pygame.Rect(
            10, SCREEN_HEIGHT - TASKBAR_HEIGHT - self.menu_height - 10,
            self.menu_width, self.menu_height
        )
        
        # Items del menú
        self.menu_items = []
        self.hovered_item = -1
        self._build_menu_items()
    
    def _build_menu_items(self):
        """Construye la lista de items del menú desde los plugins"""
        self.menu_items = []
        for app_id, app_ref in self.plugin_manager.plugins.items():
            if hasattr(app_ref, 'name') and hasattr(app_ref, 'color'):
                self.menu_items.append({
                    'name': app_ref.name,
                    'app_id': app_id,
                    'color': app_ref.color,
                    'app_ref': app_ref,
                })
    
    def update(self, mouse_pos):
        """Actualiza el menú según la posición del mouse"""
        if not self.visible:
            return
        
        self.hovered_item = -1
        item_height = 50
        for i in range(len(self.menu_items)):
            item_rect = pygame.Rect(
                self.menu_rect.x + 10,
                self.menu_rect.y + 50 + i * item_height,
                self.menu_rect.width - 20,
                item_height - 5
            )
            if item_rect.collidepoint(mouse_pos):
                self.hovered_item = i
                break
    
    def render(self):
        """Renderiza el menú de inicio"""
        if not self.visible:
            return
        
        # Fondo del menú
        pygame.draw.rect(self.screen, Colors.WINDOW_BG, self.menu_rect, border_radius=12)
        pygame.draw.rect(self.screen, Colors.BORDER, self.menu_rect, width=2, border_radius=12)
        
        # Título
        font_title = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        title = font_title.render("Aplicaciones", True, Colors.TEXT_PRIMARY)
        self.screen.blit(title, (self.menu_rect.x + 20, self.menu_rect.y + 15))
        
        # Items
        font_item = self.theme_manager.get_font(FONT_SIZE_SMALL)
        item_height = 50
        
        for i, item in enumerate(self.menu_items):
            item_rect = pygame.Rect(
                self.menu_rect.x + 10,
                self.menu_rect.y + 50 + i * item_height,
                self.menu_rect.width - 20,
                item_height - 5
            )
            
            # Fondo si está hovered
            if i == self.hovered_item:
                pygame.draw.rect(self.screen, Colors.HOVER, item_rect, border_radius=6)
            
            # Icono
            icon_path = os.path.join("assets", "imgs", f"icon_{item['app_id']}.png")
            try:
                if os.path.exists(icon_path):
                    icon_img = pygame.image.load(icon_path)
                    icon_img = pygame.transform.scale(icon_img, (32, 32))
                    self.screen.blit(icon_img, (item_rect.x + 5, item_rect.y + 8))
                else:
                    # Fallback
                    color_rect = pygame.Rect(item_rect.x + 5, item_rect.y + 8, 32, 32)
                    pygame.draw.rect(self.screen, item['color'], color_rect, border_radius=4)
            except Exception:
                # Fallback
                color_rect = pygame.Rect(item_rect.x + 5, item_rect.y + 8, 32, 32)
                pygame.draw.rect(self.screen, item['color'], color_rect, border_radius=4)
            
            # Nombre
            name_text = font_item.render(item['name'], True, Colors.TEXT_PRIMARY)
            self.screen.blit(name_text, (item_rect.x + 45, item_rect.y + 15))
    
    def handle_click(self, pos, window_manager) -> Optional[Any]:
        """Maneja clicks en el menú"""
        if not self.visible or not self.menu_rect.collidepoint(pos):
            self.visible = False
            return None
        
        item_height = 50
        for i, item in enumerate(self.menu_items):
            item_rect = pygame.Rect(
                self.menu_rect.x + 10,
                self.menu_rect.y + 50 + i * item_height,
                self.menu_rect.width - 20,
                item_height - 5
            )
            if item_rect.collidepoint(pos):
                self.visible = False
                return item['app_ref']
        
        return None


class TaskBarButton:
    """Botón en la barra de tareas con soporte para iconos PNG"""
    
    def __init__(self, name: str, color: tuple, window_ref=None, app_id: Optional[str] = None):
        """Inicializa un botón de la barra"""
        self.name = name
        self.color = color
        self.window_ref = window_ref
        self.app_id = app_id
        self.rect = pygame.Rect(0, 0, TASKBAR_ICON_SIZE + 20, TASKBAR_ICON_SIZE + 8)
        self.hover = False
        self.icon_image = self._load_icon_image()
    
    def _load_icon_image(self) -> Optional[pygame.Surface]:
        """Carga la imagen del icono desde archivo"""
        if not self.app_id:
            return None
        
        icon_path = os.path.join("assets", "imgs", f"icon_{self.app_id}.png")
        try:
            if os.path.exists(icon_path):
                img = pygame.image.load(icon_path)
                return pygame.transform.scale(img, (TASKBAR_ICON_SIZE - 10, TASKBAR_ICON_SIZE - 10))
        except Exception:
            pass
        return None
    
    def render(self, surface: pygame.Surface, theme_manager):
        """Renderiza el botón"""
        # Fondo del botón
        if self.window_ref and not self.window_ref.is_minimized:
            bg_color = Colors.ACTIVE
        elif self.hover:
            bg_color = Colors.HOVER
        else:
            bg_color = Colors.TASKBAR_BG
        
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        
        # Icono
        if self.icon_image:
            # Mostrar imagen del icono
            img_rect = self.icon_image.get_rect(center=self.rect.center)
            surface.blit(self.icon_image, img_rect)
        else:
            # Fallback: cuadrado de color
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
    
    def __init__(self, screen: pygame.Surface, theme_manager, window_manager, plugin_manager):
        """Inicializa la barra de tareas"""
        self.screen = screen
        self.theme_manager = theme_manager
        self.window_manager = window_manager
        self.plugin_manager = plugin_manager
        
        # Rectángulo de la barra
        self.rect = pygame.Rect(
            0, SCREEN_HEIGHT - TASKBAR_HEIGHT,
            SCREEN_WIDTH, TASKBAR_HEIGHT
        )
        
        # Botones
        self.buttons: List[TaskBarButton] = []
        self.start_button_rect = pygame.Rect(10, self.rect.y + 5, 180, 40)
        self.start_menu = StartMenu(screen, theme_manager, plugin_manager)
        self.logo_surface = None
        self._load_logo()

    def _load_logo(self):
        """Carga el logo del sistema para el botón de inicio"""
        try:
            logo = pygame.image.load(SYSTEM_LOGO).convert_alpha()
            self.logo_surface = pygame.transform.smoothscale(logo, (24, 24))
        except Exception:
            self.logo_surface = None
    
    def update(self, dt: float):
        """Actualiza la barra de tareas"""
        # Sincronizar botones con ventanas
        self._sync_buttons()
        
        # Actualizar hover de botones
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.hover = button.rect.collidepoint(mouse_pos)
        
        # Actualizar menú de inicio
        self.start_menu.update(mouse_pos)
    
    def _sync_buttons(self):
        """Sincroniza los botones con las ventanas abiertas"""
        windows = self.window_manager.get_windows()
        
        # Eliminar botones de ventanas cerradas
        self.buttons = [btn for btn in self.buttons if btn.window_ref in windows]
        
        # Añadir botones de ventanas nuevas
        for window in windows:
            if not any(btn.window_ref == window for btn in self.buttons):
                # Obtener app_id desde la ventana
                app_id = getattr(window, 'app_id', None)
                if hasattr(window, 'app_ref'):
                    app_id = getattr(window.app_ref, 'app_id', None)
                
                button = TaskBarButton(window.title, window.color, window, app_id)
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
        # Fondo de la barra
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
        
        # Menú de inicio
        self.start_menu.render()
        
        # Reloj
        self._render_clock()
    
    def _render_start_button(self):
        """Renderiza el botón de inicio"""
        mouse_pos = pygame.mouse.get_pos()
        hover = self.start_button_rect.collidepoint(mouse_pos)
        
        # Fondo del botón
        bg_color = Colors.HOVER if hover else Colors.TASKBAR_BG
        pygame.draw.rect(self.screen, bg_color, self.start_button_rect, border_radius=8)
        
        # Logo del sistema
        logo_rect = pygame.Rect(
            self.start_button_rect.x + 10,
            self.start_button_rect.centery - 12,
            24, 24
        )
        if self.logo_surface:
            self.screen.blit(self.logo_surface, logo_rect.topleft)
        else:
            # Fallback
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
        
        # Texto de marca
        font = self.theme_manager.get_font(FONT_SIZE_MEDIUM)
        text = font.render(tr("taskbar.brand"), True, Colors.TEXT_PRIMARY)
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
        """Maneja eventos de la barra de tareas"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            
            # Click en botón de inicio
            if self.start_button_rect.collidepoint(mouse_pos):
                self.start_menu.visible = not self.start_menu.visible
                return
            
            # Click en menú de inicio
            if self.start_menu.visible:
                app_ref = self.start_menu.handle_click(mouse_pos, self.window_manager)
                if app_ref:
                    self.plugin_manager.launch_app(app_ref)
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
