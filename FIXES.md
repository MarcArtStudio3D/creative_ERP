# Correcciones Realizadas al Proyecto

## Problemas Encontrados (ChatGPT)

El código generado por ChatGPT tenía **errores graves de sintaxis Python**:

### 1. **Indentación Incorrecta** 
Python usa espacios/tabs para bloques de código (no llaves `{}` como C++).

**INCORRECTO:**
```python
def run_app():
app = QtWidgets.QApplication(sys.argv)  # ❌ Sin indentación
window = MainWindow()
```

**CORRECTO:**
```python
def run_app():
    app = QtWidgets.QApplication(sys.argv)  # ✅ 4 espacios
    window = MainWindow()
```

### 2. **Clases sin Indentación**
```python
class MainWindow(QMainWindow):
def __init__(self):  # ❌ Debería estar indentado
super().__init__()
```

**CORRECTO:**
```python
class MainWindow(QMainWindow):
    def __init__(self):  # ✅
        super().__init__()
```

### 3. **Imports Relativos Rotos**
```python
from .views.main_window import MainWindow  # Error si no hay __init__.py
```

### 4. **Nombre de Archivo Incorrecto**
- `main-window.py` ❌ → `main_window.py` ✅
- Python usa guiones bajos (`_`), no guiones (`-`) en nombres de archivo

---

## Soluciones Aplicadas

### ✅ 1. Corregida la indentación en todos los archivos
- `app/app.py`
- `app/views/main_window.py` (renombrado desde `main-window.py`)
- `core/db.py`
- `core/models.py`
- `core/repositories.py`
- `core/invoices.py`

### ✅ 2. Creados archivos `__init__.py`
Python necesita estos archivos para reconocer directorios como paquetes:
```
app/__init__.py
app/views/__init__.py
core/__init__.py
modules/__init__.py
```

### ✅ 3. Configurado entorno virtual correctamente
```bash
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
pip install -r requirements.txt
```

### ✅ 4. Configurado VS Code para usar el venv
- Seleccionado intérprete: `.venv/bin/python`
- Pylance ahora reconoce las dependencias instaladas

### ✅ 5. Añadidas relaciones bidireccionales en modelos SQLAlchemy
```python
class Invoice(Base):
    client = relationship('Client', back_populates='invoices')
    lines = relationship('InvoiceLine', back_populates='invoice')  # Añadido

class InvoiceLine(Base):
    invoice = relationship('Invoice', back_populates='lines')  # Añadido
```

### ✅ 6. Mejorados los repositorios
- Añadido manejo correcto de sesiones con `try/finally`
- Añadidos métodos `get_by_id()`
- Documentación con docstrings

---

## Diferencias Python vs C++ (Recordatorio)

| Concepto                      | C++                       | Python                        |
|-------------------------------|---------------------------|-------------------------------|
| **Bloques**                   | `{ }`                     | Indentación (4 espacios)      |
| **Declaración de tipos**      | `int x = 5;`              | `x = 5` (tipado dinámico)     |
| **Punteros**                  | `Cliente* c`              | `c` (referencias automáticas) |
| **Includes/Imports**          | `#include "header.h"`     | `from module import Class`    |
| **Constructor**               | `MainWindow()`            | `def __init__(self)`          |
| **Herencia**                  | `: public QMainWindow`    | `class A(B):`                 |
| **NULL**                      | `nullptr`                 | `None`                        |
| **Strings**                   | `QString`                 | `str` (nativo)                |
| **Listas**                    | `std::vector<T>`          | `list`                        |
| **Diccionarios**              | `std::map<K,V>`           | `dict`                        |

---

## Estado Actual del Proyecto

### ✅ Funcionando
- Entorno virtual configurado
- Todas las dependencias instaladas
- Sin errores de sintaxis
- La aplicación arranca correctamente
- Muestra ventana principal con botón "Nueva factura"

### 🚧 Pendiente (según arquitectura diseñada)
- Migrar módulos desde C++ (facturas, clientes, etc.)
- Crear esquema de base de datos
- Implementar login y sistema de permisos
- Diseñar interfaces en Qt Designer
- Implementar lógica de negocio en controladores

---

## Comandos Útiles

### Entorno Virtual
```bash
# Activar venv
source .venv/bin/activate

# Desactivar
deactivate

# Instalar paquete
.venv/bin/python -m pip install nombre_paquete

# Ver paquetes instalados
.venv/bin/python -m pip list
```

### Ejecutar Aplicación
```bash
# Con venv activado
python main.py

# Sin activar venv
.venv/bin/python main.py
```

### Convertir UI
```bash
# Convertir todos los .ui
python convert_ui.py

# Modo watch (reconvierte al guardar en Qt Designer)
python convert_ui.py --watch
```

### Base de Datos
```bash
# Inicializar BD (cuando esté implementado)
.venv/bin/python -c "from core.db import init_db; init_db()"
```

---

## Próximos Pasos Recomendados

1. **Crear esquema de BD** - Ejecutar `init_db()` para crear tablas
2. **Implementar módulo de usuarios** - Login y permisos
3. **Diseñar UI principal** - En Qt Designer → convertir a .py
4. **Migrar un módulo C++** - Empezar por Clientes (el más simple)
5. **Probar CRUD básico** - Crear/leer/actualizar/eliminar clientes

---

**Nota Importante:** En Python, **la indentación es parte de la sintaxis**. Un error de indentación rompe el código. Usa siempre 4 espacios (configura tu editor para convertir tabs a espacios).


## Recursos de iconos (Qt .qrc)


### Estructura de carpetas
```
resources/
icons.qrc
icons/
add.svg
delete.svg
invoice.svg
```


### Archivo icons.qrc
```xml
<RCC>
<qresource prefix="/icons">
<file>add.svg</file>
<file>delete.svg</file>
<file>invoice.svg</file>
</qresource>
</RCC>
```


### Ejemplo de uso en Python
```python
from PySide6.QtGui import QIcon
btn.setIcon(QIcon(":/icons/add.svg"))
```


### Compilación del recurso
```bash
pyside6-rcc resources/icons.qrc -o resources/icons_rc.py
```