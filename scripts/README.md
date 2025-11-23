# Compilar UI y recursos (scripts)

Breve README de uso para los scripts de compilación del UI y recursos del proyecto.

Descripción
-----------
Este directorio contiene scripts útiles para recompilar los ficheros Qt (.ui y .qrc) y limpiar cachés de Python generados a partir de ellos.

Script principal
----------------
- `compile_ui.sh` — compila los ficheros `app/ui/*.ui` y `app/ui/*.qrc` y aplica algunos parches mínimos para que los módulos de recursos queden importables desde el paquete `modules`.

Qué hace exactamente
---------------------
- Compila los recursos (fichero `.qrc`) con `pyside6-rcc` y genera `modules/<basename>_rc.py`.
- Recompila todos los `ui_*.py` encontrados re-interpretando la cabecera del fichero para encontrar el `.ui` de origen.
- Parchea las importaciones de `designer_rc` (y similares) para hacer `from modules import designer_rc`, evitando errores cuando el `ui_*.py` genera una importación de recurso no resoluble.
- Limpia caches: borra `__pycache__` y `*.pyc` (excluyendo `.venv`) antes de compilar para evitar referencias antiguas en archivos compilados.

Requisitos previos
------------------
- Tener el entorno virtual creado e instalado con `pip install -r requirements.txt` (el script intenta usar las herramientas desde `.venv/bin/pyside6-uic` y `.venv/bin/pyside6-rcc`).
- Herramientas: `pyside6-uic`, `pyside6-rcc` disponibles.

Uso básico
---------
Desde la raíz del repo:
```bash
cd /home/marc/Documents/Artstudio3D/Creative_ERP
./scripts/compile_ui.sh
```

Uso manual (ejemplos)
---------------------
- Compilar un solo `.ui` manualmente:
```bash
.venv/bin/pyside6-uic --from-imports app/ui/frmClientes.ui -o modules/clientes/ui_clientes.py
```
- Compilar recursos `.qrc` manualmente:
```bash
.venv/bin/pyside6-rcc app/ui/designer.qrc -o modules/designer_rc.py
```

Notas y recomendaciones
-----------------------
- El script reescribe `ui_*.py` y `modules/*_rc.py` (generados): si prefieres no versionar estos ficheros, asegúrate de añadirlos al `.gitignore` o de seguir la política del proyecto.
- Si tu IDE/generador vuelve a crear `import designer_rc` en lugar de `from modules import designer_rc`, recompila con `--from-imports` y ejecuta el script para parchearlo.
- El script no actualmente gestiona otros recursos (p. ej., `maya_rc`) salvo para parchear `designer_rc`. Si aparecen otras referencias, se pueden añadir reglas similares.
- El script borra caché y .pyc dentro del repo para evitar residuos de compilaciones antiguas; excluye la carpeta `.venv`.

CI / Validación
----------------
- Añadimos un workflow de GitHub Actions en `.github/workflows/validate_ui_resources.yml` que realiza:
	1. Instalación de dependencias (pip install -r requirements.txt).
	2. Ejecución de `scripts/compile_ui.sh` para compilar `.qrc` y `.ui`.
	3. Ejecución de `scripts/check_resource_imports.sh` (por defecto comprueba `maya_rc`) y falla si detecta cualquier referencia no deseada.

Uso en CI
--------
El workflow se ejecuta en push/pull_request sobre `main`. Si además quieres detectar otros módulos no deseados, puedes exportar la variable `DISALLOWED_RESOURCE_MODULES` con una lista separada por espacios, por ejemplo:
```bash
DISALLOWED_RESOURCE_MODULES="maya_rc other_rc" ./scripts/check_resource_imports.sh
```

Extensiones que se pueden añadir
------------------------------
- Añadir un `Makefile` con objetivo `ui-compile` que ejecute el script.
- Añadir una comprobación CI (p. ej., GitHub Actions) que ejecute el script y falle si detecta `maya_rc` u otras importaciones no deseadas en los UI generados.

Contacto
--------
Si quieres que integre esto en el flujo del proyecto (Makefile, CI o validaciones adicionales), dímelo y lo implemento.


Para el futuro, cuando modifiques archivos 
.ui
, usa este flujo:

# 1. Compilar UI
./scripts/compile_ui.sh

# 2. Regenerar traducciones (TODO el proyecto)
.venv/bin/pyside6-lupdate . -ts translations/creative_erp_fr.ts -no-obsolete

# 3. Traducir automáticamente
.venv/bin/python scripts/translate_to_french.py translations/creative_erp_fr.ts

# 4. Compilar traducciones
lrelease translations/creative_erp_fr.ts -qm translations/creative_erp_fr.qm