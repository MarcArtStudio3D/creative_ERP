# Arquitectura Modular del Creative ERP

## 📁 Estructura del Proyecto

```
Creative_ERP/
├── core/                    # Núcleo del sistema (compartido por todos los módulos)
│   ├── db.py               # Gestión de base de datos
│   ├── models.py           # Modelos base
│   ├── repositories.py     # Repositorio base (patrón Repository)
│   ├── modules.py          # Sistema de módulos
│   ├── auth.py             # Autenticación y permisos
│   └── invoices.py         # Lógica de facturación (migrar a modules/)
│
├── modules/                 # Módulos funcionales del ERP
│   ├── facturas/           # Módulo de facturas
│   │   ├── __init__.py     # Exportaciones del módulo
│   │   ├── models.py       # Modelos de datos (Factura, LineaFactura)
│   │   ├── repository.py   # Acceso a base de datos
│   │   ├── controller.py   # Lógica de negocio
│   │   └── views.py        # Interfaces gráficas Qt
│   │
│   ├── clientes/           # Módulo de clientes
│   ├── albaranes/          # Módulo de albaranes
│   ├── proveedores/        # Módulo de proveedores
│   ├── articulos/          # Módulo de artículos/productos
│   ├── contabilidad/       # Módulo de contabilidad
│   ├── proyectos/          # Módulo de proyectos (específico creativos)
│   └── usuarios/           # Módulo de gestión de usuarios
│
├── app/                     # Aplicación Qt
│   ├── app.py              # Aplicación principal
│   ├── ui/                 # Archivos .ui originales (Qt Designer)
│   ├── ui_generated/       # Archivos .py generados desde .ui
│   └── views/              # Clases de vistas personalizadas
│
├── xml/                     # Plantillas XML (Facturae, FacturX)
├── packaging/              # Configuración de empaquetado
├── convert_ui.py           # Script para convertir .ui a .py
├── main.py                 # Punto de entrada de la aplicación
└── requirements.txt        # Dependencias Python
```

---

## 🏗️ Arquitectura de Módulos

### Cada módulo sigue el patrón MVC (Model-View-Controller):

#### 1. **models.py** - Modelos de Datos
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Factura:
    id: int
    numero: str
    cliente_id: int
    fecha: datetime
    # ... más campos
```
- Define las **entidades** del módulo
- Usa `@dataclass` para simplificar (similar a structs de C++ con métodos)
- Contiene la lógica de negocio básica (propiedades calculadas, validaciones)

#### 2. **repository.py** - Acceso a Datos
```python
class FacturaRepository(BaseRepository):
    def get_by_id(self, id: int) -> Factura:
        # SQL query
        
    def save(self, factura: Factura) -> Factura:
        # INSERT/UPDATE
```
- Implementa el **patrón Repository**
- Aísla toda la lógica SQL
- Convierte entre filas de BD y objetos Python

#### 3. **controller.py** - Lógica de Negocio
```python
class FacturaController:
    def crear_factura(self, cliente_id: int) -> Factura:
        # Lógica compleja
        
    def emitir_factura(self, factura_id: int):
        # Validaciones, cálculos, etc.
```
- Coordina entre repositorios
- Implementa las reglas de negocio
- Valida operaciones

#### 4. **views.py** - Interfaz Gráfica
```python
from PyQt6.QtWidgets import QMainWindow
from app.ui_generated.ui_factura import Ui_FacturaWindow

class FacturaView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FacturaWindow()
        self.ui.setupUi(self)
        # Conectar señales
```
- Hereda de las clases Qt
- Usa los `.py` generados desde `.ui`
- Conecta señales (eventos) con slots (funciones)

---

## 🔐 Sistema de Permisos

### Roles Predefinidos

| Rol | Descripción | Acceso |
|-----|-------------|--------|
| **ADMIN** | Administrador | Todo el sistema |
| **MANAGER** | Gestor | Todo excepto configuración |
| **ACCOUNTANT** | Contable | Contabilidad y finanzas |
| **SALES** | Comercial | Ventas y clientes |
| **PROJECT_MANAGER** | Gestor proyectos | Proyectos y tiempo |
| **EMPLOYEE** | Empleado | Solo sus proyectos |
| **VIEWER** | Consulta | Solo lectura |

### Permisos por Acción

- `READ` - Ver datos
- `CREATE` - Crear nuevos
- `UPDATE` - Modificar existentes
- `DELETE` - Eliminar
- `ADMIN` - Control total del módulo
- `EXPORT` - Exportar datos
- `IMPORT` - Importar datos
- `PRINT` - Imprimir documentos

### Ejemplo de Uso

```python
from core.auth import AuthenticationManager, User
from core.modules import ModuleManager, Permission

# Login
auth = AuthenticationManager()
session = auth.login("usuario", "contraseña", user_repo)

# Verificar permisos
if session.has_permission("facturas", Permission.CREATE):
    # Crear factura
    pass

# Obtener módulos disponibles para el usuario
module_manager = ModuleManager()
modules = module_manager.get_available_modules(
    session.user.get_effective_permissions()
)

# Construir menú solo con módulos permitidos
for module in modules:
    print(f"- {module.name} ({module.category.value})")
```

---

## 🔄 Flujo de Conversión UI

### 1. Diseñar en Qt Designer
```bash
# Abrir Qt Designer
designer app/ui/factura.ui
```

### 2. Convertir a Python
```bash
# Convertir todos los .ui
python convert_ui.py

# Convertir uno específico
python convert_ui.py app/ui/factura.ui

# Modo watch (reconvierte automáticamente)
python convert_ui.py --watch
```

### 3. Usar en tu vista
```python
from app.ui_generated.ui_factura import Ui_FacturaWindow

class FacturaView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FacturaWindow()
        self.ui.setupUi(self)  # Aplica el UI
        
        # Conectar eventos
        self.ui.btnGuardar.clicked.connect(self.guardar)
    
    def guardar(self):
        # Tu lógica
        pass
```

---

## 📦 Carga Dinámica de Módulos

El sistema carga solo los módulos a los que el usuario tiene acceso:

```python
# En el arranque de la aplicación
from core.modules import AVAILABLE_MODULES, ModuleManager

# Obtener sesión del usuario
session = auth.get_current_session()

# Cargar solo módulos permitidos
module_manager = ModuleManager()
user_modules = module_manager.get_available_modules(
    session.user.get_effective_permissions()
)

# Construir menú dinámicamente
menu = construir_menu(user_modules)
```

---

## 🔗 Dependencias entre Módulos

Los módulos pueden depender de otros:

```python
Module(
    id="facturas",
    name="Facturas",
    dependencies=["clientes", "articulos"]  # Necesita estos módulos
)
```

El sistema verifica que las dependencias estén disponibles antes de cargar un módulo.

---

## 🚀 Ventajas de esta Arquitectura

### 1. **Modularidad**
- Cada módulo es independiente
- Puedes desarrollar/testear módulos por separado
- Fácil añadir nuevos módulos

### 2. **Seguridad**
- Control granular de permisos
- Los usuarios solo ven lo que pueden usar
- Auditoría de acciones por usuario

### 3. **Escalabilidad**
- Añadir funcionalidades sin romper lo existente
- Módulos pueden tener diferentes velocidades de desarrollo

### 4. **Mantenibilidad**
- Código organizado por funcionalidad
- Fácil localizar bugs
- Separación clara de responsabilidades

### 5. **Migración desde C++**
- Puedes migrar un módulo a la vez
- La estructura es similar a Qt/C++
- Los `.ui` son compatibles

---

## 🎯 Próximos Pasos

1. **Migrar módulos** desde tu proyecto C++
2. **Crear las tablas** de base de datos para cada módulo
3. **Implementar controladores** con la lógica de negocio
4. **Diseñar vistas Qt** y convertirlas
5. **Conectar todo** en la aplicación principal

---

## 📝 Conceptos Python vs C++

| C++ | Python | Descripción |
|-----|--------|-------------|
| `struct` / `class` | `@dataclass` | Estructuras de datos |
| `QObject::connect` | `.connect()` | Señales y slots |
| `.h` y `.cpp` | `.py` | Un solo archivo |
| `nullptr` | `None` | Valor nulo |
| `std::vector` | `list` | Listas dinámicas |
| `std::map` | `dict` | Diccionarios |
| `enum class` | `Enum` | Enumeraciones |
| `QString` | `str` | Cadenas de texto |
| Punteros | Referencias | Python gestiona memoria automáticamente |

---

¿Alguna duda sobre la arquitectura? ¡Pregunta lo que necesites! 🚀
