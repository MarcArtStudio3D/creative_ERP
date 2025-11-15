# Nueva Aplicación - Creative ERP

## 🎉 ¡Aplicación Rehecha Correctamente!

He reemplazado completamente el código básico de ChatGPT por una **arquitectura profesional y modular**.

---

## ✨ Características Implementadas

### 1. **Sistema de Login** 
- Ventana de login profesional
- Autenticación de usuarios
- 5 usuarios de demostración con diferentes roles

### 2. **Dashboard Modular**
- Vista personalizada según permisos del usuario
- Módulos organizados por categorías:
  - 📊 Ventas
  - 🏪 Compras  
  - 📦 Almacén
  - 💰 Financiero
  - 📁 Proyectos
  - ⚙️ Administración

### 3. **Control de Permisos**
- Cada usuario solo ve los módulos a los que tiene acceso
- Sistema de roles predefinidos
- Permisos granulares (READ, CREATE, UPDATE, DELETE, etc.)

### 4. **Interfaz Profesional**
- Tarjetas de módulos interactivas
- Toolbar con acciones rápidas
- Barra de estado con info del usuario
- Diseño responsive con scroll

---

## 🚀 Cómo Usar

### 1. Ejecutar la Aplicación

```bash
# Asegúrate de tener el venv activado
source .venv/bin/activate

# Ejecutar
python main.py
```

### 2. Login

Se abrirá la ventana de login. Puedes usar:

**Usuarios de Demostración:**

| Usuario | Contraseña | Rol | Acceso |
|---------|-----------|-----|--------|
| `admin` | `admin` | Administrador | ✅ Todos los módulos |
| `manager` | `manager` | Gestor | ✅ Todo excepto configuración |
| `contable` | `contable` | Contable | 💰 Contabilidad y finanzas |
| `ventas` | `ventas` | Ventas | 📊 Clientes, facturas, presupuestos |
| `user` | `user` | Empleado | 📁 Solo proyectos y tiempo |

**Atajo rápido:** Presiona el botón **"Demo"** para login automático como admin.

### 3. Dashboard

Después del login verás:

- **Header** con tu nombre y rol
- **Módulos disponibles** organizados por categorías
- Solo los módulos a los que tienes acceso

### 4. Abrir Módulos

- Haz click en cualquier tarjeta de módulo
- Se mostrará un mensaje (próximamente cargará la vista del módulo)

---

## 📁 Estructura del Código Nuevo

```
app/
├── app.py                      # ✅ Aplicación principal rehecha
│   └── CreativeERPApp          # Clase que gestiona todo el ciclo de vida
│
└── views/
    ├── login_window.py         # ✅ NUEVO - Ventana de login
    └── main_window.py          # ✅ REHECHO - Dashboard modular
```

### Flujo de la Aplicación

```
main.py
  ↓
CreativeERPApp.initialize()
  ↓
  ├─→ init_db()                 # Crea tablas SQLite
  ├─→ AuthenticationManager     # Sistema de autenticación
  └─→ ModuleManager             # Gestor de módulos
  ↓
show_login()
  ↓
LoginWindow (usuarios demo)
  ↓
on_login_success()
  ↓
show_main_window()
  ↓
MainWindow(session, modules)
  ↓
  ├─→ Filtra módulos según permisos
  ├─→ Agrupa por categorías
  └─→ Crea tarjetas interactivas
```

---

## 🎨 Diferencias con la Versión de ChatGPT

| Antes (ChatGPT) | Ahora (Profesional) |
|-----------------|---------------------|
| ❌ Una ventana simple con un botón | ✅ Sistema completo con login |
| ❌ Sin permisos | ✅ Control granular de permisos |
| ❌ Sin usuarios | ✅ 5 usuarios demo con roles |
| ❌ Sin módulos | ✅ 15 módulos organizados |
| ❌ Código hardcoded | ✅ Arquitectura extensible |
| ❌ Sin diseño | ✅ UI profesional con CSS |

---

## 🔧 Qué Falta Implementar

### Corto Plazo
- [ ] Persistencia de usuarios en BD (ahora están hardcoded)
- [ ] Vistas específicas de cada módulo (ahora solo muestran mensaje)
- [ ] Cerrar sesión funcionando completamente
- [ ] Ventana de configuración

### Medio Plazo  
- [ ] Migrar UI desde tu proyecto C++
- [ ] Implementar CRUD de clientes
- [ ] Implementar CRUD de facturas
- [ ] Generación de PDFs
- [ ] Exportación XML (Facturae/FacturX)

### Largo Plazo
- [ ] Todos los módulos funcionales
- [ ] Informes y estadísticas
- [ ] Backup automático
- [ ] Multi-empresa

---

## 📝 Próximos Pasos Recomendados

### 1. **Probar con Diferentes Usuarios**
```bash
# Ejecuta y prueba login con cada usuario para ver
# cómo cambian los módulos disponibles
python main.py
```

### 2. **Migrar una Vista desde C++**
```bash
# Copia un archivo .ui de tu proyecto anterior
cp /ruta/tu/proyecto/cliente.ui app/ui/

# Conviértelo a Python
python convert_ui.py

# El archivo estará en app/ui_generated/ui_cliente.py
```

### 3. **Crear la Primera Vista de Módulo**

Ejemplo para módulo de clientes:

```python
# modules/clientes/views.py
from PySide6.QtWidgets import QMainWindow
from app.ui_generated.ui_cliente import Ui_ClienteWindow

class ClienteView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ClienteWindow()
        self.ui.setupUi(self)
```

Luego modificar `main_window.py`:
```python
def open_module(self, module: Module):
    if module.id == "clientes":
        from modules.clientes.views import ClienteView
        self.cliente_view = ClienteView()
        self.cliente_view.show()
```

### 4. **Persistir Usuarios en BD**

Crear tabla de usuarios en `core/models.py` usando SQLAlchemy
y migrar los usuarios demo a la base de datos.

---

## 🐛 Debugging

### Ver qué módulos carga cada usuario

Modifica `app.py` línea 70 para ver más detalles:

```python
print(f"\n{'='*50}")
print(f"Usuario: {session.user.full_name}")
print(f"Rol: {session.user.role.value}")
print(f"Módulos: {len(available_modules)}")
for mod in available_modules:
    print(f"  - {mod.name} ({mod.id})")
print(f"{'='*50}\n")
```

### Ver permisos de un usuario

```python
perms = session.user.get_effective_permissions()
for module_id, permissions in perms.items():
    print(f"{module_id}: {[p.value for p in permissions]}")
```

---

## 💡 Tips

1. **Botón Demo**: Usa el botón verde "Demo" en el login para entrar rápido como admin

2. **Cambiar de usuario**: Cierra la ventana y vuelve a ejecutar para probar otro usuario

3. **Módulos**: Los módulos están definidos en `core/modules.py` línea 91

4. **Permisos**: Los permisos por rol están en `core/auth.py` línea 130

5. **Estilos**: Los estilos CSS están inline, puedes crear un archivo QSS externo

---

## 📚 Documentación Relacionada

- `ARCHITECTURE.md` - Arquitectura completa del sistema
- `FIXES.md` - Correcciones aplicadas al código de ChatGPT
- `core/modules.py` - Definición de todos los módulos
- `core/auth.py` - Sistema de usuarios y permisos

---

¡La aplicación ahora tiene una base sólida para construir encima! 🚀
