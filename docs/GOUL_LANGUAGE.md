# 🎨 Lenguaje de Programación Goul

Goul es un lenguaje de programación híbrido entre Python y C# diseñado para Pixel-OS. Es simple pero permite crear cosas creativas.

## 🚀 Características

- **Variables**: Declaración con `var` o `let`
- **Funciones**: Sistema de funciones integradas
- **Arrays**: Soporte para listas
- **Expresiones**: Operaciones aritméticas y lógicas
- **POO (Próximamente)**: Clases y objetos

## 📝 Sintaxis Básica

### Variables

```goul
// Declaración de variables
var nombre = "Pixel";
let edad = 25;
var pi = 3.14;
var activo = true;
```

### Tipos de Datos

- **Strings**: `"texto"` o `'texto'`
- **Numbers**: `42`, `3.14`, `-10`
- **Booleans**: `true`, `false`
- **Arrays**: `[1, 2, 3, 4]`

### Operadores Aritméticos

```goul
var suma = 10 + 5;        // 15
var resta = 20 - 8;       // 12
var multiplicacion = 4 * 3; // 12
var division = 15 / 3;    // 5
```

### Funciones Integradas

#### print(valor)
Imprime un valor en la consola.

```goul
print("Hola, Goul!");
print(42);
print(suma);
```

#### len(array)
Retorna la longitud de un array.

```goul
var numeros = [1, 2, 3, 4, 5];
print(len(numeros));  // 5
```

#### str(valor)
Convierte un valor a string.

```goul
var numero = 42;
var texto = str(numero);
print(texto);  // "42"
```

#### int(valor)
Convierte un valor a entero.

```goul
var texto = "42";
var numero = int(texto);
print(numero);  // 42
```

#### float(valor)
Convierte un valor a decimal.

```goul
var texto = "3.14";
var decimal = float(texto);
print(decimal);  // 3.14
```

#### type(valor)
Retorna el tipo de dato.

```goul
print(type(42));        // "int"
print(type("texto"));   // "str"
print(type([1,2,3]));   // "list"
```

## 💡 Ejemplos Completos

### Ejemplo 1: Hola Mundo

```goul
// Mi primer programa en Goul
print("¡Hola, Mundo desde Goul!");
```

### Ejemplo 2: Variables y Operaciones

```goul
var nombre = "Pixel";
var edad = 25;
var altura = 1.75;

print("Hola, soy " + nombre);
print("Tengo " + str(edad) + " años");

var suma = edad + 5;
print("En 5 años tendré " + str(suma) + " años");
```

### Ejemplo 3: Arrays

```goul
var numeros = [10, 20, 30, 40, 50];
print("Longitud del array: " + str(len(numeros)));

var frutas = ["Manzana", "Banana", "Cereza"];
print("Primera fruta: " + frutas[0]);
```

### Ejemplo 4: Calculadora Básica

```goul
var a = 10;
var b = 5;

var suma = a + b;
var resta = a - b;
var multiplicacion = a * b;
var division = a / b;

print("Suma: " + str(suma));
print("Resta: " + str(resta));
print("Multiplicación: " + str(multiplicacion));
print("División: " + str(division));
```

## 🔧 Usando Goul en el Editor de Código

1. **Abrir el Editor**: Haz clic en el icono "Editor de Código" en el escritorio
2. **Escribir código**: Escribe tu programa Goul
3. **Guardar**: Presiona `Ctrl+S` para guardar (se guarda en `Documentos/`)
4. **Ejecutar**: Presiona `F5` para ejecutar el código
5. **Ver resultado**: El output aparecerá en el panel inferior

## 🎯 Atajos de Teclado

- **Ctrl+S**: Guardar archivo
- **F5**: Ejecutar código
- **Tab**: Indentación automática
- **Enter**: Nueva línea con indentación
- **Backspace**: Borrar carácter
- **Flechas**: Navegar por el código

## 🚧 Características Futuras (En Desarrollo)

### Clases y Objetos (POO)

```goul
// Próximamente
class Persona {
    var nombre;
    var edad;
    
    function saludar() {
        print("Hola, soy " + this.nombre);
    }
}

var persona = new Persona();
persona.nombre = "Pixel";
persona.saludar();
```

### Control de Flujo

```goul
// Próximamente
if (edad >= 18) {
    print("Eres mayor de edad");
} else {
    print("Eres menor de edad");
}

for (var i = 0; i < 10; i++) {
    print(i);
}

while (contador < 5) {
    print(contador);
    contador = contador + 1;
}
```

## 📚 Notas del Desarrollador

- Goul es un lenguaje interpretado en tiempo real
- Los errores se muestran en el panel de output
- El código se ejecuta línea por línea
- Los archivos se guardan con extensión `.goul` en la carpeta `Documentos`

## 🐛 Solución de Problemas

### Error: "Undefined variable"
Asegúrate de declarar las variables con `var` o `let` antes de usarlas.

### Error: "Syntax error"
Verifica que todas las líneas terminen correctamente y que las comillas estén cerradas.

### El código no se ejecuta
Presiona F5 o haz clic en el botón "▶ Ejecutar" para correr el código.

## 🎨 ¡Experimenta y Crea!

Goul está diseñado para ser simple pero poderoso. ¡Experimenta con diferentes combinaciones y crea programas creativos!

---

**Versión del Lenguaje**: Goul 1.0 Beta  
**Compatible con**: Pixel-OS v1.0  
**Última actualización**: 2024
