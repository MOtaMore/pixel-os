# 📚 Guía Completa del Lenguaje Goul

## 📖 Índice

1. [Introducción](#introducción)
2. [Conceptos Básicos](#conceptos-básicos)
3. [Variables y Tipos de Datos](#variables-y-tipos-de-datos)
4. [Operadores](#operadores)
5. [Estructuras de Control](#estructuras-de-control)
6. [Arrays y Listas](#arrays-y-listas)
7. [Strings y Concatenación](#strings-y-concatenación)
8. [Funciones Built-in](#funciones-built-in)
9. [Funciones Personalizadas](#funciones-personalizadas)
10. [Clases y POO](#clases-y-poo)
11. [HTML y Web](#html-y-web)
12. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Introducción

**Goul** es un lenguaje de programación integrado en Pixel-OS que combina características de Python y C#. Es simple de aprender pero poderoso para crear programas complejos.

### Características:
- ✅ Sintaxis limpia y fácil de entender
- ✅ Variables sin tipado estricto
- ✅ Soporte para funciones definidas por usuario
- ✅ Programación orientada a objetos (POO)
- ✅ Generación de contenido HTML
- ✅ Integración con el filesystem de Pixel-OS

### Ejecutar código Goul:
1. Abrir el **Code Editor**
2. Escribir código
3. Presionar **F5** para ejecutar
4. Ver resultado en panel Output

---

## Conceptos Básicos

### Primer Programa

```goul
// Mi primer programa
print("¡Hola, Goul!");
print("Bienvenido a Pixel-OS");
```

**Output:**
```
¡Hola, Goul!
Bienvenido a Pixel-OS
```

### Comentarios

```goul
// Comentario de línea
/* Comentario de múltiples líneas */

// Usa comentarios para documentar tu código
var x = 10; // Variable x con valor 10
```

---

## Variables y Tipos de Datos

### Declaración de Variables

```goul
// String (texto)
var nombre = "Ana";
var ciudad = "Madrid";

// Número (int)
var edad = 25;
var contador = 0;

// Número decimal (float)
var precio = 19.99;
var promedio = 85.5;

// Booleano (verdadero/falso)
var activo = true;
var conectado = false;

// Array (lista)
var numeros = [1, 2, 3, 4, 5];
var nombres = ["Alice", "Bob", "Charlie"];
```

### Modificar Variables

```goul
var x = 10;
print("Valor inicial: " + str(x));

x = 20;
print("Valor modificado: " + str(x));

x = x + 5;
print("Después de suma: " + str(x));
```

**Output:**
```
Valor inicial: 10
Valor modificado: 20
Después de suma: 25
```

---

## Operadores

### Operadores Aritméticos

```goul
// Suma
var resultado = 5 + 3;
print(resultado);  // 8

// Resta
resultado = 10 - 4;
print(resultado);  // 6

// Multiplicación
resultado = 7 * 3;
print(resultado);  // 21

// División
resultado = 20 / 4;
print(resultado);  // 5

// Módulo (residuo)
resultado = 17 % 5;
print(resultado);  // 2
```

### Operadores de Comparación

```goul
var a = 10;
var b = 20;

// Mayor que
if (a < b) {
    print("a es menor que b");  // Se ejecuta
}

// Menor o igual que
if (a <= 15) {
    print("a es menor o igual a 15");  // Se ejecuta
}

// Igual a
if (a == 10) {
    print("a es igual a 10");  // Se ejecuta
}

// No igual a
if (a != b) {
    print("a no es igual a b");  // Se ejecuta
}
```

### Operadores Lógicos

```goul
// AND (y)
var x = 15;
if (x > 10 && x < 20) {
    print("x está entre 10 y 20");  // Se ejecuta
}

// OR (o)
var hora = 8;
if (hora < 12 || hora > 18) {
    print("Es mañana o noche");  // No se ejecuta (es mañana exacta)
}

// NOT (no)
var lluvia = false;
if (!lluvia) {
    print("No hay lluvia, ir al parque");  // Se ejecuta
}
```

---

## Estructuras de Control

### Condicional if

```goul
var edad = 18;

if (edad >= 18) {
    print("Eres mayor de edad");
} else {
    print("Eres menor de edad");
}
```

### if-else if-else

```goul
var calificacion = 85;

if (calificacion >= 90) {
    print("Excelente - A");
} else if (calificacion >= 80) {
    print("Muy bien - B");
} else if (calificacion >= 70) {
    print("Bien - C");
} else {
    print("Necesita mejorar - F");
}
```

**Output:**
```
Muy bien - B
```

### Bucle for

```goul
// Imprimir números del 1 al 5
for (var i = 1; i <= 5; i = i + 1) {
    print("Número: " + str(i));
}
```

**Output:**
```
Número: 1
Número: 2
Número: 3
Número: 4
Número: 5
```

### Bucle while

```goul
var contador = 1;

while (contador <= 3) {
    print("Iteración " + str(contador));
    contador = contador + 1;
}
```

**Output:**
```
Iteración 1
Iteración 2
Iteración 3
```

---

## Arrays y Listas

### Crear Arrays

```goul
// Array de números
var numeros = [10, 20, 30, 40, 50];

// Array de strings
var frutas = ["manzana", "banana", "naranja"];

// Array mixto
var datos = ["texto", 42, 3.14, true];

// Array vacío
var vacio = [];
```

### Acceder a Elementos

```goul
var frutas = ["manzana", "banana", "naranja"];

// Acceder por índice (0-basado)
print(frutas[0]);  // manzana
print(frutas[1]);  // banana
print(frutas[2]);  // naranja
```

### Modificar Elements

```goul
var colores = ["rojo", "verde", "azul"];

// Cambiar elemento
colores[1] = "amarillo";
print(colores);  // ["rojo", "amarillo", "azul"]
```

### Longitud de Array

```goul
var items = ["a", "b", "c", "d"];
var longitud = len(items);
print("El array tiene " + str(longitud) + " elementos");
```

**Output:**
```
El array tiene 4 elementos
```

### Iterar sobre Arrays

```goul
var numeros = [10, 20, 30];

for (var i = 0; i < len(numeros); i = i + 1) {
    var num = numeros[i];
    print("Valor: " + str(num));
}
```

**Output:**
```
Valor: 10
Valor: 20
Valor: 30
```

---

## Strings y Concatenación

### Crear Strings

```goul
var texto1 = "Hola";
var texto2 = 'Mundo';
var texto3 = "Goul es awesome";
```

### Concatenación de Strings

```goul
var nombre = "Alice";
var apellido = "Smith";
var saludo = "Hola, " + nombre + " " + apellido + "!";
print(saludo);
```

**Output:**
```
Hola, Alice Smith!
```

### Números como Strings

```goul
var edad = 25;
var mensaje = "Tengo " + str(edad) + " años";
print(mensaje);
```

**Output:**
```
Tengo 25 años
```

### Longitud de String

```goul
var texto = "Python";
var longitud = len(texto);
print("La palabra tiene " + str(longitud) + " letras");
```

**Output:**
```
La palabra tiene 6 letras
```

---

## Funciones Built-in

### print()

Imprime un mensaje en la consola.

```goul
print("Hola!");
print("Texto con número: " + str(42));
print("Múltiples mensajes");
```

### len()

Devuelve la longitud de un string, array o lista.

```goul
var texto = "Goul";
print(len(texto));  // 4

var lista = [1, 2, 3, 4, 5];
print(len(lista));  // 5
```

### str()

Convierte un valor a string.

```goul
var numero = 42;
var booleano = true;

print(str(numero));     // "42"
print(str(booleano));   // "true"
```

### int()

Convierte un valor a entero.

```goul
var numero_str = "42";
var numero = int(numero_str);
print(numero + 8);  // 50
```

### float()

Convierte un valor a decimal.

```goul
var numero_str = "3.14";
var pi = float(numero_str);
print(pi);  // 3.14
```

### type()

Devuelve el tipo de datos de un valor.

```goul
print(type("texto"));           // str
print(type(42));                // int
print(type(3.14));              // float
print(type([1, 2, 3]));         // list
print(type(true));              // bool
```

---

## Funciones Personalizadas

### Definir Funciones

```goul
// Función sin parámetros
function saludar() {
    print("¡Hola desde una función!");
}

// Llamar la función
saludar();
```

**Output:**
```
¡Hola desde una función!
```

### Funciones con Parámetros

```goul
function sumar(a, b) {
    var resultado = a + b;
    return resultado;
}

var suma = sumar(10, 20);
print("La suma es: " + str(suma));
```

**Output:**
```
La suma es: 30
```

### Múltiples Parámetros

```goul
function presentar(nombre, edad, ciudad) {
    var mensaje = "Me llamo " + nombre + ", tengo " + str(edad) + " años y vivo en " + ciudad;
    print(mensaje);
}

presentar("Carlos", 30, "Barcelona");
```

**Output:**
```
Me llamo Carlos, tengo 30 años y vivo en Barcelona
```

### Funciones que Retornan Valores

```goul
function calcular_area_rectangulo(ancho, alto) {
    return ancho * alto;
}

function calcular_area_circulo(radio) {
    return 3.14159 * radio * radio;
}

var area_rect = calcular_area_rectangulo(5, 10);
var area_circ = calcular_area_circulo(7);

print("Área rectángulo: " + str(area_rect));
print("Área círculo: " + str(area_circ));
```

**Output:**
```
Área rectángulo: 50
Área círculo: 153.93929999999998
```

---

## Clases y POO

### Crear Clases

```goul
class Persona {
    var nombre;
    var edad;
    
    function presentarse() {
        return "Soy " + this.nombre + " y tengo " + str(this.edad) + " años";
    }
}

var persona1 = new Persona();
persona1.nombre = "Elena";
persona1.edad = 28;
print(persona1.presentarse());
```

**Output:**
```
Soy Elena y tengo 28 años
```

### Clases con Métodos

```goul
class Calculadora {
    function suma(a, b) {
        return a + b;
    }
    
    function multiplicar(a, b) {
        return a * b;
    }
    
    function potencia(base, exponente) {
        var resultado = 1;
        for (var i = 0; i < exponente; i = i + 1) {
            resultado = resultado * base;
        }
        return resultado;
    }
}

var calc = new Calculadora();
print("5 + 3 = " + str(calc.suma(5, 3)));
print("6 * 7 = " + str(calc.multiplicar(6, 7)));
print("2^5 = " + str(calc.potencia(2, 5)));
```

**Output:**
```
5 + 3 = 8
6 * 7 = 42
2^5 = 32
```

---

## HTML y Web

### Generar HTML

```goul
var contenido_html = html("<h1>Mi Primera Página Web</h1><p>Creada con Goul</p>");
```

### Crear Etiquetas

```goul
var titulo = tag("h1", "Bienvenido");
var parrafo = tag("p", "Este es un párrafo", {"class": "importante"});
var enlace = tag("a", "Google", {"href": "https://google.com"});

var pagina = html(titulo + parrafo + enlace);
```

### Agregar Estilos CSS

```goul
var estilo = css("body", {
    "background-color": "#f0f0f0",
    "font-family": "Arial, sans-serif",
    "color": "#333"
});

var titulo_style = css("h1", {
    "color": "#0066cc",
    "text-align": "center",
    "border-bottom": "2px solid #0066cc"
});

var pagina = "<style>" + estilo + titulo_style + "</style>" + html("<h1>Mi Sitio</h1>");
```

---

## Ejemplos Prácticos

### 1. Calculadora Básica

```goul
// Programa: Calculadora Simple
print("=== Calculadora Goul ===\n");

function calcular(a, operador, b) {
    if (operador == "+") {
        return a + b;
    } else if (operador == "-") {
        return a - b;
    } else if (operador == "*") {
        return a * b;
    } else if (operador == "/") {
        return a / b;
    }
    return 0;
}

var resultado1 = calcular(50, "+", 30);
var resultado2 = calcular(100, "-", 25);
var resultado3 = calcular(12, "*", 8);
var resultado4 = calcular(144, "/", 12);

print("50 + 30 = " + str(resultado1));
print("100 - 25 = " + str(resultado2));
print("12 * 8 = " + str(resultado3));
print("144 / 12 = " + str(resultado4));
```

**Output:**
```
=== Calculadora Goul ===

50 + 30 = 80
100 - 25 = 75
12 * 8 = 96
144 / 12 = 12
```

### 2. Análisis de Datos

```goul
// Programa: Análisis de Notas
print("=== Analizador de Notas ===\n");

var notas = [85, 92, 78, 88, 95, 81, 90];

// Calcular promedio
var suma = 0;
for (var i = 0; i < len(notas); i = i + 1) {
    suma = suma + notas[i];
}
var promedio = suma / len(notas);

// Encontrar máximo
var maximo = notas[0];
for (var i = 1; i < len(notas); i = i + 1) {
    if (notas[i] > maximo) {
        maximo = notas[i];
    }
}

// Encontrar mínimo
var minimo = notas[0];
for (var i = 1; i < len(notas); i = i + 1) {
    if (notas[i] < minimo) {
        minimo = notas[i];
    }
}

print("Total de notas: " + str(len(notas)));
print("Promedio: " + str(promedio));
print("Nota máxima: " + str(maximo));
print("Nota mínima: " + str(minimo));
```

**Output:**
```
=== Analizador de Notas ===

Total de notas: 7
Promedio: 87.28571427857143
Nota máxima: 95
Nota mínima: 78
```

### 3. Generador de Tabla HTML

```goul
// Programa: Crear tabla HTML con datos

function generar_tabla_html(datos, titulo) {
    var html = "<h2>" + titulo + "</h2>";
    html = html + "<table style='border: 1px solid black; border-collapse: collapse;'>";
    
    // Encabezados
    html = html + "<tr>";
    html = html + "<th style='border: 1px solid black; padding: 8px;'>Nombre</th>";
    html = html + "<th style='border: 1px solid black; padding: 8px;'>Edad</th>";
    html = html + "<th style='border: 1px solid black; padding: 8px;'>Ciudad</th>";
    html = html + "</tr>";
    
    return html;
}

var personas = [
    "Alice,28,Madrid",
    "Bob,32,Barcelona",
    "Charlie,25,Valencia"
];

var tabla = generar_tabla_html(personas, "Registro de Personas");
print(tabla);
```

### 4. Sistema de Reservas

```goul
// Programa: Sistema de Reservas Simple

class Reserva {
    var id;
    var nombre;
    var fecha;
    var cantidad;
    var confirmada;
    
    function confirmar() {
        this.confirmada = true;
        return "Reserva #" + str(this.id) + " confirmada";
    }
    
    function detalles() {
        var estado = "No confirmada";
        if (this.confirmada) {
            estado = "Confirmada";
        }
        return "ID: " + str(this.id) + " | " + this.nombre + " | " + this.fecha + " | Personas: " + str(this.cantidad) + " | " + estado;
    }
}

// Crear reservas
var res1 = new Reserva();
res1.id = 1001;
res1.nombre = "Juan García";
res1.fecha = "15/02/2026";
res1.cantidad = 4;
res1.confirmada = false;

var res2 = new Reserva();
res2.id = 1002;
res2.nombre = "María López";
res2.fecha = "20/02/2026";
res2.cantidad = 2;
res2.confirmada = false;

print("=== Sistema de Reservas ===\n");
print(res1.detalles());
print(res2.detalles());

print("\nConfirmando reservas...\n");
print(res1.confirmar());
print(res2.confirmar());

print("\n=== Reservas Confirmadas ===\n");
print(res1.detalles());
print(res2.detalles());
```

**Output:**
```
=== Sistema de Reservas ===

ID: 1001 | Juan García | 15/02/2026 | Personas: 4 | No confirmada
ID: 1002 | María López | 20/02/2026 | Personas: 2 | No confirmada

Confirmando reservas...

Reserva #1001 confirmada
Reserva #1002 confirmada

=== Reservas Confirmadas ===

ID: 1001 | Juan García | 15/02/2026 | Personas: 4 | Confirmada
ID: 1002 | María López | 20/02/2026 | Personas: 2 | Confirmada
```

### 5. Juego: Adivinanza de Número

```goul
// Programa: Juego de Adivinanza

print("╔═══════════════════════════════════╗");
print("║  🎮 JUEGO DE ADIVINANZA 🎮        ║");
print("╚═══════════════════════════════════╝\n");

// El número secreto (en una app real sería random, aquí es fijo)
var numero_secreto = 42;
var intentos = 0;
var adivinado = false;

print("Tengo un número en mente entre 1 y 100");
print("¿Puedes adivinarlo?\n");

// Simulamos 3 intentos
var intentos_lista = [35, 50, 42];

for (var i = 0; i < len(intentos_lista); i = i + 1) {
    var intento = intentos_lista[i];
    intentos = intentos + 1;
    
    print("Intento " + str(intentos) + ": " + str(intento));
    
    if (intento == numero_secreto) {
        print("¡¡¡ CORRECTO !!! 🎉");
        print("¡Adivinaste en " + str(intentos) + " intentos!");
        adivinado = true;
    } else if (intento < numero_secreto) {
        print("El número es MÁS ALTO");
    } else {
        print("El número es MÁS BAJO");
    }
    print("");
}

if (!adivinado) {
    print("Game Over. El número era: " + str(numero_secreto));
}
```

---

## Tips y Mejores Prácticas

### 1. Nomenclatura

```goul
// ✅ Bueno: nombres descriptivos
var edad_usuario = 25;
var cantidad_productos = 100;
function calcular_total_venta(precio, cantidad) {}

// ❌ Evitar: nombres poco claros
var x = 25;
var q = 100;
function calc_tv(p, c) {}
```

### 2. Comentarios Útiles

```goul
// ✅ Bueno: comentario explica qué hace y por qué
// Calculamos el promedio de calificaciones excluyendo la más baja
var promedio = (suma - nota_minima) / (cantidad - 1);

// ❌ Evitar: comentarios obvios
// Suma de 10 más 5
var resultado = 10 + 5;
```

### 3. DRY (Don't Repeat Yourself)

```goul
// ❌ Evitar repetición
print(nombre + " tiene " + str(edad) + " años");
print(nombre2 + " tiene " + str(edad2) + " años");
print(nombre3 + " tiene " + str(edad3) + " años");

// ✅ Mejor: usar funciones
function mostrar_persona(nombre, edad) {
    print(nombre + " tiene " + str(edad) + " años");
}

mostrar_persona(nombre, edad);
mostrar_persona(nombre2, edad2);
mostrar_persona(nombre3, edad3);
```

---

## Ejercicios Prácticos

### Ejercicio 1: Crear una tabla de multiplicar

```goul
// Crea una función que imprima la tabla de multiplicar de un número
function tabla_multiplicar(numero) {
    // TODO: Implementar
}

tabla_multiplicar(5);
// Debe imprimir: 5, 10, 15, 20, 25, 30...
```

### Ejercicio 2: Invertir un string

```goul
// Crea una función que invierta un texto
function invertir_texto(texto) {
    // TODO: Implementar
    return "";
}

var resultado = invertir_texto("Goul");
print(resultado);  // Debe imprimir: luoG
```

### Ejercicio 3: Verificar si es número primo

```goul
// Crea una función que verifique si un número es primo
function es_primo(numero) {
    // TODO: Implementar
    return false;
}

print(es_primo(17));   // true
print(es_primo(20));   // false
```

---

## Recursos Adicionales

- 📝 Terminal Guide: Ver `TERMINAL_GUIDE.md`
- 🎨 Features Completas: Ver `FEATURES_v1.2.md`
- 💾 Sistema de Archivos: Ver `TRASH_AND_FOLDERS.md`
- 🔧 Guía de Desarrollo: Ver `DEVELOPMENT_TIPS.md`

---

## Changelog

### v1.2 (Actual)
- ✅ Concatenación de strings mejorada
- ✅ HTML support básico
- ✅ Nueva función `tag()`
- ✅ Nueva función `css()`
- ✅ Editor de código mejorado
- ✅ Terminal con 13 comandos

### v1.1
- Variables y funciones básicas
- Arrays y strings
- Controles de flujo

### v1.0
- Lanzamiento inicial

---

## FAQ

**P: ¿Dónde guardo mis programas Goul?**
R: En la carpeta **Documentos** o subcarpetas. Usa `Ctrl+S` en el editor para guardar con un nombre personalizado.

**P: ¿Cómo ejecuto un archivo desde la Terminal?**
R: Navega a su carpeta con `cd` y ejecuta `goul nombre_archivo.goul`

**P: ¿Puedo acceder al filesystem desde Goul?**
R: En futuras versiones. Actualmente usa las funciones provistas.

**P: ¿Existe soporte para módulos o imports?**
R: Está en el roadmap para la próxima versión.

---

**Última actualización**: Febrero 2026
**Versión**: 1.2
**Licencia**: MIT

¡Feliz programación con Goul! 🚀
