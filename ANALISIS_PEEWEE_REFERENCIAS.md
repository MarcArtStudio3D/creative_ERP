# 🔍 ANÁLISIS: Referencias a Peewee en el proyecto

## Fecha: 2025-12-11

---

## 📋 Archivos que referencian `core.peewee_db`

### ✅ Ya migrados (usan repository_sql):
- `modules/clientes/repository_sql.py` ✅ SQL directo
- `modules/articulos/repository_sql.py` ✅ SQL directo

### ❌ Archivos obsoletos (no se usan):
- `modules/clientes/repository.py` 📦 (obsoleto, usar repository_sql)
- `modules/articulos/repository.py` 📦 (obsoleto, usar repository_sql)
- `modules/clientes/repository_peewee_backup.py` 📦 (backup)
- `modules/articulos/repository_peewee_backup.py` 📦 (backup)

### ⚠️ NECESITAN MIGRACIÓN:

#### 1. `modules/empresas/repository.py`
**Estado:** Usa `core.peewee_db`
**Líneas:** 11 - `from core.peewee_db import get_current_database, set_current_database`
**Acción:** Migrar a SQL directo con MultiDBManager

#### 2. `core/repositories.py`
**Estado:** Usa `core.peewee_db`
**Líneas:** 10 - `from core.peewee_db import ensure_initialized, get_current_database, set_current_database`
**Acción:** Revisar si todavía se usa, migrar o eliminar

#### 3. `core/models.py`
**Estado:** Define modelos Peewee
**Líneas:** 18 - `from core.peewee_db import database_proxy`
**Acción:** Mantener solo modelos que se usen con Peewee en BD main

#### 4. `modules/clientes/models.py`
**Estado:** Define modelo Cliente con Peewee
**Líneas:** 16 - `from core.peewee_db import database_proxy`
**Acción:** Ya no se usa (usamos dicts), puede eliminarse

#### 5. `modules/articulos/models.py`
**Estado:** Define modelo Articulo con Peewee
**Líneas:** 20 - `from core.peewee_db import database_proxy`
**Acción:** Ya no se usa (usamos dicts), puede eliminarse

#### 6. `modules/articulos/divisiones_repository.py`
**Estado:** Usa `core.peewee_db`
**Líneas:** 11 - `from core.peewee_db import ensure_initialized`
**Acción:** Verificar si se usa, migrar a SQL directo

### 📝 Archivos de test (no críticos):
- `test_final_core_db.py`
- `test_app_imports.py`
- `test_clientes_debug.py`

---

## 🎯 Plan de acción

### Prioridad ALTA (afecta funcionalidad):

1. **Empresas** - Migrar `modules/empresas/repository.py` a SQL directo
   - Crear `modules/empresas/repository_sql.py`
   - Actualizar controller para usar nuevo repository

2. **Core repositories** - Revisar `core/repositories.py`
   - Ver qué se usa realmente
   - Migrar o eliminar según corresponda

3. **Divisiones** - Revisar `modules/articulos/divisiones_repository.py`
   - Ver si se usa
   - Migrar a SQL directo si es necesario

### Prioridad MEDIA (limpieza):

4. **Models obsoletos** - Eliminar modelos Peewee no usados
   - `modules/clientes/models.py` (ya usamos dicts)
   - `modules/articulos/models.py` (ya usamos dicts)

5. **Repositories obsoletos** - Eliminar archivos viejos
   - `modules/clientes/repository.py`
   - `modules/articulos/repository.py`

### Prioridad BAJA (opcional):

6. **Tests** - Actualizar o eliminar tests obsoletos
7. **Backups** - Eliminar backups después de verificar todo

---

## ✅ Verificación necesaria

Antes de eliminar algo, verificar:
1. ¿Se importa este archivo en algún lugar?
2. ¿Hay alguna referencia activa en el código en uso?
3. ¿Está el replacement (repository_sql) funcionando correctamente?

---

## 📊 Estado actual

| Módulo | Repository Viejo | Repository SQL | Controller | Estado |
|--------|-----------------|----------------|------------|--------|
| Clientes | ❌ (obsoleto) | ✅ Funcional | ✅ Actualizado | ✅ LISTO |
| Artículos | ❌ (obsoleto) | ✅ Funcional | ✅ Actualizado | ✅ LISTO |
| Empresas | ⚠️ Peewee activo | ❌ No existe | ⚠️ Sin revisar | ⚠️ PENDIENTE |

---

**Próximos pasos:** Migrar módulo de Empresas siguiendo el mismo patrón que Clientes y Artículos.

