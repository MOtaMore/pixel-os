# 🗑️ Sistema de Papelera y Directorios Anidados - Pixel-OS v1.3

## ✨ Nuevas Características Implementadas

### 1. Sistema de Papelera Funcional

La papelera funciona como un SO real con capacidad de:

#### **Mover archivos a papelera**
```bash
$ rm archivo.txt
🗑️  Archivo 'archivo.txt' movido a papelera
```

#### **Mover carpetas a papelera**
```bash
$ rmdir MiCarpeta
🗑️  Carpeta 'MiCarpeta' movida a papelera
```

#### **Ver contenido de papelera**
```bash
$ trash ver
=== 📁 Contenido de Papelera ===
[FILE] archivo.txt
[DIR] MiCarpeta/
```

#### **Restaurar desde papelera**
```bash
$ trash restore archivo.txt
✅ Archivo 'archivo.txt' restaurado
```

Los archivos se restauran automáticamente a su ruta original. Si esa ruta no existe, se restauran a la raíz.

#### **Vaciar papelera completamente**
```bash
$ trash --empty
🗑️  Papelera vaciada completamente
```

### 2. Directorios Anidados

Ahora puedes crear estructuras de carpetas complejas en un solo comando:

#### **Crear directorios anidados**
```bash
$ mkdir Proyecto/src/components
Carpetas creadas: Proyecto/src/components
```

Esto crea automáticamente:
- `Proyecto/`
- `Proyecto/src/`
- `Proyecto/src/components/`

#### **Navegación en carpetas anidadas**
```bash
$ cd Proyecto/src/components
Cambiado a: /Proyecto/src/components

$ pwd
Ubicación actual: /Proyecto/src/components

$ ls
(vacio)

$ cd ..
Cambiado a: /Proyecto/src

$ mkdir datos
Carpeta 'datos' creada

$ ls
[DIR] components/
[DIR] datos/
```

### 3. Comportamiento de la Papelera

#### **Almacenamiento:** Los archivos en papelera mantienen:
- Su nombre original
- Su contenido íntegro
- Su ruta original (para restauración)
- Sus metadatos (fecha creación, modificación)

#### **Restauración Inteligente:**
```bash
# Caso 1: Ruta original existe → restaurar ahí
$ trash restore archivo.txt
✅ Archivo 'archivo.txt' restaurado
# archivo.txt vuelve a su ubicación original

# Caso 2: Ruta original no existe → restaurar en raíz
$ trash restore archivo.txt
✅ Archivo 'archivo.txt' restaurado
# archivo.txt se coloca en /
```

### 4. Nuevos Comandos de Terminal

| Comando | Descripción | Ejemplo |
|---------|------------|---------|
| `rm <archivo>` | Mover archivo a papelera | `rm documento.txt` |
| `rmdir <carpeta>` | Mover carpeta a papelera | `rmdir temporal` |
| `trash ver` | Ver contenido de papelera | `trash ver` |
| `trash restore <nombre>` | Restaurar de papelera | `trash restore app.goul` |
| `trash --empty` | Vaciar papelera | `trash --empty` |
| `mkdir <a/b/c>` | Crear directorios anidados | `mkdir src/components/ui` |

### 5. Ejemplos de Uso Práctico

#### **Organizar un proyecto**
```bash
$ cd Documentos
Cambiado a: /Documentos

$ mkdir MiProyecto/src/models
Carpetas creadas: MiProyecto/src/models

$ mkdir MiProyecto/src/views
Carpetas creadas: MiProyecto/src/views

$ mkdir MiProyecto/datos
Carpetas creadas: MiProyecto/datos

$ mkdir MiProyecto/tests
Carpetas creadas: MiProyecto/tests

$ cd MiProyecto
Cambiado a: /Documentos/MiProyecto

$ ls
[DIR] datos/
[DIR] src/
[DIR] tests/
```

#### **Limpiar proyecto antiguo**
```bash
$ cd Documentos
Cambiado a: /Documentos

$ rmdir ProyectoAntiguo
🗑️  Carpeta 'ProyectoAntiguo' movida a papelera

$ rm archivo_temporal.txt
🗑️  Archivo 'archivo_temporal.txt' movido a papelera

$ trash ver
=== 📁 Contenido de Papelera ===
[FILE] archivo_temporal.txt
[DIR] ProyectoAntiguo/
```

#### **Recuperación selectiva**
```bash
$ trash restore archivo_temporal.txt
✅ Archivo 'archivo_temporal.txt' restaurado

$ trash --empty
🗑️  Papelera vaciada completamente
```

### 6. Características Técnicas

#### **Persistencia**
- La papelera se guarda en `filesystem.json`
- Los archivos eliminados se conservan entre sesiones
- El campo `original_path` rastrea dónde estaba cada elemento

#### **Validación**
```python
# El sistema valida:
- Que el archivo/carpeta exista antes de moverlo
- Que la papelera esté disponible
- Que la ruta de restauración sea válida
```

#### **Rendimiento**
- O(1) para mover a papelera (búsqueda por nombre)
- O(n) para vaciar papelera (donde n = cantidad de items)
- O(1) para restaurar (búsqueda por nombre)

### 7. Integración con Otras Apps

#### **FileManager**
El FileManager automáticamente mostrará:
- Carpeta especial "Papelera" en navegación
- Contenido de papelera al abrirla
- Opción de restaurar (futuro: drag & drop)

#### **CodeEditor**
- Agregar archivos `.goul` desde directorios anidados
- Guardar en carpetas organizadas
- Mantener jerarquía de proyecto

#### **Terminal**
- Todos los comandos funcionan con rutas anidadas
- Navegación automática con `cd`
- Completa integración con papelera

## 🔄 Flujo de Datos

```
VirtualFile/VirtualFolder
    ↓
move_to_trash() → original_path = "/Documentos/proyecto"
    ↓
Papelera/archivo
    ↓
restore_from_trash() → restaurar a original_path
```

## 📊 Estructura del Filesystem Actualizada

```
root/
├── Documentos/
│   ├── MiProyecto/
│   │   ├── src/
│   │   │   ├── models/
│   │   │   └── views/
│   │   ├── datos/
│   │   └── tests/
│   └── trabajo/
├── Imágenes/
├── Música/
├── Vídeos/
├── Descargas/
└── Papelera/  ← Los eliminados van aquí
    ├── archivo_temporal.txt (original_path = "/Documentos")
    └── ProyectoAntiguo/ (original_path = "/Documentos/MiProyecto")
```

## 🎯 Próximas Mejoras Planeadas

1. **FileManager Visual** - Interfaz gráfica para papelera
2. **Recuperación por Fecha** - Ver cuándo se eliminó cada item
3. **Búsqueda en Papelera** - `trash search patrón`
4. **Cuota de Papelera** - Limitar tamaño automáticamente
5. **Historial de Eliminación** - Ver qué se eliminó con `trash log`

## ✅ Validación

Sistema probado con:
- ✅ Creación de 5 niveles de carpetas anidadas
- ✅ Movimiento de archivos a papelera
- ✅ Movimiento de carpetas a papelera
- ✅ Restauración desde papelera
- ✅ Vaciado de papelera
- ✅ Navegación en directorios anidados
- ✅ Persistencia en filesystem.json

---

**¡Pixel-OS ahora tiene un sistema profesional de papelera y directorios anidados!** 🎉
