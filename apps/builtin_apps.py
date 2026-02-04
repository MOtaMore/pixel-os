"""
Aplicaciones integradas del sistema Pixel-OS
"""
import pygame
from core.plugin_manager import Application
from config.settings import *


class TerminalApp(Application):
    """Terminal simple con temática pastel"""
    
    def __init__(self):
        super().__init__("Terminal", color=Colors.GREEN)
        self.lines = ["Pixel-OS Terminal v1.0", "Escribe 'help' para ver comandos", ""]
        self.current_input = ""
        self.cursor_blink = 0
        self.commands = {
            "help": self._cmd_help,
            "clear": self._cmd_clear,
            "echo": self._cmd_echo,
            "date": self._cmd_date,
            "color": self._cmd_color,
        }
    
    def _cmd_help(self, args):
        return ["Comandos disponibles:", "  help  - Muestra esta ayuda", 
                "  clear - Limpia la pantalla", "  echo  - Repite el texto",
                "  date  - Muestra la fecha", "  color - Cambia el color"]
    
    def _cmd_clear(self, args):
        self.lines = []
        return []
    
    def _cmd_echo(self, args):
        return [" ".join(args)]
    
    def _cmd_date(self, args):
        import datetime
        return [datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    
    def _cmd_color(self, args):
        if args:
            color_map = {
                "pink": Colors.PINK, "blue": Colors.BLUE,
                "green": Colors.GREEN, "yellow": Colors.YELLOW,
                "purple": Colors.PURPLE, "peach": Colors.PEACH
            }
            if args[0] in color_map:
                self.color = color_map[args[0]]
                if self.window:
                    self.window.color = self.color
                return [f"Color cambiado a {args[0]}"]
        return ["Usa: color [pink|blue|green|yellow|purple|peach]"]
    
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
                        self.lines.append(f"Comando desconocido: {cmd}")
                self.lines.append("")
                self.current_input = ""
            elif event.key == pygame.K_BACKSPACE:
                self.current_input = self.current_input[:-1]
            else:
                if event.unicode.isprintable():
                    self.current_input += event.unicode
    
    def update(self, dt):
        self.cursor_blink += dt
    
    def render(self, surface, rect):
        # Fondo oscuro pastel
        bg_color = (40, 35, 50)
        pygame.draw.rect(surface, bg_color, rect)
        
        # Renderizar líneas
        try:
            font = pygame.font.Font(FONT_PATH, 14)
        except:
            font = pygame.font.Font(None, 14)
        
        y = rect.y + 10
        line_height = 20
        
        # Mostrar últimas líneas que caben
        visible_lines = (rect.height - 40) // line_height
        start_idx = max(0, len(self.lines) - visible_lines)
        
        for line in self.lines[start_idx:]:
            text = font.render(line, True, (200, 255, 200))
            surface.blit(text, (rect.x + 10, y))
            y += line_height
        
        # Prompt actual
        prompt = f"> {self.current_input}"
        cursor = "|" if int(self.cursor_blink * 2) % 2 == 0 else " "
        text = font.render(prompt + cursor, True, (150, 255, 150))
        surface.blit(text, (rect.x + 10, y))


class TextEditorApp(Application):
    """Editor de texto simple"""
    
    def __init__(self):
        super().__init__("Editor de Texto", color=Colors.BLUE)
        self.lines = [""]
        self.cursor_line = 0
        self.cursor_col = 0
        self.cursor_blink = 0
    
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
            elif event.key == pygame.K_DOWN and self.cursor_line < len(self.lines) - 1:
                self.cursor_line += 1
                self.cursor_col = min(self.cursor_col, len(self.lines[self.cursor_line]))
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
        
        for i, line in enumerate(self.lines):
            # Highlight de línea actual
            if i == self.cursor_line:
                highlight = pygame.Rect(rect.x, y - 2, rect.width, line_height)
                pygame.draw.rect(surface, Colors.HOVER, highlight)
            
            # Texto
            text = font.render(line if line else " ", True, Colors.TEXT_PRIMARY)
            surface.blit(text, (rect.x + 10, y))
            
            # Cursor
            if i == self.cursor_line and int(self.cursor_blink * 2) % 2 == 0:
                cursor_x = rect.x + 10 + font.size(line[:self.cursor_col])[0]
                pygame.draw.line(surface, Colors.TEXT_PRIMARY,
                               (cursor_x, y), (cursor_x, y + line_height - 4), 2)
            
            y += line_height


class FileManagerApp(Application):
    """Explorador de archivos básico"""
    
    def __init__(self):
        super().__init__("Explorador de Archivos", color=Colors.YELLOW)
        self.current_path = "/"
        self.items = [
            ("📁 Documentos", "folder"),
            ("📁 Imágenes", "folder"),
            ("📁 Música", "folder"),
            ("📁 Videos", "folder"),
            ("📄 readme.txt", "file"),
            ("📄 notas.txt", "file"),
        ]
        self.selected_idx = -1
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.window:
                mouse_pos = event.pos
                # Calcular qué item se clickeó
                content_y = self.window.content_rect.y + 50
                item_height = 40
                
                for i, item in enumerate(self.items):
                    item_rect = pygame.Rect(
                        self.window.content_rect.x + 10,
                        content_y + i * item_height,
                        self.window.content_rect.width - 20,
                        item_height - 5
                    )
                    if item_rect.collidepoint(mouse_pos):
                        self.selected_idx = i
                        break
    
    def render(self, surface, rect):
        # Fondo
        pygame.draw.rect(surface, Colors.WINDOW_BG, rect)
        
        # Barra de dirección
        address_bar = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 20, 30)
        pygame.draw.rect(surface, (240, 240, 250), address_bar, border_radius=6)
        
        try:
            font = pygame.font.Font(FONT_PATH, 14)
        except:
            font = pygame.font.Font(None, 14)
        
        path_text = font.render(self.current_path, True, Colors.TEXT_PRIMARY)
        surface.blit(path_text, (address_bar.x + 10, address_bar.y + 8))
        
        # Lista de archivos
        y = rect.y + 50
        item_height = 40
        
        for i, (name, item_type) in enumerate(self.items):
            item_rect = pygame.Rect(rect.x + 10, y, rect.width - 20, item_height - 5)
            
            # Fondo si está seleccionado
            if i == self.selected_idx:
                pygame.draw.rect(surface, Colors.ACTIVE, item_rect, border_radius=6)
            elif item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(surface, Colors.HOVER, item_rect, border_radius=6)
            
            # Nombre del item
            text = font.render(name, True, Colors.TEXT_PRIMARY)
            surface.blit(text, (item_rect.x + 10, item_rect.y + 10))
            
            y += item_height


class SettingsApp(Application):
    """Configuración del sistema"""
    
    def __init__(self):
        super().__init__("Configuración", color=Colors.PURPLE)
        self.sections = [
            "🎨 Personalización",
            "🔊 Sonido",
            "🖥️ Pantalla",
            "⚙️ Sistema",
            "🔌 Plugins",
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
        content = font.render("Opciones de configuración aquí...", True, Colors.TEXT_SECONDARY)
        surface.blit(content, (content_x, rect.y + 60))
