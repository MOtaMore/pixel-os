# 📝 Changelog - Pixel-OS

Todos los cambios notables del proyecto se documentan aquí.

## [1.0.0] - 2026-02-04

### ✨ Agregado
- **Sistema Base**
  - Motor principal con bucle de juego a 60 FPS
  - Gestor de ventanas con soporte para múltiples ventanas
  - Sistema de plugins/mods completamente funcional
  - Gestor de temas con fuente Monocraft integrada

- **UI Components**
  - Desktop con iconos arrastrables
  - Barra de tareas estilo Windows 11
  - Ventanas con bordes redondeados y sombras
  - Botones de control (minimizar, maximizar, cerrar)
  - Animaciones suaves y transiciones

- **Aplicaciones Integradas**
  - Terminal interactiva con comandos personalizados
  - Editor de texto básico pero funcional
  - Explorador de archivos con vista de lista
  - Panel de configuración del sistema

- **Mods de Ejemplo**
  - Calculadora con diseño pastel
  - Paint/aplicación de dibujo
  
- **Sistema de Ventanas**
  - Arrastrar y soltar ventanas
  - Maximizar/restaurar ventanas
  - Minimizar a barra de tareas
  - Focus automático al hacer click
  - Gestión de Z-order (capas)

- **Paleta de Colores**
  - 6 colores pastel principales
  - Colores de UI consistentes
  - Temas personalizables

- **Documentación**
  - README.md completo
  - MODDING_GUIDE.md con ejemplos
  - Comentarios en código
  - Script de información del sistema

- **Herramientas de Desarrollo**
  - create_mod.py para generar plantillas
  - info.py para estadísticas del proyecto
  - Configuraciones de VS Code
  - Sistema de debug integrado

### 🎨 Características Visuales
- Diseño pixel art cozy
- Animaciones fluidas
- Efectos de hover
- Sombras suaves
- Bordes redondeados

### 🔧 Características Técnicas
- Arquitectura POO completa
- Sistema modular y extensible
- Carga dinámica de plugins
- Event system robusto
- 60 FPS estables

### 📚 Documentación
- Guía completa de modding
- Ejemplos de código
- Best practices
- API documentation

---

## [Futuras Versiones]

### Ideas para v1.1.0
- [ ] Menú Start funcional con búsqueda
- [ ] Notificaciones del sistema
- [ ] Selector de temas (modo oscuro)
- [ ] Sonidos ambiente suaves
- [ ] Wallpapers personalizables
- [ ] Dock/lanzador de apps alternativo

### Ideas para v1.2.0
- [ ] Sistema de archivos virtual
- [ ] Persistencia de datos
- [ ] Multi-escritorio/workspaces
- [ ] Atajos de teclado globales
- [ ] Panel de widgets

### Ideas para v2.0.0
- [ ] Multitarea real con procesos
- [ ] Networking entre instancias
- [ ] Tienda de mods integrada
- [ ] Editor visual de temas
- [ ] Sistema de logros
- [ ] Tutorial interactivo

---

## 🐛 Bugs Conocidos

Ninguno reportado actualmente. Si encuentras alguno, ¡crea un issue!

## 🤝 Contribuciones

Si quieres contribuir:
1. Haz fork del proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

**Convenciones de versioning**: [Semantic Versioning](https://semver.org/)
- MAJOR: Cambios incompatibles en la API
- MINOR: Nuevas funcionalidades compatibles
- PATCH: Correcciones de bugs
