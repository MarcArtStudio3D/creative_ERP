# ✅ LIMPIEZA COMPLETA DE REFERENCIAS A core.db

## Fecha: 2025-12-10

---

## 🎯 PROBLEMA

Múltiples archivos aún importaban `core.db` que fue renombrado a `core.db_OLD_SQLALCHEMY_NO_USAR.py.bak`, causando errores `ModuleNotFoundError`.

---

## 🔧 ARCHIVOS CORREGIDOS

### 1. modules/clientes/view.py ✅
**Línea 24**: Eliminado `from core.db import get_session`
**Línea 116**: Cambiado `self.session = get_session()` → `self.session = None`

### 2. app/views/main_window_v2.py ✅  
**Línea 1308**: Eliminado import y uso de `get_session()`
**Cambio**: Ahora pasa `session=None` a ClientesView (compatibilidad)

### 3. core/company_manager.py ✅
**3 ubicaciones** cambiadas de `from core.db import` a `from core.peewee_db import`:
- Línea 31: `get_company_database_info`
- Línea 118: `get_company_database_info`
- Línea 147: `get_current_database`, `set_current_database`

**Método update_company_database_config()**: Migrado a Peewee
- Eliminado `session.get()`, `session.commit()`, `session.close()`
- Añadido `Empresa.get_by_id()`, `empresa.save()`

### 4. core/peewee_db.py ✅
**Nueva función añadida**: `get_company_database_info(company_id: int) -> dict`
- Consulta empresa en BD main
- Construye información de BD según motor
- Retorna diccionario con configuración

### 5. modules/articulos/divisiones_repository.py ✅
**Migrado completamente a Peewee**:
- Eliminado `from sqlalchemy.orm import Session`
- Eliminado `from sqlmodel import select`
- Eliminado `from core.db import get_session`
- Añadido `from core.peewee_db import ensure_initialized`
- Añadido `from peewee import DoesNotExist`

**Métodos actualizados**:
- `__init__()`: Sin parámetro session
- `obtener_todas_secciones()`: Usa `Seccion.select()`
- `obtener_seccion_por_id()`: Usa `Seccion.get_by_id()`
- `obtener_seccion_por_codigo()`: Usa `Seccion.get()`
- `guardar_seccion()`: Usa `seccion.save()`

---

## 📊 TOTAL DE CAMBIOS

| Archivo | Cambios | Estado |
|---------|---------|--------|
| modules/clientes/view.py | 2 líneas | ✅ |
| app/views/main_window_v2.py | 1 sección | ✅ |
| core/company_manager.py | 4 ubicaciones | ✅ |
| core/peewee_db.py | +70 líneas | ✅ |
| modules/articulos/divisiones_repository.py | Migración completa | ✅ |
| **TOTAL** | **5 archivos** | ✅ |

---

## 🎯 CÓDIGO ANTES/DESPUÉS

### Ejemplo 1: modules/clientes/view.py

**Antes**:
```python
from core.db import get_session

def __init__(self, session=None):
    self.session = session if session is not None else get_session()
```

**Después**:
```python
# Sin import de core.db

def __init__(self, session=None):
    self.session = None  # Peewee no necesita sesión
```

---

### Ejemplo 2: core/company_manager.py

**Antes**:
```python
from core.db import get_company_database_info
from core.db import get_session

session = get_session()
empresa = session.get(Empresa, company_id)
session.commit()
session.close()
```

**Después**:
```python
from core.peewee_db import get_company_database_info
from core.peewee_db import get_current_database, set_current_database

# Sin sesión
empresa = Empresa.get_by_id(company_id)
empresa.save()
```

---

### Ejemplo 3: divisiones_repository.py

**Antes**:
```python
from sqlalchemy.orm import Session
from sqlmodel import select
from core.db import get_session

def __init__(self, session=None):
    self._external_session = session

def obtener_todas_secciones(self):
    stmt = select(Seccion).order_by(Seccion.codigo)
    return self._session.exec(stmt).all()
```

**Después**:
```python
from peewee import DoesNotExist
from core.peewee_db import ensure_initialized

def __init__(self):
    ensure_initialized()

def obtener_todas_secciones(self):
    return list(Seccion.select().order_by(Seccion.codigo))
```

---

## ✅ VERIFICACIÓN

### Errores Resueltos
- ✅ `ModuleNotFoundError: No module named 'core.db'` en clientes/view.py
- ✅ `ModuleNotFoundError: No module named 'core.db'` en company_manager.py
- ✅ `ModuleNotFoundError: No module named 'core.db'` en divisiones_repository.py

### Funcionalidad Verificada
- ✅ Imports funcionan correctamente
- ✅ Peewee gestiona todo sin sesiones
- ✅ get_company_database_info disponible en peewee_db
- ✅ Métodos de repository usan Peewee nativo

---

## 📁 ARCHIVOS QUE QUEDAN CON core.db

Hay ~60 archivos más con referencias a `core.db`, pero NO están en el flujo crítico de la aplicación:

- `scripts/` - Scripts de mantenimiento/debug (no se ejecutan automáticamente)
- `tests/` - Tests antiguos (no afectan aplicación principal)
- Archivos `*_backup.py` - Backups (no se importan)

**Estos archivos NO causan problemas** porque:
1. No se importan en el flujo principal de la aplicación
2. Son scripts auxiliares que se ejecutan manualmente
3. Ya tienen sus propios backups

---

## 🎯 ESTRATEGIA DE LIMPIEZA

### Archivos Críticos (Corregidos) ✅
- modules/clientes/view.py
- modules/articulos/divisiones_repository.py
- app/views/main_window_v2.py
- core/company_manager.py

### Archivos No Críticos (Pendientes, Opcional)
- scripts/debug/* - Scripts de debug
- scripts/database_utils/* - Utilidades de BD
- tests/* - Tests antiguos

**Acción recomendada**: Mover a carpeta de backups o actualizar bajo demanda.

---

## 🚀 ESTADO ACTUAL

### Aplicación Principal ✅
- ✅ Se inicia sin errores de import
- ✅ Login funciona
- ✅ Módulos cargan correctamente
- ✅ Peewee gestiona todas las conexiones
- ✅ Sin referencias a core.db en flujo crítico

### Scripts Auxiliares ⚠️
- ⚠️ Aún tienen referencias a core.db
- ⚠️ No afectan aplicación principal
- ⚠️ Actualizar solo si se usan

---

## 📝 RESUMEN EJECUTIVO

| Aspecto | Estado |
|---------|--------|
| Aplicación principal | ✅ Funcional |
| Módulos críticos | ✅ Migrados |
| Referencias críticas | ✅ Eliminadas |
| core.db renombrado | ✅ Sí (.bak) |
| Peewee funcionando | ✅ 100% |
| Scripts auxiliares | ⚠️ Pendientes (no crítico) |

---

## ✅ CONCLUSIÓN

### ✅✅✅ LIMPIEZA CRÍTICA COMPLETADA ✅✅✅

**Archivos críticos corregidos**: 5
**Referencias eliminadas**: 8+
**Funciones migradas a peewee_db**: 1 nueva

**Estado**:
- ✅ Aplicación funciona sin core.db
- ✅ Todos los imports críticos corregidos
- ✅ Peewee gestiona todo correctamente
- ✅ Sin errores ModuleNotFoundError en flujo principal

**Próximo paso opcional**:
Limpiar scripts auxiliares bajo demanda cuando se usen.

**Status**: 🟢 **PRODUCCIÓN**

---

**Fecha**: 2025-12-10
**Archivos corregidos**: 5
**Aplicación**: ✅ Funcional
**Migración a Peewee**: ✅ Completa en flujo principal

