# Gestor de Módulos

Módulo para gestionar permisos de módulos por rol de forma visual.

## Arquitectura

Este módulo sigue el patrón **MVC (Model-View-Controller)** para separar responsabilidades:

### 📁 Estructura de Archivos

```
gestor_modulos/
├── __init__.py          # Inicialización del paquete
├── model.py             # Lógica de negocio (Modelo)
├── view.py              # Interfaz gráfica (Vista)
└── README.md            # Documentación
```

### 🎯 Responsabilidades

#### `model.py` - Lógica de Negocio
**Clase:** `RolePermissionsManager`

Responsabilidades:
- ✅ Cargar permisos desde `role_permissions.json`
- ✅ Validar y normalizar permisos
- ✅ Guardar permisos en el archivo JSON
- ✅ Obtener/establecer permisos de módulos
- ✅ Calcular permisos comunes entre módulos
- ✅ Gestión de múltiples módulos simultáneamente

**NO contiene:** Código de interfaz gráfica (Qt/PySide6)

#### `view.py` - Interfaz Gráfica
**Clase:** `GestorModulosView`

Responsabilidades:
- ✅ Construir la interfaz de usuario
- ✅ Manejar eventos de usuario (clicks, selecciones)
- ✅ Actualizar la vista según el estado
- ✅ Mostrar mensajes al usuario
- ✅ Delegar operaciones de datos al modelo

**NO contiene:** Lógica de validación, normalización o persistencia

## Uso

### Desde la aplicación principal

```python
from modules.gestor_modulos.view import GestorModulosView

# Crear la vista
gestor_view = GestorModulosView()
gestor_view.show()
```

### Uso del modelo directamente

```python
from modules.gestor_modulos.model import RolePermissionsManager

# Crear gestor
manager = RolePermissionsManager()

# Obtener permisos de un módulo
perms = manager.get_module_permissions('admin', 'clientes')

# Establecer permisos
manager.set_module_permissions('sales', 'facturas', ['READ', 'CREATE'])

# Guardar cambios
manager.save()
```

## Funcionalidades

### Selección Múltiple
- **Ctrl+Click**: Seleccionar/deseleccionar módulos individuales
- **Shift+Click**: Seleccionar rango de módulos
- **Click simple**: Seleccionar un solo módulo

### Asignación de Permisos
- Seleccionar permisos individuales con checkboxes
- Botón "✓ Todos" para seleccionar todos los permisos
- Botón "✗ Ninguno" para deseleccionar todos
- Aplicar permisos a múltiples módulos simultáneamente

### Permisos Disponibles
- `READ`: Ver datos
- `CREATE`: Crear registros
- `UPDATE`: Modificar registros
- `DELETE`: Eliminar registros
- `ADMIN`: Acceso total
- `EXPORT`: Exportar datos
- `IMPORT`: Importar datos
- `PRINT`: Imprimir documentos

## Persistencia

Los permisos se guardan en:
```
Creative_ERP/role_permissions.json
```

Formato:
```json
{
  "admin": {
    "clientes": ["ADMIN"],
    "facturas": ["ADMIN"]
  },
  "sales": {
    "clientes": ["READ", "CREATE", "UPDATE"],
    "facturas": ["READ", "CREATE"]
  }
}
```

## Ventajas de la Separación

✅ **Mantenibilidad**: Cambios en UI no afectan lógica de negocio  
✅ **Testabilidad**: Modelo puede ser testeado sin UI  
✅ **Reutilización**: Modelo puede usarse desde CLI, API, etc.  
✅ **Claridad**: Responsabilidades bien definidas  
✅ **Escalabilidad**: Fácil agregar nuevas vistas o modelos
