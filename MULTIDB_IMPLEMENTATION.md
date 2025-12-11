# Sistema MultiDBManager - Implementación Completada

## 📋 Resumen

Se ha implementado un **sistema de gestión multi-base de datos SIN ORM** que resuelve todos los problemas que tenías con SQLAlchemy, SQLModel y Peewee.

## ✅ Archivos creados/modificados

### Nuevos archivos creados:
1. **`core/db_manager.py`** - Gestor central de múltiples bases de datos
2. **`core/base_repository.py`** - Clase base para repositorios con SQL directo
3. **`modules/clientes/repository_sql.py`** - Repository de clientes con SQL puro
4. **`modules/articulos/repository_sql.py`** - Repository de artículos con SQL puro ⭐ NUEVO
5. **`test_multidb.py`** - Script de prueba del sistema
6. **`test_articulos_repo.py`** - Script de prueba para artículos ⭐ NUEVO

### Archivos modificados:
1. **`app/app.py`** - Inicializa MultiDBManager al arrancar
2. **`core/company_manager.py`** - Usa MultiDBManager en lugar de Peewee
3. **`modules/clientes/__init__.py`** - Importa el nuevo repository
4. **`modules/articulos/__init__.py`** - Importa el nuevo repository ⭐ NUEVO

### Backups creados:
- `modules/clientes/repository_peewee_backup.py` - Backup del repository antiguo
- `modules/articulos/repository_peewee_backup.py` - Backup del repository antiguo ⭐ NUEVO

---

## 🚀 Ventajas del nuevo sistema

### VS SQLAlchemy/SQLModel/Peewee:

| Característica | ORM tradicional | MultiDBManager |
|----------------|----------------|----------------|
| **Multi-empresa** | ❌ Complejo, requiere sesiones | ✅ Trivial con `switch_empresa()` |
| **Cross-DB queries** | ❌ No soportado | ✅ `ATTACH DATABASE` (SQLite) |
| **Cambio de DB** | ❌ Recrear sesiones/modelos | ✅ Un comando |
| **Debugging** | 🔴 SQL oculto en ORM | 🟢 SQL visible |
| **Performance** | ⚠️ Overhead de mapeo | ✅ SQL directo |
| **Mantenibilidad** | 🔴 Abstracciones complejas | 🟢 Código simple |

---

## 💻 Cómo usar el nuevo sistema

### 1. Inicialización (ya está en `app.py`):

```python
from core.db_manager import init_db_manager

# Configurar BD principal
main_db_config = {
    'type': 'mariadb',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'admin',
    'password': 'admin123',
    'database': 'creative_erp_main'
}

db_manager = init_db_manager(main_db_config)
```

### 2. Registrar y cambiar de empresa:

```python
from core.db_manager import get_db_manager

db_manager = get_db_manager()

# Registrar empresa
db_config = {
    'type': 'mariadb',
    'host': 'localhost',
    'port': 3306,
    'user': 'admin',
    'password': 'admin123',
    'database': 'artstudio3d'
}
db_manager.register_empresa(empresa_id=1, db_config=db_config)

# Cambiar a empresa
db_manager.switch_empresa(1)
```

### 3. Consultas directas:

```python
# Query a BD de empresa actual
clientes = db_manager.fetch_all(
    "SELECT * FROM clientes WHERE activo = %s",
    (1,)
)

# Query a BD principal
empresas = db_manager.fetch_all(
    "SELECT * FROM empresas WHERE activa = %s",
    (1,),
    use_main=True
)

# Insertar
cliente_id = db_manager.insert('clientes', {
    'codigo_cliente': 'CLI-001',
    'nombre_fiscal': 'Cliente Ejemplo',
    'email': 'cliente@example.com'
})

# Actualizar
db_manager.update(
    'clientes',
    {'email': 'nuevo@example.com'},
    where='id = %s',
    params=(cliente_id,)
)
```

### 4. Usando Repositories:

#### Clientes:

```python
from modules.clientes.repository_sql import ClienteRepository

repo = ClienteRepository()

# Obtener todos
clientes = repo.obtener_todos(filtro="García", limit=10)

# Obtener por ID
cliente = repo.obtener_por_id(5)

# Crear
nuevo_cliente = repo.crear({
    'codigo_cliente': 'CLI-123',
    'nombre_fiscal': 'EMPRESA NUEVA SL',
    'cif_nif_siren': 'B12345678',
    'email': 'contacto@empresa.com'
})

# Actualizar
cliente_actualizado = repo.actualizar(5, {
    'email': 'nuevo_email@empresa.com',
    'telefono1': '912345678'
})

# Direcciones alternativas
direcciones = repo.obtener_direcciones(cliente_id=5)
nueva_direccion = repo.crear_direccion({
    'id_cliente': 5,
    'descripcion': 'Almacén principal',
    'direccion1': 'Calle Mayor 123',
    'cp': '28001',
    'poblacion': 'Madrid'
})
```

#### Artículos:

```python
from modules.articulos.repository_sql import ArticuloRepository

repo = ArticuloRepository()

# Obtener todos con paginación
articulos = repo.obtener_todos(
    filtro="tornillo",
    limit=20,
    offset=0,
    order_by="codigo",
    order_dir="ASC"
)

# Contar total
total = repo.contar_todos(filtro="tornillo")

# Obtener por código
articulo = repo.obtener_por_codigo("ART-001")

# Crear artículo
nuevo = repo.crear({
    'codigo': 'ART-999',
    'descripcion_reducida': 'Tornillo M8',
    'precio_venta': 2.50,
    'coste': 1.20,
    'stock_real': 100
})

# Actualizar
actualizado = repo.actualizar(15, {
    'precio_venta': 2.75,
    'stock_real': 150
})

# Navegación
siguiente = repo.obtener_siguiente(current_id=15)
anterior = repo.obtener_anterior(current_id=15)

# Tarifas
tarifas = repo.obtener_tarifas(articulo_id=15)
repo.actualizar_tarifa(tarifa_id=5, {
    'precio': 3.00,
    'porc_dto': 10.0,
    'precio_final': 2.70
})

# Promociones
promociones = repo.obtener_promociones(articulo_id=15)
nueva_promo = repo.crear_promocion({
    'id_articulo': 15,
    'descripcion': 'Oferta Black Friday',
    'precio_oferta': 2.00,
    'fecha_inicio': '2025-11-01',
    'fecha_fin': '2025-11-30'
})

# Secciones, familias, subfamilias
secciones = repo.obtener_secciones()
familias = repo.obtener_familias(id_seccion=3)
subfamilias = repo.obtener_subfamilias(id_familia=5)
```

### 5. Consultas cross-database (solo SQLite):

```python
# Adjuntar otra empresa
db_manager.attach_database(target_empresa_id=2, alias='emp2')

# Query entre dos empresas
cursor = db_manager.execute("""
    SELECT 
        c1.nombre_fiscal as cliente_emp1,
        c2.nombre_fiscal as cliente_emp2
    FROM clientes c1
    JOIN emp2.clientes c2 ON c1.codigo_cliente = c2.codigo_cliente
""")

# Desadjuntar
db_manager.detach_database('emp2')
```

### 6. Transacciones:

```python
# Con context manager
with db_manager.transaction():
    db_manager.insert('clientes', {...})
    db_manager.update('clientes', {...}, 'id = %s', (5,))
    # Auto-commit si no hay excepciones
```

---

## 🔧 Crear nuevos Repositories

Para crear un repository para otro módulo (ej: artículos):

```python
# modules/articulos/repository_sql.py

from core.base_repository import BaseRepository

class ArticuloRepository(BaseRepository):
    
    def obtener_todos(self, filtro: str = "") -> list[dict]:
        sql = "SELECT * FROM articulos WHERE 1=1"
        params = []
        
        if filtro:
            sql += " AND (codigo LIKE %s OR descripcion LIKE %s)"
            filtro_like = f"%{filtro}%"
            params.extend([filtro_like, filtro_like])
        
        return self._fetch_all(sql, tuple(params) if params else None)
    
    def obtener_por_id(self, id: int) -> Optional[dict]:
        return self._fetch_one("SELECT * FROM articulos WHERE id = %s", (id,))
    
    def crear(self, data: dict) -> Optional[dict]:
        articulo_id = self._insert('articulos', data)
        return self.obtener_por_id(articulo_id)
    
    def actualizar(self, id: int, data: dict) -> Optional[dict]:
        self._update('articulos', data, 'id = %s', (id,))
        return self.obtener_por_id(id)
```

---

## 📝 Migrando desde Peewee/SQLAlchemy

### Antes (con Peewee):
```python
# Modelo ORM
from peewee import *

class Cliente(Model):
    nombre = CharField()
    email = CharField()
    
    class Meta:
        database = db_proxy

# Uso
cliente = Cliente.get_by_id(5)
cliente.email = 'nuevo@example.com'
cliente.save()
```

### Ahora (SQL directo):
```python
# Sin modelo, directo a dict
repo = ClienteRepository()

cliente = repo.obtener_por_id(5)
cliente_actualizado = repo.actualizar(5, {
    'email': 'nuevo@example.com'
})
```

---

## 🎯 Próximos pasos recomendados

1. **Probar el sistema**:
   ```bash
   # Prueba general del MultiDBManager
   python3 test_multidb.py
   
   # Prueba específica de artículos
   python3 test_articulos_repo.py
   ```

2. ✅ **Módulo de artículos MIGRADO** - Ya usa SQL directo

3. **Migrar otros módulos** (opcional):
   - `divisiones_repository.py` - Si usa Peewee
   - `proveedores` - Si existe
   - Otros módulos según necesidad

4. **Eliminar código Peewee/SQLAlchemy**:
   - Una vez verificado que todo funciona
   - Borrar archivos `peewee_db.py`, modelos antiguos, etc.

5. **Consultas estadísticas cross-database**:
   - Implementar queries que comparen datos entre empresas
   - Usar `ATTACH DATABASE` para SQLite
   - Para MariaDB, hacer queries separadas y combinar en Python

---

## ❓ Preguntas frecuentes

**Q: ¿Puedo mezclar SQL directo y ORM?**  
A: Sí, pero no es recomendable. Es mejor migrar todo al nuevo sistema.

**Q: ¿Cómo hago JOIN entre tablas?**  
A: Escribe el SQL JOIN normal:
```python
sql = """
    SELECT c.*, d.descripcion
    FROM clientes c
    LEFT JOIN direcciones_alternativas d ON c.id = d.id_cliente
"""
resultados = db_manager.fetch_all(sql)
```

**Q: ¿Cómo valido datos antes de insertar?**  
A: En el repository o controller:
```python
def crear(self, data: dict):
    # Validaciones
    if not data.get('nombre_fiscal'):
        raise ValueError("nombre_fiscal es obligatorio")
    
    # Insertar
    return self._insert('clientes', data)
```

**Q: ¿Funciona con PostgreSQL?**  
A: Sí, solo cambia el tipo en la configuración:
```python
db_config = {
    'type': 'postgresql',  # Nota: requiere instalar psycopg2
    'host': 'localhost',
    ...
}
```

---

## 📞 Soporte

Si encuentras algún problema:
1. Revisa los logs (logging está activado en nivel DEBUG)
2. Verifica que las conexiones a BD funcionen manualmente
3. Comprueba que las tablas existen en las DBs correctas

**¡El nuevo sistema está listo para usar!** 🎉

