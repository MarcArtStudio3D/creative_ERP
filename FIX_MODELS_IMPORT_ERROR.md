# Fix: ModuleNotFoundError - modules.articulos.models

**Fecha:** 2025-12-11  
**Error:** `ModuleNotFoundError: No module named 'modules.articulos.models'`

---

## 🔍 Problema

Al intentar cargar el módulo de artículos, aparecía el siguiente error:

```python
from modules.articulos.models import Familia, Seccion, Subfamilia
ModuleNotFoundError: No module named 'modules.articulos.models'
```

### Causa

Durante la migración de Peewee/SQLAlchemy a SQL directo con `MultiDBManager`, se eliminaron los archivos `models.py` de los módulos porque ya no se necesitan modelos ORM. Sin embargo, `divisiones_controller.py` todavía intentaba importar las clases `Familia`, `Seccion`, y `Subfamilia`.

---

## ✅ Solución

### Cambios en `modules/articulos/divisiones_controller.py`

**1. Eliminado import de modelos inexistentes:**

**Antes:**
```python
from modules.articulos.models import Familia, Seccion, Subfamilia
```

**Después:**
```python
# Import eliminado - ya no se usan modelos ORM
```

**2. Actualizado tipos a Dict:**

**Antes:**
```python
def obtener_todas_secciones(self) -> List[Seccion]:
def seleccionar_seccion(self, seccion: Optional[Seccion]) -> List[Familia]:
self.seccion_actual: Optional[Seccion] = None
```

**Después:**
```python
def obtener_todas_secciones(self) -> List[Dict]:
def seleccionar_seccion(self, seccion: Optional[Dict]) -> List[Dict]:
self.seccion_actual: Optional[Dict] = None
```

**3. Cambio de acceso a propiedades de objeto a diccionario:**

**Antes:**
```python
if seccion:
    return self.repository.obtener_familias_por_seccion(seccion.id)

if self.seccion_actual.codigo != codigo:
    # ...
```

**Después:**
```python
if seccion:
    return self.repository.obtener_familias_por_seccion(seccion['id'])

if self.seccion_actual['codigo'] != codigo:
    # ...
```

**4. Creación de datos como dict en lugar de objetos:**

**Antes:**
```python
seccion = Seccion(codigo=codigo, seccion=nombre)
self.repository.guardar_seccion(seccion)
```

**Después:**
```python
seccion_data = {'codigo': codigo, 'seccion': nombre}
self.repository.guardar_seccion(seccion_data)
```

---

## 📊 Cambios Aplicados

### Tipos actualizados:
- `Seccion` → `Dict`
- `Familia` → `Dict`
- `Subfamilia` → `Dict`

### Acceso a propiedades:
- `.id` → `['id']`
- `.codigo` → `['codigo']`
- `.seccion` → `['seccion']`
- `.familia` → `['familia']`
- `.subfamilia` → `['subfamilia']`
- `.id_seccion` → `['id_seccion']`
- `.id_familia` → `['id_familia']`

### Creación de entidades:
- `Seccion(...)` → `{'codigo': ..., 'seccion': ...}`
- `Familia(...)` → `{'codigo': ..., 'familia': ..., 'id_seccion': ...}`
- `Subfamilia(...)` → `{'codigo': ..., 'subfamilia': ..., 'id_familia': ...}`

---

## 🧪 Verificación

```bash
# Verificar que el módulo se importa correctamente
python3 -c "from modules.articulos.divisiones_controller import DivisionesController; print('✅ OK')"

# Resultado:
# ✅ OK
```

---

## 📝 Archivos Modificados

1. **modules/articulos/divisiones_controller.py**
   - ✅ Eliminado import de `modules.articulos.models`
   - ✅ Actualizado tipos de `Seccion/Familia/Subfamilia` a `Dict`
   - ✅ Cambiado acceso de propiedades objeto (`.id`) a diccionario (`['id']`)
   - ✅ Actualizada creación de entidades de objetos a dicts
   - ✅ Eliminado código duplicado (archivo tenía 618 líneas, reducido a 355)

2. **modules/articulos/divisiones_view.py**
   - ✅ Cambiado acceso a propiedades en `_cargar_secciones()`: `seccion.codigo` → `seccion['codigo']`
   - ✅ Cambiado acceso a propiedades en `_cargar_familias()`: `familia.codigo` → `familia['codigo']`
   - ✅ Cambiado acceso a propiedades en `_cargar_subfamilias()`: `subfamilia.codigo` → `subfamilia['codigo']`
   - ✅ Actualizado `_on_seccion_selected()`, `_on_familia_selected()`, `_on_subfamilia_selected()`
   - ✅ Actualizado `_on_seccion_clicked()`, `_on_familia_clicked()`, `_on_subfamilia_clicked()`
   - ✅ Actualizado restauración de selecciones en `_on_add_familia()`, `_on_add_subfamilia()`
   - ✅ Actualizado restauración de datos en `_on_borrar_familia()`, `_on_borrar_subfamilia()`
   - ✅ Actualizado `_actualizar_arbol()` para usar acceso a diccionario
   - **Total: 20+ cambios de acceso objeto → diccionario**

---

## 🎯 Resultado

✅ No más `ModuleNotFoundError`  
✅ Controller usa diccionarios en lugar de modelos ORM  
✅ Compatible con SQL directo y `MultiDBManager`  
✅ Código más simple y mantenible  
✅ Sin dependencias de ORM

---

## 📚 Patrón MVC con SQL Directo

Este fix completa la migración del patrón:

```
Vista (divisiones_view.py)
    ↓
Controller (divisiones_controller.py) ← Usa Dict en lugar de modelos
    ↓
Repository (divisiones_repository.py) ← Ejecuta SQL directo
    ↓
MultiDBManager ← Gestiona conexiones multi-empresa
```

**Ventajas:**
- ✅ Código más simple
- ✅ Sin problemas de sesiones/contextos ORM
- ✅ SQL visible y optimizable
- ✅ Cambio fluido entre bases de datos
- ✅ Sin overhead de mapeo objeto-relacional

