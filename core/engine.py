"""
Motor principal de Pixel-OS
Gestiona el ciclo de vida del sistema operativo simulado
"""
import pygame
import sys
from typing import List, Optional
from config.settings import *
from core.window_manager import WindowManager
from core.theme_manager import ThemeManager
from core.plugin_manager import PluginManager
from core.filesystem import VirtualFilesystem
from ui.desktop import Desktop
from ui.taskbar import TaskBar
from apps.builtin_apps import (
    TerminalApp,
    TextEditorApp,
    FileManagerApp,
    SettingsApp,
    MiniBrowserApp,
    CodeEditorApp,
    VideoPlayerApp,
)


class LoadingScreen:
    """Pantalla de carga estilo retro"""
    
    def __init__(self, screen: pygame.Surface, theme_manager):
        self.screen = screen
        self.theme_manager = theme_manager
        self.progress = 0.0  # 0.0 a 1.0
        self.elapsed_time = 0.0
    
    def update(self, dt: float):
        """Actualiza la pantalla de carga"""
        self.elapsed_time += dt
        # Transición suave
        self.progress = min(1.0, self.elapsed_time / 2.0)  # 2 segundos para llenar
    
    def render(self):
        """Renderiza la pantalla de carga"""
        # Fondo
        bg_color = (20, 15, 30)
        self.screen.fill(bg_color)
        
        # Logo/Texto central
        try:
            font_title = self.theme_manager.get_font(FONT_SIZE_LARGE)
            logo_text = font_title.render("Pixel-OS", True, Colors.BLUE)
            logo_rect = logo_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
            self.screen.blit(logo_text, logo_rect)
        except:
            pass
        
        # Barra de carga
        bar_width = 300
        bar_height = 20
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT // 2 + 20
        
        # Fondo de barra
        bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        pygame.draw.rect(self.screen, (40, 40, 60), bar_rect, border_radius=4)
        pygame.draw.rect(self.screen, Colors.BLUE, bar_rect, width=2, border_radius=4)
        
        # Barra de progreso
        progress_width = int(bar_width * self.progress)
        progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
        pygame.draw.rect(self.screen, Colors.BLUE, progress_rect, border_radius=4)
        
        # Porcentaje
        try:
            font_small = self.theme_manager.get_font(FONT_SIZE_SMALL)
            percent_text = font_small.render(f"{int(self.progress * 100)}%", True, Colors.TEXT_PRIMARY)
            percent_rect = percent_text.get_rect(center=(SCREEN_WIDTH // 2, bar_y + 40))
            self.screen.blit(percent_text, percent_rect)
        except:
            pass
        
        # Mensaje de carga
        try:
            font_small = self.theme_manager.get_font(FONT_SIZE_SMALL)
            msg_text = font_small.render("Inicializando sistema...", True, Colors.TEXT_SECONDARY)
            msg_rect = msg_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            self.screen.blit(msg_text, msg_rect)
        except:
            pass
        
        pygame.display.flip()
    
    def is_complete(self) -> bool:
        """Indica si la pantalla de carga finalizó"""
        return self.progress >= 1.0


class PixelOS:
    """Clase principal del sistema operativo"""
    
    def __init__(self):
        """Inicializa el sistema operativo"""
        pygame.init()
        
        # Configurar pantalla - Fullscreen sin bordes
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN | pygame.NOFRAME)
        pygame.display.set_caption(TITLE)
        
        # Cargar logo
        try:
            logo = pygame.image.load(SYSTEM_LOGO)
            pygame.display.set_icon(logo)
        except:
            print("⚠️ No se pudo cargar el logo del sistema")
        
        # Reloj para controlar FPS
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Pantalla de carga
        self.theme_manager = ThemeManager()
        self.loading_screen = LoadingScreen(self.screen, self.theme_manager)
        self.show_loading = True
        
        # Managers del sistema
        self.window_manager = WindowManager(self.screen, self.theme_manager)
        self.plugin_manager = PluginManager(self)
        self.filesystem = VirtualFilesystem()
        
        # Componentes de UI
        self.desktop = Desktop(self.screen, self.theme_manager)
        self.taskbar = TaskBar(self.screen, self.theme_manager, self.window_manager, self.plugin_manager)
        self._register_builtin_apps()
        
        # Cargar plugins y mods
        self.plugin_manager.load_plugins()
        self.taskbar.start_menu._build_menu_items()
        
        print("✨ Pixel-OS iniciado correctamente")
    
    def handle_events(self):
        """Procesa todos los eventos del sistema"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Alt+F4 para cerrar
                if event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_ALT:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked_icon = self.desktop.handle_click(event.pos)
                if clicked_icon and clicked_icon.app_ref:
                    self.plugin_manager.launch_app(clicked_icon.app_ref)
            
            # Delegar eventos a componentes
            self.taskbar.handle_event(event)
            self.window_manager.handle_event(event)

            # Eventos para la app enfocada
            if self.window_manager.focused_window:
                window = self.window_manager.focused_window
                if window.app_ref and hasattr(window.app_ref, "handle_event"):
                    window.app_ref.handle_event(event)
        
        # Verificar si se solicitó apagar
        if hasattr(self.plugin_manager, 'should_shutdown') and self.plugin_manager.should_shutdown:
            self.running = False
    
    def update(self, dt: float):
        """Actualiza el estado del sistema
        
        Args:
            dt: Delta time en segundos
        """
        if self.show_loading:
            self.loading_screen.update(dt)
            if self.loading_screen.is_complete():
                self.show_loading = False
        else:
            self.window_manager.update(dt)
            self.taskbar.update(dt)
            self.desktop.update(dt)
    
    def render(self):
        """Renderiza todos los componentes del sistema"""
        if self.show_loading:
            # Mostrar pantalla de carga
            self.loading_screen.render()
        else:
            # Fondo del desktop
            self.screen.fill(Colors.BACKGROUND)
            
            # Renderizar componentes en orden
            self.desktop.render()
            for window in self.window_manager.windows:
                window.render(self.screen, self.theme_manager)
                if window.app_ref and not window.is_minimized:
                    prev_clip = self.screen.get_clip()
                    self.screen.set_clip(window.content_rect)
                    window.app_ref.render(self.screen, window.content_rect)
                    self.screen.set_clip(prev_clip)
            self.taskbar.render()
            
            # Actualizar pantalla
            pygame.display.flip()

    def _register_builtin_apps(self):
        """Registra aplicaciones integradas y enlaza iconos del escritorio"""
        apps = [
            TerminalApp(),
            TextEditorApp(),
            FileManagerApp(),
            SettingsApp(),
            MiniBrowserApp(),
            CodeEditorApp(),
            VideoPlayerApp(),
        ]

        def app_launcher(app_id: str, path: str, filename: str | None):
            app = self.plugin_manager.plugins.get(app_id)
            if not app:
                return False
            if not app.is_running:
                self.plugin_manager.launch_app(app)
            if filename and hasattr(app, "load_file"):
                app.load_file(path, filename)
            elif not filename and hasattr(app, "open_path"):
                app.open_path(path)
            return True

        for app in apps:
            self.plugin_manager.plugins[app.app_id] = app

        terminal = self.plugin_manager.plugins.get("terminal")
        if terminal and hasattr(terminal, "set_app_launcher"):
            terminal.set_app_launcher(app_launcher)

        # Re-crear iconos del escritorio con referencias correctas
        self.desktop.icons = []
        default_ids = ["terminal", "text_editor", "file_manager", "settings"]
        for app_id in default_ids:
            app = self.plugin_manager.plugins.get(app_id)
            if app:
                self.desktop.add_icon(app.name, app_ref=app, color=app.color)
    
    def run(self):
        """Bucle principal del sistema"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time en segundos
            
            self.handle_events()
            self.update(dt)
            self.render()
        
        self.quit()
    
    def quit(self):
        """Cierra el sistema correctamente"""
        print("👋 Cerrando Pixel-OS...")
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    # Este archivo no debe ejecutarse directamente
    print("❌ Ejecuta main.py para iniciar Pixel-OS")
