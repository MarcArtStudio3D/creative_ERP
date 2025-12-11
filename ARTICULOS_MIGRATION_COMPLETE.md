# ✅ MIGRACIÓN COMPLETADA: Módulo de Artículos

## 🎯 Resumen

El módulo de **Artículos** ha sido completamente migrado de Peewee a **SQL directo** usando MultiDBManager.

---

## 📁 Archivos modificados/creados

### ✅ Creados:
- **`modules/articulos/repository_sql.py`** - Nuevo repository con SQL directo
- **`test_articulos_repo.py`** - Script de prueba del repository

### ✅ Modificados:
- **`modules/articulos/__init__.py`** - Ahora importa `repository_sql`

### 📦 Backup:
- **`modules/articulos/repository_peewee_backup.py`** - Backup del repository antiguo

---

## 🚀 Funcionalidades implementadas

### CRUD básico:
- ✅ `obtener_todos()` - Con paginación, filtros y ordenación
- ✅ `contar_todos()` - Cuenta artículos con filtros
- ✅ `obtener_por_id()` - Obtiene artículo por ID
- ✅ `obtener_por_codigo()` - Obtiene artículo por código
- ✅ `obtener_siguiente()` - Navegación (siguiente artículo)
- ✅ `obtener_anterior()` - Navegación (artículo anterior)
- ✅ `crear()` - Crea nuevo artículo con código auto-generado
- ✅ `actualizar()` - Actualiza artículo existente
- ✅ `eliminar()` - Elimina artículo y relaciones

### Tarifas:
- ✅ `obtener_tarifas()` - Lista tarifas del artículo
- ✅ `actualizar_tarifa()` - Actualiza precio/descuento
- ✅ `crear_tarifas_para_articulo()` - Crea tarifas por defecto

### Promociones:
- ✅ `obtener_promociones()` - Lista promociones del artículo
- ✅ `obtener_promocion_por_id()` - Obtiene promoción específica
- ✅ `crear_promocion()` - Crea nueva promoción
- ✅ `actualizar_promocion()` - Actualiza promoción existente
- ✅ `eliminar_promocion()` - Elimina promoción

### Clasificación (Secciones/Familias/Subfamilias):
- ✅ `obtener_secciones()` - Lista todas las secciones
- ✅ `obtener_familias()` - Lista familias (opcionalmente por sección)
- ✅ `obtener_subfamilias()` - Lista subfamilias (opcionalmente por familia)
- ✅ `obtener_seccion_por_id()` - Obtiene sección específica
- ✅ `obtener_familia_por_id()` - Obtiene familia específica
- ✅ `obtener_subfamilia_por_id()` - Obtiene subfamilia específica

### Proveedores:
- ✅ `obtener_proveedores()` - Lista todos los proveedores

---

## 💻 Ejemplos de uso

### Listar artículos con filtro y paginación:
```python
from modules.articulos.repository_sql import ArticuloRepository

repo = ArticuloRepository()

# Buscar "tornillo" con paginación
articulos = repo.obtener_todos(
    filtro="tornillo",
    limit=20,
    offset=0,
    order_by="codigo",
    order_dir="ASC"
)

# Contar resultados totales
total = repo.contar_todos(filtro="tornillo")
print(f"Encontrados {len(articulos)} de {total} artículos")
```

### Crear artículo con tarifas automáticas:
```python
# Crear artículo
nuevo = repo.crear({
    'codigo': 'ART-999',
    'descripcion_reducida': 'Tornillo hexagonal M8x40',
    'descripcion_ampliada': 'Tornillo hexagonal acero inoxidable M8x40mm',
    'precio_venta': 2.50,
    'coste': 1.20,
    'stock_real': 500,
    'stock_minimo': 100,
    'id_seccion': 3,
    'id_familia': 15,
    'activo': True
})

print(f"Artículo creado con ID: {nuevo['id']}")

# Las tarifas se crean automáticamente
tarifas = repo.obtener_tarifas(nuevo['id'])
print(f"Tarifas creadas: {len(tarifas)}")
```

### Gestionar tarifas:
```python
# Obtener tarifas del artículo
tarifas = repo.obtener_tarifas(articulo_id=15)

for tarifa in tarifas:
    print(f"Tarifa {tarifa['codigo']}: {tarifa['precio']}€")

# Actualizar tarifa
repo.actualizar_tarifa(tarifa_id=5, {
    'precio': 3.00,
    'porc_dto': 10.0,
    'precio_final': 2.70
})
```

### Crear promoción:
```python
# Crear oferta Black Friday
promo = repo.crear_promocion({
    'id_articulo': 15,
    'descripcion': 'Oferta Black Friday 2025',
    'precio_oferta': 1.99,
    'fecha_inicio': '2025-11-25',
    'fecha_fin': '2025-11-30',
    'activa': True
})

print(f"Promoción creada: {promo['descripcion']}")
```

### Navegación entre artículos:
```python
# Artículo actual
articulo_actual = repo.obtener_por_id(100)

# Siguiente artículo
siguiente = repo.obtener_siguiente(articulo_actual['id'])
if siguiente:
    print(f"Siguiente: {siguiente['codigo']}")

# Artículo anterior
anterior = repo.obtener_anterior(articulo_actual['id'])
if anterior:
    print(f"Anterior: {anterior['codigo']}")
```

### Obtener clasificación:
```python
# Listar secciones
secciones = repo.obtener_secciones()
for sec in secciones:
    print(f"Sección: {sec['codigo']} - {sec['seccion']}")

# Familias de una sección
familias = repo.obtener_familias(id_seccion=3)
for fam in familias:
    print(f"  Familia: {fam['codigo']} - {fam['familia']}")

# Subfamilias de una familia
subfamilias = repo.obtener_subfamilias(id_familia=15)
for sub in subfamilias:
    print(f"    Subfamilia: {sub['codigo']} - {sub['subfamilia']}")
```

---

## 🧪 Pruebas

Ejecuta el script de prueba:

```bash
python3 test_articulos_repo.py
```

Este script verifica:
1. ✅ Conexión a MultiDBManager
2. ✅ Registro de empresa
3. ✅ Obtención de artículos con paginación
4. ✅ Conteo de artículos
5. ✅ Obtención por ID
6. ✅ Tarifas del artículo
7. ✅ Promociones del artículo
8. ✅ Secciones/familias/subfamilias
9. ✅ Navegación siguiente/anterior

---

## 📊 Comparativa: Antes vs Ahora

### Antes (con Peewee):
```python
from peewee import DoesNotExist

# Obtener artículo
try:
    articulo = Articulo.get_by_id(15)
    # Convertir modelo a dict
    data = self._model_to_dict(articulo)
except DoesNotExist:
    data = None

# Actualizar
articulo.precio_venta = 2.50
articulo.save()
```

### Ahora (SQL directo):
```python
# Obtener artículo (ya es dict)
articulo = repo.obtener_por_id(15)

# Actualizar
repo.actualizar(15, {'precio_venta': 2.50})
```

**Ventajas:**
- ✅ Código más simple y directo
- ✅ Sin problemas de contexto/sesión
- ✅ SQL visible y optimizable
- ✅ Fácil cambio entre empresas
- ✅ Sin overhead de ORM

---

## 🔄 Integración con Controller

El controller de artículos debe usar el nuevo repository:

```python
# modules/articulos/controller.py

from .repository_sql import ArticuloRepository

class ArticuloController:
    def __init__(self):
        self.repo = ArticuloRepository()
    
    def cargar_articulos(self, page=1, per_page=50, filtro=""):
        offset = (page - 1) * per_page
        articulos = self.repo.obtener_todos(
            filtro=filtro,
            limit=per_page,
            offset=offset
        )
        total = self.repo.contar_todos(filtro=filtro)
        
        return {
            'articulos': articulos,
            'total': total,
            'page': page,
            'pages': (total + per_page - 1) // per_page
        }
```

---

## ✅ Estado final

### Módulos migrados a SQL directo:
- ✅ **Clientes** (`modules/clientes/repository_sql.py`)
- ✅ **Artículos** (`modules/articulos/repository_sql.py`)

### Pendientes (si usan Peewee):
- ⏳ Divisiones (si aplica)
- ⏳ Proveedores (si aplica)
- ⏳ Otros módulos según necesidad

---

## 🎉 Conclusión

El módulo de **Artículos** ahora:
- ✅ Usa SQL directo (sin ORM)
- ✅ Funciona perfectamente con MultiDBManager
- ✅ Soporta multi-empresa sin problemas
- ✅ Es más rápido y fácil de mantener
- ✅ Permite consultas cross-database (SQLite)

**¡La migración está completa y funcionando!** 🚀

