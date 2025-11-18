# Creative ERP - Estructura de proyecto (Qt6 + Python)
# Archivo único que contiene la estructura inicial y archivos base.
# Guarda cada bloque en su propio archivo según el árbol mostrado.


# Árbol del proyecto
# creative_erp/
# ├─ README.md
# ├─ requirements.txt
# ├─ pyproject.toml
# ├─ setup_build.sh
# ├─ main.py
# ├─ app/
# │ ├─ __init__.py
# │ ├─ app.py # arranque de la app Qt
# │ ├─ resources.qrc # recursos (logos, iconos)
# │ ├─ ui/
# │ │ ├─ main_window.ui
# │ │ └─ invoice_dialog.ui
# │ └─ views/
# │ └─ main_window.py
# ├─ core/
# │ ├─ __init__.py
# │ ├─ db.py # conexion y session SQLAlchemy
# │ ├─ models.py # modelos SQLAlchemy
# │ ├─ repositories.py # acceso a datos
# │ ├─ invoices.py # lógica de facturación (PDF/XML)
# │ └─ taxes.py # reglas fiscales (ES/FR)
# ├─ xml_templates/
# │ ├─ facturae_template.xml.j2
# │ └─ facturx_template.xml.j2
# └─ packaging/
# ├─ pyinstaller.spec
# └─ build_notes.md


"""
Creative ERP - Qt6 + Python


Instrucciones rápidas:
1. Crear entorno virtual: python -m venv .venv
2. Activar: source .venv/bin/activate (Linux/macOS) o .\\.venv\\Scripts\\activate (Windows)
3. pip install -r requirements.txt
4. Configurar base de datos: python scripts/migrate.py upgrade head
5. Ejecutar: python main.py


Estructura del proyecto: app (UI), core (lógica), xml_templates (plantillas XML), packaging.


## Migraciones de Base de Datos

El proyecto utiliza Alembic para gestionar migraciones de base de datos, similar a Laravel o Django.

### Comandos principales:

```bash
# Aplicar todas las migraciones pendientes
python scripts/migrate.py upgrade head

# Ver el estado actual de las migraciones
python scripts/migrate.py current

# Ver el historial de migraciones
python scripts/migrate.py history

# Crear una nueva migración (después de cambiar modelos)
python scripts/migrate.py revision -m "Descripción de los cambios"

# Deshacer la última migración
python scripts/migrate.py downgrade -1
```

### Estructura de migraciones:

- `alembic/versions/` contiene los archivos de migración
- `alembic.ini` configuración de Alembic
- `alembic/env.py` configuración específica del proyecto

Las migraciones se crean automáticamente basándose en los cambios en `core/models.py`.
"""