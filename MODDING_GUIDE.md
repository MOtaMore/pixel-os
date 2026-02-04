# 🎨 Guía de Desarrollo de Mods para Pixel-OS

## 📚 Índice
1. [Introducción](#introducción)
2. [Estructura Básica](#estructura-básica)
3. [API Disponible](#api-disponible)
4. [Ejemplos Prácticos](#ejemplos-prácticos)
5. [Best Practices](#best-practices)

## Introducción

Pixel-OS está diseñado para ser completamente extensible mediante mods. Cada mod es una aplicación que se puede abrir en una ventana del sistema.

## Estructura Básica

### Clase Application

Todos los mods deben heredar de `Application`:

```python
from core.plugin_manager import Application
import pygame

class MiMod(Application):
    def __init__(self):
        super().__init__(
            name="Mi Aplicación",
            icon_path="mods/mi_mod/icon.png",  # Opcional
            color=(255, 179, 217)  # Color pastel de acento
        )
    
    def on_open(self):
        """Llamado cuando se abre la app"""
        pass
    
    def on_close(self):
        """Llamado cuando se cierra la app"""
        pass
    
    def update(self, dt: float):
        """Actualiza cada frame (dt = delta time)"""
        pass
    
    def render(self, surface, rect):
        """Renderiza el contenido de la app
        
        Args:
            surface: pygame.Surface principal
            rect: pygame.Rect del área de contenido
        """
        pass
    
    def handle_event(self, event):
        """Maneja eventos de mouse/teclado
        
        Args:
            event: pygame.event.Event
        """
        pass
```

## API Disponible

### Acceso a la Ventana

```python
# En cualquier método de tu aplicación
if self.window:
    # Cambiar título
    self.window.title = "Nuevo Título"
    
    # Cambiar color de acento
    self.window.color = Colors.PURPLE
    
    # Maximizar/Restaurar
    self.window.maximize(SCREEN_WIDTH, SCREEN_HEIGHT)
    self.window.restore()
    
    # Minimizar
    self.window.minimize()
```

### Colores Pastel Predefinidos

```python
from config.settings import Colors

# Colores principales
Colors.PINK        # (255, 179, 217)
Colors.BLUE        # (179, 217, 255)
Colors.GREEN       # (179, 255, 217)
Colors.YELLOW      # (255, 229, 179)
Colors.PURPLE      # (217, 179, 255)
Colors.PEACH       # (255, 212, 179)

# Colores de UI
Colors.BACKGROUND  # Fondo del desktop
Colors.WINDOW_BG   # Fondo de ventanas
Colors.HOVER       # Estado hover
Colors.ACTIVE      # Elemento activo
Colors.TEXT_PRIMARY    # Texto principal
Colors.TEXT_SECONDARY  # Texto secundario
```

### Fuente Monocraft

```python
from config.settings import FONT_PATH, FONT_SIZE_SMALL, FONT_SIZE_MEDIUM, FONT_SIZE_LARGE
import pygame

# Cargar fuente con try/except por si falla
try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE_MEDIUM)
except:
    font = pygame.font.Font(None, 16)  # Fallback

# Renderizar texto
text_surface = font.render("Hola Pixel-OS", True, Colors.TEXT_PRIMARY)
```

### Dibujar Elementos Pastel

```python
import pygame
from config.settings import Colors

def render(self, surface, rect):
    # Fondo suave
    pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
    
    # Botón con bordes redondeados
    button_rect = pygame.Rect(rect.x + 20, rect.y + 20, 120, 40)
    pygame.draw.rect(surface, Colors.BLUE, button_rect, border_radius=8)
    
    # Texto centrado en el botón
    font = pygame.font.Font(None, 20)
    text = font.render("Aceptar", True, Colors.TEXT_PRIMARY)
    text_rect = text.get_rect(center=button_rect.center)
    surface.blit(text, text_rect)
    
    # Borde opcional
    pygame.draw.rect(surface, Colors.BORDER, button_rect, width=2, border_radius=8)
```

## Ejemplos Prácticos

### Ejemplo 1: Aplicación Simple

```python
from core.plugin_manager import Application
from config.settings import Colors, FONT_PATH
import pygame

class HelloWorldApp(Application):
    def __init__(self):
        super().__init__("Hello World", color=Colors.PINK)
        self.counter = 0
    
    def update(self, dt):
        self.counter += dt
    
    def render(self, surface, rect):
        # Fondo
        pygame.draw.rect(surface, (255, 250, 250), rect)
        
        # Mensaje
        try:
            font = pygame.font.Font(FONT_PATH, 24)
        except:
            font = pygame.font.Font(None, 28)
        
        text = font.render(f"¡Hola! {int(self.counter)}s", True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=rect.center)
        surface.blit(text, text_rect)
```

### Ejemplo 2: App Interactiva

```python
from core.plugin_manager import Application
from config.settings import Colors, FONT_PATH
import pygame

class ClickerApp(Application):
    def __init__(self):
        super().__init__("Clicker Game", color=Colors.YELLOW)
        self.clicks = 0
        self.button_rect = None
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect and self.button_rect.collidepoint(event.pos):
                self.clicks += 1
    
    def render(self, surface, rect):
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        # Botón
        button_size = 100
        self.button_rect = pygame.Rect(
            rect.centerx - button_size // 2,
            rect.centery - button_size // 2,
            button_size, button_size
        )
        
        # Hover effect
        mouse_pos = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            color = tuple(min(255, c + 20) for c in Colors.YELLOW)
        else:
            color = Colors.YELLOW
        
        pygame.draw.rect(surface, color, self.button_rect, border_radius=12)
        
        # Texto
        try:
            font = pygame.font.Font(FONT_PATH, 20)
        except:
            font = pygame.font.Font(None, 24)
        
        text = font.render(f"{self.clicks}", True, Colors.TEXT_PRIMARY)
        text_rect = text.get_rect(center=self.button_rect.center)
        surface.blit(text, text_rect)
```

### Ejemplo 3: App con Estado Persistente

```python
import json
import os
from core.plugin_manager import Application
from config.settings import Colors, FONT_PATH, BASE_DIR
import pygame

class NotesApp(Application):
    def __init__(self):
        super().__init__("Notas", color=Colors.GREEN)
        self.notes = []
        self.save_path = os.path.join(BASE_DIR, "user_data", "notes.json")
        self.load_notes()
    
    def load_notes(self):
        """Carga notas desde archivo"""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r', encoding='utf-8') as f:
                    self.notes = json.load(f)
            except:
                self.notes = []
    
    def save_notes(self):
        """Guarda notas en archivo"""
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)
        with open(self.save_path, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
    
    def on_close(self):
        """Guardar al cerrar"""
        self.save_notes()
    
    def render(self, surface, rect):
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        # Renderizar notas
        try:
            font = pygame.font.Font(FONT_PATH, 14)
        except:
            font = pygame.font.Font(None, 16)
        
        y = rect.y + 20
        for note in self.notes:
            text = font.render(note, True, Colors.TEXT_PRIMARY)
            surface.blit(text, (rect.x + 20, y))
            y += 25
```

## Best Practices

### 1. Performance
- Evita operaciones pesadas en `render()`
- Usa `update()` para lógica que no depende de renderizado
- Cachea recursos (fuentes, imágenes) en `__init__()` o `on_open()`

### 2. Manejo de Errores
```python
def render(self, surface, rect):
    try:
        # Tu código
        pass
    except Exception as e:
        # Renderizar mensaje de error
        font = pygame.font.Font(None, 16)
        error = font.render(f"Error: {str(e)}", True, (255, 100, 100))
        surface.blit(error, (rect.x + 10, rect.y + 10))
```

### 3. Diseño Responsivo
```python
def render(self, surface, rect):
    # Adaptar al tamaño de la ventana
    padding = 20
    usable_width = rect.width - padding * 2
    usable_height = rect.height - padding * 2
    
    # Centrar elementos
    element_rect = pygame.Rect(0, 0, 200, 100)
    element_rect.center = rect.center
```

### 4. Colores Consistentes
- Siempre usa los colores de `Colors` para mantener la estética pastel
- Si necesitas variaciones, ajusta sutilmente:
```python
# Hacer más claro
lighter = tuple(min(255, c + 30) for c in Colors.BLUE)

# Hacer más oscuro
darker = tuple(max(0, c - 30) for c in Colors.BLUE)
```

### 5. Animaciones Suaves
```python
class AnimatedApp(Application):
    def __init__(self):
        super().__init__("Animated", color=Colors.PURPLE)
        self.position = 0
        self.target_position = 100
    
    def update(self, dt):
        # Interpolación suave (lerp)
        speed = 5.0  # Ajusta la velocidad
        self.position += (self.target_position - self.position) * speed * dt
```

## 🎯 Testing

Para testear tu mod:

1. Guarda tu archivo `.py` en la carpeta `mods/`
2. Reinicia Pixel-OS
3. Tu mod debería aparecer cargado en la consola
4. Puedes abrirlo desde el menú Start (si lo implementas) o:

```python
# Añadir icono en el desktop (edita main.py temporalmente)
from mods.mi_mod import MiMod
mi_app = MiMod()
pixel_os.plugin_manager.plugins[mi_app.name] = mi_app
pixel_os.desktop.add_icon(mi_app.name, app_ref=mi_app, color=mi_app.color)
```

## 🚀 Publicar tu Mod

1. Crea una carpeta en `mods/` con el nombre de tu mod
2. Incluye:
   - `main.py` o `nombre_mod.py` con tu clase
   - `README.md` con descripción e instrucciones
   - `icon.png` (opcional, 48x48px, pixel art)
   - Cualquier recurso adicional

## 💡 Ideas de Mods

- 🎵 Reproductor de música
- 📊 Visualizador de datos
- 🎮 Mini-juegos (snake, tetris, pong)
- 📝 Gestor de tareas/TODO
- 🌐 Navegador web simple
- 💬 Chat local
- 📷 Capturador de pantalla
- 🔐 Gestor de contraseñas
- 🎨 Más herramientas de dibujo
- 🧮 Calculadora científica

¡Diviértete creando! 🎨✨
