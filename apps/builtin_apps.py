"""
Aplicaciones integradas del sistema Pixel-OS
"""
import pygame
from core.plugin_manager import Application
from config.i18n import tr
from config.settings import *

# Funciones para manejo de clipboard
def get_clipboard():
    """Obtiene texto del clipboard del sistema"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        try:
            text = root.clipboard_get()
            return text
        except:
            return ""
        finally:
            root.destroy()
    except:
        return ""

def set_clipboard(text):
    """Copia texto al clipboard del sistema"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Ocultar ventana
        try:
            root.clipboard_clear()
            root.clipboard_append(text)
            root.update()  # Necesario para actualizar clipboard
            return True
        finally:
            root.destroy()
    except:
        return False


class TerminalApp(Application):
    """Terminal mejorada con navegación del filesystem y ejecución de Goul"""
    
    def __init__(self):
        super().__init__(tr("app.terminal"), color=Colors.GREEN, app_id="terminal")
        self.lines = [
            "=== Pixel-OS Terminal ===",
            "Escribe 'help' para ver los comandos disponibles",
            ""
        ]
        self.current_input = ""
        self.cursor_blink = 0
        self.current_path = ""  # Ruta actual en el filesystem
        self.filesystem = None
        self.app_launcher = None
        self.scroll_offset = 0  # Para scrollbar
        self.scrollbar_dragging = False  # Para dragging del scrollbar
        self.last_mouse_y = 0  # Para trackear movimiento del mouse
        self.window = None  # Referencia a la ventana (se asigna desde engine)
        
        self.commands = {
            "help": self._cmd_help,
            "clear": self._cmd_clear,
            "echo": self._cmd_echo,
            "date": self._cmd_date,
            "ls": self._cmd_ls,
            "cd": self._cmd_cd,
            "pwd": self._cmd_pwd,
            "cat": self._cmd_cat,
            "goul": self._cmd_goul,
            "touch": self._cmd_touch,
            "mkdir": self._cmd_mkdir,
            "rm": self._cmd_rm,
            "rmdir": self._cmd_rmdir,
            "trash": self._cmd_trash,
            "open": self._cmd_open,
        }
    
    def set_filesystem(self, filesystem):
        """Asigna el filesystem virtual"""
        self.filesystem = filesystem

    def set_app_launcher(self, launcher):
        """Asigna un launcher para abrir archivos con apps"""
        self.app_launcher = launcher
    
    def _cmd_help(self, args):
        """Muestra ayuda de comandos"""
        return [
            "=== Comandos Disponibles ===",
            "  help           - Mostrar esta ayuda",
            "  clear          - Limpiar pantalla",
            "  ls             - Listar directorio actual",
            "  cd <ruta>      - Cambiar directorio",
            "  pwd            - Mostrar ruta actual",
            "  cat <archivo>  - Mostrar contenido de archivo",
            "  mkdir <nombre> - Crear carpeta (soporta a/b/c)",
            "  touch <nombre> - Crear archivo",
            "  rm <archivo>   - Mover archivo a papelera",
            "  rmdir <folder> - Mover carpeta a papelera",
            "  trash <op>     - Ver papelera (ver/restore nombre/--empty)",
            "  open <archivo> - Abrir archivo (--editor|--browser|--player)",
            "  goul <archivo> - Ejecutar archivo Goul",
            "  echo <texto>   - Imprimir texto",
            "  date           - Mostrar fecha/hora",
            "",
            "=== Atajos de Teclado ===",
            "  Ctrl+A         - Copiar todo el historial al clipboard",
            "  Ctrl+C         - Copiar entrada actual",
            "  Ctrl+V         - Pegar desde clipboard",
        ]
    
    def _cmd_clear(self, args):
        """Limpia la pantalla"""
        self.lines = []
        return []
    
    def _cmd_echo(self, args):
        """Imprime texto"""
        return [" ".join(args) if args else ""]
    
    def _cmd_date(self, args):
        """Muestra fecha y hora"""
        import datetime
        return [datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")]
    
    def _cmd_ls(self, args):
        """Lista archivos y carpetas del directorio actual"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        try:
            contents = self.filesystem.list_directory(self.current_path)
            result = []
            
            # Mostrar carpetas
            for folder in sorted(contents['folders']):
                result.append(f"[DIR] {folder}/")
            
            # Mostrar archivos
            for file in sorted(contents['files']):
                result.append(f"[FILE] {file}")
            
            return result if result else ["(vacio)"]
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_cd(self, args):
        """Cambia directorio"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            self.current_path = ""
            return ["Cambiado a: /"]
        
        try:
            target = args[0]
            
            # Ir a raíz
            if target == "/":
                self.current_path = ""
                return ["Cambiado a: /"]
            
            # Ir atrás
            if target == "..":
                if "/" in self.current_path:
                    parts = self.current_path.split("/")
                    self.current_path = "/".join(parts[:-1])
                else:
                    self.current_path = ""
                display = f"/{self.current_path}" if self.current_path else "/"
                return [f"Cambiado a: {display}"]
            
            # Ir a carpeta específica
            new_path = f"{self.current_path}/{target}" if self.current_path else target
            folder = self.filesystem.get_path(new_path)
            
            if folder:
                self.current_path = new_path
                return [f"Cambiado a: /{new_path}"]
            else:
                return [f"Error: Carpeta '{target}' no encontrada"]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_pwd(self, args):
        """Muestra ruta actual"""
        path = f"/{self.current_path}" if self.current_path else "/"
        return [f"Ubicación actual: {path}"]
    
    def _cmd_cat(self, args):
        """Muestra contenido de archivo"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: cat <archivo>"]
        
        try:
            filename = args[0]
            folder = self.filesystem.get_path(self.current_path)
            
            if not folder:
                return ["Error: Directorio no encontrado"]
            
            file_obj = folder.get_file(filename)
            if file_obj:
                return file_obj.content.split('\n')
            else:
                return [f"Error: Archivo '{filename}' no encontrado"]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_goul(self, args):
        """Ejecuta un archivo Goul"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: goul <archivo.goul>"]
        
        try:
            from core.goul_interpreter import run_goul_code
            
            filename = args[0]
            folder = self.filesystem.get_path(self.current_path)
            
            if not folder:
                return ["Error: Directorio no encontrado"]
            
            file_obj = folder.get_file(filename)
            if not file_obj:
                return [f"Error: Archivo '{filename}' no encontrado"]
            
            code = file_obj.content
            output = run_goul_code(code)
            return output.split('\n')
        
        except Exception as e:
            return [f"Error ejecutando archivo: {e}"]
    
    def _cmd_touch(self, args):
        """Crea archivo vacío"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: touch <nombre>"]
        
        try:
            filename = args[0]
            self.filesystem.create_file(self.current_path, filename, "", "txt")
            return [f"Archivo '{filename}' creado"]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_mkdir(self, args):
        """Crea carpeta (soporta rutas anidadas como a/b/c)"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: mkdir <nombre> o mkdir <a/b/c>"]
        
        try:
            folder_path = args[0]
            # Si contiene /, crear anidado
            if "/" in folder_path:
                self.filesystem.create_nested_folder(self.current_path, folder_path)
                return [f"Carpetas creadas: {folder_path}"]
            else:
                self.filesystem.create_folder(self.current_path, folder_path)
                return [f"Carpeta '{folder_path}' creada"]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_rm(self, args):
        """Mueve archivo a papelera"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: rm <archivo>"]
        
        try:
            filename = args[0]
            if self.filesystem.move_to_trash(self.current_path, filename, is_folder=False):
                return [f"🗑️  Archivo '{filename}' movido a papelera"]
            else:
                return [f"Error: Archivo '{filename}' no encontrado"]
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_rmdir(self, args):
        """Mueve carpeta a papelera"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: rmdir <carpeta>"]
        
        try:
            foldername = args[0]
            if self.filesystem.move_to_trash(self.current_path, foldername, is_folder=True):
                return [f"🗑️  Carpeta '{foldername}' movida a papelera"]
            else:
                return [f"Error: Carpeta '{foldername}' no encontrada"]
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_trash(self, args):
        """Gestiona la papelera (ver, restaurar o vaciar)"""
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        try:
            if not args or args[0] == "ver":
                # Ver contenido de papelera
                contents = self.filesystem.list_directory("Papelera")
                if not contents:
                    return ["Papelera vacía"]
                
                result = ["=== 📁 Contenido de Papelera ==="]
                for folder in sorted(contents['folders']):
                    result.append(f"[DIR] {folder}/")
                for file in sorted(contents['files']):
                    result.append(f"[FILE] {file}")
                return result
            
            elif args[0] == "--empty":
                # Vaciar papelera
                if self.filesystem.empty_trash():
                    return ["🗑️  Papelera vaciada completamente"]
                else:
                    return ["Error: No se pudo vaciar la papelera"]
            
            elif args[0] == "restore":
                # Restaurar archivo
                if len(args) < 2:
                    return ["Uso: trash restore <nombre>"]
                filename = args[1]
                
                # Intentar restaurar como archivo primero
                if self.filesystem.restore_from_trash(filename, is_folder=False):
                    return [f"✅ Archivo '{filename}' restaurado"]
                # Si no, intentar como carpeta
                elif self.filesystem.restore_from_trash(filename, is_folder=True):
                    return [f"✅ Carpeta '{filename}' restaurada"]
                else:
                    return [f"Error: '{filename}' no encontrado en papelera"]
            
            else:
                return [
                    "Uso: trash [ver|restore <nombre>|--empty]",
                    "  trash ver            - Ver contenido de papelera",
                    "  trash restore <nom>  - Restaurar archivo o carpeta",
                    "  trash --empty        - Vaciar papelera",
                ]
        except Exception as e:
            return [f"Error: {e}"]
    
    def _cmd_open(self, args):
        """Abre un archivo con una aplicación
        
        Uso: open <archivo> [--editor|--browser|--player]
        Ejemplos:
          open script.goul              # Abre con editor por defecto
          open documento.html --browser # Abre con navegador
        """
        if not self.filesystem:
            return ["Error: Filesystem no disponible"]
        
        if not args:
            return ["Uso: open <archivo> [--editor|--browser|--player]"]
        
        if not self.app_launcher:
            return ["Error: Launcher no disponible"]
        
        try:
            target = args[0]
            app_type = args[1].lstrip('-') if len(args) > 1 else "editor"

            # Resolver ruta y nombre
            if "/" in target:
                path_part, name = target.rsplit("/", 1)
                path = path_part.strip("/")
            else:
                path = self.current_path
                name = target

            folder_path = f"{path}/{name}" if name and path else (name or path)

            # Si es carpeta, abrir en el explorador
            if self.filesystem.get_path(folder_path):
                if self.app_launcher("file_manager", folder_path, None):
                    return [f"Abriendo carpeta: /{folder_path}" ]
                return ["Error: No se pudo abrir la carpeta"]

            # Validar archivo
            folder = self.filesystem.get_path(path)
            if not folder:
                return ["Error: Directorio no encontrado"]
            file_obj = folder.get_file(name)
            if not file_obj:
                return [f"Error: Archivo '{name}' no encontrado"]

            if app_type == "editor":
                app_id = "code_editor"
            elif app_type == "browser":
                app_id = "mini_browser"
            elif app_type == "player":
                app_id = "video_player"
            else:
                app_id = app_type
            if self.app_launcher(app_id, path, name):
                return [f"Abriendo {name} con {app_type}"]
            return ["Error: No se pudo abrir el archivo"]
        
        except Exception as e:
            return [f"Error: {e}"]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Ejecutar comando
                self.lines.append(f"> {self.current_input}")
                parts = self.current_input.split()
                if parts:
                    cmd = parts[0].lower()
                    args = parts[1:]
                    if cmd in self.commands:
                        result = self.commands[cmd](args)
                        self.lines.extend(result)
                    else:
                        self.lines.append(f"Comando desconocido: '{cmd}'. Escribe 'help' para ayuda.")
                else:
                    pass
                self.lines.append("")
                self.current_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            elif event.key == pygame.K_UP:
                # Implementar historial (futuro)
                pass
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+A: Copiar todo el historial de terminal
                all_text = '\n'.join(self.lines)
                if all_text:
                    set_clipboard(all_text)
                    self.lines.append("[Todo el historial copiado al clipboard]")
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+C: Copiar entrada actual
                if self.current_input:
                    set_clipboard(self.current_input)
                    self.lines.append("[Copiado al clipboard]")
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+V: Pegar desde clipboard (soporta múltiples líneas)
                text = get_clipboard()
                if text:
                    # Si contiene saltos de línea, solo pegar la primera línea en entrada
                    if '\n' in text:
                        first_line = text.split('\n')[0]
                        self.current_input += first_line
                    else:
                        self.current_input += text
            else:
                if event.unicode.isprintable():
                    self.current_input += event.unicode
        
        # Mouse wheel scroll
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Rueda arriba
                self.scroll_offset = max(0, self.scroll_offset - 3)
                return
            elif event.button == 5:  # Rueda abajo
                if self.window:
                    line_height = 18
                    visible_lines = (self.window.content_rect.height - 50) // line_height
                    max_scroll = max(0, len(self.lines) - visible_lines)
                    self.scroll_offset = min(max_scroll, self.scroll_offset + 3)
                return
            elif event.button == 1 and self.window:  # Click izquierdo en scrollbar
                rect = self.window.content_rect
                scrollbar_x = rect.x + rect.width - 12
                line_height = 18
                visible_lines = (rect.height - 50) // line_height
                scrollbar_area = pygame.Rect(scrollbar_x, rect.y + 10, 12, rect.height - 50)
                
                if scrollbar_area.collidepoint(event.pos) and len(self.lines) > visible_lines:
                    self.scrollbar_dragging = True
                    self.last_mouse_y = event.pos[1]
                    return
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.scrollbar_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.scrollbar_dragging and self.window:
            # Dragging scrollbar
            rect = self.window.content_rect
            line_height = 18
            visible_lines = (rect.height - 50) // line_height
            dy = event.pos[1] - self.last_mouse_y
            
            if abs(dy) > 0:
                # Convertir movimiento del mouse a scroll
                max_scroll = max(0, len(self.lines) - visible_lines)
                scroll_delta = (dy * len(self.lines)) // (rect.height - 50)
                self.scroll_offset = max(0, min(max_scroll, self.scroll_offset + scroll_delta))
                self.last_mouse_y = event.pos[1]
    
    def update(self, dt):
        self.cursor_blink += dt
    
    def render(self, surface, rect):
        # Fondo oscuro pastel
        bg_color = (40, 35, 50)
        pygame.draw.rect(surface, bg_color, rect)
        
        # Renderizar líneas
        try:
            font = pygame.font.Font(FONT_PATH, 13)
        except:
            font = pygame.font.Font(None, 13)
        
        y = rect.y + 10
        line_height = 18
        
        # Mostrar líneas con scroll
        line_height = 18
        visible_lines = (rect.height - 50) // line_height
        
        # Clamped scroll
        max_scroll = max(0, len(self.lines) - visible_lines)
        self.scroll_offset = min(self.scroll_offset, max_scroll)
        
        start_idx = self.scroll_offset
        y = rect.y + 10
        
        for i in range(visible_lines):
            line_idx = start_idx + i
            if line_idx >= len(self.lines):
                break
            
            line = self.lines[line_idx]
            # Colorear comandos (>)
            if line.startswith(">"):
                text = font.render(line, True, (150, 200, 255))
            else:
                text = font.render(line, True, (150, 255, 150))
            surface.blit(text, (rect.x + 10, y))
            y += line_height
        
        # Dibujar scrollbar
        if len(self.lines) > visible_lines:
            scrollbar_x = rect.x + rect.width - 12
            scrollbar_area = pygame.Rect(scrollbar_x, rect.y + 10, 12, rect.height - 50)
            
            # Fondo
            pygame.draw.rect(surface, (40, 40, 50), scrollbar_area)
            
            # Thumb
            scroll_ratio = self.scroll_offset / max_scroll if max_scroll > 0 else 0
            thumb_height = max(20, (visible_lines / len(self.lines)) * (rect.height - 50))
            thumb_y = int(scrollbar_area.y + (scroll_ratio * ((rect.height - 50) - thumb_height)))
            
            thumb_rect = pygame.Rect(scrollbar_x, thumb_y, 12, int(thumb_height))
            pygame.draw.rect(surface, (100, 100, 120), thumb_rect, border_radius=2)
        
        # Prompt actual con ruta
        current_dir = f"~/{self.current_path}" if self.current_path else "~"
        prompt = f"{current_dir}> {self.current_input}"
        cursor = "|" if int(self.cursor_blink * 2) % 2 == 0 else " "
        text = font.render(prompt + cursor, True, (100, 200, 255))
        surface.blit(text, (rect.x + 10, y))


class TextEditorApp(Application):
    """Editor de texto simple"""
    
    def __init__(self):
        super().__init__(tr("app.text_editor"), color=Colors.BLUE, app_id="text_editor")
        self.lines = [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.cursor_blink = 0
        self.scroll_y = 0  # Scroll vertical
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Nueva línea
                current = self.lines[self.cursor_line]
                self.lines[self.cursor_line] = current[:self.cursor_col]
                self.lines.insert(self.cursor_line + 1, current[self.cursor_col:])
                self.cursor_line += 1
                self.cursor_col = 0
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_col > 0:
                    line = self.lines[self.cursor_line]
                    self.lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    prev_line = self.lines[self.cursor_line - 1]
                    self.cursor_col = len(prev_line)
                    self.lines[self.cursor_line - 1] += self.lines[self.cursor_line]
                    self.lines.pop(self.cursor_line)
                    self.cursor_line -= 1
            elif event.key == pygame.K_LEFT and self.cursor_col > 0:
                self.cursor_col -= 1
            elif event.key == pygame.K_RIGHT and self.cursor_col < len(self.lines[self.cursor_line]):
                self.cursor_col += 1
            elif event.key == pygame.K_UP and self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
                if self.cursor_line < self.scroll_y:
                    self.scroll_y = self.cursor_line
            elif event.key == pygame.K_DOWN and self.cursor_line < len(self.lines) - 1:
                self.cursor_line += 1
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
                if self.cursor_line > self.scroll_y + 20:
                    self.scroll_y = self.cursor_line - 20
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+A: Seleccionar todo y copiar al clipboard
                all_text = '\n'.join(self.lines)
                if all_text:
                    set_clipboard(all_text)
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+C: Copiar línea actual
                line = self.lines[self.cursor_line]
                if line:
                    set_clipboard(line)
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+V: Pegar desde clipboard (soporta múltiples líneas)
                text = get_clipboard()
                if text:
                    # Si el texto contiene saltos de línea, insertar como múltiples líneas
                    if '\n' in text:
                        parts = text.split('\n')
                        line = self.lines[self.cursor_line]
                        # Primera parte en la línea actual
                        self.lines[self.cursor_line] = line[:self.cursor_col] + parts[0]
                        self.cursor_col = len(self.lines[self.cursor_line])
                        # Resto de líneas
                        for part in parts[1:]:
                            self.cursor_line += 1
                            self.lines.insert(self.cursor_line, part)
                        self.cursor_col = len(self.lines[self.cursor_line])
                    else:
                        # Pegar texto en una sola línea
                        line = self.lines[self.cursor_line]
                        self.lines[self.cursor_line] = (line[:self.cursor_col] + 
                                                       text + 
                                                       line[self.cursor_col:])
                        self.cursor_col += len(text)
            else:
                if event.unicode.isprintable():
                    line = self.lines[self.cursor_line]
                    self.lines[self.cursor_line] = (line[:self.cursor_col] + 
                                                   event.unicode + 
                                                   line[self.cursor_col:])
                    self.cursor_col += 1
    
    def update(self, dt):
        self.cursor_blink += dt
    
    def render(self, surface, rect):
        # Fondo blanco suave
        pygame.draw.rect(surface, (255, 255, 255), rect)
        
        # Renderizar texto
        try:
            font = pygame.font.Font(FONT_PATH, 14)
        except:
            font = pygame.font.Font(None, 14)
        
        y = rect.y + 10
        line_height = 22
        visible_lines = (rect.height - 20) // line_height
        
        # Clamped scroll
        max_scroll = max(0, len(self.lines) - visible_lines)
        self.scroll_y = min(self.scroll_y, max_scroll)
        
        # Renderizar líneas con scroll
        for i in range(visible_lines):
            line_idx = self.scroll_y + i
            if line_idx >= len(self.lines):
                break
            
            line = self.lines[line_idx]
            
            # Highlight de línea actual
            if line_idx == self.cursor_line:
                highlight = pygame.Rect(rect.x, y - 2, rect.width - 15, line_height)
                pygame.draw.rect(surface, Colors.HOVER, highlight)
            
            # Texto
            text = font.render(line if line else " ", True, Colors.TEXT_PRIMARY)
            surface.blit(text, (rect.x + 10, y))
            
            # Cursor
            if line_idx == self.cursor_line and int(self.cursor_blink * 2) % 2 == 0:
                cursor_x = rect.x + 10 + font.size(line[:self.cursor_col])[0]
                pygame.draw.line(surface, Colors.TEXT_PRIMARY,
                               (cursor_x, y), (cursor_x, y + line_height - 4), 2)
            
            y += line_height
        
        # Dibujar scrollbar
        if len(self.lines) > visible_lines:
            scrollbar_x = rect.x + rect.width - 12
            scrollbar_area = pygame.Rect(scrollbar_x, rect.y + 10, 12, rect.height - 20)
            
            # Fondo de scrollbar
            pygame.draw.rect(surface, (230, 230, 230), scrollbar_area)
            
            # Thumb
            scroll_ratio = self.scroll_y / max_scroll if max_scroll > 0 else 0
            thumb_height = max(20, (visible_lines / len(self.lines)) * (rect.height - 20))
            thumb_y = int(scrollbar_area.y + (scroll_ratio * ((rect.height - 20) - thumb_height)))
            
            thumb_rect = pygame.Rect(scrollbar_x, thumb_y, 12, int(thumb_height))
            pygame.draw.rect(surface, (150, 150, 170), thumb_rect, border_radius=2)


class FileManagerApp(Application):
    """Explorador de archivos integrado con filesystem virtual"""
    
    def __init__(self):
        super().__init__(tr("app.file_manager"), color=Colors.YELLOW, app_id="file_manager")
        self.current_path = ""  # Ruta actual (relativo a root)
        self.items = []  # Lista de archivos y carpetas
        self.selected_idx = -1
        self.filesystem = None
        self.path_history = []  # Historial de navegación
        self._refresh_items()
    
    def set_filesystem(self, filesystem):
        """Asigna el filesystem virtual"""
        self.filesystem = filesystem
        self._refresh_items()

    def open_path(self, path: str):
        """Abre una ruta específica en el explorador"""
        self.current_path = path.strip("/")
        self._refresh_items()
        self.selected_idx = -1
    
    def _refresh_items(self):
        """Recarga la lista de items desde el filesystem"""
        if self.filesystem:
            try:
                contents = self.filesystem.list_directory(self.current_path)
                self.items = []
                
                # Agregar carpetas primero
                for folder in sorted(contents['folders']):
                    self.items.append((folder, "folder"))
                
                # Agregar archivos después
                for file in sorted(contents['files']):
                    self.items.append((file, "file"))
            except Exception as e:
                print(f"Error cargando directorio: {e}")
                self.items = []
        else:
            # Fallback a items hardcodeados si no hay filesystem
            self.items = [
                ("Documentos", "folder"),
                ("Imágenes", "folder"),
                ("Música", "folder"),
                ("Vídeos", "folder"),
            ]
    
    def _navigate_to_folder(self, folder_name):
        """Navega a una carpeta"""
        if self.current_path == "":
            new_path = folder_name
        else:
            new_path = f"{self.current_path}/{folder_name}"
        
        # Guardar en historial
        self.path_history.append(self.current_path)
        self.current_path = new_path
        self._refresh_items()
        self.selected_idx = -1
    
    def _go_back(self):
        """Vuelve a la carpeta anterior"""
        if self.path_history:
            self.current_path = self.path_history.pop()
            self._refresh_items()
            self.selected_idx = -1
        elif self.current_path:
            # Si no hay historial, ir a la raíz
            if "/" in self.current_path:
                parts = self.current_path.split("/")
                self.current_path = "/".join(parts[:-1])
            else:
                self.current_path = ""
            self._refresh_items()
            self.selected_idx = -1
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.window:
                mouse_pos = event.pos
                rect = self.window.content_rect
                
                # Botón Atrás
                back_btn = pygame.Rect(rect.x + 10, rect.y + 10, 80, 30)
                if back_btn.collidepoint(mouse_pos):
                    self._go_back()
                    return
                
                # Botón Refrescar
                refresh_btn = pygame.Rect(rect.x + 100, rect.y + 10, 90, 30)
                if refresh_btn.collidepoint(mouse_pos):
                    self._refresh_items()
                    return
                
                # Calcular qué item se clickeó
                content_y = rect.y + 55
                item_height = 40
                
                for i, (name, item_type) in enumerate(self.items):
                    item_rect = pygame.Rect(
                        rect.x + 10,
                        content_y + i * item_height,
                        rect.width - 20,
                        item_height - 5
                    )
                    if item_rect.collidepoint(mouse_pos):
                        if self.selected_idx == i and item_type == "folder":
                            # Doble click: navegar a carpeta
                            self._navigate_to_folder(name)
                        else:
                            self.selected_idx = i
                        break
    
    def render(self, surface, rect):
        # Fondo
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        try:
            font = pygame.font.Font(FONT_PATH, 14)
            small_font = pygame.font.Font(FONT_PATH, 11)
        except:
            font = pygame.font.Font(None, 14)
            small_font = pygame.font.Font(None, 11)
        
        # Botones de navegación
        back_btn = pygame.Rect(rect.x + 10, rect.y + 10, 80, 30)
        pygame.draw.rect(surface, (220, 220, 230), back_btn, border_radius=4)
        back_text = font.render("← Atrás", True, Colors.TEXT_PRIMARY)
        surface.blit(back_text, (back_btn.x + 8, back_btn.y + 7))
        
        refresh_btn = pygame.Rect(rect.x + 100, rect.y + 10, 90, 30)
        pygame.draw.rect(surface, (220, 220, 230), refresh_btn, border_radius=4)
        refresh_text = font.render("↻ Refrescar", True, Colors.TEXT_PRIMARY)
        surface.blit(refresh_text, (refresh_btn.x + 8, refresh_btn.y + 7))
        
        # Ruta actual
        path_display = f"📁 /{self.current_path}" if self.current_path else "📁 Raíz"
        path_text = small_font.render(path_display, True, (100, 100, 120))
        surface.blit(path_text, (rect.x + 200, rect.y + 18))
        
        # Lista de archivos
        y = rect.y + 55
        item_height = 40
        
        for i, (name, item_type) in enumerate(self.items):
            item_rect = pygame.Rect(rect.x + 10, y, rect.width - 20, item_height - 5)
            
            # Fondo si está seleccionado
            if i == self.selected_idx:
                pygame.draw.rect(surface, Colors.ACTIVE, item_rect, border_radius=6)
            elif item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, Colors.HOVER, item_rect, border_radius=6)
            
            # Icono y nombre del item
            icon = "📁" if item_type == "folder" else "📄"
            text = font.render(f"{icon} {name}", True, Colors.TEXT_PRIMARY)
            surface.blit(text, (item_rect.x + 10, item_rect.y + 10))
            
            y += item_height


class SettingsApp(Application):
    """Configuración del sistema"""
    
    def __init__(self):
        super().__init__(tr("app.settings"), color=Colors.PURPLE, app_id="settings")
        self.sections = [
            tr("settings.section.personalization"),
            tr("settings.section.sound"),
            tr("settings.section.display"),
            tr("settings.section.system"),
            tr("settings.section.plugins"),
        ]
        self.selected = 0
    
    def render(self, surface, rect):
        # Fondo
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        # Panel lateral
        sidebar_width = 200
        sidebar = pygame.Rect(rect.x, rect.y, sidebar_width, rect.height)
        pygame.draw.rect(surface, (245, 245, 255), sidebar)
        
        try:
            font = pygame.font.Font(FONT_PATH, 14)
        except:
            font = pygame.font.Font(None, 14)
        
        # Secciones
        y = rect.y + 20
        for i, section in enumerate(self.sections):
            section_rect = pygame.Rect(rect.x + 10, y, sidebar_width - 20, 35)
            
            if i == self.selected:
                pygame.draw.rect(surface, Colors.ACTIVE, section_rect, border_radius=6)
            
            text = font.render(section, True, Colors.TEXT_PRIMARY)
            surface.blit(text, (section_rect.x + 10, section_rect.y + 10))
            y += 40
        
        # Panel de contenido
        content_x = rect.x + sidebar_width + 20
        title_font = pygame.font.Font(None, 24)
        title = title_font.render(self.sections[self.selected], True, Colors.TEXT_PRIMARY)
        surface.blit(title, (content_x, rect.y + 20))
        
        # Contenido de ejemplo
        content = font.render(tr("settings.options"), True, Colors.TEXT_SECONDARY)
        surface.blit(content, (content_x, rect.y + 60))


class MiniBrowserApp(Application):
    """Mini navegador web con soporte HTML básico"""
    
    def __init__(self):
        super().__init__(tr("app.mini_browser"), color=Colors.BLUE, app_id="mini_browser")
        self.url = "https://pixel-os.local"
        self.html_content = ""
        self.rendered_lines = []
        self.history = []
        self.filesystem = None
        self.scroll_offset = 0
        self._load_home_page()
    
    def set_filesystem(self, filesystem):
        """Asigna el filesystem virtual"""
        self.filesystem = filesystem
    
    def _load_home_page(self):
        """Carga la página de inicio"""
        self.html_content = """
        <h1>Bienvenido a Pixel Browser</h1>
        <p>Este es un navegador web simple integrado en Pixel-OS</p>
        <h2>Características:</h2>
        <p>✓ Renderiza HTML básico</p>
        <p>✓ Integración con Goul</p>
        <p>✓ Carga archivos .html</p>
        """
        self._render_html()
    
    def _render_html(self):
        """Renderiza HTML a líneas de texto simple"""
        self.rendered_lines = []
        
        # Parser HTML muy simple - elimina tags y mantiene contenido
        import re
        content = self.html_content
        
        # Extraer contenido entre tags y formatear
        lines = re.sub(r'<[^>]+>', '\n', content)
        lines = re.sub(r'\s+', ' ', lines)
        
        # Dividir en líneas y agregar al rendered_lines
        for line in lines.split('\n'):
            line = line.strip()
            if line:
                # Formateo básico según tag (simulado por contenido)
                if any(h in content[:content.find(line)] and content[:content.find(line)].count(f'<{h}') > content[:content.find(line)].count(f'</{h}') for h in ['h1', 'h2', 'h3']):
                    self.rendered_lines.append(f"► {line}")
                else:
                    self.rendered_lines.append(line)

    def _wrap_text(self, text: str, font, max_width: int):
        """Divide texto en líneas que caben en el ancho disponible"""
        words = text.split(" ")
        lines = []
        current = ""
        for word in words:
            test = f"{current} {word}".strip()
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                # Si una palabra es muy larga, cortarla
                if font.size(word)[0] > max_width:
                    chunk = ""
                    for ch in word:
                        if font.size(chunk + ch)[0] <= max_width:
                            chunk += ch
                        else:
                            lines.append(chunk)
                            chunk = ch
                    if chunk:
                        current = chunk
                    else:
                        current = ""
                else:
                    current = word
        if current:
            lines.append(current)
        return lines

    def _get_display_lines(self, font, title_font, max_width: int):
        """Crea líneas visibles con wrapping"""
        display = []
        for line in self.rendered_lines:
            is_title = line.startswith('►')
            text = line[1:].strip() if is_title else line
            use_font = title_font if is_title else font
            wrapped = self._wrap_text(text, use_font, max_width)
            for w in wrapped:
                display.append((w, is_title))
        return display
    
    def load_file(self, path: str, filename: str):
        """Carga un archivo HTML desde el filesystem
        
        Args:
            path: Ruta del archivo
            filename: Nombre del archivo
        """
        if not self.filesystem:
            self.html_content = "Error: Filesystem no disponible"
            return
        
        try:
            folder = self.filesystem.get_path(path)
            if folder:
                file_obj = folder.get_file(filename)
                if file_obj and filename.endswith('.html'):
                    self.url = f"/{path}/{filename}" if path else f"/{filename}"
                    self.html_content = file_obj.content
                    self._render_html()
                    return
            
            self.html_content = f"Error: No se pudo cargar {filename}"
        except Exception as e:
            self.html_content = f"Error: {str(e)}"
        
        self._render_html()
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset = max(0, self.scroll_offset - 1)
            elif event.key == pygame.K_DOWN:
                self.scroll_offset += 1
            elif event.key == pygame.K_RETURN:
                self._load_home_page()
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+C: Copiar URL
                if self.url:
                    set_clipboard(self.url)
    
    def render(self, surface, rect):
        # Fondo
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        try:
            font = pygame.font.Font(FONT_PATH, 11)
            title_font = pygame.font.Font(FONT_PATH, 13)
        except:
            font = pygame.font.Font(None, 11)
            title_font = pygame.font.Font(None, 13)
        
        # Barra de direcciones
        address_bar = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 90, 28)
        pygame.draw.rect(surface, (240, 240, 250), address_bar, border_radius=4)
        pygame.draw.rect(surface, Colors.BORDER, address_bar, width=1, border_radius=4)
        
        # URL texto
        url_display = self.url[:40] + "..." if len(self.url) > 40 else self.url
        url_text = font.render(url_display, True, Colors.TEXT_PRIMARY)
        surface.blit(url_text, (address_bar.x + 6, address_bar.y + 6))
        
        # Botones
        back_btn = pygame.Rect(rect.x + rect.width - 75, rect.y + 10, 25, 28)
        reload_btn = pygame.Rect(rect.x + rect.width - 45, rect.y + 10, 25, 28)
        home_btn = pygame.Rect(rect.x + rect.width - 15, rect.y + 10, 25, 28)
        
        for btn in [back_btn, reload_btn, home_btn]:
            pygame.draw.rect(surface, (200, 200, 220), btn, border_radius=3)
            pygame.draw.rect(surface, Colors.BORDER, btn, width=1, border_radius=3)
        
        back_text = font.render("←", True, Colors.TEXT_PRIMARY)
        reload_text = font.render("↻", True, Colors.TEXT_PRIMARY)
        home_text = font.render("⌂", True, Colors.TEXT_PRIMARY)
        
        surface.blit(back_text, (back_btn.centerx - 4, back_btn.centery - 6))
        surface.blit(reload_text, (reload_btn.centerx - 4, reload_btn.centery - 6))
        surface.blit(home_text, (home_btn.centerx - 4, home_btn.centery - 6))
        
        # Área de contenido
        content_rect = pygame.Rect(rect.x + 10, rect.y + 50, rect.width - 20, rect.height - 60)
        pygame.draw.rect(surface, (255, 255, 255), content_rect, border_radius=4)
        pygame.draw.rect(surface, Colors.BORDER, content_rect, width=1, border_radius=4)
        
        # Renderizar líneas de HTML con wrapping
        max_width = content_rect.width - 30
        display_lines = self._get_display_lines(font, title_font, max_width)
        if self.scroll_offset > max(0, len(display_lines) - 1):
            self.scroll_offset = max(0, len(display_lines) - 1)
        y = content_rect.y + 10
        line_height = 16
        visible_lines = (content_rect.height - 20) // line_height
        
        for i in range(visible_lines):
            line_idx = self.scroll_offset + i
            if line_idx < len(display_lines):
                text, is_title = display_lines[line_idx]
                text_color = Colors.ACTIVE if is_title else Colors.TEXT_PRIMARY
                font_to_use = title_font if is_title else font
                line_text = font_to_use.render(text, True, text_color)
                surface.blit(line_text, (content_rect.x + 15, y))
                y += line_height


class CodeEditorApp(Application):
    """Editor de código con soporte para lenguaje Goul, scrollbars funcionales e inspirado en VS Code"""
    
    def __init__(self):
        super().__init__(tr("app.code_editor"), color=Colors.YELLOW, app_id="code_editor")
        self.code_lines = [
            "// Bienvenido al Editor de Código Goul!",
            "// Presiona F5 para ejecutar o Ctrl+S para guardar",
            "",
            "// Ejemplo: Variables y concatenación",
            "var nombre = \"Pixel\";",
            "echo \"Hola, \" + nombre + \"!\";",
            "",
            "// Ejemplo: Arrays",
            "var numeros = [1, 2, 3, 4, 5];",
            "echo \"Array: \" + str(numeros);",
            "echo \"Longitud: \" + str(len(numeros));"
        ]
        self.cursor_line = 0
        self.cursor_col = 0
        self.cursor_blink = 0
        self.current_file = "sin_titulo.goul"
        self.output_lines = []
        self.show_output = False
        self.show_save_dialog = False
        self.save_input = ""
        
        # Scroll
        self.scroll_y = 0  
        self.scroll_x = 0
        self.last_visible_lines = 0  # Para detectar cambios de tamaño
        
        # Referencia al filesystem (se asignará desde main.py)
        self.filesystem = None
        
        # File tree management
        self.show_file_tree = True
        self.expanded_folders = set()
        self.current_folder = "Documentos"
        
        # Scrollbar dragging
        self.scrollbar_dragging = False
        self.last_mouse_y = 0
    
    def set_filesystem(self, filesystem):
        """Asigna el filesystem virtual para guardar archivos"""
        self.filesystem = filesystem
    
    def load_file(self, path: str, filename: str):
        """Carga un archivo desde el filesystem
        
        Args:
            path: Ruta de la carpeta (ej: "Documentos" o "")
            filename: Nombre del archivo a cargar
        """
        if not self.filesystem:
            self.output_lines = ["Error: Filesystem no disponible"]
            self.show_output = True
            return
        
        try:
            folder = self.filesystem.get_path(path)
            if not folder:
                self.output_lines = [f"Error: Ruta '{path}' no encontrada"]
                self.show_output = True
                return
            
            file_obj = folder.get_file(filename)
            if not file_obj:
                self.output_lines = [f"Error: Archivo '{filename}' no encontrado"]
                self.show_output = True
                return
            
            # Cargar el contenido del archivo
            self.code_lines = file_obj.content.split('\n')
            self.current_file = filename
            self.cursor_line = 0
            self.cursor_col = 0
            self.output_lines = [f"✓ Archivo cargado: {filename}"]
            self.show_output = True
        
        except Exception as e:
            self.output_lines = [f"Error al cargar archivo: {str(e)}"]
            self.show_output = True
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Cuando el diálogo de guardado está activo
            if self.show_save_dialog:
                if event.key == pygame.K_RETURN:
                    # Guardar con el nombre ingresado
                    if self.save_input.strip():
                        self.current_file = self.save_input.strip()
                        if not self.current_file.endswith('.goul'):
                            self.current_file += '.goul'
                        self._save_file()
                    self.show_save_dialog = False
                    self.save_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.save_input = self.save_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    self.show_save_dialog = False
                    self.save_input = ""
                else:
                    if event.unicode.isprintable():
                        self.save_input += event.unicode
                return
            
            # Atajo Ctrl+S para guardar
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.show_save_dialog = True
                self.save_input = self.current_file.replace('.goul', '')
                return
            
            # Atajo F5 para ejecutar
            if event.key == pygame.K_F5:
                self._run_code()
                return
            
            # PageUp / PageDown para desplazamiento rápido
            if event.key == pygame.K_PAGEUP:
                self.scroll_y = max(0, self.scroll_y - self.last_visible_lines)
                self.cursor_line = max(0, self.cursor_line - self.last_visible_lines)
                return
            elif event.key == pygame.K_PAGEDOWN:
                self.scroll_y = min(len(self.code_lines) - 1, self.scroll_y + self.last_visible_lines)
                self.cursor_line = min(len(self.code_lines) - 1, self.cursor_line + self.last_visible_lines)
                return
            
            # Ctrl+Home / Ctrl+End para ir al principio/final
            if event.key == pygame.K_HOME and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.cursor_line = 0
                self.cursor_col = 0
                self.scroll_y = 0
                return
            elif event.key == pygame.K_END and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.cursor_line = len(self.code_lines) - 1
                self.cursor_col = len(self.code_lines[-1])
                return
            
            # Home / End para ir al inicio/final de la línea
            if event.key == pygame.K_HOME:
                self.cursor_col = 0
                return
            elif event.key == pygame.K_END:
                self.cursor_col = len(self.code_lines[self.cursor_line])
                return
            
            # Navegación y edición de código
            if event.key == pygame.K_RETURN:
                current = self.code_lines[self.cursor_line]
                self.code_lines[self.cursor_line] = current[:self.cursor_col]
                indent = len(current) - len(current.lstrip())
                self.code_lines.insert(self.cursor_line + 1, " " * indent + current[self.cursor_col:])
                self.cursor_line += 1
                self.cursor_col = indent
            elif event.key == pygame.K_BACKSPACE:
                if self.cursor_col > 0:
                    line = self.code_lines[self.cursor_line]
                    self.code_lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
                    self.cursor_col -= 1
                elif self.cursor_line > 0:
                    prev_line = self.code_lines[self.cursor_line - 1]
                    self.cursor_col = len(prev_line)
                    self.code_lines[self.cursor_line - 1] += self.code_lines[self.cursor_line]
                    self.code_lines.pop(self.cursor_line)
                    self.cursor_line -= 1
            elif event.key == pygame.K_LEFT and self.cursor_col > 0:
                self.cursor_col -= 1
            elif event.key == pygame.K_RIGHT and self.cursor_col < len(self.code_lines[self.cursor_line]):
                self.cursor_col += 1
            elif event.key == pygame.K_UP and self.cursor_line > 0:
                self.cursor_line -= 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
                if self.cursor_line < self.scroll_y:
                    self.scroll_y = self.cursor_line
            elif event.key == pygame.K_DOWN and self.cursor_line < len(self.code_lines) - 1:
                self.cursor_line += 1
                self.cursor_col = min(self.cursor_col, len(self.code_lines[self.cursor_line]))
                if self.cursor_line > self.scroll_y + max(1, self.last_visible_lines - 1):
                    self.scroll_y = self.cursor_line - max(1, self.last_visible_lines - 1)
            elif event.key == pygame.K_TAB:
                line = self.code_lines[self.cursor_line]
                self.code_lines[self.cursor_line] = line[:self.cursor_col] + "    " + line[self.cursor_col:]
                self.cursor_col += 4
            elif event.key == pygame.K_DELETE:
                line = self.code_lines[self.cursor_line]
                if self.cursor_col < len(line):
                    self.code_lines[self.cursor_line] = line[:self.cursor_col] + line[self.cursor_col + 1:]
            elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+A: Seleccionar todo y copiar
                all_code = '\n'.join(self.code_lines)
                if all_code:
                    set_clipboard(all_code)
                    self.output_lines = ["✓ Todo el código copiado al clipboard"]
                    self.show_output = True
            elif event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+C: Copiar línea
                line = self.code_lines[self.cursor_line]
                if line:
                    set_clipboard(line)
            elif event.key == pygame.K_x and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+X: Cortar línea
                line = self.code_lines[self.cursor_line]
                if line:
                    set_clipboard(line)
                    self.code_lines.pop(self.cursor_line)
                    self.cursor_line = min(self.cursor_line, len(self.code_lines) - 1)
                    self.cursor_col = 0
            elif event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+V: Pegar
                text = get_clipboard()
                if text:
                    if '\n' in text:
                        parts = text.split('\n')
                        line = self.code_lines[self.cursor_line]
                        self.code_lines[self.cursor_line] = line[:self.cursor_col] + parts[0]
                        self.cursor_col = len(self.code_lines[self.cursor_line])
                        for part in parts[1:]:
                            self.cursor_line += 1
                            self.code_lines.insert(self.cursor_line, part)
                        self.cursor_col = len(self.code_lines[self.cursor_line])
                    else:
                        line = self.code_lines[self.cursor_line]
                        self.code_lines[self.cursor_line] = (line[:self.cursor_col] + text + line[self.cursor_col:])
                        self.cursor_col += len(text)
            elif event.key == pygame.K_z and pygame.key.get_mods() & pygame.KMOD_CTRL:
                # Ctrl+Z: Deshacer (TODO: implementar historial)
                pass
            else:
                if event.unicode.isprintable():
                    line = self.code_lines[self.cursor_line]
                    self.code_lines[self.cursor_line] = line[:self.cursor_col] + event.unicode + line[self.cursor_col:]
                    self.cursor_col += 1
        
        # Mouse wheel scroll
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Rueda arriba
                self.scroll_y = max(0, self.scroll_y - 3)
                return
            elif event.button == 5:  # Rueda abajo
                self.scroll_y = min(len(self.code_lines) - 1, self.scroll_y + 3)
                return
            elif event.button == 1 and self.window:  # Click izquierdo
                self.last_mouse_y = event.pos[1]
                rect = self.window.content_rect
                tree_width = 160 if self.show_file_tree else 0
                code_start_x = rect.x + tree_width
                
                # Click en el árbol de archivos
                if self.show_file_tree and event.pos[0] < rect.x + tree_width:
                    tree_rect = pygame.Rect(rect.x, rect.y + 25, tree_width, rect.height - 65)
                    if tree_rect.collidepoint(event.pos):
                        items = self._get_tree_items()
                        row_height = 16
                        start_y = tree_rect.y + 30 + row_height
                        idx = (event.pos[1] - start_y) // row_height
                        if 0 <= idx < len(items):
                            item = items[idx]
                            if item["type"] == "up":
                                self.current_folder = item["path"]
                            elif item["type"] == "folder":
                                self.current_folder = item["path"]
                            elif item["type"] == "file":
                                self.load_file(self.current_folder, item["name"])
                        return
                
                # Click en scrollbar
                scrollbar_x = rect.x + rect.width - 12
                scrollbar_area = pygame.Rect(scrollbar_x, rect.y + 35, 12, rect.height - 75)
                
                if scrollbar_area.collidepoint(event.pos) and len(self.code_lines) > self.last_visible_lines:
                    self.scrollbar_dragging = True
                    self.last_mouse_y = event.pos[1]
                    return
                
                # Click en área de código (para colocar cursor)
                code_area = pygame.Rect(code_start_x, rect.y + 35, rect.width - tree_width - 30, rect.height - 75)
                if code_area.collidepoint(event.pos):
                    line_height = 18
                    relative_y = event.pos[1] - code_area.y
                    line_idx = self.scroll_y + (relative_y // line_height)
                    if 0 <= line_idx < len(self.code_lines):
                        self.cursor_line = line_idx
                        # Calcular posición del cursor en la línea
                        try:
                            font = pygame.font.Font(FONT_PATH, 12)
                        except:
                            font = pygame.font.Font(None, 12)
                        line = self.code_lines[self.cursor_line]
                        # Aproximación simple: basada en ancho de caracteres
                        char_width = font.size("x")[0]
                        relative_x = event.pos[0] - (code_area.x + 35)
                        self.cursor_col = max(0, min(len(line), relative_x // char_width))
                    return
                
                # Botones inferiores
                btn_x = code_start_x + 10
                btn_y = rect.y + rect.height - 40
                
                save_btn = pygame.Rect(btn_x, btn_y, 80, 30)
                if save_btn.collidepoint(event.pos):
                    self.show_save_dialog = True
                    self.save_input = self.current_file.replace('.goul', '')
                
                run_btn = pygame.Rect(btn_x + 90, btn_y, 80, 30)
                if run_btn.collidepoint(event.pos):
                    self._run_code()
                
                output_btn = pygame.Rect(btn_x + 180, btn_y, 100, 30)
                if output_btn.collidepoint(event.pos):
                    self.show_output = not self.show_output
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.scrollbar_dragging = False
        
        elif event.type == pygame.MOUSEMOTION and self.scrollbar_dragging and self.window:
            # Dragging scrollbar
            rect = self.window.content_rect
            dy = event.pos[1] - self.last_mouse_y
            if abs(dy) > 0:
                # Convertir movimiento del mouse a scroll
                line_height = 18
                scroll_delta = (dy * len(self.code_lines)) // (rect.height - 75)
                self.scroll_y = max(0, min(len(self.code_lines) - self.last_visible_lines, self.scroll_y + scroll_delta))
                self.last_mouse_y = event.pos[1]
    
    def _save_file(self):
        """Guarda el archivo en el filesystem"""
        if self.filesystem:
            code_content = '\n'.join(self.code_lines)
            # Guardar en carpeta Documentos
            result = self.filesystem.create_file("Documentos", self.current_file, code_content, "goul")
            if result:
                self.output_lines = ["Archivo guardado: " + self.current_file]
            else:
                # Actualizar archivo existente
                self.filesystem.save_file("Documentos", self.current_file, code_content)
                self.output_lines = ["Archivo actualizado: " + self.current_file]
            self.show_output = True
    
    def _run_code(self):
        """Ejecuta el código Goul"""
        from core.goul_interpreter import run_goul_code
        
        code = '\n'.join(self.code_lines)
        output = run_goul_code(code)
        
        self.output_lines = output.split('\n')
        self.show_output = True
    
    def update(self, dt):
        self.cursor_blink += dt
    
    def _get_folder_contents(self, folder_path):
        """Obtiene los contenidos de una carpeta desde el filesystem"""
        if not self.filesystem:
            return {'folders': [], 'files': []}
        try:
            contents = self.filesystem.list_directory(folder_path)
            if not contents:
                return {'folders': [], 'files': []}
            return contents
        except Exception:
            return {'folders': [], 'files': []}

    def _get_tree_items(self):
        """Devuelve items visibles del árbol para render y clicks"""
        items = []
        current = self.current_folder.strip("/")
        if current:
            parent = "/".join(current.split("/")[:-1])
            items.append({"type": "up", "label": "..", "path": parent})

        contents = self._get_folder_contents(current)
        for folder in sorted(contents.get("folders", [])):
            path = f"{current}/{folder}" if current else folder
            items.append({"type": "folder", "label": f"▶ {folder}/", "path": path})
        for file in sorted(contents.get("files", [])):
            icon = "📄"
            if file.endswith('.goul'):
                icon = "⚙️ "
            elif file.endswith('.html'):
                icon = "🌐"
            elif file.endswith('.py'):
                icon = "🐍"
            items.append({"type": "file", "label": f"{icon} {file}", "name": file})
        return items
    
    def _render_file_tree(self, surface, tree_rect, font):
        """Renderiza el árbol de archivos en el sidebar izquierdo"""
        pygame.draw.rect(surface, (35, 35, 45), tree_rect)
        pygame.draw.rect(surface, Colors.BORDER, tree_rect, width=1)
        
        # Título del explorador
        title = "📁 Explorer"
        title_text = font.render(title, True, (200, 200, 200))
        surface.blit(title_text, (tree_rect.x + 8, tree_rect.y + 8))
        
        # Área de contenido del árbol
        content_y = tree_rect.y + 30
        content_x = tree_rect.x + 8
        line_height = 16

        # Ruta actual
        path_display = f"/{self.current_folder}" if self.current_folder else "/"
        path_text = font.render(path_display, True, (140, 140, 160))
        surface.blit(path_text, (content_x, content_y))
        content_y += line_height

        try:
            items = self._get_tree_items()
            for item in items[:20]:
                label = item["label"]
                color = (150, 180, 220) if item["type"] in ("folder", "up") else (200, 200, 200)
                item_text = font.render(label, True, color)
                surface.blit(item_text, (content_x, content_y))
                content_y += line_height
        except Exception:
            error_text = font.render("Error al cargar", True, (200, 100, 100))
            surface.blit(error_text, (content_x, content_y))
    
    def render(self, surface, rect):
        """Renderiza el editor de código con scrollbars funcionales"""
        # Fondo
        pygame.draw.rect(surface, (30, 30, 40), rect)
        
        try:
            font = pygame.font.Font(FONT_PATH, 12)
        except:
            font = pygame.font.Font(None, 12)
        
        tree_width = 160 if self.show_file_tree else 0
        
        # Barra superior
        header_rect = pygame.Rect(rect.x, rect.y, rect.width, 25)
        pygame.draw.rect(surface, (40, 40, 50), header_rect)
        file_text = font.render(f"📝 {self.current_file}", True, (180, 180, 200))
        surface.blit(file_text, (rect.x + 10, rect.y + 5))
        
        # Renderizar file tree
        if self.show_file_tree:
            tree_rect = pygame.Rect(rect.x, rect.y + 25, tree_width, rect.height - 65)
            self._render_file_tree(surface, tree_rect, font)
        
        # Área de código
        code_start_x = rect.x + tree_width
        code_width = rect.width - tree_width
        code_area_height = rect.height - 75 if not self.show_output else (rect.height - 75) // 2
        
        # Altura de línea y cálculo de líneas visibles
        line_height = 18
        visible_lines = code_area_height // line_height
        self.last_visible_lines = visible_lines
        
        # Asegurar que scroll_y está dentro de límites
        max_scroll = max(0, len(self.code_lines) - visible_lines)
        self.scroll_y = min(max(0, self.scroll_y), max_scroll)
        
        # Renderizar líneas de código
        y = rect.y + 35
        for i in range(visible_lines):
            line_idx = self.scroll_y + i
            if line_idx >= len(self.code_lines):
                break
            
            line = self.code_lines[line_idx]
            
            # Número de línea
            line_num = font.render(f"{line_idx + 1:4d}", True, (100, 100, 120))
            surface.blit(line_num, (code_start_x + 5, y))
            
            # Highlight de la línea actual
            if line_idx == self.cursor_line:
                hl_rect = pygame.Rect(code_start_x + 35, y - 2, code_width - 50, line_height)
                pygame.draw.rect(surface, (50, 50, 70), hl_rect)
            
            # Syntax highlighting simple
            code_color = (150, 200, 150)
            if line.strip().startswith('//'):
                code_color = (100, 150, 100)
            elif any(kw in line for kw in ['echo', 'var', 'fn', 'return', 'if', 'else']):
                code_color = (200, 150, 200)
            
            code_text = font.render(line if line else " ", True, code_color)
            surface.blit(code_text, (code_start_x + 35, y))
            
            # Cursor parpadeante
            if line_idx == self.cursor_line and int(self.cursor_blink * 2) % 2 == 0:
                cursor_x = code_start_x + 35 + font.size(line[:self.cursor_col])[0]
                pygame.draw.line(surface, (200, 200, 100), (cursor_x, y), (cursor_x, y + line_height - 4), 2)
            
            y += line_height
        
        # SCROLLBAR VERTICAL (ARREGLADA)
        if len(self.code_lines) > visible_lines:
            scrollbar_x = rect.x + rect.width - 14
            scrollbar_y = rect.y + 35
            scrollbar_height = code_area_height
            
            # Fondo de la scrollbar
            bg_rect = pygame.Rect(scrollbar_x, scrollbar_y, 12, scrollbar_height)
            pygame.draw.rect(surface, (40, 40, 50), bg_rect)
            
            # Calcular altura y posición del thumb
            thumb_height_ratio = visible_lines / len(self.code_lines)
            thumb_height = max(20, int(scrollbar_height * thumb_height_ratio))
            
            # Posición del thumb basada en scroll_y
            scroll_ratio = self.scroll_y / max(1, len(self.code_lines) - visible_lines)
            thumb_y = int(scrollbar_y + (scroll_ratio * (scrollbar_height - thumb_height)))
            
            # Dibujar thumb con hover effect
            thumb_rect = pygame.Rect(scrollbar_x + 2, thumb_y, 8, thumb_height)
            hover_color = (120, 120, 140) if self.scrollbar_dragging else (90, 90, 110)
            pygame.draw.rect(surface, hover_color, thumb_rect, border_radius=2)
        
        # Panel de output
        if self.show_output and self.output_lines:
            output_y = rect.y + code_area_height + 35
            output_rect = pygame.Rect(code_start_x, output_y, code_width - 14, (rect.height - 75) // 2)
            pygame.draw.rect(surface, (20, 20, 30), output_rect)
            pygame.draw.rect(surface, (50, 50, 70), output_rect, 1)
            
            # Título
            title_text = font.render("Output", True, (150, 150, 200))
            surface.blit(title_text, (code_start_x + 10, output_y + 5))
            
            # Líneas de output
            out_y = output_y + 25
            for line in self.output_lines[:10]:
                out_text = font.render(str(line), True, (200, 200, 150))
                surface.blit(out_text, (code_start_x + 10, out_y))
                out_y += line_height
        
        # Botones inferiores
        btn_y = rect.y + rect.height - 40
        btn_x = code_start_x + 10
        
        buttons = [
            (btn_x, "Guardar", (60, 120, 60)),
            (btn_x + 90, "▶ F5", (60, 100, 160)),
            (btn_x + 180, "Output", (80, 80, 120) if self.show_output else (60, 60, 80))
        ]
        
        for btn_x_pos, btn_text, btn_color in buttons:
            btn_rect = pygame.Rect(btn_x_pos, btn_y, 80, 30)
            pygame.draw.rect(surface, btn_color, btn_rect, border_radius=4)
            text = font.render(btn_text, True, (255, 255, 255))
            surface.blit(text, (btn_x_pos + 10, btn_y + 8))
        
        # Diálogo de guardado
        if self.show_save_dialog:
            self._render_save_dialog(surface, rect, font)
    
    def _render_save_dialog(self, surface, rect, font):
        """Renderiza el diálogo de guardado"""
        # Fondo oscuro semi-transparente
        dialog_width = 350
        dialog_height = 120
        dialog_x = rect.x + (rect.width - dialog_width) // 2
        dialog_y = rect.y + (rect.height - dialog_height) // 2
        
        # Panel del diálogo
        pygame.draw.rect(surface, (40, 40, 50), pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height))
        pygame.draw.rect(surface, (100, 100, 150), pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height), 2)
        
        # Título del diálogo
        title_text = font.render("Guardar archivo", True, (200, 200, 200))
        surface.blit(title_text, (dialog_x + 15, dialog_y + 10))
        
        # Campo de entrada
        input_rect = pygame.Rect(dialog_x + 15, dialog_y + 35, dialog_width - 30, 25)
        pygame.draw.rect(surface, (60, 60, 70), input_rect)
        pygame.draw.rect(surface, (100, 100, 150), input_rect, 1)
        
        input_text = font.render(self.save_input, True, (200, 200, 200))
        surface.blit(input_text, (input_rect.x + 5, input_rect.y + 5))
        
        # Cursor en el input
        cursor = "|" if int(self.cursor_blink * 2) % 2 == 0 else " "
        cursor_text = font.render(cursor, True, (200, 200, 200))
        surface.blit(cursor_text, (input_rect.x + 5 + font.size(self.save_input)[0], input_rect.y + 5))
        
        # Hint
        hint = font.render("Presiona Enter para guardar, ESC para cancelar", True, (150, 150, 150))
        surface.blit(hint, (dialog_x + 15, dialog_y + 70))


class VideoPlayerApp(Application):
    """Reproductor de video simple"""
    
    def __init__(self):
        super().__init__(tr("app.video_player"), color=Colors.PEACH, app_id="video_player")
        self.playlist = [
            tr("video_player.sample.video1"),
            tr("video_player.sample.video2"),
            tr("video_player.sample.video3"),
        ]
        self.current_video = 0
        self.is_playing = False
        self.current_time = 0
        self.duration = 300  # 5 minutos
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.is_playing = not self.is_playing
            elif event.key == pygame.K_RIGHT:
                self.current_video = (self.current_video + 1) % len(self.playlist)
                self.current_time = 0
                self.is_playing = False
            elif event.key == pygame.K_LEFT:
                self.current_video = (self.current_video - 1) % len(self.playlist)
                self.current_time = 0
                self.is_playing = False
    
    def update(self, dt):
        if self.is_playing:
            self.current_time = min(self.current_time + dt, self.duration)
    
    def render(self, surface, rect):
        # Pantalla negra
        pygame.draw.rect(surface, Colors.BLACK, rect)
        
        try:
            font = pygame.font.Font(FONT_PATH, 14)
            title_font = pygame.font.Font(FONT_PATH, 16)
        except:
            font = pygame.font.Font(None, 14)
            title_font = pygame.font.Font(None, 16)
        
        # Área de video
        video_rect = pygame.Rect(rect.x + 20, rect.y + 20, rect.width - 40, rect.height - 120)
        pygame.draw.rect(surface, (50, 50, 50), video_rect, border_radius=6)
        
        # Nombre del video
        video_name = self.playlist[self.current_video]
        video_text = title_font.render(video_name, True, (200, 200, 200))
        surface.blit(video_text, (video_rect.x + 10, video_rect.y + 10))
        
        # Botón de play/pausa
        play_btn = pygame.Rect(rect.x + rect.width // 2 - 30, video_rect.y + video_rect.height // 2 - 15, 60, 30)
        pygame.draw.rect(surface, (100, 100, 150), play_btn, border_radius=6)
        play_text = font.render(tr("video_player.button.play") if not self.is_playing else tr("video_player.button.pause"), True, (200, 200, 200))
        surface.blit(play_text, (play_btn.x + 8, play_btn.y + 6))
        
        # Barra de progreso
        progress_rect = pygame.Rect(rect.x + 20, rect.y + rect.height - 80, rect.width - 40, 20)
        pygame.draw.rect(surface, (80, 80, 100), progress_rect, border_radius=4)
        
        if self.duration > 0:
            filled_width = int((self.current_time / self.duration) * (progress_rect.width - 4))
            filled_rect = pygame.Rect(progress_rect.x + 2, progress_rect.y + 2, filled_width, progress_rect.height - 4)
            pygame.draw.rect(surface, (100, 200, 100), filled_rect, border_radius=3)
        
        # Tiempo
        time_min = int(self.current_time) // 60
        time_sec = int(self.current_time) % 60
        dur_min = self.duration // 60
        dur_sec = self.duration % 60
        time_text = font.render(f"{time_min}:{time_sec:02d} / {dur_min}:{dur_sec:02d}", True, (180, 180, 200))
        surface.blit(time_text, (rect.x + 20, rect.y + rect.height - 35))
        
        # Instrucciones
        help_text = font.render(tr("video_player.help"), True, (120, 120, 140))
        surface.blit(help_text, (rect.x + 20, rect.y + rect.height - 15))
