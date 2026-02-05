# 🎮 Pixel-OS: Un Sistema Operativo Retro en Python

**Pixel-OS v1.4** es un sistema operativo simulado construido con Python y Pygame que captura la esencia de los sistemas antiguos con una estética retro-pastel. Incluye un ecosistema completo de aplicaciones integradas, un lenguaje de programación personalizado llamado **Goul**, y un sistema de plugins completamente extensible.

---

## 📋 Tabla de Contenidos

1. [Características Principales](#características-principales)
2. [Requisitos e Instalación](#requisitos-e-instalación)
3. [Usar Pixel-OS](#usar-pixel-os)
4. [Aplicaciones Integradas](#aplicaciones-integradas)
5. [Terminal y Comandos](#terminal-y-comandos)
6. [Lenguaje Goul - Tutorial Completo](#lenguaje-goul--tutorial-completo)
7. [Sistema de Plugins](#sistema-de-plugins)
8. [Desarrollo](#desarrollo)

---

## ✨ Características Principales

### 🎨 Interfaz Retro-Pastel
- Diseño inspirado en sistemas operativos clásicos (Windows 95/XP, Mac OS 9)
- Colores pastel suaves y agradables a la vista
- Fuente monoespaciada personalizada (Monocraft)
- Ventanas redimensionables, arrastrables y minimizables
- Barra de tareas con menú de inicio estilo Windows

### 💾 Sistema de Archivos Virtual
- Almacenamiento JSON persistente en `filesystem.json`
- Carpetas personalizables (Documentos, Descargas, etc.)
- Papelera con capacidad de restauración
- Soporte para múltiples tipos de archivos
- Permisos y metadatos de archivo

### 🖥️ Terminal Completa
- 15+ comandos integrados (ls, cd, cat, mkdir, etc.)
- Navegación de filesystem
- Ejecución de scripts Goul
- Gestión de archivos y carpetas
- Clipboard integration (Ctrl+C/V/A)
- **Scrollbar funcional con soporte para rueda del mouse** ✨

### 📝 Aplicaciones Incluidas
1. **Terminal**: Línea de comandos completa
2. **Text Editor**: Editor de texto simple
3. **Code Editor**: Editor de código Goul con sintaxis resaltada
4. **File Manager**: Explorador de archivos visual
5. **Mini Browser**: Navegador de HTML simple
6. **Video Player**: Reproductor de video
7. **Settings**: Configuración del sistema
8. **Calculator** (Plugin de ejemplo): Calculadora básica
9. **Paint** (Plugin de ejemplo): Editor de dibujo simple

### 🎮 Sistema de Plugins/Mods
- Arquitectura basada en Application base class
- Carga automática desde carpeta `mods/`
- Acceso completo a filesystem y window manager
- Ejemplo proporcionado: `paint_example.py` y `calculator_example.py`

### 💻 Lenguaje de Programación Goul
- Lenguaje interpretado personalizado
- Sintaxis similar a JavaScript/Python
- Variables, funciones, arrays, objetos
- Operaciones matemáticas y manipulación de strings
- Soporte para HTML generation
- Ciclos (for, while) y condicionales (if/else)
- **¡Tutorial completo incluido más abajo!** 📖

---

## 📦 Requisitos e Instalación

### Requisitos
- **Python 3.8+**
- **Pygame 2.0+**
- **tkinter** (generalmente incluido con Python)

### Instalación

1. **Clonar o descargar el proyecto:**
```bash
cd pixel-os
```

2. **Instalar dependencias:**
```bash
pip install pygame
```

3. **Ejecutar el sistema operativo:**
```bash
python main.py
```

El sistema se iniciará en modo fullscreen sin bordes. Use **ESC** o **Alt+F4** para salir.

---

## 🚀 Usar Pixel-OS

### Interfaz Principal

Cuando inicia Pixel-OS, verá:
- **Pantalla de carga**: Barra de progreso durante la inicialización
- **Desktop**: Fondo con iconos de aplicaciones
- **Taskbar**: Barra inferior con botón de inicio y aplicaciones activas
- **Ventanas**: Aplicaciones flotantes redimensionables

### Navegación Básica

| Acción | Atajo |
|--------|-------|
| Abrir aplicación | Click en icono del escritorio o menú inicio |
| Cerrar ventana | Botón X de la ventana |
| Minimizar ventana | Botón - de la ventana |
| Maximizar ventana | Doble-click en barra de título |
| Mostrar menú inicio | Click en botón de Pixel-OS |
| Apagar sistema | Menú inicio > Apagar |
| Salir | ESC o Alt+F4 |

### Menú de Inicio

El menú de inicio (esquina inferior izquierda) muestra:
- Todas las aplicaciones instaladas
- Botón "Apagar" en rojo al final
- Información sobre aplicación al pasar mouse

---

## 🛠️ Aplicaciones Integradas

### 1. 🖥️ Terminal
La terminal es el corazón de Pixel-OS, proporcionando acceso a comandos del sistema.

**Características:**
- Línea de comandos completa
- Historial de comandos
- Navegación de filesystem
- Ejecución de scripts Goul
- Copy/Paste de historial

**Atajos de Teclado:**
- `Ctrl+A` - Copiar todo el historial al clipboard
- `Ctrl+C` - Copiar entrada actual
- `Ctrl+V` - Pegar desde clipboard

### 2. 📝 Text Editor
Editor simple para archivos de texto plano.

**Características:**
- Edición de múltiples líneas
- Auto-indentación
- Ctrl+A/C/V para copiar/pegar
- Guardado de archivos

### 3. 💻 Code Editor
Editor especializado para código Goul con características avanzadas.

**Características:**
- Sintaxis resaltada para Goul
- Árbol de archivos (Ctrl+T)
- Ejecución de código (F5)
- Guardado (Ctrl+S)
- Panel de salida
- **Scrollbar funcional con mouse wheel** ✨

**Atajos:**
- `F5` - Ejecutar código
- `Ctrl+S` - Guardar archivo
- `Ctrl+A` - Seleccionar todo
- `Ctrl+V` - Pegar código
- `PageUp/PageDown` - Desplazamiento rápido
- `Ctrl+Home/End` - Ir al inicio/final

### 4. 📁 File Manager
Explorador visual del filesystem virtual.

**Características:**
- Vista de carpetas y archivos
- Doble-click para abrir
- Crear carpetas/archivos
- Eliminar (a papelera)
- Abrir con aplicación específica
- Información de archivo

### 5. 🌐 Mini Browser
Navegador HTML simple.

**Características:**
- Renderizado básico de HTML
- Links (limitados)
- Images (soporte)
- Historial de navegación

### 6. 🎬 Video Player
Reproductor multimedia simple.

**Características:**
- Reproducción de archivos de video
- Controles básicos

### 7. ⚙️ Settings
Configuración del sistema.

**Características:**
- Tema del sistema
- Información del SO
- Variables de entorno

---

## 🖥️ Terminal y Comandos

La terminal proporciona poder total sobre el sistema. Escriba `help` para ver todos los comandos.

### Comandos Disponibles

#### Sistema
```bash
help                    # Mostrar ayuda de todos los comandos
clear                   # Limpiar pantalla
date                    # Mostrar fecha y hora actual
echo <texto>           # Imprimir texto
```

#### Navegación de Archivos
```bash
ls                      # Listar directorio actual
cd <ruta>              # Cambiar directorio
cd ..                  # Ir a carpeta padre
cd /                   # Ir a raíz
pwd                    # Mostrar ruta actual
```

#### Gestión de Archivos
```bash
touch <nombre>         # Crear archivo vacío
mkdir <nombre>         # Crear carpeta
mkdir a/b/c            # Crear carpetas anidadas
cat <archivo>          # Mostrar contenido de archivo
rm <archivo>           # Mover archivo a papelera
rmdir <carpeta>        # Mover carpeta a papelera
```

#### Papelera
```bash
trash ver              # Ver contenido de papelera
trash restore <name>   # Restaurar archivo de papelera
trash --empty          # Vaciar papelera completa
```

#### Abrir Archivos
```bash
open <archivo>                  # Abrir con editor
open <archivo> --editor         # Abrir con editor de código
open <archivo> --browser        # Abrir con navegador
open <archivo> --player         # Abrir con reproductor
```

#### Goul (Lenguaje de Programación)
```bash
goul <archivo.goul>    # Ejecutar archivo Goul
```

### Ejemplos de Comandos

```bash
# Crear estructura de carpetas
mkdir Proyectos/Scripts/Goul

# Navegar
cd Proyectos/Scripts/Goul

# Crear archivo
touch mi_script.goul

# Ver archivo
cat mi_script.goul

# Ejecutar código Goul
goul mi_script.goul

# Copiar todo a clipboard
Ctrl+A
```

---

## 🎮 Lenguaje Goul - Tutorial Completo

Goul es un lenguaje de programación simple pero poderoso diseñado específicamente para Pixel-OS. Combina conceptos de JavaScript y Python con una sintaxis accesible.

### 📚 Tutorial: De Principiante a Avanzado

#### NIVEL 1: Conceptos Básicos

##### 1.1 Variables y Tipos de Datos

En Goul, las variables se declaran con la palabra clave `var`:

```goul
// Strings (texto)
var nombre = "Juan";
var mensaje = "Hola, mundo!";

// Numbers (números)
var edad = 25;
var precio = 19.99;
var numero_negativo = -42;

// Booleans (verdadero/falso)
var es_activo = true;
var es_mayor = false;

// Arrays (listas)
var numeros = [1, 2, 3, 4, 5];
var colores = ["rojo", "azul", "verde"];
var mixto = [1, "dos", true];

// Objetos (diccionarios)
var persona = {
  nombre: "Ana",
  edad: 30,
  ciudad: "Madrid"
};
```

**Nota:** Goul detecta automáticamente el tipo de dato basado en el valor asignado.

##### 1.2 Imprimiendo Datos

La función `echo` imprime valores:

```goul
echo "Hola, mundo!";
echo 42;
echo "El resultado es " + 10;

// Convertir a string para concatenar
var numero = 5;
echo "Número: " + str(numero);
```

##### 1.3 Operaciones Matemáticas

```goul
var a = 10;
var b = 3;

echo a + b;        // 13
echo a - b;        // 7
echo a * b;        // 30
echo a / b;        // 3.333...
echo a % b;        // 1 (módulo)
echo a ** b;       // 1000 (exponente)

// Operaciones en cadenas
echo "Hola" + " " + "Mundo";     // "Hola Mundo"
echo "Número: " + 42;            // "Número: 42"
```

##### 1.4 Manipulación de Strings

```goul
var texto = "Goul";

// Funciones de string
echo len(texto);              // 4 (longitud)
echo upper(texto);            // "GOUL"
echo lower(texto);            // "goul"
echo str(123);                // "123" (convertir a string)

// Concatenación
var saludo = "Hola, " + "Goul!";
echo saludo;
```

---

#### NIVEL 2: Control de Flujo

##### 2.1 Condicionales If/Else

```goul
var edad = 18;

if edad >= 18 {
  echo "Eres mayor de edad";
} else {
  echo "Eres menor de edad";
}

// Múltiples condiciones
var calificacion = 85;

if calificacion >= 90 {
  echo "Sobresaliente";
} else {
  if calificacion >= 80 {
    echo "Notable";
  } else {
    if calificacion >= 70 {
      echo "Bien";
    } else {
      echo "Necesita mejorar";
    }
  }
}

// Operadores lógicos
var edad = 25;
var tiene_licencia = true;

if edad >= 18 && tiene_licencia {
  echo "Puedes conducir";
}

if edad < 15 || edad > 65 {
  echo "Posible descuento en transporte";
}
```

**Operadores de Comparación:**
- `==` - Igual
- `!=` - No igual
- `>` - Mayor que
- `<` - Menor que
- `>=` - Mayor o igual
- `<=` - Menor o igual

**Operadores Lógicos:**
- `&&` - Y (AND)
- `||` - O (OR)
- `!` - NO (NOT)

##### 2.2 Bucles For

```goul
// Bucle for simple
for i = 0; i < 5; i = i + 1 {
  echo i;
}
// Salida: 0, 1, 2, 3, 4

// Dos incrementos
for i = 1; i <= 10; i = i + 2 {
  echo i;
}
// Salida: 1, 3, 5, 7, 9

// Recorrer arrays
var frutas = ["manzana", "plátano", "naranja"];
for i = 0; i < len(frutas); i = i + 1 {
  echo frutas[i];
}
```

##### 2.3 Bucles While

```goul
// While básico
var contador = 0;
while contador < 5 {
  echo contador;
  contador = contador + 1;
}

// Procesamiento de datos
var texto = "Goul";
var indice = 0;
while indice < len(texto) {
  echo texto[indice];
  indice = indice + 1;
}
```

---

#### NIVEL 3: Funciones

##### 3.1 Crear Funciones

```goul
// Función sin parámetros
fn saludar {
  echo "¡Hola, Goul!";
}

// Llamar función
saludar();

// Función con parámetros
fn sumar(a, b) {
  var resultado = a + b;
  return resultado;
}

// Usar función
var suma = sumar(5, 3);
echo suma;  // 8

// Función con múltiples líneas
fn calcular_descuento(precio, porcentaje) {
  var descuento = (precio * porcentaje) / 100;
  var precio_final = precio - descuento;
  return precio_final;
}

var precio_producto = 100;
var price_con_descuento = calcular_descuento(precio_producto, 20);
echo "Precio final: " + str(price_con_descuento);  // 80
```

##### 3.2 Funciones Integradas

```goul
// Strings
var texto = "Goul";
echo len(texto);           // 4
echo upper(texto);         // "GOUL"
echo lower(texto);         // "goul"

// Números
echo str(42);              // "42"
echo int("123");           // 123 (convertir string a número)
echo abs(-10);             // 10

// Arrays
var lista = [1, 2, 3];
echo len(lista);           // 3
echo str(lista);           // "[1, 2, 3]"

// Objetos
var persona = {nombre: "Ana", edad: 30};
echo len(persona);         // 2 (número de pares clave-valor)
```

---

#### NIVEL 4: Trabajar con Arrays

##### 4.1 Accediendo a Arrays

```goul
var colores = ["rojo", "verde", "azul"];

// Acceder a elemento
echo colores[0];      // "rojo"
echo colores[1];      // "verde"
echo colores[2];      // "azul"

// Obtener número de elementos
echo len(colores);    // 3

// Recorrer array
for i = 0; i < len(colores); i = i + 1 {
  echo colores[i];
}
```

##### 4.2 Operaciones con Arrays

```goul
var números = [1, 2, 3, 4, 5];

// Sumar todos los números
fn sumar_array(arr) {
  var total = 0;
  for i = 0; i < len(arr); i = i + 1 {
    total = total + arr[i];
  }
  return total;
}

echo sumar_array(números);  // 15

// Buscar máximo
fn encontrar_maximo(arr) {
  var max = arr[0];
  for i = 1; i < len(arr); i = i + 1 {
    if arr[i] > max {
      max = arr[i];
    }
  }
  return max;
}

echo encontrar_maximo([3, 7, 2, 9, 1]);  // 9
```

---

#### NIVEL 5: Trabajar con Objetos

##### 5.1 Crear y Acceder Objetos

```goul
// Crear objeto
var persona = {
  nombre: "Carlos",
  edad: 28,
  ciudad: "Barcelona",
  es_programador: true
};

// Acceder propiedades
echo persona["nombre"];  // "Carlos"
echo persona["edad"];    // 28

// Modificar propiedades
persona["edad"] = 29;
echo persona["edad"];    // 29

// Agregar nueva propiedad
persona["email"] = "carlos@ejemplo.com";
```

##### 5.2 Objetos Complejos

```goul
// Objeto con arrays
var empresa = {
  nombre: "TechCorp",
  empleados: ["Ana", "Juan", "María"],
  ubicación: "Madrid"
};

echo empresa["empleados"][0];  // "Ana"

// Array de objetos
var usuarios = [
  {nombre: "Ana", edad: 25},
  {nombre: "Juan", edad: 30},
  {nombre: "María", edad: 28}
];

echo usuarios[0]["nombre"];    // "Ana"
echo usuarios[1]["edad"];      // 30

// Recorrer array de objetos
for i = 0; i < len(usuarios); i = i + 1 {
  var usuario = usuarios[i];
  echo usuario["nombre"];
}
```

---

#### NIVEL 6: HTML Generation

##### 6.1 Generar HTML

Goul tiene soporte especial para generar HTML:

```goul
// Función tag() crea etiquetas HTML
var contenido = tag("h1", "Bienvenido a Goul");
var parrafo = tag("p", "Este es un párrafo");
var lista = tag("ul", "<li>Elemento 1</li><li>Elemento 2</li>");

// Generar HTML completo
fn generar_pagina(titulo, contenido) {
  var html = "<html><body>";
  html = html + tag("h1", titulo);
  html = html + tag("p", contenido);
  html = html + "</body></html>";
  return html;
}

var pagina = generar_pagina("Mi Página", "Hola mundo");
echo pagina;
```

##### 6.2 Funciones HTML

```goul
// tag() - Crear etiquetas
tag("h1", "Título");     // <h1>Título</h1>
tag("p", "Texto");       // <p>Texto</p>

// taghtml() - Crear etiquetas con atributos
taghtml("h1", "Título", {id: "main", class: "custom"});
// <h1 id="main" class="custom">Título</h1>
```

---

#### NIVEL 7: Proyectos Prácticos

##### 7.1 Generador de Tabla de Multiplicar

```goul
fn generar_tabla_multiplicar(numero) {
  var resultado = numero + " x ";
  
  for i = 1; i <= 10; i = i + 1 {
    if i < 10 {
      resultado = resultado + str(i * numero) + ", ";
    } else {
      resultado = resultado + str(i * numero);
    }
  }
  
  return resultado;
}

echo generar_tabla_multiplicar(7);
// 7 x 7, 14, 21, 28, 35, 42, 49, 56, 63, 70
```

##### 7.2 Validador de Email Básico

```goul
fn validar_email(email) {
  var tiene_arroba = false;
  
  for i = 0; i < len(email); i = i + 1 {
    if email[i] == "@" {
      tiene_arroba = true;
    }
  }
  
  var tiene_punto = false;
  for i = 0; i < len(email); i = i + 1 {
    if email[i] == "." {
      tiene_punto = true;
    }
  }
  
  if tiene_arroba && tiene_punto {
    return "Email válido";
  } else {
    return "Email inválido";
  }
}

echo validar_email("usuario@ejemplo.com");  // Email válido
echo validar_email("usuarioejemplo.com");   // Email inválido
```

##### 7.3 Generador de HTML Simple para Blog

```goul
fn crear_post(titulo, contenido, autor, fecha) {
  var html = "<article>";
  html = html + tag("h2", titulo);
  html = html + tag("p", contenido);
  html = html + tag("small", "Por " + autor + " el " + fecha);
  html = html + "</article>";
  return html;
}

var post = crear_post(
  "Mi Primer Post",
  "Este es el contenido del post",
  "Usuario",
  "2026-02-05"
);

echo post;
```

---

### 🔧 Referencia Completa de Goul

#### Variables
```goul
var nombre = "valor";      // Declare variable
nombre = "nuevo_valor";    // Asignar valor
```

#### Operadores
```goul
// Matemáticos: +, -, *, /, %, ** (exponente)
// Comparación: ==, !=, <, >, <=, >=
// Lógicos: &&, ||, !
// String: + (concatenación)
```

#### Control de Flujo
```goul
if condicion { ... }
if condicion { ... } else { ... }

for i = inicio; i < fin; i = i + paso { ... }
while condicion { ... }

fn nombre(param1, param2) { return valor; }
fn nombre { ... }  // Sin parámetros
```

#### Funciones Integradas
```goul
// String
len(str)        // Longitud
upper(str)      // Mayúsculas
lower(str)      // Minúsculas
str(value)      // Convertir a string

// Número
abs(num)        // Valor absoluto
int(str)        // Convertir a entero

// Array/Objeto
len(arr)        // Longitud/tamaño
str(arr)        // Convertir a string

// HTML
tag(nombre, contenido)                    // Etiqueta simple
taghtml(nombre, contenido, atributos)     // Con atributos
```

#### Ejemplo Completo

```goul
// Programa: Calificador de Examen

fn calcular_calificacion(preguntas_correctas, total) {
  var porcentaje = (preguntas_correctas * 100) / total;
  
  if porcentaje >= 90 {
    return "A - Sobresaliente";
  } else {
    if porcentaje >= 80 {
      return "B - Notable";
    } else {
      if porcentaje >= 70 {
        return "C - Bien";
      } else {
        if porcentaje >= 60 {
          return "D - Aprobado";
        } else {
          return "F - Desaprobado";
        }
      }
    }
  }
}

// Datos de estudiantes
var estudiantes = [
  {nombre: "Ana", correctas: 45, total: 50},
  {nombre: "Juan", correctas: 40, total: 50},
  {nombre: "María", correctas: 35, total: 50}
];

// Procesar cada estudiante
echo "<h1>Resultados del Examen</h1>";

for i = 0; i < len(estudiantes); i = i + 1 {
  var estudiante = estudiantes[i];
  var calificacion = calcular_calificacion(
    estudiante["correctas"],
    estudiante["total"]
  );
  
  var html = "<div>";
  html = html + tag("h3", estudiante["nombre"]);
  html = html + tag("p", estudiante["correctas"] + "/" + estudiante["total"]);
  html = html + tag("p", calificacion);
  html = html + "</div>";
  
  echo html;
}
```

---

## 🔌 Sistema de Plugins

Pixel-OS es completamente extensible. Puede crear sus propias aplicaciones.

### Crear un Plugin

1. **Crear archivo en `mods/` carpeta:**

```python
# mods/mi_aplicacion.py
from core.plugin_manager import Application
import pygame
from config.settings import Colors

class MiAplicacion(Application):
    def __init__(self):
        super().__init__(
            name="Mi Aplicación",
            icon_path="mods/mi_app/icon.png",  # Opcional
            color=(200, 150, 200),  # Color pastel RGB
            app_id="mi_aplicacion"  # ID único
        )
        self.data = "Estado inicial"
    
    def handle_event(self, event):
        """Maneja eventos de teclado y mouse"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                self.data = "Presionó A"
    
    def render(self, surface, rect):
        """Renderiza la aplicación en la ventana"""
        # Fondo
        pygame.draw.rect(surface, (40, 35, 50), rect)
        
        # Texto
        font = pygame.font.Font(None, 24)
        text = font.render(self.data, True, (200, 200, 200))
        surface.blit(text, (rect.x + 20, rect.y + 20))
    
    def on_open(self):
        """Llamado cuando se abre la aplicación"""
        print(f"Abierto: {self.name}")
    
    def on_close(self):
        """Llamado cuando se cierra la aplicación"""
        print(f"Cerrado: {self.name}")
```

2. **Reiniciar Pixel-OS** - El plugin se cargará automáticamente

### Ejemplos Incluidos

- `mods/calculator_example.py` - Calculadora simple
- `mods/paint_example.py` - Aplicación de dibujo

---

## 🛠️ Desarrollo

### Estructura del Proyecto

```
pixel-os/
├── main.py                      # Punto de entrada
├── config/
│   ├── settings.py              # Configuración global
│   └── i18n.py                  # Internacionalización
├── core/
│   ├── engine.py                # Motor principal
│   ├── window_manager.py         # Gestión de ventanas
│   ├── theme_manager.py          # Temas y diseño
│   ├── plugin_manager.py         # Sistema de plugins
│   ├── filesystem.py             # Filesystem virtual
│   └── goul_interpreter.py       # Intérprete de Goul
├── ui/
│   ├── desktop.py                # Escritorio
│   ├── taskbar.py                # Barra de tareas
│   └── colors.py                 # Paleta de colores
├── apps/
│   └── builtin_apps.py           # Aplicaciones integradas
├── mods/
│   ├── calculator_example.py      # Ejemplo: Calculadora
│   └── paint_example.py           # Ejemplo: Paint
├── assets/
│   ├── fonts/                    # Fuentes
│   └── imgs/                     # Imágenes
└── README.md                     # Este archivo
```

### Contribuciones

Se aceptan contribuciones para:
- Nuevas aplicaciones integradas
- Mejoras en el lenguaje Goul
- Optimizaciones de rendimiento
- Corrección de bugs
- Mejor documentación

### Próximas Características Planeadas

- [ ] Soporte para archivos de imagen en File Manager
- [ ] Editor de HTML visual
- [ ] Soporte para importación de módulos en Goul
- [ ] Temas personalizables de usuario
- [ ] Multiplayer (compartir filesystem en red)
- [ ] Animaciones más fluidas
- [ ] Más aplicaciones integradas

---

## 📝 Licencia

Pixel-OS está disponible bajo licencia MIT. Ver `LICENSE` para más detalles.

---

## 🙏 Créditos

- Diseño de interfaz inspirado en sistemas retro clásicos
- Fuente Monocraft utilizada bajo su licencia correspondiente
- Pygame como base de renderizado
- Toda una comunidad que ama lo retro ✨

---

## 📞 Soporte

Para reportar bugs o sugerir características, por favor cree un issue en el repositorio.

Para preguntas sobre **Goul**, consulte el tutorial completo en este README.

---

**¡Disfrute Pixel-OS!** 🎮✨
