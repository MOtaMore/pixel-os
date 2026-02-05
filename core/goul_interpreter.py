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
        self.functions['echo'] = self._builtin_print  # Alias de print
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
    
    def _builtin_tag(self, tag_name: str, content: str = "", attributes: Optional[dict] = None) -> str:
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
            # Primero, parsear definiciones de funciones
            self._parse_function_definitions(code)
            
            # Luego ejecutar el código principal (filtrando definiciones de funciones)
            lines = code.strip().split('\n')
            executable_lines = self._filter_executable_lines(lines)
            self._execute_block(executable_lines)
        except GoulRuntimeError as e:
            self.output.append(f"Error: {e}")
        except Exception as e:
            self.output.append(f"Error inesperado: {str(e)}")
        
        return '\n'.join(self.output)
    
    def _filter_executable_lines(self, lines: List[str]) -> List[str]:
        """Filtra líneas de código, eliminando definiciones de funciones"""
        filtered = []
        i = 0
        in_function = False
        brace_count = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Detectar inicio de función
            if stripped.startswith('fn ') and '{' in line:
                in_function = True
                brace_count = line.count('{') - line.count('}')
                i += 1
                continue
            
            # Si estamos en una función, seguir contando braces
            if in_function:
                brace_count += line.count('{') - line.count('}')
                if brace_count <= 0:
                    in_function = False
                i += 1
                continue
            
            # Si no estamos en una función, agregar la línea
            filtered.append(line)
            i += 1
        
        return filtered
    
    def _parse_function_definitions(self, code: str):
        """Parsea definiciones de funciones en el código de forma más robusta"""
        lines = code.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Buscar inicio de función: fn nombre(...) {
            if line.startswith('fn ') and '{' in line:
                # Extraer nombre y parámetros
                match = re.match(r'fn\s+(\w+)\s*\((.*?)\)\s*\{', line)
                if match:
                    fn_name = match.group(1)
                    params_str = match.group(2)
                    params = [p.strip() for p in params_str.split(',') if p.strip()]
                    
                    # Encontrar el bloque de la función (respetando llaves)
                    fn_body_lines = []
                    brace_count = line.count('{') - line.count('}')
                    
                    # Agregar el resto de la línea si hay más después de {
                    rest = line[line.find('{') + 1:]
                    if rest.strip():
                        fn_body_lines.append(rest)
                    
                    i += 1
                    
                    # Leer líneas hasta encontrar la llave de cierre
                    while i < len(lines) and brace_count > 0:
                        current_line = lines[i]
                        brace_count += current_line.count('{') - current_line.count('}')
                        
                        # Si aún hay braces, procesar la línea
                        if brace_count > 0:
                            fn_body_lines.append(current_line)
                        else:
                            # Última línea - agregar solo lo antes del cierre
                            closing_idx = current_line.rfind('}')
                            if closing_idx > 0:
                                fn_body_lines.append(current_line[:closing_idx])
                            elif closing_idx == 0 and fn_body_lines:
                                # El } está al inicio, la función está lista
                                pass
                            else:
                                fn_body_lines.append(current_line)
                        
                        i += 1
                    
                    # Guardar función
                    fn_body = '\n'.join(fn_body_lines).strip()
                    self._user_functions[fn_name] = {
                        'params': params,
                        'body': fn_body
                    }
                    continue
            
            i += 1
    
    def _execute_block(self, lines: List[str], indent_level: int = 0):
        """Ejecuta un bloque de código"""
        i = 0
        return_value = None
        
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
            
            # Manejar return
            if stripped.startswith('return'):
                return_value = self._handle_return(stripped)
                break
            
            # Ejecutar línea
            self._execute_line(stripped)
            i += 1
        
        return return_value
    
    def _handle_return(self, line: str):
        """Maneja return statement"""
        # return expr o return
        if line == 'return':
            return None
        
        expr = line[6:].strip()  # Remover 'return'
        return self._evaluate_expression(expr)
    
    def _call_user_function(self, func_name: str, args: List[Any]) -> Any:
        """Llama una función definida por el usuario"""
        if func_name not in self._user_functions:
            raise GoulRuntimeError(f"Función '{func_name}' no definida")
        
        func_def = self._user_functions[func_name]
        params = func_def['params']
        body = func_def['body']
        
        # Guardar variables locales actuales
        old_vars = self.variables.copy()
        
        # Asignar parámetros a variables
        for i, param in enumerate(params):
            if i < len(args):
                self.variables[param] = args[i]
        
        # Ejecutar cuerpo de la función
        # El body puede tener líneas con diferentes niveles de indentation
        # Necesitamos normalizarlas a indent_level=0
        body_lines = body.split('\n')
        
        # Procesar cada línea para remover indentation común
        normalized_lines = []
        for line in body_lines:
            # Remover espacios al inicio (hasta 4 espacios típicos)
            if line.startswith('    '):
                # Remover till 4 spaces
                normalized_lines.append(line[4:])
            elif line.startswith('  '):
                # Remover till 2 spaces
                normalized_lines.append(line[2:])
            else:
                # Sin indentation, agregar como está
                normalized_lines.append(line)
        
        result = self._execute_block(normalized_lines, indent_level=0)
        
        # Restaurar variables originales (mantener el resultado)
        self.variables = old_vars
        
        # Si una función no tiene return explícito, devuelve None
        # Pero los echo() y print() dentro de la función afectan el output global
        return result
    def _execute_line(self, line: str):
        """Ejecuta una línea de código"""
        # Ignorar definiciones de funciones (ya parseadas)
        if line.startswith('fn '):
            return
        
        # Ignorar cierres de funciones
        if line.strip() == '}':
            return
        
        # Comando echo (sin paréntesis)
        if line.startswith('echo '):
            arg_str = line[5:].strip()
            value = self._evaluate_expression(arg_str)
            self.output.append(str(value))
            return
        
        # Variable declaration: var x = 10 o let x = "hello"
        if line.startswith('var ') or line.startswith('let '):
            self._handle_variable_declaration(line)
            return
        
        # Assignment: x = value
        elif '=' in line and not any(op in line for op in ['==', '!=', '<=', '>=', 'if ', 'for ', 'while ']):
            self._handle_assignment(line)
            return
        
        # Function call: print("hello") o function()
        elif '(' in line and ')' in line:
            try:
                self._evaluate_expression(line)
            except GoulRuntimeError:
                # Ignorar si no se puede evaluar (puede ser bloque)
                pass
            return
        
        # If statement
        elif line.startswith('if '):
            pass  # Manejado en bloque
        
        # For loop
        elif line.startswith('for '):
            pass  # Manejado en bloque
        
        # While loop
        elif line.startswith('while '):
            pass  # Manejado en bloque
        
        # Function definition
        elif line.startswith('fn '):
            pass  # Ya procesado en _parse_function_definitions
        
        # Class definition
        elif line.startswith('class '):
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
        """Evalúa una expresión de forma optimizada"""
        expr = expr.strip().rstrip(';')
        
        if not expr:
            return None
        
        # String literals
        if self._is_string_literal(expr):
            return expr[1:-1]
        
        # Number literals
        if self._is_number_literal(expr):
            return self._parse_number(expr)
        
        # Boolean/Null literals
        literal_map = {'true': True, 'false': False, 'null': None}
        if expr in literal_map:
            return literal_map[expr]
        
        # Array literal (ANTES que function calls)
        if expr.startswith('[') and expr.endswith(']'):
            return self._parse_array_literal(expr)
        
        # Variable reference (ANTES que concatenation/arithmetic)
        if expr.isidentifier() and expr in self.variables:
            return self.variables[expr]
        
        # String concatenation with + (ANTES que function calls)
        if '+' in expr and ('"' in expr or "'" in expr or self._has_string_concat(expr)):
            return self._evaluate_concatenation(expr)
        
        # Function or array index access
        if self._is_function_call_expr(expr):
            try:
                return self._try_function_call(expr)
            except GoulRuntimeError:
                # Si no es una función válida, continuar
                pass
        
        # Arithmetic operations (SOLO si no fue string concat)
        if '+' in expr or '*' in expr or '/' in expr:
            for operator in ['*', '/', '+']:  # No '-' por ambigüedad
                if operator in expr:
                    result = self._evaluate_arithmetic(expr, operator)
                    if result is not None and result != expr:
                        return result
        
        raise GoulRuntimeError(f"No se puede evaluar expresión: {expr}")
    
    def _is_function_call_expr(self, expr: str) -> bool:
        """Verifica si una expresión es claramente una llamada a función"""
        if '(' not in expr or ')' not in expr:
            return False
        paren_idx = expr.find('(')
        if paren_idx <= 0:
            return False
        potential_func = expr[:paren_idx].strip()
        return potential_func.isidentifier()
    
    def _is_string_literal(self, expr: str) -> bool:
        """Verifica si es un string literal"""
        if len(expr) < 2:
            return False
        quote_char = expr[0]
        if quote_char not in ('"', "'"):
            return False
        if not expr.endswith(quote_char):
            return False
        # Contar comillas (debe ser exactamente 2)
        return expr.count(quote_char) == 2
    
    def _is_number_literal(self, expr: str) -> bool:
        """Verifica si es un número"""
        try:
            float(expr)
            return True
        except ValueError:
            return False
    
    def _parse_number(self, expr: str) -> float | int:
        """Parsea un número"""
        if '.' in expr:
            return float(expr)
        return int(expr)
    
    def _parse_array_literal(self, expr: str) -> list:
        """Parsea un array literal"""
        items_str = expr[1:-1].strip()
        if not items_str:
            return []
        return [self._evaluate_expression(item) 
                for item in self._split_arguments(items_str)]
    
    def _has_string_concat(self, expr: str) -> bool:
        """Verifica si hay concatenación de strings con variables"""
        if '+' not in expr:
            return False
        parts = expr.split('+')
        return any(part.strip() in self.variables for part in parts)
    
    def _evaluate_concatenation(self, expr: str) -> str:
        """Evalúa concatenación de strings"""
        parts = self._split_by_operator(expr, '+')
        if len(parts) > 1:
            return "".join(str(self._evaluate_expression(p)) for p in parts)
        return str(self._evaluate_expression(expr))
    
    def _evaluate_arithmetic(self, expr: str, operator: str) -> float | int | str | None:
        """Evalúa operaciones aritméticas (consolidado)"""
        if operator == '*':
            parts = self._split_by_operator(expr, '*')
            if len(parts) > 1:
                result = 1
                for p in parts:
                    result *= self._evaluate_expression(p)
                return result
        elif operator == '/':
            parts = self._split_by_operator(expr, '/')
            if len(parts) > 1:
                result = self._evaluate_expression(parts[0])
                for p in parts[1:]:
                    result /= self._evaluate_expression(p)
                return result
        elif operator == '+':
            # SOLO para operaciones aritméticas de números
            # String concatenation es manejado en _evaluate_concatenation
            if '"' not in expr and "'" not in expr:
                parts = self._split_by_operator(expr, '+')
                if len(parts) > 1:
                    try:
                        return sum(self._evaluate_expression(p) for p in parts)
                    except (TypeError, ValueError):
                        # Si falla, no es aritmética
                        return None
        
        return None
    
    def _try_function_call(self, expr: str) -> Any:
        """Intenta hacer una llamada a función"""
        if '(' not in expr or ')' not in expr:
            return None
        
        paren_idx = expr.find('(')
        if paren_idx <= 0:
            return None
        
        potential_func = expr[:paren_idx].strip()
        if not potential_func.isidentifier():
            return None
        
        close_paren = expr.rfind(')')
        if close_paren <= paren_idx:
            return None
        
        func_name = potential_func
        args_str = expr[paren_idx + 1:close_paren]
        args = [self._evaluate_expression(arg) for arg in self._split_arguments(args_str)]
        
        # Buscar en funciones del usuario primero
        if func_name in self._user_functions:
            return self._call_user_function(func_name, args)
        
        # Luego en built-in
        if func_name in self.functions:
            return self.functions[func_name](*args)
        
        raise GoulRuntimeError(f"Función '{func_name}' no definida")
    
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
