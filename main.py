"""
Punto de entrada principal de Pixel-OS
"""
from core.engine import PixelOS
from apps.builtin_apps import TerminalApp, TextEditorApp, FileManagerApp, SettingsApp


def main():
    """Función principal"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║            🎮 Pixel-OS v1.0 🎮            ║
    ║                                           ║
    ║   Sistema Operativo Simulado              ║
    ║   Temática: Pixel Art Cozy & Pastel       ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)
    
    # Crear e iniciar el sistema
    pixel_os = PixelOS()
    
    # Registrar aplicaciones integradas
    apps = [
        TerminalApp(),
        TextEditorApp(),
        FileManagerApp(),
        SettingsApp()
    ]
    
    # Añadir apps al sistema
    for app in apps:
        pixel_os.plugin_manager.plugins[app.name] = app
    
    # Vincular apps con iconos del escritorio
    desktop_icons = pixel_os.desktop.icons
    if len(desktop_icons) >= 4:
        desktop_icons[0].app_ref = apps[0]  # Terminal
        desktop_icons[1].app_ref = apps[1]  # Editor
        desktop_icons[2].app_ref = apps[2]  # Archivos
        desktop_icons[3].app_ref = apps[3]  # Configuración
    
    # Manejar clicks en el desktop
    def handle_desktop_click(event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked_icon = pixel_os.desktop.handle_click(event.pos)
            if clicked_icon and clicked_icon.app_ref:
                pixel_os.plugin_manager.launch_app(clicked_icon.app_ref)
    
    # Agregar manejador de eventos de desktop
    import pygame
    original_handle = pixel_os.handle_events
    
    def extended_handle():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pixel_os.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pixel_os.running = False
            
            # Eventos del desktop
            handle_desktop_click(event)
            
            # Delegar eventos a componentes
            pixel_os.taskbar.handle_event(event)
            pixel_os.window_manager.handle_event(event)
            
            # Eventos a apps abiertas
            if pixel_os.window_manager.focused_window:
                window = pixel_os.window_manager.focused_window
                if window.app_ref and hasattr(window.app_ref, 'handle_event'):
                    window.app_ref.handle_event(event)
    
    pixel_os.handle_events = extended_handle
    
    # Extender render para apps
    original_render = pixel_os.render
    
    def extended_render():
        # Fondo del desktop
        pixel_os.screen.fill(Colors.BACKGROUND)
        
        # Renderizar componentes en orden
        pixel_os.desktop.render()
        
        # Renderizar ventanas y su contenido
        for window in pixel_os.window_manager.windows:
            window.render(pixel_os.screen, pixel_os.theme_manager)
            
            # Renderizar contenido de la app si existe
            if window.app_ref and hasattr(window.app_ref, 'render') and not window.is_minimized:
                window.app_ref.render(pixel_os.screen, window.content_rect)
        
        pixel_os.taskbar.render()
        
        # Actualizar pantalla
        pygame.display.flip()
    
    from config.settings import Colors
    pixel_os.render = extended_render
    
    # Mensaje de bienvenida
    print("✨ Sistema iniciado correctamente")
    print("📌 Haz click en los iconos del escritorio para abrir aplicaciones")
    print("🎨 Disfruta de la experiencia Pixel-OS!\n")
    
    # Ejecutar el sistema
    pixel_os.run()


if __name__ == "__main__":
    main()
