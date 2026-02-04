# 🎮 Pixel-OS

<div align="center">

![Pixel-OS Logo](assets/imgs/System.png)

**Un sistema operativo simulado con temática pixel art cozy y colores pastel** 🌸

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6+-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Características](#-características) • [Instalación](#-instalación) • [Uso](#️-ejecutar) • [Crear Mods](#-crear-modsaddons) • [Documentación](#-documentación)

</div>

---

## 🌸 Características

✨ **Estética Pixel Art**: Diseño cozy con paleta de colores pastel cuidadosamente seleccionada  
🏗️ **Arquitectura POO**: Código limpio, modular y fácil de extender  
🔌 **Sistema de Mods**: Soporte completo para plugins y aplicaciones personalizadas  
🪟 **Ventanas Modernas**: Diseño inspirado en Windows 11 con funcionalidad estilo Linux  
🎬 **Animaciones Fluidas**: Experiencia visual relajante y suave  
🎨 **Fuente Monocraft**: Tipografía pixel art incluida para máxima autenticidad  
🎯 **Apps Integradas**: Terminal, editor de texto, explorador de archivos y más

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- Windows / Linux / macOS

### Pasos

1. **Clonar el repositorio**
```bash
git clone <tu-repo>
cd pixel-os
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **¡Listo para usar!**

## ▶️ Ejecutar

```bash
python main.py
```

### Desde VS Code
Presiona `F5` o usa la configuración "🎮 Run Pixel-OS" del panel de Debug.

### Controles
- **Click izquierdo**: Interactuar con ventanas e iconos
- **Arrastrar ventanas**: Click en la barra de título
- **Minimizar/Maximizar/Cerrar**: Botones en la barra de título
- **ESC**: Salir del sistema

## 🔌 Crear Mods/Addons

### Método Rápido

```bash
python create_mod.py nombre_de_tu_mod
```

Este comando crea una plantilla completa lista para personalizar.

### Método Manual

Los mods se colocan en la carpeta `mods/` y deben heredar de la clase `Application`:

```p� Documentación

- [README.md](README.md) - Este archivo
- [MODDING_GUIDE.md](MODDING_GUIDE.md) - Guía completa para crear mods
- [create_mod.py](create_mod.py) - Utilidad para generar plantillas de mods

## 🎨 Apps Integradas

### 🖥️ Terminal
Terminal interactiva con comandos personalizados:
- `help` - Lista de comandos
- `clear` - Limpia la pantalla
- `echo [texto]` - Repite el texto
- `date` - Muestra fecha y hora
- `color [nombre]` - Cambia el color del terminal

### ✏️ Editor de Texto
Editor simple pero funcional con:
- Múltiples líneas
- Navegación con flechas
- Backspace y Delete

### 📁 Explorador de Archivos
Navegador de archivos con interfaz intuitiva

### ⚙️ Configuración
Panel de configuración del sistema

## 🎯 Mods de Ejemplo

El proyecto incluye mods de ejemplo en la carpeta `mods/`:
- **Calculadora**: Calculadora con diseño pastel
- **Paint**: Aplicación de dibujo con paleta de colores

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si quieres añadir:
- Nuevas aplicaciones integradas
- Mejoras al sistema de ventanas
- Optimizaciones de rendimiento
- Corrección de bugs

Siéntete libre de hacer un fork y enviar un pull request.

## 🐛 Reportar Bugs

Si encuentras algún problema, por favor crea un issue con:
- Descripción del problema
- Pasos para reproducirlo
- Sistema operativo y versión de Python
- Logs de error (si aplica)

## 🎨 Créditos

- **Fuente Monocraft**: [IdreesInc/Monocraft](https://github.com/IdreesInc/Monocraft)
- **Inspiración**: Windows 11, Linux Desktop Environments
- **Framework**: Pygame

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

<div align="center">

**Hecho con 💖 y mucho ☕**

*Disfruta creando en Pixel-OS!* ✨

</div>
class MiApp(Application):
    def __init__(self):
        super().__init__("Mi App", icon_path="mods/mi_app/icon.png")
    
    def on_open(self):
        # Tu código aquí
        pass
```

## 📁 Estructura del Proyecto

```
pixel-os/
├── assets/          # Recursos (fuentes, imágenes, sonidos)
├── core/            # Motor principal del SO
├── ui/              # Componentes de interfaz
├── apps/            # Aplicaciones integradas
├── mods/            # Plugins y addons de usuario
├── config/          # Configuración del sistema
└── main.py          # Punto de entrada
```

## 🎨 Paleta de Colores Pastel

- **Rosa**: #FFB3D9
- **Azul**: #B3D9FF
- **Verde**: #B3FFD9
- **Amarillo**: #FFE5B3
- **Morado**: #D9B3FF
- **Melocotón**: #FFD4B3

## 📝 Licencia

MIT License
