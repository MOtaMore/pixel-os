"""
Script para mostrar información del sistema Pixel-OS
"""
import os
from config.settings import *


def print_banner():
    """Imprime el banner de Pixel-OS"""
    print("""
    ╔═══════════════════════════════════════════╗
    ║                                           ║
    ║         ✨ Pixel-OS - Info ✨            ║
    ║                                           ║
    ╚═══════════════════════════════════════════╝
    """)


def count_files_in_dir(directory, extension=".py"):
    """Cuenta archivos con cierta extensión en un directorio"""
    count = 0
    if os.path.exists(directory):
        for root, dirs, files in os.walk(directory):
            count += sum(1 for f in files if f.endswith(extension))
    return count


def get_lines_of_code():
    """Cuenta las líneas de código del proyecto"""
    total = 0
    for root, dirs, files in os.walk(BASE_DIR):
        # Ignorar ciertos directorios
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', '.vscode', 'prebuilt_downloads']]
        
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        total += sum(1 for line in f if line.strip())
                except:
                    pass
    return total


def show_info():
    """Muestra información del sistema"""
    print_banner()
    
    print("📊 Estadísticas del Proyecto:")
    print(f"  • Nombre: {TITLE}")
    print(f"  • Resolución: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"  • FPS: {FPS}")
    print(f"  • Fuente: Monocraft.ttc")
    
    print("\n📁 Estructura:")
    core_files = count_files_in_dir(os.path.join(BASE_DIR, "core"))
    ui_files = count_files_in_dir(os.path.join(BASE_DIR, "ui"))
    app_files = count_files_in_dir(os.path.join(BASE_DIR, "apps"))
    mod_files = count_files_in_dir(MODS_DIR)
    
    print(f"  • Archivos Core: {core_files}")
    print(f"  • Componentes UI: {ui_files}")
    print(f"  • Apps Integradas: {app_files}")
    print(f"  • Mods: {mod_files}")
    
    print("\n💻 Código:")
    loc = get_lines_of_code()
    print(f"  • Líneas de código: ~{loc:,}")
    
    print("\n🎨 Paleta de Colores Pastel:")
    colors_info = [
        ("Rosa", Colors.PINK, "#FFB3D9"),
        ("Azul", Colors.BLUE, "#B3D9FF"),
        ("Verde", Colors.GREEN, "#B3FFD9"),
        ("Amarillo", Colors.YELLOW, "#FFE5B3"),
        ("Morado", Colors.PURPLE, "#D9B3FF"),
        ("Melocotón", Colors.PEACH, "#FFD4B3"),
    ]
    
    for name, rgb, hex_code in colors_info:
        print(f"  • {name:12} {hex_code:8}  RGB{rgb}")
    
    print("\n🪟 Sistema de Ventanas:")
    print(f"  • Radio de bordes: {WINDOW_BORDER_RADIUS}px")
    print(f"  • Altura de título: {WINDOW_TITLEBAR_HEIGHT}px")
    print(f"  • Tamaño de sombra: {WINDOW_SHADOW_SIZE}px")
    print(f"  • Tamaño mínimo: {WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}px")
    
    print("\n📋 Barra de Tareas:")
    print(f"  • Altura: {TASKBAR_HEIGHT}px")
    print(f"  • Posición: {TASKBAR_POSITION}")
    print(f"  • Tamaño de icono: {TASKBAR_ICON_SIZE}px")
    
    print("\n🗂️ Desktop:")
    print(f"  • Tamaño de icono: {DESKTOP_ICON_SIZE}px")
    print(f"  • Espaciado: {DESKTOP_ICON_SPACING}px")
    print(f"  • Snap a grid: {'Sí' if DESKTOP_GRID_SNAP else 'No'}")
    
    print("\n✨ Animaciones:")
    print(f"  • Velocidad: {ANIMATION_SPEED}")
    print(f"  • Easing: {EASING}")
    
    print("\n📦 Rutas del Proyecto:")
    print(f"  • Base: {BASE_DIR}")
    print(f"  • Assets: {ASSETS_DIR}")
    print(f"  • Mods: {MODS_DIR}")
    
    print("\n" + "="*50)
    print("Para más información, lee README.md y MODDING_GUIDE.md")
    print("="*50 + "\n")


if __name__ == "__main__":
    show_info()
