# 🎉 Mejoras de Pixel-OS v1.2

## 🖥️ Terminal Mejorada

### Nuevos Comandos

La Terminal ahora soporta navegación completa del filesystem virtual y ejecución de archivos:

#### `ls` - Listar directorio
```bash
~> ls
[DIR] Documentos/
[DIR] Imágenes/
[DIR] Música/
[DIR] Vídeos/
```

#### `cd <ruta>` - Cambiar directorio
```bash
~> cd Documentos
~/Documentos> cd ..
~> 
```

#### `pwd` - Mostrar directorio actual
```bash
~/Documentos> pwd
Ubicación actual: /Documentos
```

#### `cat <archivo>` - Ver contenido de archivo
```bash
~/Documentos> cat mi_programa.goul
// Mi primer programa Goul
var nombre = "Pixel";
print("Hola, " + nombre + "!");
```

#### `goul <archivo>` - Ejecutar archivo Goul
```bash
~/Documentos> goul mi_programa.goul
Hola, Pixel!
```

#### `mkdir <nombre>` - Crear carpeta
```bash
~> mkdir ProyectosPython
~ Carpeta 'ProyectosPython' creada
```

#### `touch <nombre>` - Crear archivo vacío
```bash
~> touch archivo.txt
Archivo 'archivo.txt' creado
```

### Características de Terminal
- Navegación por rutas: `/`, directorio padre `..`
- Historial de navegación (futuro: flechas arriba/abajo)
- Prompt dinámico mostrando directorio actual
- Colores diferenciados para comandos y output
- Ejecución de archivos Goul remotamente

### Ejemplo de Flujo Completo

```bash
~> mkdir MisScripts
Carpeta 'MisScripts' creada

~> cd MisScripts
~/MisScripts> touch programa.goul
Archivo 'programa.goul' creado

~/MisScripts> cat programa.goul
(vacio)

~/MisScripts> ls
[FILE] programa.goul

~/MisScripts> goul programa.goul
(sin output)
```

## 📝 Editor de Código Mejorado

### Guardado Personalizado

Ahora puedes guardar archivos con nombres personalizados:

1. **Presiona `Ctrl+S`** o **haz clic en Guardar**
2. Se abre un **diálogo de entrada** de nombre
3. Escribe el nombre del archivo (sin necesidad de `.goul`)
4. Presiona **Enter** para guardar
5. El archivo se guarda en `Documentos/`

### Características Nuevas

- ✅ **Diálogo de guardado**: Ingresa nombre personalizado
- ✅ **Auto-extensión**: Agrega `.goul` automáticamente si no la incluye
- ✅ **Nombre visible**: Muestra el nombre actual en la barra superior
- ✅ **Mejor UI del diálogo**: Incluye hints de uso
- ✅ **ESC para cancelar**: Cancela el guardado presionando ESC

### Atajos de Teclado

| Atajo | Acción |
|-------|--------|
| `Ctrl+S` | Guardar archivo (abre diálogo) |
| `F5` | Ejecutar código |
| `Tab` | Indentación automática |
| `Enter` | Nueva línea con indentación |
| Flechas | Navegación del cursor |

### Mejoras Visuales

- Sintaxis highlighting mejorado
- Detecta palabras clave: `print`, `var`, `let`, `function`, `class`
- Comentarios en verde: `//`
- Panel de output integrado con toggle
- Número de líneas visible

### Ejemplo de Uso

```goul
// Guardado: mi_calculadora.goul

function sumar(a, b) {
    return a + b;
}

var resultado = sumar(10, 5);
print("Resultado: " + str(resultado));

// Output: Resultado: 15
```

## 🔄 Integración Terminal ↔ Editor

### Flujo de Trabajo Completo

1. **Escribe código en el editor**
   ```
   Editor de Código → escribe programa.goul
   ```

2. **Guarda con Ctrl+S**
   ```
   Editor → Diálogo → escribe: "mi_programa"
   → Archivo guardado en Documentos/mi_programa.goul
   ```

3. **Abre Terminal y navega**
   ```
   Terminal: cd Documentos
   ```

4. **Ejecuta archivo con goul**
   ```
   Terminal: goul mi_programa.goul
   → Se ejecuta inmediatamente
   ```

5. **Ve el output en Terminal**
   ```
   Output del programa en Terminal
   ```

### Alternativa: Ejecutar en el Editor

1. Escribe código en Editor
2. Presiona `F5`
3. Ve el output en el panel inferior

## 🎯 Estructura del Filesystem Virtual

Ahora tienes acceso completo desde Terminal:

```
/
├── Documentos/          (guarda aquí con Ctrl+S)
│   ├── mi_programa.goul
│   ├── calculadora.goul
│   └── juego.goul
├── Imágenes/
├── Música/
├── Vídeos/
├── Descargas/
└── Papelera/
```

## 📚 Operaciones Disponibles

### Crear Proyecto

```bash
~> mkdir MiProyecto
Carpeta 'MiProyecto' creada

~> cd MiProyecto
~/MiProyecto> 

# Ahora abre Editor de Código y guarda archivos aquí
# O crea archivo con terminal: touch script.goul
```

### Organizar Código

```bash
~> mkdir Documentos/Utilidades
Carpeta 'Utilidades' creada

~> cd Documentos/Utilidades
~/Documentos/Utilidades> ls
(vacio)
```

### Ejecutar Programas

```bash
~/Documentos> goul mi_programa.goul

# Output se muestra en la terminal
```

## 🚀 Próximas Mejoras Planeadas

### Fase 1: Funciones en Goul
```goul
function saludar(nombre) {
    return "Hola, " + nombre;
}

var mensaje = saludar("Pixel");
print(mensaje);  // Hola, Pixel
```

### Fase 2: Clases en Goul
```goul
class Persona {
    var nombre;
    var edad;
    
    function presentarse() {
        return "Soy " + this.nombre;
    }
}

var p = new Persona();
p.nombre = "Alice";
print(p.presentarse());
```

### Fase 3: Módulos/Imports
```goul
// archivo1.goul
function utilidad() {
    return "Soy una utilidad";
}

// archivo2.goul
use "archivo1";
print(utilidad());  // Accede a función de archivo1
```

### Fase 4: APIs Avanzadas
- Lectura y escritura de archivos
- Operaciones del filesystem desde Goul
- Variables de entorno
- Control total del SO simulado

## 💡 Tips y Trucos

### Copiar código entre archivos
```bash
# En Terminal
~/Documentos> cat programa1.goul
# Copiar output manualmente
```

### Crear backup
```bash
# Rename archivo creando copia
~/Documentos> touch programa_backup.goul
# Luego copiar contenido manualmente
```

### Limpiar Terminal
```bash
~> clear
# Limpia pantalla
```

### Ver fecha/hora
```bash
~> date
05/02/2026 14:30:45
```

## 🐛 Solución de Problemas

### Terminal no reconoce comando
```bash
~/Documentos> foo
Comando desconocido: 'foo'. Escribe 'help' para ayuda.
```
→ Escribe `help` para ver comandos disponibles

### No puedo encontrar mi archivo
```bash
~> cd Documentos
~/Documentos> ls
[FILE] archivo.goul
```
→ Usa `ls` para listar archivos en directorio actual

### Error al ejecutar Goul
```bash
~/Documentos> goul noexiste.goul
Error: Archivo 'noexiste.goul' no encontrado
```
→ Verifica que el archivo existe con `ls`

## 📖 Referencia Rápida

### Comandos de Navegación
```bash
pwd              # Ver ubicación actual
ls               # Listar contenido
cd <ruta>        # Cambiar directorio
cd ..            # Ir atrás
cd /             # Ir a raíz
```

### Comandos de Archivo
```bash
touch <nombre>   # Crear archivo
mkdir <nombre>   # Crear carpeta
cat <archivo>    # Ver contenido
goul <archivo>   # Ejecutar Goul
```

### Otros
```bash
help             # Ayuda
clear            # Limpiar pantalla
echo <texto>     # Imprimir texto
date             # Fecha/hora
```

## ✨ Resumen de Mejoras v1.2

| Feature | Estado | Detalles |
|---------|--------|----------|
| Terminal con fs | ✅ | Plenos comandos ls, cd, cat, goul |
| Guardado personalizado | ✅ | Diálogo + auto-extensión |
| Navegación completa | ✅ | Rutas relativas y absolutas |
| Ejecución remota | ✅ | Ejecutar Goul desde Terminal |
| Mejor UI | ✅ | Diálogo profesional |
| Funciones Goul | ⏳ | Próxima fase |
| Clases Goul | ⏳ | Próxima fase |
| Módulos/Imports | ⏳ | Próxima fase |

---

**¡Disfruta de las nuevas características!** 🚀

Para preguntas o sugerencias, con gusto ayudaré a implementar más mejoras.
