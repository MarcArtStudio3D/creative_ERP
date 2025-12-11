# Fix: Error "No hay empresa activa"

**Fecha:** 2025-12-11  
**Problema:** Al intentar cargar el módulo de clientes, aparece el error "No hay empresa activa. Usa switch_empresa() primero."

---

## 🔍 Diagnóstico

### Síntomas
```
ERROR: Error obteniendo todos los clientes: No hay empresa activa. Usa switch_empresa() primero.
```

Este error ocurría cuando:
1. El usuario hacía login exitoso
2. Se intentaba cargar el módulo de clientes
3. El `ClienteRepository` intentaba ejecutar una consulta SQL
4. El `MultiDBManager` no tenía una empresa activa (`current_empresa_id = None`)

### Causa Raíz

El problema tenía tres partes:

#### 1. Import local de logging que causa UnboundLocalError

**Archivo:** `app/views/login_window_multi.py`  
**Línea:** 636

Había un `import logging` dentro de un bloque `except` en el método `on_login_clicked()`:

```python
except Exception as e:
    import logging  # ❌ ESTO CAUSA UNBOUND LOCAL ERROR
    logging.getLogger(__name__).exception(f"Error verificando permisos: {e}")
```

Python considera que si hay un `import logging` en cualquier parte de una función, `logging` es una variable local de esa función. Por lo tanto, cualquier uso de `logging` **antes** de ese import resulta en `UnboundLocalError`.

**Solución:** Eliminar el import local y usar el `logging` importado globalmente al inicio del archivo.

```python
except Exception as e:
    logging.getLogger(__name__).exception(f"Error verificando permisos: {e}")  # ✅
```

#### 2. Segundo UnboundLocalError al intentar crear logger

**Archivo:** `app/views/login_window_multi.py`  
**Línea:** 656

Debido al import local mencionado arriba, cuando se intentaba crear `logger = logging.getLogger(__name__)` en la línea 656, Python lanzaba `UnboundLocalError` porque aún no se había ejecutado el `import logging` de la línea 636.

#### 3. Soporte incompleto para diccionarios vs objetos

El código intentaba acceder a `company.id` y `company.nombre_fiscal` asumiendo que `company` era un objeto, pero en realidad era un diccionario devuelto desde la base de datos.

---

## ✅ Solución Implementada

### 1. Eliminación de import local de logging

**Antes:**
```python
except Exception as e:
    import logging  # ❌ Causa UnboundLocalError en todo el método
    logging.getLogger(__name__).exception(f"Error verificando permisos: {e}")
```

**Después:**
```python
except Exception as e:
    # Usar logging ya importado globalmente
    logging.getLogger(__name__).exception(f"Error verificando permisos: {e}")
```

**Cambio crítico:** Eliminar el `import logging` local que causaba que Python tratara `logging` como variable local en todo el método.

### 2. Corrección del UnboundLocalError en configuración de empresa

**Antes:**
```python
try:
    # ... código ...
    logging.getLogger(__name__).info("✅ Base de datos configurada...")  # ❌ UnboundLocalError
except Exception as e:
    logging.getLogger(__name__).exception(f"❌ Error: {e}")  # ❌ UnboundLocalError
```

**Después:**
```python
logger = logging.getLogger(__name__)
try:
    # ... código ...
    logger.info("✅ Base de datos configurada para empresa: %s", company_name)
except Exception as e:
    logger.exception("❌ Error configurando empresa: %s", e)
    from core.ui_helpers import show_warning
    show_warning(self, self.tr("Error"), self.tr(f"Error al configurar empresa: {str(e)}"))
    return  # CRÍTICO: No continuar si falla
```

**Cambios:**
- Crear variable `logger` al principio (ahora funciona porque eliminamos el import local)
- Agregar `return` explícito en el bloque `except` para no emitir la señal si falla
- Mejorar manejo de errores con mensaje al usuario

### 3. Soporte correcto para diccionarios

**Antes:**
```python
company_id = company.id
company_name = company.nombre_fiscal
```

**Después:**
```python
company_id = company.get("id") if isinstance(company, dict) else company.id
company_name = company.get("nombre_fiscal") if isinstance(company, dict) else company.nombre_fiscal
```

### 4. Logging adicional para depuración

**En `company_manager.py`:**
```python
logging.getLogger(__name__).debug(f"Intentando registrar empresa {company_id} en MultiDBManager...")
db_manager.register_empresa(company_id, db_config)
logging.getLogger(__name__).debug(f"✓ Empresa {company_id} registrada")

logging.getLogger(__name__).debug(f"Cambiando a empresa activa: {company_id}")
db_manager.switch_empresa(company_id)
logging.getLogger(__name__).debug(f"✓ Cambiado a empresa {company_id}, current_empresa_id={db_manager.current_empresa_id}")
```

---

## 📊 Flujo Correcto

1. **Usuario hace login** → `LoginWindowMultiCompany.on_login_clicked()`
2. **Autenticación exitosa** → `try_login()` retorna sesión válida
3. **Verificación de permisos** → Usuario autorizado para grupo/empresa
4. **Configuración de empresa:**
   - Obtener ID y nombre de empresa desde dict/objeto
   - Llamar `company_manager.select_company(company_id)`
   - `MultiDBManager.register_empresa()` → Registra configuración de BD
   - `MultiDBManager.switch_empresa()` → Activa empresa (`current_empresa_id = company_id`)
   - Log de confirmación
5. **Emitir señal de éxito** → `login_successful.emit(context)`
6. **Mostrar ventana principal** → `app.on_login_success()`
7. **Cargar módulo de clientes** → `ClientesView.__init__()`
8. **Consultar clientes** → `ClienteRepository.obtener_todos()`
   - `MultiDBManager` tiene `current_empresa_id = 1` ✅
   - Consulta se ejecuta en la BD de la empresa correcta

---

## 🧪 Verificación

Para verificar que el fix funciona:

```bash
# Ejecutar la aplicación
python3 main.py

# Verificar en los logs:
# 1. ✓ MultiDBManager inicializado
# 2. DEBUG: Intentando registrar empresa 1...
# 3. DEBUG: ✓ Empresa 1 registrada
# 4. DEBUG: Cambiando a empresa activa: 1
# 5. DEBUG: ✓ Cambiado a empresa 1, current_empresa_id=1
# 6. INFO: ✅ Base de datos configurada para empresa: Artstudio3d
# 7. DEBUG: ClientesController inicializado con SQL directo
# 8. DEBUG: SQL ejecutado: SELECT * FROM clientes...
# 9. (SIN ERROR "No hay empresa activa")
```

---

## 📝 Archivos Modificados

1. **app/views/login_window_multi.py**
   - Corregido UnboundLocalError con logging
   - Agregado soporte para diccionarios en company
   - Mejorado manejo de errores con return explícito

2. **core/company_manager.py**
   - Agregado logging detallado para depuración
   - Verificación de registro y switch de empresa

3. **modules/clientes/view.py**
   - Agregado logging en __init__ para depuración

---

## 🎯 Resultado

✅ El login ahora funciona correctamente  
✅ La empresa se configura antes de cargar las vistas  
✅ Los módulos pueden acceder a la BD de empresa  
✅ No más error "No hay empresa activa"  
✅ Mejor logging para depuración futura

