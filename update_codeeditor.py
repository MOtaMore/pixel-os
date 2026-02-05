#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update CodeEditor to support file tree interaction"""

# Read the file
with open('apps/builtin_apps.py', 'r', encoding='utf-8') as f:
    content = f.read()

# The two parts to adjust button positions
old_run_btn = "            # Botón Ejecutar\n            run_btn = pygame.Rect(rect.x + 100, rect.y + rect.height - 40, 80, 30)"
new_run_btn = """            # Botón Ejecutar
            run_btn = pygame.Rect(rect.x + btn_x_offset + 90, rect.y + rect.height - 40, 80, 30)"""

old_output_btn = "            # Botón Output\n            output_btn = pygame.Rect(rect.x + 190, rect.y + rect.height - 40, 100, 30)"
new_output_btn = """            # Botón Output
            output_btn = pygame.Rect(rect.x + btn_x_offset + 180, rect.y + rect.height - 40, 100, 30)"""

# Replace button positions
if old_run_btn in content:
    content = content.replace(old_run_btn, new_run_btn)
    print("✓ Updated run button position")

if old_output_btn in content:
    content = content.replace(old_output_btn, new_output_btn)
    print("✓ Updated output button position")

# Find mouse click handling and update it
before_part = """        # Clicks en los botones
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.window:
            mouse_pos = event.pos
            rect = self.window.content_rect
            
            # Botón Guardar
            save_btn = pygame.Rect(rect.x + 10, rect.y + rect.height - 40, 80, 30)"""

new_part = """        # Clicks en los botones y file tree
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.window:
            mouse_pos = event.pos
            rect = self.window.content_rect
            tree_width = 160 if self.show_file_tree else 0
            
            # Click en el file tree
            if self.show_file_tree and mouse_pos[0] < rect.x + tree_width:
                # Interactuar con el árbol de archivos
                contents = self._get_folder_contents(self.current_folder)
                tree_start_y = rect.y + 55  # Posición Y donde empieza el contenido del árbol
                line_height = 16
                
                # Calcular qué elemento fue clickeado
                clicked_item_idx = (mouse_pos[1] - tree_start_y) // line_height
                all_items = sorted(contents['folders']) + sorted(contents['files'])
                
                if 0 <= clicked_item_idx < len(all_items):
                    item = all_items[clicked_item_idx]
                    if item in contents['folders']:
                        # Toggle carpeta expandida
                        if item in self.expanded_folders:
                            self.expanded_folders.discard(item)
                        else:
                            self.expanded_folders.add(item)
                    else:
                        # Cargar archivo
                        self.load_file(self.current_folder, item)
                return
            
            # Ajustar posiciones de botones por el tree width
            btn_x_offset = tree_width
            
            # Botón Guardar
            save_btn = pygame.Rect(rect.x + btn_x_offset + 10, rect.y + rect.height - 40, 80, 30)"""

if before_part in content:
    content = content.replace(before_part, new_part)
    print("✓ Updated mouse click handling for file tree")
else:
    print("✗ Could not find exact mouse click pattern")

# Write back
with open('apps/builtin_apps.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("✓ CodeEditor file updated successfully")
