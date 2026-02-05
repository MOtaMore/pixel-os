# 🎉 Nuevas Características de Pixel-OS v1.1

## 📝 Editor de Código Mejorado

### Funcionalidades Nuevas

#### ✅ Guardar Archivos
- **Atajo**: `Ctrl+S`
- **Ubicación**: Los archivos se guardan automáticamente en `Documentos/`
- **Formato**: Archivos con extensión `.goul`
- **Feedback**: Mensaje de confirmación en el panel de output

#### ✅ Ejecutar Código
- **Atajo**: `F5`
- **Botón**: Click en "▶ Ejecutar"
- **Output**: Resultados visibles en el panel inferior
- **Errores**: Mensajes de error mostrados en el output

#### ✅ Panel de Output
- **Toggle**: Botón "Output" para mostrar/ocultar
- **Contenido**: Muestra resultados de ejecución y mensajes del sistema
- **Límite**: Muestra las últimas 10 líneas de output

#### ✅ Interfaz Mejorada
- Tema oscuro optimizado para programación
- Números de línea visibles
- Highlight de la línea actual
- Cursor parpadeante
- Sintaxis highlighting básico (comentarios, palabras clave)
- Indentación automática con Tab
- Barra superior con nombre de archivo
- Hints de atajos de teclado

## 🎨 Lenguaje Goul

### ¿Qué es Goul?

Goul es un lenguaje de programación híbrido entre Python y C#, diseñado específicamente para Pixel-OS. Es simple de aprender pero poderoso para crear cosas creativas.

### Características Actuales

#### Variables
```goul
var nombre = "Pixel";
let edad = 25;
var pi = 3.14;
var activo = true;
```

#### Tipos de Datos
- **String**: `"texto"` o `'texto'`
- **Number**: `42`, `3.14`, `-10`
- **Boolean**: `true`, `false`
- **Array**: `[1, 2, 3, 4]`

#### Operadores
- Aritméticos: `+`, `-`, `*`, `/`
- Concatenación: `"Hola " + "Mundo"`
- Acceso a arrays: `array[0]`

#### Funciones Integradas
- `print(valor)`: Imprimir en consola
- `len(array)`: Longitud de array
- `str(valor)`: Convertir a string
- `int(valor)`: Convertir a entero
- `float(valor)`: Convertir a decimal
- `type(valor)`: Obtener tipo de dato

### Ejemplos Incluidos

En la carpeta `examples/` encontrarás:
1. **ejemplo_goul.goul** - Introducción básica al lenguaje
2. **calculadora.goul** - Calculadora avanzada con operaciones
3. **rpg_simulator.goul** - Simulador de combate RPG
4. **analisis_datos.goul** - Análisis de ventas con estadísticas

### Características Futuras (Próximamente)

#### Clases y POO
```goul
class Persona {
    var nombre;
    var edad;
    
    function saludar() {
        print("Hola, soy " + this.nombre);
    }
}
```

#### Control de Flujo
```goul
if (condicion) {
    // código
}

while (contador < 10) {
    // bucle
}

for (var i = 0; i < 10; i++) {
    // iteración
}
```

#### Métodos de Objetos
```goul
var persona = new Persona();
persona.nombre = "Pixel";
persona.saludar();
```

## 💾 Sistema de Archivos Virtual

### Características

#### ✅ Filesystem Persistente
- Almacenamiento en JSON
- Carga automática al iniciar
- Guardado automático al modificar
- Ubicación: `user_data/filesystem/filesystem.json`

#### ✅ Estructura Predeterminada
- 📁 Documentos
- 🖼️ Imágenes
- 🎵 Música
- 🎬 Vídeos
- 📥 Descargas
- 🗑️ Papelera

#### ✅ Operaciones Soportadas
- Crear archivos y carpetas
- Guardar contenido en archivos
- Listar contenidos de directorios
- Navegación por rutas
- Timestamps automáticos (creación y modificación)

### API de Filesystem

```python
# Crear archivo
filesystem.create_file("Documentos", "mi_codigo.goul", "var x = 10;", "goul")

# Guardar archivo existente
filesystem.save_file("Documentos", "mi_codigo.goul", "var x = 20;")

# Listar directorio
contents = filesystem.list_directory("Documentos")
# Retorna: {'files': [...], 'folders': [...]}

# Navegar a carpeta
folder = filesystem.get_path("Documentos/Trabajo")
```

## 📁 Explorador de Archivos Mejorado

### Nuevas Funcionalidades

#### ✅ Navegación Interactiva
- **Doble Click**: Abrir carpetas
- **Botón Atrás**: Volver a la carpeta anterior
- **Botón Refrescar**: Actualizar contenidos
- **Historial**: Guarda el path de navegación

#### ✅ Visualización Mejorada
- Iconos diferenciados: 📁 para carpetas, 📄 para archivos
- Ruta actual visible en la parte superior
- Highlight al hacer hover
- Selección visual clara
- Ordenado alfabéticamente (carpetas primero)

#### ✅ Integración con Filesystem
- Lee directamente del sistema virtual
- Actualización en tiempo real
- Sincronizado con otras apps

## 🎯 Menú Start

### Características

#### ✅ Lanzador de Aplicaciones
- Click en el botón "SO" de la taskbar
- Lista completa de apps disponibles
- Iconos PNG para cada aplicación
- Click para abrir aplicaciones

#### ✅ Diseño
- Menú estilo Windows 11
- Tamaño: 350x500px
- Fondo con transparencia
- Scroll automático si hay muchas apps

## 🎨 Iconos PNG

### Sistema de Iconos

Todas las aplicaciones ahora tienen iconos PNG personalizados:
- 🖥️ Sistema
- 📝 Editor de Texto
- 📁 Explorador de Archivos
- 💻 Terminal
- ⚙️ Configuración
- 🎵 Reproductor de Música
- 🖼️ Galería
- 🌐 Mini Browser
- 📝 Editor de Código
- 🎬 Reproductor de Video

#### Ubicación
Los iconos se encuentran en: `assets/imgs/icon_[app_id].png`

#### Fallback
Si un icono no se encuentra, se muestra un cuadrado de color como antes.

## 🔧 Integración Técnica

### Flujo de Trabajo

1. **Al abrir el Editor de Código**:
   - Se asigna automáticamente el filesystem
   - El usuario puede escribir código Goul
   
2. **Al presionar Ctrl+S**:
   - El código se guarda en `Documentos/`
   - Se asigna el nombre `sin_titulo.goul` por defecto
   - Aparece confirmación en el output

3. **Al presionar F5**:
   - El código se envía al intérprete Goul
   - Se ejecuta línea por línea
   - Los resultados aparecen en el panel de output
   - Los errores se muestran con mensajes claros

4. **Al abrir el Explorador de Archivos**:
   - Se cargan los contenidos del filesystem virtual
   - Se puede navegar por carpetas
   - Se pueden ver los archivos guardados

### Arquitectura

```
PixelOS
├── VirtualFilesystem (Singleton)
│   ├── Documentos/
│   │   └── sin_titulo.goul (archivo guardado)
│   ├── Imágenes/
│   ├── Música/
│   └── ...
│
├── CodeEditorApp
│   ├── set_filesystem() → Recibe referencia
│   ├── _save_file() → Usa filesystem.create_file()
│   └── _run_code() → Usa run_goul_code()
│
├── FileManagerApp
│   ├── set_filesystem() → Recibe referencia
│   └── _refresh_items() → Usa filesystem.list_directory()
│
└── GoulInterpreter
    ├── execute(code) → Ejecuta el código
    └── run_goul_code(code) → Wrapper simple
```

## 📊 Comparación: Antes vs Ahora

| Característica | Antes (v1.0) | Ahora (v1.1) |
|----------------|--------------|--------------|
| **Editor de Código** | Solo visualización | Guardar y ejecutar |
| **Lenguaje** | N/A | Goul implementado |
| **File Manager** | Hardcodeado | Filesystem virtual |
| **Persistencia** | No | Sí (JSON) |
| **Iconos** | Cuadrados de color | PNG personalizados |
| **Menú Start** | No | Sí, estilo Win11 |
| **Output de Código** | No | Panel integrado |

## 🚀 Próximos Pasos

### Mejoras Planificadas

1. **Goul Avanzado**:
   - Implementar clases y POO
   - Agregar control de flujo (if, while, for)
   - Métodos de objetos
   - Herencia de clases

2. **Editor de Código**:
   - Diálogo para nombrar archivos al guardar
   - Abrir archivos desde File Manager
   - Auto-completado básico
   - Múltiples pestañas

3. **File Manager**:
   - Crear nuevas carpetas desde UI
   - Eliminar archivos (mover a papelera)
   - Copiar/pegar archivos
   - Búsqueda de archivos

4. **Sistema**:
   - Notificaciones del sistema
   - Gestión de permisos
   - Configuraciones persistentes
   - Temas personalizables

## 📖 Recursos Adicionales

- **Documentación Goul**: `docs/GOUL_LANGUAGE.md`
- **Ejemplos de Código**: `examples/*.goul`
- **README Principal**: `README.md`
- **Sistema de Mods**: `mods/README.md`

## 🎓 Tutoriales Rápidos

### Cómo escribir tu primer programa Goul

1. Abre el Editor de Código
2. Escribe:
   ```goul
   var nombre = "Tu Nombre";
   print("Hola, " + nombre + "!");
   ```
3. Presiona F5
4. ¡Mira el resultado en el output!

### Cómo guardar tu código

1. Escribe tu código en el editor
2. Presiona Ctrl+S
3. El archivo se guarda como `sin_titulo.goul` en Documentos
4. Puedes verlo en el File Manager

### Cómo explorar tus archivos

1. Abre el Explorador de Archivos
2. Doble click en "Documentos"
3. Verás tus archivos .goul guardados
4. Usa el botón "← Atrás" para volver

---

**¡Disfruta de las nuevas características de Pixel-OS v1.1!** 🎉
