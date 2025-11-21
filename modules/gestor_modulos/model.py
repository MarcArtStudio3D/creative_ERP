"""
Modelo de negocio para el gestor de módulos.

Maneja la lógica de carga, validación, normalización y guardado de permisos por rol.
"""

from typing import Dict, List, Set, Optional
import json
import os


class RolePermissionsManager:
    """Gestor de permisos por rol.
    
    Maneja la persistencia y validación de permisos de módulos por rol
    en el archivo role_permissions.json.
    """
    
    VALID_PERMISSIONS: Set[str] = {
        'READ', 'CREATE', 'UPDATE', 'DELETE', 
        'ADMIN', 'EXPORT', 'IMPORT', 'PRINT'
    }
    
    def __init__(self, file_path: Optional[str] = None):
        """
        Inicializa el gestor de permisos.
        
        Args:
            file_path: Ruta al archivo role_permissions.json. 
                      Si es None, se usa la ruta por defecto.
        """
        if file_path is None:
            # Ruta por defecto: raíz del proyecto
            base = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            file_path = os.path.join(base, 'role_permissions.json')
        
        self.file_path = file_path
        self.permissions: Dict[str, Dict[str, List[str]]] = {}
        self.load()
    
    def load(self) -> None:
        """Carga los permisos desde el archivo JSON."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.permissions = json.load(f)
            else:
                self.permissions = {}
        except Exception as e:
            print(f"Error al cargar permisos: {e}")
            self.permissions = {}
        
        # Normalizar después de cargar
        self.normalize()
    
    def normalize(self) -> bool:
        """
        Normaliza los permisos asegurando formato correcto.
        
        Returns:
            True si se realizaron cambios, False si no.
        """
        changed = False
        
        try:
            normalized = {}
            
            for role, modules in (self.permissions or {}).items():
                if not isinstance(modules, dict):
                    continue
                
                normalized_modules = {}
                
                for module_id, perms in modules.items():
                    if not isinstance(perms, list):
                        continue
                    
                    # Limpiar y validar permisos
                    cleaned_perms = []
                    for perm in perms:
                        if not isinstance(perm, str):
                            continue
                        
                        # Normalizar a mayúsculas
                        perm_upper = perm.strip().upper()
                        
                        # Ignorar valores vacíos o 'NONE'
                        if perm_upper in ('', 'NONE'):
                            continue
                        
                        # Validar que sea un permiso válido
                        if perm_upper in self.VALID_PERMISSIONS:
                            cleaned_perms.append(perm_upper)
                    
                    # Solo guardar si hay permisos válidos
                    if cleaned_perms:
                        # Eliminar duplicados y ordenar
                        normalized_modules[module_id] = sorted(list(set(cleaned_perms)))
                
                # Solo guardar roles con módulos
                if normalized_modules:
                    normalized[role] = normalized_modules
            
            # Verificar si hubo cambios
            if normalized != (self.permissions or {}):
                self.permissions = normalized
                changed = True
        
        except Exception as e:
            print(f"Error al normalizar permisos: {e}")
            return False
        
        # Si hubo cambios, persistir automáticamente
        if changed:
            self.save()
        
        return changed
    
    def save(self) -> bool:
        """
        Guarda los permisos en el archivo JSON.
        
        Returns:
            True si se guardó correctamente, False si hubo error.
        """
        try:
            # Normalizar antes de guardar
            self.normalize()
            
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.permissions, f, indent=2, ensure_ascii=False)
            
            return True
        
        except Exception as e:
            print(f"Error al guardar permisos: {e}")
            return False
    
    def get_module_permissions(self, role: str, module_id: str) -> List[str]:
        """
        Obtiene los permisos de un módulo para un rol específico.
        
        Args:
            role: Nombre del rol
            module_id: ID del módulo
            
        Returns:
            Lista de permisos (strings en mayúsculas)
        """
        role_perms = self.permissions.get(role, {})
        return role_perms.get(module_id, [])
    
    def set_module_permissions(self, role: str, module_id: str, perms: List[str]) -> None:
        """
        Establece los permisos de un módulo para un rol.
        
        Args:
            role: Nombre del rol
            module_id: ID del módulo
            perms: Lista de permisos a asignar
        """
        if role not in self.permissions:
            self.permissions[role] = {}
        
        # Normalizar permisos antes de guardar
        normalized_perms = [p.strip().upper() for p in perms if p.strip().upper() in self.VALID_PERMISSIONS]
        
        if normalized_perms:
            self.permissions[role][module_id] = sorted(list(set(normalized_perms)))
        else:
            # Si no hay permisos, eliminar la entrada
            if module_id in self.permissions[role]:
                del self.permissions[role][module_id]
    
    def set_multiple_modules_permissions(self, role: str, module_ids: List[str], perms: List[str]) -> int:
        """
        Establece los mismos permisos para múltiples módulos.
        
        Args:
            role: Nombre del rol
            module_ids: Lista de IDs de módulos
            perms: Lista de permisos a asignar
            
        Returns:
            Número de módulos actualizados
        """
        count = 0
        for module_id in module_ids:
            self.set_module_permissions(role, module_id, perms)
            count += 1
        return count
    
    def get_common_permissions(self, role: str, module_ids: List[str]) -> Set[str]:
        """
        Obtiene los permisos comunes a todos los módulos especificados.
        
        Args:
            role: Nombre del rol
            module_ids: Lista de IDs de módulos
            
        Returns:
            Conjunto de permisos comunes a todos los módulos
        """
        if not module_ids:
            return set()
        
        # Obtener permisos del primer módulo
        common = set(self.get_module_permissions(role, module_ids[0]))
        
        # Intersección con los demás módulos
        for module_id in module_ids[1:]:
            module_perms = set(self.get_module_permissions(role, module_id))
            common &= module_perms
        
        return common
    
    def get_all_roles(self) -> List[str]:
        """
        Obtiene todos los roles que tienen permisos configurados.
        
        Returns:
            Lista de nombres de roles
        """
        return list(self.permissions.keys())
    
    def get_all_modules_for_role(self, role: str) -> List[str]:
        """
        Obtiene todos los módulos que tienen permisos para un rol.
        
        Args:
            role: Nombre del rol
            
        Returns:
            Lista de IDs de módulos
        """
        role_perms = self.permissions.get(role, {})
        return list(role_perms.keys())
