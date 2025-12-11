# ✅ CORRECCIÓN: Sistema de permisos funcionando con dicts

## 🔍 Problema reportado:
```
"No se pueden verificar los permisos del usuario"
```

## 📋 Análisis:

El sistema de permisos estaba configurado correctamente:
- ✅ Archivo `role_permissions.json` existe en la raíz
- ✅ Función `get_role_permissions()` carga permisos correctamente
- ✅ Clase `User` (objeto) tiene método `has_permission()`

**PERO:** Después de la migración a SQL directo, los usuarios de BD son **diccionarios**, no objetos `User`.

## 🐛 Causa raíz:

La clase `Session` tenía estos métodos que asumían `self.user` es un objeto:

```python
# ❌ ANTES - Solo funcionaba con objetos User
def is_valid(self) -> bool:
    return self.user.is_active  # AttributeError si user es dict

def has_permission(self, module_id: str, permission: Permission) -> bool:
    return self.user.has_permission(module_id, permission)  # No existe en dict
```

## ✅ Solución aplicada:

Actualizada la clase `Session` en `core/auth.py` para soportar **ambos formatos**:

### 1. Método `is_valid()`:
```python
def is_valid(self) -> bool:
    """Verifica si la sesión es válida."""
    if isinstance(self.user, dict):
        return bool(self.user.get("is_active", False))
    return self.user.is_active
```

### 2. Método `has_permission()`:
```python
def has_permission(self, module_id: str, permission: Permission) -> bool:
    """
    Shortcut para verificar permisos desde la sesión.
    Soporta tanto objetos User como dicts.
    """
    if isinstance(self.user, dict):
        # Usuario de BD (dict) - calcular permisos manualmente
        role_str = self.user.get("role", "")
        try:
            role = UserRole(role_str) if role_str else UserRole.EMPLOYEE
        except:
            role = UserRole.EMPLOYEE
        
        # Obtener permisos base del rol
        role_perms = get_role_permissions(role)
        module_perms = role_perms.get(module_id, [])
        
        # Admin siempre tiene acceso
        if Permission.ADMIN in module_perms:
            return True
        
        return permission in module_perms
    else:
        # Objeto User (demo) - usar método del objeto
        return self.user.has_permission(module_id, permission)
```

### 3. Métodos auxiliares actualizados:
```python
def get_company_name(self) -> str:
    """Obtiene el nombre de la empresa activa."""
    if self.company_context:
        company = self.company_context.company
        if isinstance(company, dict):
            return company.get("nombre_comercial") or company.get("nombre_fiscal", "Sin empresa")
        return company.nombre_comercial or company.nombre_fiscal
    return "Sin empresa"

def get_group_name(self) -> str:
    """Obtiene el nombre del grupo activo."""
    if self.company_context:
        group = self.company_context.group
        if isinstance(group, dict):
            return group.get("name", "Sin grupo")
        return group.name
    return "Sin grupo"
```

---

## 🎯 Cómo funciona el sistema de permisos:

### 1. Archivo `role_permissions.json`:
```json
{
  "admin": {
    "clientes": ["ADMIN", "CREATE", "DELETE", "EXPORT", ...],
    "articulos": ["ADMIN", "CREATE", "DELETE", ...],
    ...
  },
  "manager": {
    "clientes": ["READ", "CREATE", "UPDATE"],
    ...
  },
  ...
}
```

### 2. Función `get_role_permissions(role)`:
- Retorna permisos base según el rol
- Aplica overrides del archivo JSON
- Retorna dict: `{module_id: [Permission.READ, Permission.CREATE, ...]}`

### 3. Verificación de permisos:
```python
# Desde la sesión
if session.has_permission("clientes", Permission.READ):
    # Usuario puede ver clientes
    
# Desde el usuario (si es objeto)
if user.has_permission("clientes", Permission.CREATE):
    # Usuario puede crear clientes
```

### 4. Permisos disponibles:
```python
class Permission(Enum):
    READ = "read"
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    ADMIN = "admin"
    EXPORT = "export"
    IMPORT = "import"
    PRINT = "print"
```

---

## ✅ Verificación:

### Usuarios de BD (dicts):
```python
user = UserRepository.get_user_by_username("admin")
# user = {'id': 1, 'username': 'admin', 'role': 'admin', 'is_active': 1, ...}

session = Session(user=user, login_time=datetime.now(), token="...")
✅ session.is_valid() → True
✅ session.has_permission("clientes", Permission.READ) → True
```

### Demo users (objetos):
```python
user = User(username="admin", role=UserRole.ADMIN, ...)
session = Session(user=user, login_time=datetime.now(), token="...")
✅ session.is_valid() → True
✅ session.has_permission("clientes", Permission.READ) → True
```

---

## 📊 Archivos modificados:

| Archivo | Cambios |
|---------|---------|
| `core/auth.py` | ✅ Clase `Session` actualizada (3 métodos) |

---

## 🎉 Resultado:

**¡El sistema de permisos ahora funciona correctamente con usuarios de BD (dicts) y demo users (objetos)!**

```
✅ Permisos se cargan desde role_permissions.json
✅ session.has_permission() funciona con dicts
✅ session.is_valid() funciona con dicts
✅ Compatibilidad con objetos User mantenida
✅ get_company_name() y get_group_name() funcionan con dicts
```

---

**Fecha:** 2025-12-11  
**Estado:** ✅ RESUELTO  
**Sistema de permisos:** ✅ FUNCIONAL

