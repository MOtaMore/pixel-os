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
from ui.desktop import Desktop
from ui.taskbar import TaskBar


class PixelOS:
    """Clase principal del sistema operativo"""
    
    def __init__(self):
        """Inicializa el sistema operativo"""
        pygame.init()
        
        # Configurar pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        
        # Managers del sistema
        self.theme_manager = ThemeManager()
        self.window_manager = WindowManager(self.screen, self.theme_manager)
        self.plugin_manager = PluginManager(self)
        
        # Componentes de UI
        self.desktop = Desktop(self.screen, self.theme_manager)
        self.taskbar = TaskBar(self.screen, self.theme_manager, self.window_manager)
        
        # Cargar plugins y mods
        self.plugin_manager.load_plugins()
        
        print("✨ Pixel-OS iniciado correctamente")
    
    def handle_events(self):
        """Procesa todos los eventos del sistema"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            
            # Delegar eventos a componentes
            self.taskbar.handle_event(event)
            self.window_manager.handle_event(event)
    
    def update(self, dt: float):
        """Actualiza el estado del sistema
        
        Args:
            dt: Delta time en segundos
        """
        self.window_manager.update(dt)
        self.taskbar.update(dt)
        self.desktop.update(dt)
    
    def render(self):
        """Renderiza todos los componentes del sistema"""
        # Fondo del desktop
        self.screen.fill(Colors.BACKGROUND)
        
        # Renderizar componentes en orden
        self.desktop.render()
        self.window_manager.render()
        self.taskbar.render()
        
        # Actualizar pantalla
        pygame.display.flip()
    
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
