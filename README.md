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
4. Ejecutar: python main.py


Estructura del proyecto: app (UI), core (lógica), xml_templates (plantillas XML), packaging.
"""