"""
Goul Programming Language Interpreter
Lenguaje de programación que combina Python y C# con POO
"""
import re
from typing import Any, Dict, List, Optional


class GoulRuntimeError(Exception):
    """Error en tiempo de ejecución de Goul"""
    pass


class GoulObject:
    """Clase base para objetos Goul"""
    def __init__(self):
        self.attributes = {}
    
    def get_attr(self, name: str) -> Any:
        return self.attributes.get(name)
    
    def set_attr(self, name: str, value: Any):
        self.attributes[name] = value


class GoulClass:
    """Representa una clase en Goul"""
    def __init__(self, name: str, methods: Dict, properties: Dict):
        self.name = name
        self.methods = methods
        self.properties = properties
    
    def instantiate(self) -> GoulObject:
        """Crea una instancia de esta clase"""
        obj = GoulObject()
        # Copiar propiedades por defecto
        for prop_name, prop_value in self.properties.items():
            obj.set_attr(prop_name, prop_value)
        # Enlazar métodos
        for method_name, method_func in self.methods.items():
            obj.set_attr(method_name, lambda *args, o=obj, m=method_func: m(o, *args))
        return obj


class GoulInterpreter:
    """Intérprete del lenguaje Goul"""
    
    def __init__(self):
        self.variables = {}
        self.classes = {}
        self.output = []
        self.functions = {}
        self._user_functions = {}  # Funciones definidas por usuario
        self._user_classes = {}     # Clases definidas por usuario
        self._init_builtins()
    
    def _init_builtins(self):
        """Inicializa funciones built-in"""
        self.functions['print'] = self._builtin_print
        self.functions['input'] = self._builtin_input
        self.functions['len'] = self._builtin_len
        self.functions['str'] = lambda x: str(x)
        self.functions['int'] = lambda x: int(x)
        self.functions['float'] = lambda x: float(x)
        self.functions['type'] = lambda x: type(x).__name__
        # HTML support
        self.functions['html'] = self._builtin_html
        self.functions['tag'] = self._builtin_tag
        self.functions['css'] = self._builtin_css
    
    def _builtin_print(self, *args):
        """Función print"""
        text = ' '.join(str(arg) for arg in args)
        self.output.append(text)
        return text
    
    def _builtin_input(self, prompt=""):
        """Función input (simulada)"""
        self.output.append(f"[INPUT REQUIRED: {prompt}]")
        return "user_input"
    
    def _builtin_len(self, obj):
        """Función len"""
        if isinstance(obj, (list, str, dict)):
            return len(obj)
        return 0
    
    def _builtin_html(self, content: str) -> str:
        """Crea contenido HTML
        
        Args:
            content: Código HTML como string
            
        Returns:
            El HTML con estructura básica
        """
        # Envasar en estructura HTML básica si no la tiene
        if not content.strip().startswith('<!DOCTYPE') and not content.strip().startswith('<html'):
            html = f"<!DOCTYPE html><html><body>{content}</body></html>"
        else:
            html = content
        self.output.append(f"[HTML]{html}[/HTML]")
        return html
    
    def _builtin_tag(self, tag_name: str, content: str = "", attributes: dict = None) -> str:
        """Crea una etiqueta HTML
        
        Args:
            tag_name: Nombre de la etiqueta (p, div, h1, etc)
            content: Contenido dentro de la etiqueta
            attributes: Diccionario de atributos (id, class, style, etc)
            
        Returns:
            String con la etiqueta HTML
        """
        attrs_str = ""
        if attributes:
            for key, value in attributes.items():
                attrs_str += f' {key}="{value}"'
        
        return f"<{tag_name}{attrs_str}>{content}</{tag_name}>"
    
    def _builtin_css(self, selector: str, style: dict) -> str:
        """Crea una regla CSS
        
        Args:
            selector: Selector CSS (p, .class, #id, etc)
            style: Diccionario de estilos (color, font-size, etc)
            
        Returns:
            String con la regla CSS
        """
        style_str = "; ".join([f"{k}: {v}" for k, v in style.items()])
        css = f"{selector} {{ {style_str}; }}"
        return css
    
    def execute(self, code: str) -> str:
        """Ejecuta código Goul
        
        Args:
            code: Código fuente Goul
            
        Returns:
            Salida del programa
        """
        self.output = []
        
        try:
            lines = code.strip().split('\n')
            self._execute_block(lines)
        except GoulRuntimeError as e:
            self.output.append(f"Error: {e}")
        except Exception as e:
            self.output.append(f"Error inesperado: {e}")
        
        return '\n'.join(self.output)
    
    def _execute_block(self, lines: List[str], indent_level: int = 0):
        """Ejecuta un bloque de código"""
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Ignorar líneas vacías y comentarios
            stripped = line.strip()
            if not stripped or stripped.startswith('//'):
                i += 1
                continue
            
            # Detectar nivel de indentación
            current_indent = len(line) - len(line.lstrip())
            
            if current_indent < indent_level:
                break
            
            if current_indent > indent_level:
                i += 1
                continue
            
            # Ejecutar línea
            self._execute_line(stripped)
            i += 1
    
    def _execute_line(self, line: str):
        """Ejecuta una línea de código"""
        # Variable declaration: var x = 10 o let x = "hello"
        if line.startswith('var ') or line.startswith('let '):
            self._handle_variable_declaration(line)
        
        # Assignment: x = value
        elif '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=']):
            self._handle_assignment(line)
        
        # Function call: print("hello")
        elif '(' in line and ')' in line:
            self._evaluate_expression(line)
        
        # Class definition: class Person { }
        elif line.startswith('class '):
            pass  # Manejado en bloque
        
        # Control structures
        elif line.startswith('if '):
            pass  # Manejado en bloque
        
        elif line.startswith('for '):
            pass  # Manejado en bloque
        
        elif line.startswith('while '):
            pass  # Manejado en bloque
    
    def _handle_variable_declaration(self, line: str):
        """Maneja declaración de variables"""
        # var name = value o let name = value
        match = re.match(r'(var|let)\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name = match.group(2)
            value_expr = match.group(3).strip()
            value = self._evaluate_expression(value_expr)
            self.variables[var_name] = value
    
    def _handle_assignment(self, line: str):
        """Maneja asignación de variables"""
        parts = line.split('=', 1)
        if len(parts) == 2:
            var_name = parts[0].strip()
            value_expr = parts[1].strip()
            value = self._evaluate_expression(value_expr)
            self.variables[var_name] = value
    
    def _split_arguments(self, args_str: str) -> List[str]:
        """Divide argumentos de función respetando strings y arrays"""
        if not args_str.strip():
            return []
        
        args = []
        current_arg = ""
        in_string = False
        in_array = False
        string_char = None
        bracket_depth = 0
        
        for char in args_str:
            if char in ('"', "'") and not in_array:
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                    string_char = None
                current_arg += char
            elif char == '[' and not in_string:
                in_array = True
                bracket_depth += 1
                current_arg += char
            elif char == ']' and not in_string:
                bracket_depth -= 1
                if bracket_depth == 0:
                    in_array = False
                current_arg += char
            elif char == ',' and not in_string and not in_array:
                args.append(current_arg.strip())
                current_arg = ""
            else:
                current_arg += char
        
        if current_arg.strip():
            args.append(current_arg.strip())
        
        return args
    
    def _evaluate_expression(self, expr: str) -> Any:
        """Evalúa una expresión"""
        expr = expr.strip().rstrip(';')
        
        if not expr:
            return None
        
        # String literals (verificar que no tenga operadores fuera)
        if ((expr.startswith('"') and expr.endswith('"')) or \
           (expr.startswith("'") and expr.endswith("'"))) and \
           not any(op in expr[1:-1] for op in [' + ', ' - ', ' * ', ' / ']):
            # Verificar que solo haya un par de comillas
            quote_char = expr[0]
            count = expr.count(quote_char)
            if count == 2:
                return expr[1:-1]
        
        # Number literals
        if expr.replace('.', '', 1).replace('-', '', 1).isdigit():
            try:
                if '.' in expr:
                    return float(expr)
                return int(expr)
            except ValueError:
                pass
        
        # Boolean literals
        if expr == 'true':
            return True
        if expr == 'false':
            return False
        if expr == 'null':
            return None
        
        # Function call
        func_match = re.match(r'(\w+)\((.*)\)$', expr, re.DOTALL)
        if func_match:
            func_name = func_match.group(1)
            args_str = func_match.group(2)
            
            # Evaluar argumentos usando split inteligente
            args = []
            for arg in self._split_arguments(args_str):
                args.append(self._evaluate_expression(arg))
            
            # Llamar función
            if func_name in self.functions:
                return self.functions[func_name](*args)
            else:
                raise GoulRuntimeError(f"Función '{func_name}' no definida")
        
        # Array literal
        if expr.startswith('[') and expr.endswith(']'):
            items_str = expr[1:-1]
            if not items_str.strip():
                return []
            items = [self._evaluate_expression(item) 
                    for item in self._split_arguments(items_str)]
            return items
        
        # Array index access: array[0]
        array_match = re.match(r'(\w+)\[(\d+)\]', expr)
        if array_match:
            var_name = array_match.group(1)
            index = int(array_match.group(2))
            if var_name in self.variables:
                arr = self.variables[var_name]
                if isinstance(arr, list) and 0 <= index < len(arr):
                    return arr[index]
        
        # Variable reference
        if expr.isidentifier() and expr in self.variables:
            return self.variables[expr]
        
        # String concatenation with +
        if '+' in expr and ('"' in expr or "'" in expr or any(v in self.variables for v in expr.split())):
            parts = self._split_by_operator(expr, '+')
            if len(parts) > 1:
                result = ""
                for part in parts:
                    val = self._evaluate_expression(part)
                    result += str(val)
                return result
        
        # Arithmetic operations (solo si no hay strings)
        if '+' in expr and '"' not in expr and "'" not in expr:
            parts = self._split_by_operator(expr, '+')
            if len(parts) > 1:
                return sum(self._evaluate_expression(p) for p in parts)
        
        if '-' in expr and expr.count('-') == 1 and not expr.startswith('-'):
            parts = expr.split('-', 1)
            if len(parts) == 2:
                left = self._evaluate_expression(parts[0].strip())
                right = self._evaluate_expression(parts[1].strip())
                return left - right
        
        if '*' in expr:
            parts = self._split_by_operator(expr, '*')
            if len(parts) > 1:
                result = 1
                for p in parts:
                    result *= self._evaluate_expression(p)
                return result
        
        if '/' in expr:
            parts = self._split_by_operator(expr, '/')
            if len(parts) > 1:
                result = self._evaluate_expression(parts[0])
                for p in parts[1:]:
                    result /= self._evaluate_expression(p)
                return result
        
        raise GoulRuntimeError(f"No se puede evaluar expresión: {expr}")
    
    def _split_by_operator(self, expr: str, operator: str) -> List[str]:
        """Divide expresión por operador respetando strings"""
        parts = []
        current = ""
        in_string = False
        string_char = None
        
        for char in expr:
            if char in ('"', "'") and not in_string:
                in_string = True
                string_char = char
                current += char
            elif char == string_char and in_string:
                in_string = False
                string_char = None
                current += char
            elif char == operator and not in_string:
                parts.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            parts.append(current.strip())
        
        return parts


def run_goul_code(code: str) -> str:
    """Ejecuta código Goul y retorna la salida
    
    Args:
        code: Código fuente Goul
        
    Returns:
        Salida del programa
    """
    interpreter = GoulInterpreter()
    return interpreter.execute(code)


# Ejemplos de código Goul
GOUL_EXAMPLES = {
    'hello_world': '''// Hola Mundo en Goul
print("¡Hola, Mundo!");
print("Bienvenido a Goul");
''',
    
    'variables': '''// Variables y tipos
var nombre = "Alice";
var edad = 25;
var altura = 1.75;

print("Nombre:", nombre);
print("Edad:", edad);
print("Altura:", altura);
''',
    
    'arithmetic': '''// Operaciones matemáticas
var a = 10;
var b = 5;

var suma = a + b;
var resta = a - b;
var mult = a * b;
var div = a / b;

print("Suma:", suma);
print("Resta:", resta);
print("Multiplicación:", mult);
print("División:", div);
''',
    
    'arrays': '''// Arrays y listas
var numeros = [1, 2, 3, 4, 5];
var nombres = ["Ana", "Bob", "Carlos"];

print("Números:", numeros);
print("Nombres:", nombres);
print("Longitud:", len(numeros));
''',
}
