"""
Script de utilidad para crear nuevos mods fácilmente
Uso: python create_mod.py nombre_del_mod
"""
import os
import sys
from config.settings import MODS_DIR, Colors


def create_mod_template(mod_name: str):
    """Crea una plantilla de mod con estructura básica
    
    Args:
        mod_name: Nombre del mod (snake_case)
    """
    # Convertir nombre a formato adecuado
    class_name = ''.join(word.capitalize() for word in mod_name.split('_')) + 'App'
    display_name = ' '.join(word.capitalize() for word in mod_name.split('_'))
    
    # Template del mod
    template = f'''"""
{display_name} - Mod para Pixel-OS
Autor: Tu Nombre
Descripción: Descripción de tu mod
"""
import pygame
from core.plugin_manager import Application
from config.settings import Colors, FONT_PATH


class {class_name}(Application):
    """Aplicación {display_name}"""
    
    def __init__(self):
        super().__init__(
            name="{display_name}",
            color=Colors.BLUE  # Cambia el color a tu preferencia
        )
        # Inicializa tus variables aquí
        self.data = {{}}
    
    def on_open(self):
        """Llamado cuando se abre la aplicación"""
        print(f"{{self.name}} abierta!")
        # Inicialización adicional aquí
    
    def on_close(self):
        """Llamado cuando se cierra la aplicación"""
        print(f"{{self.name}} cerrada!")
        # Limpieza o guardado de datos aquí
    
    def update(self, dt: float):
        """Actualiza el estado de la aplicación
        
        Args:
            dt: Delta time en segundos
        """
        # Lógica de actualización aquí
        pass
    
    def render(self, surface: pygame.Surface, rect: pygame.Rect):
        """Renderiza el contenido de la aplicación
        
        Args:
            surface: Superficie donde renderizar
            rect: Rectángulo del área de contenido
        """
        # Fondo
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        # Renderizar tu contenido aquí
        try:
            font = pygame.font.Font(FONT_PATH, 20)
        except:
            font = pygame.font.Font(None, 24)
        
        # Ejemplo: texto centrado
        text = font.render("¡Hola desde {display_name}!", True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
        
        # Añade más elementos aquí:
        # - Botones
        # - Listas
        # - Gráficos
        # - etc.
    
    def handle_event(self, event: pygame.event.Event):
        """Maneja eventos de usuario
        
        Args:
            event: Evento de Pygame
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Click del mouse
            mouse_pos = event.pos
            # Maneja clicks aquí
            pass
        
        elif event.type == pygame.KEYDOWN:
            # Tecla presionada
            if event.key == pygame.K_SPACE:
                # Ejemplo: espacio presionado
                pass


# Exportar la clase para que el plugin manager la encuentre
__all__ = ['{class_name}']
'''
    
    # Crear archivo del mod
    mod_file = os.path.join(MODS_DIR, f"{mod_name}.py")
    
    if os.path.exists(mod_file):
        print(f"❌ El mod '{mod_name}' ya existe!")
        return False
    
    with open(mod_file, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"""
✅ Mod creado exitosamente!

📁 Ubicación: {mod_file}
📝 Clase: {class_name}
🎨 Nombre: {display_name}

Próximos pasos:
1. Edita el archivo y personaliza tu mod
2. Reinicia Pixel-OS para cargar el mod
3. Abre tu mod desde el menú Start o desktop

💡 Tip: Lee MODDING_GUIDE.md para más información
""")
    
    return True


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("""
🔧 Creador de Mods para Pixel-OS

Uso:
    python create_mod.py nombre_del_mod

Ejemplos:
    python create_mod.py mi_calculadora
    python create_mod.py juego_snake
    python create_mod.py editor_imagenes

El nombre debe estar en snake_case (minúsculas con guiones bajos)
        """)
        return
    
    mod_name = sys.argv[1].lower()
    
    # Validar nombre
    if not mod_name.replace('_', '').isalnum():
        print("❌ El nombre del mod solo puede contener letras, números y guiones bajos")
        return
    
    print(f"\n🎨 Creando mod '{mod_name}'...")
    create_mod_template(mod_name)


if __name__ == "__main__":
    main()
