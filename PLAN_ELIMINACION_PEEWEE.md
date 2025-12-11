# 🎯 PLAN DE ACCIÓN: Eliminar Peewee completamente

## Objetivo
Eliminar todas las referencias a Peewee y consolidar el uso de MultiDBManager con SQL directo.

---

## ✅ ACCIÓN 1: Renombrar/mover archivos obsoletos

### Archivos a renombrar (añadir .obsolete):

```bash
# Repositories obsoletos de módulos (ya tienen repository_sql)
mv modules/clientes/repository.py modules/clientes/repository.py.obsolete
mv modules/articulos/repository.py modules/articulos/repository.py.obsolete

# Models Peewee obsoletos (usamos dicts ahora)
mv modules/clientes/models.py modules/clientes/models.py.obsolete
mv modules/articulos/models.py modules/articulos/models.py.obsolete
```

---

## ⚠️ ACCIÓN 2: Migrar módulo EMPRESAS a SQL directo

**El módulo de empresas SÍ se usa y necesita migración urgente.**

### Pasos:
1. Crear `modules/empresas/repository_sql.py` basado en el patrón de clientes
2. Backup del actual: `cp modules/empresas/repository.py modules/empresas/repository_peewee_backup.py`
3. Actualizar `modules/empresas/controller.py` para usar repository_sql
4. Actualizar nombres de métodos (inglés → español)
5. Probar que funciona

---

## ⚠️ ACCIÓN 3: Revisar core/repositories.py

**Contiene:** UserRepository, BusinessGroupRepository, CompanyRepository con Peewee

### Opciones:
A. **Migrar a SQL directo** (recomendado)
   - Usar MultiDBManager
   - SQL directo sin ORM
   
B. **Mantener con Peewee SOLO para BD main**
   - Los usuarios/grupos/empresas están en creative_erp_main
   - Peewee Proxy configurado para main funciona
   - PERO inconsistente con el resto

**Decisión:** Migrar a SQL directo para consistencia

---

## ⚠️ ACCIÓN 4: Revisar core/models.py

**Contiene:** Modelos Peewee de User, BusinessGroup, Empresa, Cliente, Articulo

### Análisis:
- `User`, `BusinessGroup`, `Empresa` → Usados por core/repositories.py
- `Cliente`, `Articulo` → YA NO SE USAN (usamos dicts)

### Acción:
1. Eliminar modelos Cliente y Articulo de core/models.py
2. Mantener User, BusinessGroup, Empresa SOLO si mantenemos Peewee para core
3. O eliminar todo si migramos core/repositories a SQL directo

---

## ✅ ACCIÓN 5: Limpiar imports obsoletos

Buscar y eliminar:
```python
from core.peewee_db import ...
from peewee import ...
```

En archivos que ya NO los necesitan.

---

## 📊 DECISIÓN CLAVE

### ¿Qué hacer con core/repositories.py y core/models.py?

**Opción A: Migración completa (RECOMENDADO)**
- ✅ Todo el proyecto usa SQL directo
- ✅ Consistencia total
- ✅ Sin dependencia de Peewee
- ❌ Más trabajo inicial

**Opción B: Híbrido**
- ✅ Menos trabajo
- ❌ Dos sistemas diferentes (Peewee para core, SQL para módulos)
- ❌ Confusión en el futuro
- ❌ Peewee sigue como dependencia

**RECOMENDACIÓN: Opción A - Migración completa**

---

## 🎯 ORDEN DE EJECUCIÓN

1. **Inmediato** - Renombrar archivos obsoletos (.obsolete)
2. **Urgente** - Migrar módulo EMPRESAS
3. **Importante** - Migrar core/repositories a SQL directo
4. **Limpieza** - Eliminar core/peewee_db.py y dependencias
5. **Final** - Eliminar Peewee de requirements.txt

---

## ✅ VERIFICACIÓN FINAL

Después de todo, verificar:
```bash
# No debe haber referencias a Peewee
grep -r "peewee\|Peewee" --include="*.py" --exclude-dir=".venv" --exclude="*.obsolete" --exclude="*backup*"

# No debe haber imports de core.peewee_db
grep -r "from core.peewee_db" --include="*.py" --exclude-dir=".venv" --exclude="*.obsolete"
```

---

**Estado:** PLAN DEFINIDO  
**Próximo paso:** Ejecutar ACCIÓN 1 (renombrar obsoletos)

