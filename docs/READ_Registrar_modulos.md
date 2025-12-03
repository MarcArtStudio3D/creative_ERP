# Registrar módulos y categorías en Creative_ERP

Este documento explica, paso a paso, cómo registrar un nuevo módulo en el ERP (para que aparezca automáticamente en menús y pueda gestionarse por permisos), y cómo añadir nuevas categorías si es necesario.

Está orientado al repositorio de Creative_ERP y asume que trabajas en la rama de desarrollo local con un entorno virtual activado.

Índice rápido
- Añadir la definición del módulo (core/module_manager.py)
- Añadir las traducciones necesarias (helpers ya incluidos en module_manager)
- Añadir permisos por defecto / roles (role_permissions.json)
- Asegurar que la UI está disponible / compilada (scripts/compile_ui.sh)
- Registrar entradas necesarias en otros lugares (scripts, tests, README)

IMPORTANTE: Registrar un módulo NO crea automáticamente botones ni pantallas — el comportamiento por defecto del sistema es mostrar botones según la lista de módulos disponibles y los permisos del usuario (ModuleManager + role_permissions.json). Si quieres que la pantalla se muestre automáticamente en ciertos menús, asegúrate de que la UI está exportada por el módulo y que `AVAILABLE_MODULES` define la categoría correcta.

---

1) Añadir la definición del módulo
---------------------------------

- Archivo: `core/module_manager.py`
- Paso: Añade una nueva entrada en el diccionario `AVAILABLE_MODULES` con la estructura de `Module(...)` ya existente.

Ejemplo (copiar / adaptar a tu nueva funcionalidad):

```py
"mi_modulo_ejemplo": Module(
    id="mi_modulo_ejemplo",
    name="Nombre visible",
    description="Descripción breve para el menú",
    icon="",  # (opcional) ruta o nombre simbólico
    category=ModuleCategory.ALMACEN,  # u otra categoría disponible
    required_permissions=[Permission.READ],
    dependencies=["articulos"]  # sólo si depende de otros módulos
),
```

Notas:
- `id` debe ser único (snake_case) y coherente con el módulo (ej. `tarifas_maestras`).
- `category` debe estar en `ModuleCategory` — si necesitas una nueva categoría, mira el siguiente apartado.

2) Añadir nuevas categorías (si procede)
----------------------------------------

Si el módulo no encaja en las categorías existentes (VENTAS, COMPRAS, ALMACEN, FINANCIERO, PROYECTOS, ADMINISTRACION), puedes añadir una nueva categoría:

- Archivo: `core/module_manager.py`
- Paso: Añade la nueva entrada en la enumeración `ModuleCategory`.

Ejemplo:

```py
class ModuleCategory(Enum):
    ...
    NUEVA_CATEGORIA = "nueva_categoria"
```

Notas:
- Añadir una categoría nueva tiene impacto en la UI si hay lógica que agrupa módulos por categoría — revisa `ModuleManager.get_modules_by_category()` y la generación del menú.

3) Añadir traducciones de nombre/desc (opcional pero recomendado)
---------------------------------------------------------------

El proyecto contiene un bloque dummy en `core/module_manager.py` para que `lupdate` detecte cadenas traducibles. Para añadir traducciones:

- Añade la cadena en el bloque `_dummy_translations()` para que las herramientas de internacionalización las recojan.
- Después, re-ejecuta el flujo de localización (p. ej. `lupdate`, editar .ts, `lrelease`).

4) Conceder permisos por defecto a roles
---------------------------------------

Si quieres que ciertos roles tengan permiso sobre el nuevo módulo por defecto, añade las entradas en `role_permissions.json`.

Ejemplo (admin completo + employee con CRUD básico):

```json
  "admin": {
    "mi_modulo_ejemplo": ["ADMIN","CREATE","DELETE","EXPORT","IMPORT","PRINT","READ","UPDATE"],
    ...
  },
  "employee": {
    "mi_modulo_ejemplo": ["CREATE","DELETE","READ","UPDATE"],
    ...
  }
```

Notas:
- `role_permissions.json` es el sitio central donde se configuran permisos por rol; modificaciones aquí son un punto de partida, pueden ser extendidas por el gestor de permisos en runtime.

5) Registrar pantallas / UI assets
---------------------------------

Si tu módulo provee una UI `.ui` o recursos, sigue el flujo del proyecto:

- Añade el .ui a `app/ui/` o `modules/<tu_modulo>/` según convenga.
- Asegúrate de que `scripts/compile_ui.sh` incluye la ruta para compilar el .ui y el .qrc (si procede). Revisa cómo está registrado `frmTarifasBase.ui` para reproducir el patrón.

6) Añadir tests
---------------

Es recomendable añadir pruebas unitarias simples:

- Test que compruebe que `AVAILABLE_MODULES` contiene la entrada (similar a `tests/test_module_registration.py`).
- Test que verifique que `ModuleManager.get_module('mi_modulo_ejemplo')` devuelve el objeto correcto y que su `category` es la esperada.

7) Hacer que el módulo aparezca en la UI del menú (comportamiento estándar)
-------------------------------------------------------------------------

El menú se construye de forma dinámica usando `ModuleManager` y los permisos del usuario. Para que el nuevo botón (ej. "Tarifas maestras") aparezca:

- Asegúrate de que `AVAILABLE_MODULES` contiene la definición que agregaste.
- Asegúrate de que el usuario (o el rol por defecto) tiene permiso `READ` para ese módulo (ej. `role_permissions.json`).
- Si la UI del menú filtra por `category` (por ejemplo ALMACEN), asegúrate de que has definido correctamente `ModuleCategory.ALMACEN` o la que corresponda.

8) Ejemplo de flujo completo (pasos terminal)
--------------------------------------------

```bash
# 1. Añadir/editar core/module_manager.py
# 2. Añadir permisos en role_permissions.json
# 3. Añadir modelo / repo / controller / view en modules/<mi_modulo>
# 4. Añadir tests en tests/
git checkout -b feat/register-mi-modulo
git add core/module_manager.py role_permissions.json modules/mi_modulo tests/test_mi_modulo_registration.py
git commit -m "feat(modules): registrar mi_modulo_ejemplo y permisos iniciales"
git push -u origin HEAD
```

9) Recomendaciones y buenas prácticas
------------------------------------

- Mantener coherencia en el id del módulo (snake_case) y el nombre del paquete/module Python.
- Nunca registres un módulo que no esté implementado: primero crea la carpeta `modules/<id>/` con al menos `__init__.py`, `models.py` y/o `view.py` para evitar enlaces rotos en tiempo de ejecución.
- Añade tests pequeños que validen la existencia del módulo y su categoría antes de abrir PR.
- Revisa los permisos en `role_permissions.json` con tu equipo de seguridad / producto antes de dar permisos amplios.

---

Si quieres, puedo:

- Añadir un script de verificación que valide que `AVAILABLE_MODULES` y `role_permissions.json` están sincronizados (IDs presentes en ambos), o
- Crear una plantilla de PR (o *checklist*) para registrar un módulo nueva que incluya todos los pasos (tests, docs, UI wiring, permisos).

¿Quieres que genere el script de verificación o una plantilla PR como siguiente paso? (dímelo en castellano)
