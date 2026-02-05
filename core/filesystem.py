"""
Virtual Filesystem - Sistema de almacenamiento de archivos para Pixel-OS
Permite guardar y organizar archivos creados en el SO
"""
import os
import json
from typing import Dict, List, Optional
from datetime import datetime


class VirtualFile:
    """Representa un archivo en el filesystem virtual"""
    
    def __init__(self, name: str, content: str = "", file_type: str = "text"):
        """Inicializa un archivo
        
        Args:
            name: Nombre del archivo
            content: Contenido del archivo
            file_type: Tipo de archivo (text, image, document, etc)
        """
        self.name = name
        self.content = content
        self.file_type = file_type
        self.created_at = datetime.now().isoformat()
        self.modified_at = datetime.now().isoformat()
        self.size = len(content)
        self.original_path: Optional[str] = None  # Para papelera: dónde estaba antes
    
    def update_content(self, content: str):
        """Actualiza el contenido del archivo"""
        self.content = content
        self.modified_at = datetime.now().isoformat()
        self.size = len(content)
    
    def to_dict(self) -> Dict:
        """Convierte el archivo a diccionario para serialización"""
        return {
            'name': self.name,
            'content': self.content,
            'type': self.file_type,
            'created_at': self.created_at,
            'modified_at': self.modified_at,
            'size': self.size,
            'original_path': self.original_path,
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'VirtualFile':
        """Crea un archivo desde un diccionario"""
        file = VirtualFile(data['name'], data.get('content', ''), data.get('type', 'text'))
        file.created_at = data.get('created_at', file.created_at)
        file.modified_at = data.get('modified_at', file.modified_at)
        file.size = data.get('size', file.size)
        file.original_path = data.get('original_path')
        return file


class VirtualFolder:
    """Representa una carpeta en el filesystem virtual"""
    
    def __init__(self, name: str):
        """Inicializa una carpeta"""
        self.name = name
        self.files: Dict[str, VirtualFile] = {}
        self.folders: Dict[str, 'VirtualFolder'] = {}
        self.created_at = datetime.now().isoformat()
        self.original_path: Optional[str] = None  # Para papelera: dónde estaba antes
    
    def create_file(self, name: str, content: str = "", file_type: str = "text") -> VirtualFile:
        """Crea un archivo en esta carpeta"""
        file = VirtualFile(name, content, file_type)
        self.files[name] = file
        return file
    
    def create_folder(self, name: str) -> 'VirtualFolder':
        """Crea una subcarpeta"""
        folder = VirtualFolder(name)
        self.folders[name] = folder
        return folder
    
    def delete_file(self, name: str) -> bool:
        """Elimina un archivo"""
        if name in self.files:
            del self.files[name]
            return True
        return False
    
    def delete_folder(self, name: str) -> bool:
        """Elimina una carpeta (solo si está vacía)"""
        if name in self.folders and not self.folders[name].files and not self.folders[name].folders:
            del self.folders[name]
            return True
        return False
    
    def get_file(self, name: str) -> Optional[VirtualFile]:
        """Obtiene un archivo por nombre"""
        return self.files.get(name)
    
    def get_folder(self, name: str) -> Optional['VirtualFolder']:
        """Obtiene una subcarpeta por nombre"""
        return self.folders.get(name)
    
    def list_contents(self) -> Dict:
        """Lista el contenido de la carpeta"""
        return {
            'files': list(self.files.keys()),
            'folders': list(self.folders.keys()),
        }
    
    def to_dict(self) -> Dict:
        """Convierte la carpeta a diccionario para serialización"""
        return {
            'name': self.name,
            'type': 'folder',
            'created_at': self.created_at,
            'original_path': self.original_path,
            'files': {name: file.to_dict() for name, file in self.files.items()},
            'folders': {name: folder.to_dict() for name, folder in self.folders.items()},
        }
    
    @staticmethod
    def from_dict(data: Dict) -> 'VirtualFolder':
        """Crea una carpeta desde un diccionario"""
        folder = VirtualFolder(data['name'])
        folder.created_at = data.get('created_at', folder.created_at)
        folder.original_path = data.get('original_path')
        
        # Restaurar archivos
        for file_name, file_data in data.get('files', {}).items():
            folder.files[file_name] = VirtualFile.from_dict(file_data)
        
        # Restaurar carpetas
        for folder_name, folder_data in data.get('folders', {}).items():
            folder.folders[folder_name] = VirtualFolder.from_dict(folder_data)
        
        return folder


class VirtualFilesystem:
    """Filesystem virtual para Pixel-OS"""
    
    def __init__(self, storage_path: str = "user_data/filesystem"):
        """Inicializa el filesystem virtual
        
        Args:
            storage_path: Ruta donde se almacenan los datos del filesystem
        """
        self.storage_path = storage_path
        self.root = VirtualFolder("root")
        
        # Crear estructura por defecto
        self._create_default_structure()
        
        # Cargar datos guardados
        self.load()
    
    def _create_default_structure(self):
        """Crea la estructura de carpetas por defecto"""
        self.root.create_folder("Documentos")
        self.root.create_folder("Imágenes")
        self.root.create_folder("Música")
        self.root.create_folder("Vídeos")
        self.root.create_folder("Descargas")
        self.root.create_folder("Papelera")
    
    def save(self):
        """Guarda el filesystem a archivo"""
        os.makedirs(self.storage_path, exist_ok=True)
        
        data = {
            'version': '1.0',
            'created_at': datetime.now().isoformat(),
            'filesystem': self.root.to_dict(),
        }
        
        filepath = os.path.join(self.storage_path, "filesystem.json")
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error guardando filesystem: {e}")
    
    def load(self):
        """Carga el filesystem desde archivo"""
        filepath = os.path.join(self.storage_path, "filesystem.json")
        
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.root = VirtualFolder.from_dict(data['filesystem'])
            except Exception as e:
                print(f"Error cargando filesystem: {e}")
                self._create_default_structure()
    
    def get_path(self, path: str) -> Optional[VirtualFolder]:
        """Navega hasta una carpeta usando una ruta (ej: "Documentos/Trabajo")
        
        Args:
            path: Ruta separada por barras
            
        Returns:
            La carpeta destino o None si no existe
        """
        current = self.root
        
        if path == "/" or path == "":
            return current
        
        parts = path.strip("/").split("/")
        for part in parts:
            if part:
                current = current.get_folder(part)
                if not current:
                    return None
        
        return current
    
    def create_file(self, path: str, name: str, content: str = "", file_type: str = "text") -> Optional[VirtualFile]:
        """Crea un archivo en la ruta especificada
        
        Args:
            path: Ruta donde crear el archivo
            name: Nombre del archivo
            content: Contenido inicial
            file_type: Tipo de archivo
            
        Returns:
            El archivo creado o None si la ruta no existe
        """
        folder = self.get_path(path)
        if folder:
            file = folder.create_file(name, content, file_type)
            self.save()
            return file
        return None
    
    def create_folder(self, path: str, name: str) -> Optional[VirtualFolder]:
        """Crea una carpeta en la ruta especificada"""
        folder = self.get_path(path)
        if folder:
            new_folder = folder.create_folder(name)
            self.save()
            return new_folder
        return None
    
    def delete_file(self, path: str, name: str) -> bool:
        """Elimina un archivo"""
        folder = self.get_path(path)
        if folder and folder.delete_file(name):
            self.save()
            return True
        return False
    
    def save_file(self, path: str, name: str, content: str) -> bool:
        """Guarda o actualiza el contenido de un archivo"""
        folder = self.get_path(path)
        if folder:
            file = folder.get_file(name)
            if file:
                file.update_content(content)
                self.save()
                return True
        return False
    
    def list_directory(self, path: str) -> Optional[Dict]:
        """Lista el contenido de una carpeta"""
        folder = self.get_path(path)
        if folder:
            return folder.list_contents()
        return None
    
    def move_to_trash(self, path: str, name: str, is_folder: bool = False) -> bool:
        """Mueve un archivo o carpeta a la papelera
        
        Args:
            path: Ruta donde está el elemento
            name: Nombre del elemento
            is_folder: True si es una carpeta, False si es archivo
            
        Returns:
            True si fue exitoso, False en caso contrario
        """
        try:
            folder = self.get_path(path)
            if not folder:
                return False
            
            trash = self.get_path("Papelera")
            if not trash:
                return False
            
            # Guardar ruta original
            original_path = f"/{path}" if path else "/"
            
            if is_folder:
                # Mover carpeta
                if name not in folder.folders:
                    return False
                target = folder.folders.pop(name)
                target.original_path = original_path
                trash.folders[name] = target
            else:
                # Mover archivo
                if name not in folder.files:
                    return False
                target = folder.files.pop(name)
                target.original_path = original_path
                trash.files[name] = target
            
            self.save()
            return True
        except Exception as e:
            print(f"Error moviendo a papelera: {e}")
            return False
    
    def restore_from_trash(self, name: str, is_folder: bool = False) -> bool:
        """Restaura un archivo o carpeta desde la papelera
        
        Args:
            name: Nombre del elemento a restaurar
            is_folder: True si es una carpeta
            
        Returns:
            True si fue exitoso
        """
        try:
            trash = self.get_path("Papelera")
            if not trash:
                return False
            
            if is_folder:
                if name not in trash.folders:
                    return False
                target = trash.folders.pop(name)
                original_path = target.original_path or ""
            else:
                if name not in trash.files:
                    return False
                target = trash.files.pop(name)
                original_path = target.original_path or ""
            
            # Restaurar a la ruta original
            dest = self.get_path(original_path)
            if not dest:
                # Si la ruta original no existe, restaurar a raíz
                dest = self.root
            
            if is_folder:
                target.original_path = None
                dest.folders[name] = target
            else:
                target.original_path = None
                dest.files[name] = target
            
            self.save()
            return True
        except Exception as e:
            print(f"Error restaurando de papelera: {e}")
            return False
    
    def empty_trash(self) -> bool:
        """Vacía completamente la papelera"""
        try:
            trash = self.get_path("Papelera")
            if not trash:
                return False
            
            trash.files.clear()
            trash.folders.clear()
            self.save()
            return True
        except Exception as e:
            print(f"Error vaciando papelera: {e}")
            return False
    
    def create_nested_folder(self, path: str, nested_path: str) -> Optional[VirtualFolder]:
        """Crea carpetas anidadas (ej: mkdir a/b/c desde raíz)
        
        Args:
            path: Ruta base donde crear
            nested_path: Ruta anidada (ej: "a/b/c")
            
        Returns:
            La última carpeta creada o None si falla
        """
        try:
            current = self.get_path(path)
            if not current:
                return None
            
            parts = nested_path.strip("/").split("/")
            for part in parts:
                if part:
                    folder = current.get_folder(part)
                    if not folder:
                        folder = current.create_folder(part)
                    current = folder
            
            self.save()
            return current
        except Exception as e:
            print(f"Error creando carpetas anidadas: {e}")
            return None
