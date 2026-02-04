"""
Plugin Manager - Sistema modular para cargar mods y aplicaciones
Inspirado en el sistema de plugins de Linux
"""
import os
import importlib.util
import inspect
from typing import List, Dict, Type, Optional, Tuple
from config.settings import MODS_DIR


class Application:
    """Clase base para todas las aplicaciones del sistema
    
    Los mods deben heredar de esta clase para ser cargados correctamente
    """
    
    def __init__(self, name: str = "Unnamed App", icon_path: Optional[str] = None,
                 color: Optional[Tuple[int, int, int]] = None):
        """Inicializa una aplicación
        
        Args:
            name: Nombre de la aplicación
            icon_path: Ruta al icono (opcional)
            color: Color de acento pastel (opcional)
        """
        self.name = name
        self.icon_path = icon_path
        self.color = color
        self.window = None
        self.is_running = False
    
    def on_open(self):
        """Llamado cuando se abre la aplicación"""
        pass
    
    def on_close(self):
        """Llamado cuando se cierra la aplicación"""
        pass
    
    def update(self, dt: float):
        """Actualiza el estado de la aplicación
        
        Args:
            dt: Delta time en segundos
        """
        pass
    
    def render(self, surface, rect):
        """Renderiza el contenido de la aplicación
        
        Args:
            surface: Superficie donde renderizar
            rect: Rectángulo del área de contenido
        """
        pass
    
    def handle_event(self, event):
        """Maneja eventos de la aplicación
        
        Args:
            event: Evento de Pygame
        """
        pass


class PluginManager:
    """Gestiona la carga y ejecución de plugins/mods"""
    
    def __init__(self, os_ref):
        """Inicializa el gestor de plugins
        
        Args:
            os_ref: Referencia al objeto PixelOS principal
        """
        self.os_ref = os_ref
        self.plugins: Dict[str, Application] = {}
        self.plugin_classes: List[Type[Application]] = []
        
        # Crear directorio de mods si no existe
        if not os.path.exists(MODS_DIR):
            os.makedirs(MODS_DIR)
            self._create_readme()
    
    def _create_readme(self):
        """Crea un README en el directorio de mods"""
        readme_path = os.path.join(MODS_DIR, "README.md")
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write("""# 🔌 Mods y Plugins de Pixel-OS

Coloca tus mods aquí para que se carguen automáticamente al iniciar el sistema.

## Estructura de un Mod

```python
# mi_app.py
from core.plugin_manager import Application
import pygame

class MiAplicacion(Application):
    def __init__(self):
        super().__init__(
            name="Mi Aplicación",
            icon_path="mods/mi_app/icon.png",
            color=(255, 179, 217)  # Color pastel
        )
    
    def on_open(self):
        print(f"{self.name} abierta!")
    
    def render(self, surface, rect):
        # Dibuja tu UI aquí
        font = pygame.font.Font(None, 24)
        text = font.render("¡Hola desde mi mod!", True, (80, 70, 100))
        surface.blit(text, (rect.x + 20, rect.y + 20))
```

## Características Disponibles

- Acceso al sistema de ventanas
- Eventos de mouse y teclado
- Renderizado personalizado
- Colores pastel predefinidos
- Fuente Monocraft integrada

¡Diviértete creando! 🎨
""")
    
    def load_plugins(self):
        """Carga todos los plugins desde el directorio de mods"""
        if not os.path.exists(MODS_DIR):
            return
        
        print("\n🔍 Buscando mods...")
        
        # Buscar archivos .py en el directorio de mods
        for item in os.listdir(MODS_DIR):
            item_path = os.path.join(MODS_DIR, item)
            
            # Cargar módulos Python
            if item.endswith('.py') and item != '__init__.py':
                self._load_plugin_file(item_path, item[:-3])
            
            # Cargar desde subdirectorios
            elif os.path.isdir(item_path):
                main_file = os.path.join(item_path, 'main.py')
                if os.path.exists(main_file):
                    self._load_plugin_file(main_file, item)
        
        print(f"✅ {len(self.plugin_classes)} plugin(s) cargado(s)\n")
    
    def _load_plugin_file(self, file_path: str, module_name: str):
        """Carga un archivo de plugin
        
        Args:
            file_path: Ruta al archivo Python
            module_name: Nombre del módulo
        """
        try:
            # Cargar el módulo dinámicamente
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Buscar clases que hereden de Application
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, Application) and obj != Application:
                        self.plugin_classes.append(obj)
                        print(f"  📦 Cargado: {name} desde {module_name}")
        
        except Exception as e:
            print(f"  ❌ Error cargando {module_name}: {e}")
    
    def create_app_instance(self, plugin_class: Type[Application]) -> Optional[Application]:
        """Crea una instancia de una aplicación
        
        Args:
            plugin_class: Clase del plugin
            
        Returns:
            Instancia de la aplicación
        """
        try:
            app = plugin_class()
            self.plugins[app.name] = app
            return app
        except Exception as e:
            print(f"❌ Error creando instancia de {plugin_class.__name__}: {e}")
            return None
    
    def launch_app(self, app: Application):
        """Lanza una aplicación
        
        Args:
            app: Aplicación a lanzar
        """
        if not app.is_running:
            app.is_running = True
            
            # Crear ventana para la aplicación
            window = self.os_ref.window_manager.create_window(
                title=app.name,
                width=600,
                height=400,
                color=app.color,
                app_ref=app
            )
            
            app.window = window
            app.on_open()
    
    def get_plugin_classes(self) -> List[Type[Application]]:
        """Obtiene todas las clases de plugins cargadas
        
        Returns:
            Lista de clases de plugins
        """
        return self.plugin_classes
