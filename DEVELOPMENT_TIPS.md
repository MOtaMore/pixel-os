# 💡 Tips de Desarrollo para Pixel-OS

## 🚀 Comenzando

### Setup Inicial
1. Asegúrate de tener Python 3.8+
2. Instala dependencias: `pip install -r requirements.txt`
3. Ejecuta: `python main.py`
4. ¡Empieza a crear!

### Estructura del Proyecto
```
pixel-os/
├── core/           # Motor del sistema
│   ├── engine.py           # Loop principal
│   ├── window_manager.py   # Gestión de ventanas
│   ├── theme_manager.py    # Temas y estilos
│   └── plugin_manager.py   # Sistema de mods
├── ui/             # Componentes de interfaz
│   ├── desktop.py   # Escritorio
│   └── taskbar.py   # Barra de tareas
├── apps/           # Apps integradas
├── mods/           # Tus mods aquí
└── config/         # Configuración
```

## 🎯 Desarrollo de Mods

### Flujo Rápido
```bash
# 1. Crear nuevo mod
python create_mod.py mi_app_genial

# 2. Editar mods/mi_app_genial.py
# 3. Reiniciar Pixel-OS
# 4. ¡Tu app estará cargada!
```

### Template Mínimo
```python
from core.plugin_manager import Application
from config.settings import Colors
import pygame

class MiApp(Application):
    def __init__(self):
        super().__init__("Mi App", color=Colors.BLUE)
    
    def render(self, surface, rect):
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
```

### Tips de Performance

#### ✅ HACER
```python
class MiApp(Application):
    def __init__(self):
        super().__init__("App")
        # Cachear fuentes y recursos
        self.font = pygame.font.Font(FONT_PATH, 16)
        self.heavy_data = self.load_data()
    
    def render(self, surface, rect):
        # Renderizar elementos pre-calculados
        surface.blit(self.cached_image, rect)
```

#### ❌ NO HACER
```python
def render(self, surface, rect):
    # NO cargar fuentes cada frame
    font = pygame.font.Font(FONT_PATH, 16)  # ❌
    
    # NO hacer operaciones pesadas
    result = heavy_calculation()  # ❌
```

### Manejo de Eventos

```python
def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # Click izquierdo
            # Tu código
            pass
        elif event.button == 3:  # Click derecho
            # Menú contextual
            pass
    
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_RETURN:
            # Enter presionado
            pass
        elif event.key == pygame.K_ESCAPE:
            # Cerrar app
            self.window.close() if self.window else None
```

## 🎨 Diseño UI

### Colores Consistentes
```python
from config.settings import Colors

# Colores pastel principales
bg = Colors.WINDOW_BG
text = Colors.TEXT_PRIMARY
accent = Colors.BLUE

# Crear variaciones
lighter = tuple(min(255, c + 30) for c in accent)
darker = tuple(max(0, c - 30) for c in accent)
```

### Botones con Hover
```python
def render(self, surface, rect):
    button_rect = pygame.Rect(rect.x + 20, rect.y + 20, 100, 40)
    
    # Detectar hover
    mouse_pos = pygame.mouse.get_pos()
    is_hover = button_rect.collidepoint(mouse_pos)
    
    # Color dinámico
    color = Colors.HOVER if is_hover else Colors.BLUE
    
    # Dibujar
    pygame.draw.rect(surface, color, button_rect, border_radius=8)
```

### Layouts Responsivos
```python
def render(self, surface, rect):
    # Usar el rect para adaptar al tamaño
    padding = 20
    
    # Sidebar
    sidebar_width = min(200, rect.width // 4)
    sidebar = pygame.Rect(rect.x, rect.y, sidebar_width, rect.height)
    
    # Contenido principal
    content = pygame.Rect(
        rect.x + sidebar_width + padding,
        rect.y + padding,
        rect.width - sidebar_width - padding * 2,
        rect.height - padding * 2
    )
```

## 🐛 Debug

### Print Debug
```python
def on_open(self):
    print(f"[{self.name}] Abierta")

def handle_event(self, event):
    print(f"[{self.name}] Evento: {event.type}")
```

### Debug Visual
```python
def render(self, surface, rect):
    # Mostrar rect de debug
    pygame.draw.rect(surface, (255, 0, 0), rect, 2)
    
    # Mostrar posición del mouse
    mouse_pos = pygame.mouse.get_pos()
    font = pygame.font.Font(None, 14)
    text = font.render(f"Mouse: {mouse_pos}", True, (0, 0, 0))
    surface.blit(text, (rect.x + 5, rect.y + 5))
```

## 📝 Best Practices

### 1. Nombrado Claro
```python
# ✅ Bueno
def calculate_total_price(items):
    pass

# ❌ Malo
def calc(x):
    pass
```

### 2. Comentarios Útiles
```python
# ✅ Bueno
# Calcular posición centrada teniendo en cuenta el padding
center_x = rect.centerx - (width // 2)

# ❌ Innecesario
# Sumar 1
count += 1
```

### 3. Manejo de Errores
```python
def render(self, surface, rect):
    try:
        # Código que podría fallar
        image = pygame.image.load(self.image_path)
        surface.blit(image, rect)
    except FileNotFoundError:
        # Fallback visual
        pygame.draw.rect(surface, Colors.PINK, rect)
        font = pygame.font.Font(None, 16)
        text = font.render("Imagen no encontrada", True, Colors.TEXT_PRIMARY)
        surface.blit(text, (rect.x + 10, rect.y + 10))
    except Exception as e:
        print(f"Error en {self.name}: {e}")
```

### 4. Recursos Compartidos
```python
# Crear un módulo para recursos compartidos
# mods/shared_resources.py
import pygame
from config.settings import FONT_PATH

class SharedResources:
    _fonts = {}
    
    @classmethod
    def get_font(cls, size):
        if size not in cls._fonts:
            try:
                cls._fonts[size] = pygame.font.Font(FONT_PATH, size)
            except:
                cls._fonts[size] = pygame.font.Font(None, size)
        return cls._fonts[size]
```

## 🔧 Herramientas Útiles

### VS Code Tasks
Presiona `Ctrl+Shift+P` y escribe "Run Task"
- Build
- Run
- Debug

### Scripts Útiles
```bash
# Ver información del sistema
python info.py

# Crear nuevo mod
python create_mod.py mi_mod

# Ejecutar con logs
python main.py 2>&1 | tee output.log
```

## 📚 Recursos de Aprendizaje

### Pygame
- [Documentación oficial](https://www.pygame.org/docs/)
- [Pygame examples](https://github.com/pygame/pygame/tree/main/examples)

### Pixel Art
- Lospec Palette List
- Piskel (editor online)
- Aseprite (editor profesional)

### Python
- [Python.org tutorials](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

## 💬 Comunidad

Si tienes preguntas:
1. Lee MODDING_GUIDE.md
2. Revisa los ejemplos en mods/
3. Consulta el código en core/ y ui/
4. Crea un issue en GitHub

## 🎯 Checklist para Publicar un Mod

- [ ] El código está comentado
- [ ] Funciona sin errores
- [ ] Usa la paleta de colores pastel
- [ ] Tiene manejo de errores
- [ ] Se adapta a diferentes tamaños de ventana
- [ ] Incluye README.md con descripción
- [ ] Los recursos están en la carpeta del mod
- [ ] Funciona con la fuente por defecto (fallback)

## 🌟 Ideas de Proyectos

### Fácil
- Reloj digital
- Cronómetro/temporizador
- Conversor de unidades
- Generador de colores aleatorios

### Medio
- Todo list con persistencia
- Reproductor de música
- Galería de imágenes
- Chat local

### Avanzado
- Mini-IDE con syntax highlighting
- Juego completo (Snake, Tetris, etc.)
- Sistema de partículas
- Visualizador de datos

¡Diviértete creando! 🎨✨
