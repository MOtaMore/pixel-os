# 🖥️ Terminal y Editor de Código - Guía Rápida v1.2

## NUEVAS CARACTERÍSTICAS

### 1. Terminal Mejorada 💻

La Terminal ahora funciona como una **consola real** con navegación completa del filesystem:

**Comandos principales:**
```bash
# Navegación
ls                  # Listar archivos y carpetas
cd <carpeta>        # Cambiar directorio
cd ..               # Ir a carpeta anterior
pwd                 # Mostrar ubicación actual

# Archivos
cat <archivo>       # Ver contenido de archivo
goul <archivo>      # Ejecutar programa Goul
touch <archivo>     # Crear archivo vacío
mkdir <carpeta>     # Crear carpeta

# Utilidad
help                # Ver todos los comandos
clear               # Limpiar pantalla
```

**Ejemplo de uso:**
```bash
~> mkdir MisProyectos
Carpeta 'MisProyectos' creada

~> cd MisProyectos
~/MisProyectos> touch proyecto1.goul
Archivo 'proyecto1.goul' creado

~/MisProyectos> ls
[FILE] proyecto1.goul

~/MisProyectos> goul proyecto1.goul
# (ejecuta el archivo)
```

### 2. Editor de Código Mejorado 📝

**Guardado Personalizado:**
1. Presiona `Ctrl+S` o haz clic en Guardar
2. Se abre un diálogo de entrada
3. Escribe el nombre del archivo
4. Presiona Enter (automáticamente agrega `.goul`)
5. Listo! Archivo guardado en Documentos/

**Características:**
- ✅ Diálogo de nombre personalizado
- ✅ Auto-extensión `.goul`
- ✅ Ver nombre actual en barra superior
- ✅ Sintaxis highlighting mejorado
- ✅ Atajos de teclado intuitivos

**Atajos:**
```
Ctrl+S    → Guardar con nombre personalizado
F5        → Ejecutar código y ver output
ESC       → Cancelar diálogo
```

### 3. Integración Terminal + Editor 🔄

Ahora puedes:

1. **Escribir código en el Editor**
   - Edita el archivo
   - Presiona F5 para ver resultados

2. **Guardarcon nombre propio**
   - Ctrl+S → Escribe nombre → Enter
   - Se guarda en Documentos/

3. **Ejecutar desde Terminal**
   ```bash
   ~> cd Documentos
   ~/Documentos> goul mi_programa.goul
   # Output aparece en Terminal
   ```

## FLUJO DE TRABAJO

### Opción 1: Editor local
```
Editor → Código → F5 → Ver Output en Editor
```

### Opción 2: Editor + Terminal
```
Editor → Código → Ctrl+S → "archivo"
Terminal → cd Documentos
Terminal → goul archivo.goul → Ver Output
```

### Opción 3: Crear en Terminal
```
Terminal → touch script.goul
Editor → Abrir y editar
Terminal → goul script.goul
```

## EJEMPLOS PRÁCTICOS

### Crear un Proyecto
```bash
~> mkdir MiProyecto
~> cd MiProyecto
~/MiProyecto> 

# Abre Editor y guarda archivo aquí
# O desde Terminal: touch programa.goul
```

### Ejecutar Programa
```bash
# En Terminal
~/Documentos> goul calculadora.goul

# Output:
# 10 + 5 = 15
# 20 - 3 = 17
```

### Ver Código Guardado
```bash
~/Documentos> cat calculadora.goul
// Calculadora simple
var a = 10;
var b = 5;
print("10 + 5 = " + str(a + b));
```

## ESTRUCTURA DEL FILESYSTEM

Desde Terminal, tienes acceso a:

```
/ (raíz)
├── Documentos/      ← Guardan aquí con Ctrl+S
├── Imágenes/
├── Música/
├── Vídeos/
├── Descargas/
└── Papelera/
```

Puedes crear más carpetas con `mkdir`

## TROUBLESHOOTING

**Q: No veo mis archivos en la Terminal**
```bash
# Verifica la ruta actual
~> pwd
Ubicación actual: /

# Navega a Documentos
~> cd Documentos
~/Documentos> ls
```

**Q: Quiero ejecutar un archivo que guardé**
```bash
# Primero ve a la carpeta
~> cd Documentos

# Luego ejecuta
~/Documentos> goul archivo.goul
```

**Q: El archivo no se guarda**
1. Presiona Ctrl+S
2. Escribe nombre (sin .goul)
3. Presiona Enter
4. Ver confirmación en Output del Editor

## PRÓXIMAS CARACTERÍSTICAS

- 🔜 Funciones: `function nombre(params) { }`
- 🔜 Clases: `class Persona { }`
- 🔜 Módulos: `use "archivo";`
- 🔜 APIs: `filesystem.read()`, `filesystem.write()`

## DOCUMENTACIÓN COMPLETA

Para más detalles, ver:
- [Características Completas](docs/FEATURES_v1.2.md)
- [Lenguaje Goul](docs/GOUL_LANGUAGE.md)
- [Ejemplos de Código](examples/)

---

**¡Listo para programar!** 🚀
