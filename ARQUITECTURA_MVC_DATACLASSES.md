# Arquitectura MVC con Dataclasses (Sin ORM)

**Fecha:** 2025-12-11  
**Implementación:** Dataclasses como Modelos + SQL Directo

---

## 🏗️ Arquitectura Implementada

```
┌─────────────────────────────────────────────────────────┐
│                     VISTA (View)                        │
│  - UI Qt/PySide6                                       │
│  - Maneja eventos de usuario                          │
│  - Muestra datos usando objetos modelo                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 CONTROLADOR (Controller)                │
│  - Lógica de negocio                                   │
│  - Validaciones                                        │
│  - Coordina Model ↔ Repository                        │
│  - Trabaja con objetos Dataclass                      │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                   MODELO (Model)                        │
│  - Dataclasses Python (sin ORM)                       │
│  - Define estructura de datos                         │
│  - Métodos from_dict() / to_dict()                    │
│  - Validación de tipos                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│                 REPOSITORIO (Repository)                │
│  - Acceso a datos (SQL directo)                       │
│  - Convierte Dict → Model                             │
│  - Convierte Model → Dict                             │
│  - Ejecuta queries SQL                                │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│              BASE DE DATOS (Database)                   │
│  - MariaDB / MySQL / SQLite / PostgreSQL              │
│  - Gestionado por MultiDBManager                      │
│  - Sin ORM, SQL puro                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 📦 Modelos Creados

### **1. Módulo Artículos** (`modules/articulos/models.py`)
```python
from modules.articulos.models import Seccion, Familia, Subfamilia, Articulo, Promocion
```

**Modelos:**
- ✅ `Seccion` - Secciones del almacén
- ✅ `Familia` - Familias de productos
- ✅ `Subfamilia` - Subfamilias de productos
- ✅ `Articulo` - Artículos/productos
- ✅ `Promocion` - Promociones de artículos

### **2. Módulo Clientes** (`modules/clientes/models.py`)
```python
from modules.clientes.models import Cliente, DireccionAlternativa
```

**Modelos:**
- ✅ `Cliente` - Datos completos del cliente (80+ campos)
- ✅ `DireccionAlternativa` - Direcciones alternativas de entrega

### **3. Módulo Empresas** (`modules/empresas/models.py`)
```python
from modules.empresas.models import Empresa
```

**Modelos:**
- ✅ `Empresa` - Configuración completa de empresa (150+ campos)

---

## 💻 Uso de los Modelos

### **Ejemplo 1: Repository → Model**

```python
# Repository (divisiones_repository.py)
class DivisionesRepository:
    def obtener_todas_secciones(self) -> List[Seccion]:
        query = "SELECT * FROM secciones ORDER BY codigo"
        rows = self.db.fetch_all(query)  # ← Retorna List[Dict]
        
        # Convertir dicts a objetos Seccion
        return [Seccion.from_dict(row) for row in rows]
    
    def crear_seccion(self, seccion: Seccion) -> int:
        query = "INSERT INTO secciones (codigo, seccion) VALUES (?, ?)"
        # Convertir objeto a dict para SQL
        data = seccion.to_dict()
        return self.db.execute(query, (data['codigo'], data['seccion']))
```

### **Ejemplo 2: Controller → Model**

```python
# Controller (divisiones_controller.py)
class DivisionesController:
    def __init__(self):
        self.repository = DivisionesRepository()
        self.seccion_actual: Optional[Seccion] = None  # ✅ Objeto
    
    def seleccionar_seccion(self, seccion: Optional[Seccion]):
        self.seccion_actual = seccion
        if seccion:
            # ✅ Acceso con atributos, no dict
            logger.debug(f"Sección: {seccion.codigo} - {seccion.seccion}")
    
    def crear_seccion(self, codigo: str, nombre: str) -> bool:
        # ✅ Crear objeto modelo
        nueva = Seccion(id=None, codigo=codigo, seccion=nombre)
        return self.repository.crear_seccion(nueva)
```

### **Ejemplo 3: View → Model**

```python
# View (divisiones_view.py)
def _cargar_secciones(self):
    secciones = self.controller.obtener_todas_secciones()
    
    for seccion in secciones:  # ✅ Cada seccion es un objeto Seccion
        item = QListWidgetItem(
            f"{seccion.codigo} - {seccion.seccion}"  # ✅ Atributos
        )
        item.setData(Qt.UserRole, seccion)  # ✅ Guardar objeto
        self.list_secciones.addItem(item)

def _on_seccion_selected(self, item):
    seccion = item.data(Qt.UserRole)  # ✅ Recuperar objeto
    logger.debug(f"Código: {seccion.codigo}")  # ✅ Atributo
```

---

## 🎯 Ventajas de esta Arquitectura

### **✅ MVC Puro**
- Separación clara de responsabilidades
- Modelos independientes del framework
- Vista solo conoce Controller
- Controller orquesta Model + Repository

### **✅ Type Safety**
```python
# ❌ Con Dict - Error en runtime
cliente['nombre']  # Si escribes mal, falla al ejecutar

# ✅ Con Dataclass - Error en desarrollo
cliente.nombre  # IDE te avisa si está mal
```

### **✅ Autocompletado IDE**
```python
seccion.  # ← IDE muestra: id, codigo, seccion
```

### **✅ Sin ORM**
- SQL directo y visible
- Control total sobre queries
- Sin problemas de sesiones/contextos
- Compatible con MultiDBManager

### **✅ Validación de Datos**
```python
@dataclass
class Cliente:
    nombre_fiscal: str = ""  # ✅ Type hint
    email: Optional[str] = None  # ✅ Puede ser None
    activo: bool = True  # ✅ Valor por defecto
```

### **✅ Conversión Automática**
```python
# Dict → Model
cliente = Cliente.from_dict(row_from_db)

# Model → Dict
data = cliente.to_dict()
db.insert('clientes', data)
```

---

## 📊 Comparación: Dict vs Dataclass

| Característica | Dict | Dataclass |
|---------------|------|-----------|
| **Sintaxis** | `obj['campo']` | `obj.campo` |
| **Type Hints** | ❌ | ✅ |
| **IDE Support** | ❌ | ✅ Autocompletado |
| **Errores** | Runtime | Desarrollo |
| **Validación** | Manual | Automática |
| **MVC** | ⚠️ Mezclado | ✅ Puro |
| **Debugging** | Difícil | Fácil |
| **Documentación** | Implícita | Explícita |

---

## 🔄 Flujo Completo de Datos

### **CREATE (Insertar)**
```python
# 1. Vista captura datos
codigo = self.ui.txtCodigo.text()
nombre = self.ui.txtNombre.text()

# 2. Controller crea modelo
nueva_seccion = Seccion(id=None, codigo=codigo, seccion=nombre)

# 3. Controller llama a repository
success = self.repository.crear_seccion(nueva_seccion)

# 4. Repository convierte a dict y ejecuta SQL
data = nueva_seccion.to_dict()
query = "INSERT INTO secciones (codigo, seccion) VALUES (?, ?)"
db.execute(query, (data['codigo'], data['seccion']))
```

### **READ (Consultar)**
```python
# 1. Repository ejecuta SQL
query = "SELECT * FROM secciones"
rows = db.fetch_all(query)  # ← List[Dict]

# 2. Repository convierte a modelos
secciones = [Seccion.from_dict(row) for row in rows]  # ← List[Seccion]

# 3. Controller retorna modelos
return secciones

# 4. Vista muestra datos
for seccion in secciones:
    print(f"{seccion.codigo} - {seccion.seccion}")
```

### **UPDATE (Actualizar)**
```python
# 1. Vista tiene modelo cargado
seccion = self.seccion_actual  # ← Objeto Seccion

# 2. Vista modifica modelo
seccion.codigo = "NUEVO"
seccion.seccion = "Nombre Nuevo"

# 3. Controller actualiza en BD
self.repository.actualizar_seccion(seccion)

# 4. Repository convierte y ejecuta
data = seccion.to_dict()
query = "UPDATE secciones SET codigo=?, seccion=? WHERE id=?"
db.execute(query, (data['codigo'], data['seccion'], data['id']))
```

---

## 📝 Archivos Creados

1. **modules/articulos/models.py**
   - Seccion, Familia, Subfamilia, Articulo, Promocion
   
2. **modules/clientes/models.py**
   - Cliente, DireccionAlternativa
   
3. **modules/empresas/models.py**
   - Empresa

---

## 🎯 Próximos Pasos

1. ✅ **Modelos creados** en cada módulo
2. ⏭️ **Actualizar repositories** para retornar objetos
3. ⏭️ **Actualizar controllers** para trabajar con objetos
4. ⏭️ **Actualizar views** para usar `.atributo` en lugar de `['clave']`

---

## 🔍 Testing

```python
# Test de conversión
def test_seccion_from_dict():
    data = {'id': 1, 'codigo': 'A', 'seccion': 'Almacén'}
    seccion = Seccion.from_dict(data)
    
    assert seccion.id == 1
    assert seccion.codigo == 'A'
    assert seccion.seccion == 'Almacén'

def test_seccion_to_dict():
    seccion = Seccion(id=1, codigo='A', seccion='Almacén')
    data = seccion.to_dict()
    
    assert data['id'] == 1
    assert data['codigo'] == 'A'
    assert data['seccion'] == 'Almacén'
```

---

## ✨ Resultado Final

✅ **Arquitectura MVC pura**  
✅ **Modelos como Dataclasses**  
✅ **SQL directo (sin ORM)**  
✅ **Type safety completo**  
✅ **Autocompletado IDE**  
✅ **Fácil testing**  
✅ **Código limpio y mantenible**

