# Módulo de Divisiones del Almacén

## Descripción
Este módulo gestiona las divisiones jerárquicas del almacén: **Secciones**, **Familias** y **Subfamilias**. Estas divisiones se utilizan para clasificar los artículos de forma organizada.

## Estructura Jerárquica
```
Sección (ej: S001 - Electrónica)
  └── Familia (ej: F001 - Teléfonos)
       └── Subfamilia (ej: SF001 - Smartphones)
            └── Artículos
```

## Arquitectura MVC + Repository

El módulo sigue la arquitectura en capas (Layered Architecture) con el patrón Repository:

### 1. **Models** (`models.py`)
Define las tres entidades de base de datos:
- `Seccion`: Primera división del almacén
- `Familia`: Segunda división (pertenece a una sección)
- `Subfamilia`: Tercera división (pertenece a una familia)

### 2. **Repository** (`divisiones_repository.py`)
Capa de acceso a datos. Encapsula todas las operaciones CRUD:
- Métodos para Secciones: `obtener_todas_secciones()`, `guardar_seccion()`, etc.
- Métodos para Familias: `obtener_familias_por_seccion()`, `guardar_familia()`, etc.
- Métodos para Subfamilias: `obtener_subfamilias_por_familia()`, `guardar_subfamilia()`, etc.
- Generación automática de códigos: `generar_codigo_seccion()`, etc.

### 3. **Controller** (`divisiones_controller.py`)
Lógica de negocio y coordinación:
- Gestiona el estado de la aplicación (qué está seleccionado)
- Coordina las operaciones entre las tres entidades
- Valida las reglas de negocio (ej: no borrar sección con familias)
- Maneja el flujo de creación/edición

### 4. **View** (`divisiones_view.py`)
Interfaz de usuario con PySide6:
- Tres listas para navegar la jerarquía
- Formulario de edición compartido
- Botones de acción (Añadir, Borrar, Editar, Guardar)
- Árbol de navegación que muestra la ruta seleccionada

### 5. **UI** (`ui_frmDivisiones.py`)
Archivo generado automáticamente desde `frmDivisiones.ui` con Qt Designer.

## Uso

### Abrir el diálogo desde código:
```python
from modules.articulos.divisiones_view import DivisionesView

# Crear y mostrar el diálogo
dialogo = DivisionesView(parent=self)
resultado = dialogo.exec()
```

### Flujo de trabajo del usuario:
1. **Seleccionar Sección** → Se muestran sus familias
2. **Seleccionar Familia** → Se muestran sus subfamilias
3. **Seleccionar Subfamilia** → Se muestra en el árbol
4. **Añadir/Editar** → El formulario se habilita con código autogenerado
5. **Guardar** → Se valida y guarda en la base de datos

## Características

### Códigos Autogenerados
- Secciones: `S001`, `S002`, `S003`, ...
- Familias: `F001`, `F002`, `F003`, ...
- Subfamilias: `SF001`, `SF002`, `SF003`, ...

### Validaciones
- Códigos únicos
- Nombres obligatorios
- No se puede borrar sección/familia con hijos
- Debe seleccionar padre antes de crear hijo

### Borrado en Cascada
- Al borrar una Sección, se borran todas sus Familias y Subfamilias
- Al borrar una Familia, se borran todas sus Subfamilias

## Base de Datos

Las tres tablas se crean automáticamente en la base de datos de cada empresa:

```sql
CREATE TABLE secciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT TRUE
);

CREATE TABLE familias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    id_seccion INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_seccion) REFERENCES secciones(id)
);

CREATE TABLE subfamilias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    descripcion TEXT,
    id_familia INTEGER NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_familia) REFERENCES familias(id)
);
```

## Integración con Artículos

El modelo `Articulo` ya tiene los campos para relacionarse con las divisiones:
```python
class Articulo(Base):
    id_seccion: Mapped[Optional[int]]
    id_familia: Mapped[Optional[int]]
    id_subfamilia: Mapped[Optional[int]]
```

## Testing

Para probar el módulo en aislamiento:
```python
# Ejecutar desde la raíz del proyecto
python -c "
from modules.articulos.divisiones_view import DivisionesView
from PySide6.QtWidgets import QApplication
import sys

app = QApplication(sys.argv)
dialog = DivisionesView()
dialog.show()
sys.exit(app.exec())
"
```

## Notas Técnicas

- **Base de datos por empresa**: Las tablas se crean en la BD de cada empresa, no en `creative_erp_main`
- **Session management**: El repository usa `get_session()` que automáticamente usa la BD de la empresa activa
- **Importaciones circulares**: Se evitan importando `Base` desde `core.db` en lugar de `core.models`
