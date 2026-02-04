# 🎉 ¡Bienvenido a Pixel-OS!

## 🚀 Inicio Rápido (5 minutos)

### 1️⃣ Verifica la instalación
```bash
python test.py
```
Deberías ver: ✅ TODOS LOS TESTS PASARON

### 2️⃣ Ejecuta Pixel-OS
```bash
python main.py
```

### 3️⃣ Explora el sistema
- Haz **click** en los iconos del escritorio
- **Arrastra** las ventanas desde la barra de título
- Usa los botones **minimizar/maximizar/cerrar**
- Interactúa con las **aplicaciones**

---

## 🎮 Controles Básicos

| Acción | Control |
|--------|---------|
| Abrir aplicación | Click en icono del desktop |
| Mover ventana | Arrastrar barra de título |
| Minimizar | Click en botón `-` |
| Maximizar | Click en botón `□` |
| Cerrar | Click en botón `×` |
| Salir del sistema | Tecla `ESC` |

---

## 📱 Aplicaciones Incluidas

### 🖥️ Terminal
Comandos disponibles:
```
help   - Muestra ayuda
clear  - Limpia la pantalla
echo   - Repite texto
date   - Muestra fecha y hora
color  - Cambia color (pink, blue, green, yellow, purple, peach)
```

### ✏️ Editor de Texto
- Escribe libremente
- Usa **flechas** para navegar
- **Backspace** para borrar
- **Enter** para nueva línea

### 📁 Explorador de Archivos
- Navega por carpetas simuladas
- Click para seleccionar archivos

### ⚙️ Configuración
- Panel de configuración del sistema

### 🧮 Calculadora (Mod)
- Operaciones básicas: +, -, ×, ÷
- Click en botones o usa teclado
- Botón `C` para limpiar

### 🎨 Paint (Mod)
- Dibuja con el mouse
- Selecciona colores de la paleta izquierda
- Click y arrastra para dibujar

---

## 🔧 Crear tu Primer Mod (10 minutos)

### Método Rápido
```bash
python create_mod.py mi_primer_mod
```

Esto crea: `mods/mi_primer_mod.py`

### Edita el archivo
```python
# mods/mi_primer_mod.py
def render(self, surface, rect):
    # ¡Tu código aquí!
    pygame.draw.rect(surface, Colors.PINK, rect)
```

### Reinicia Pixel-OS
```bash
python main.py
```

Tu mod aparecerá cargado en la consola! 🎉

---

## 📚 Siguiente Nivel

### Lee la documentación completa:
1. **[MODDING_GUIDE.md](MODDING_GUIDE.md)** - Tutorial de mods paso a paso
2. **[DEVELOPMENT_TIPS.md](DEVELOPMENT_TIPS.md)** - Tips y best practices
3. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Visión general del proyecto

### Explora el código:
- `core/` - Motor del sistema
- `ui/` - Componentes de interfaz
- `apps/` - Aplicaciones integradas
- `mods/` - Tus mods aquí

### Scripts útiles:
```bash
python info.py              # Info del sistema
python create_mod.py <name> # Crear nuevo mod
python test.py              # Ejecutar tests
```

---

## 🎨 Personalización

### Cambiar colores
Edita `config/settings.py`:
```python
class Colors:
    PINK = (255, 179, 217)  # ← Cambia estos valores
    # ...
```

### Cambiar resolución
```python
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
```

### Ajustar animaciones
```python
ANIMATION_SPEED = 0.5  # Más lento
FPS = 120              # Más fluido
```

---

## 🐛 ¿Problemas?

### El sistema no inicia
```bash
# Reinstalar dependencias
pip install -r requirements.txt --upgrade

# Verificar instalación
python test.py
```

### No se ve la fuente Monocraft
Es normal, usa una fuente por defecto como fallback

### Los mods no cargan
- Verifica que estén en la carpeta `mods/`
- Asegúrate que hereden de `Application`
- Revisa errores en la consola

### Performance bajo
- Cierra otras aplicaciones
- Reduce `SCREEN_WIDTH` y `SCREEN_HEIGHT`
- Limita ventanas abiertas

---

## 💡 Ideas de Proyectos

### Fácil (1 hora)
- [ ] Reloj digital con alarma
- [ ] Conversor de unidades
- [ ] Generador de paletas de colores

### Medio (3 horas)
- [ ] Todo list con persistencia
- [ ] Juego Snake
- [ ] Reproductor de música

### Avanzado (1 día)
- [ ] Mini-IDE con syntax highlighting
- [ ] Juego RPG completo
- [ ] Sistema de archivos real

---

## 🎯 Checklist del Primer Día

- [ ] ✅ Ejecuté `python test.py` exitosamente
- [ ] 🎮 Abrí todas las aplicaciones integradas
- [ ] 🖱️ Probé mover, minimizar y maximizar ventanas
- [ ] 🧮 Usé la calculadora
- [ ] 🎨 Dibujé algo en Paint
- [ ] 📝 Escribí texto en el Editor
- [ ] 💻 Ejecuté comandos en Terminal
- [ ] 🔧 Creé mi primer mod
- [ ] 📖 Leí MODDING_GUIDE.md
- [ ] 🚀 Personalicé el sistema

---

## 🌟 Comparte tu Trabajo

¿Creaste algo genial? ¡Compártelo!
- Toma screenshots y colócalos en `screenshots/`
- Documenta tu mod en un README
- Comparte con la comunidad

---

## 📞 Soporte

### Recursos
- **Documentación**: Lee los archivos .md del proyecto
- **Código de ejemplo**: Revisa `apps/` y `mods/`
- **Tests**: `python test.py` para diagnosticar

### Comunidad
- Abre un issue en GitHub
- Contribuye con pull requests
- Comparte tus mods

---

<div align="center">

## 🎉 ¡Disfruta de Pixel-OS! 🎉

**Recuerda**: El límite es tu imaginación 🚀

*¡Diviértete creando!* ✨

---

**Próximos pasos sugeridos:**
1. Ejecuta `python main.py`
2. Explora todas las apps
3. Lee `MODDING_GUIDE.md`
4. Crea tu primer mod
5. ¡Comparte tu creación!

</div>
