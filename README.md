# Migrado a Creative Flow en Kotlin por ser mejor para este proyecto que qt6+Python además de facilitar mucho el multiplataforma usando KMP
# Creative ERP - Sistema Multi-Base de Datos

**Creative ERP** es una aplicación de gestión empresarial desarrollada con Qt6 y Python, que utiliza un sistema avanzado de múltiples bases de datos para una arquitectura escalable y modular.

## 🚀 Características Principales

- **Multi-Base de Datos**: Arquitectura flexible con bases de datos separadas para diferentes módulos
- **Selección Dinámica de Empresa**: Cambio automático de base de datos según empresa seleccionada
- **Interfaz Qt6**: Interfaz de usuario moderna y responsiva con integración completa
- **SQLAlchemy ORM**: Gestión robusta de bases de datos
- **Configuración por Entorno**: Variables de entorno para desarrollo, testing y producción
- **Módulos Independientes**: Clientes, facturas, contabilidad, etc.
- **Soporte Multi-Idioma**: Español y Francés
- **Generación XML**: FacturaE y Factur-X

## 🗄️ Arquitectura de Bases de Datos

### Bases de Datos Disponibles

1. **`creative_erp_main`** - Base de datos principal
   - `users` - Usuarios del sistema
   - `business_groups` - Grupos empresariales
   - `empresas` - Empresas globales con configuración de BD

2. **`artstudio3d`** - Base de datos específica para ArtStudio3D
   - `clientes` - Clientes específicos
   - `tipocliente_def` - Tipos de cliente
   - `tiposubcliente_def` - Subtipos de cliente
   - `direcciones_alternativas` - Direcciones adicionales

3. **Bases de datos por empresa** - Una BD por empresa según motor configurado
   - MariaDB: `nombre_base_datos_maria_db`
   - PostgreSQL: `nombre_base_datos_postgresql`

### Selección Automática de Base de Datos

El sistema cambia automáticamente de base de datos según la empresa seleccionada:

```python
from core.company_manager import company_manager

# Seleccionar empresa (cambia automáticamente la BD)
success = company_manager.select_company(empresa_id)

# El sistema usa el campo 'motor_base_datos' para elegir MariaDB/PostgreSQL
# Y los campos 'nombre_base_datos_maria_db'/'nombre_base_datos_postgresql'
```

### Configuración de Bases de Datos

```python
from core.db import set_current_database, get_current_database

# Cambiar a base de datos principal
set_current_database('main')

# Cambiar a base de datos ArtStudio3D
set_current_database('artstudio3d')

# Ver base de datos actual
print(get_current_database())
```

### Variables de Entorno

```bash
# Base de datos por defecto
export CREATIVE_ERP_DEFAULT_DB=main

# URLs específicas de bases de datos
export CREATIVE_ERP_MAIN_DB=mysql+pymysql://user:pass@host/db_main
export ARTSTUDIO3D_DB=mysql+pymysql://user:pass@host/artstudio3d
```

## 🖥️ Integración con Qt

### Selección de Empresa en la UI

La aplicación incluye un sistema completo para selección de empresa con cambio automático de BD:

```python
from qt_company_integration_example import CompanySelectionWidget

# Crear widget de selección
company_widget = CompanySelectionWidget()

# Conectar señal de cambio de empresa
company_widget.company_changed.connect(on_company_changed)

# El widget maneja automáticamente:
# - Carga de empresas desde BD principal
# - Validación de configuración de BD
# - Cambio automático de base de datos
# - Logging de operaciones
```

### Ejemplo de Ventana Principal

```python
from qt_company_integration_example import MainWindow

# Crear y mostrar ventana principal
window = MainWindow()
window.show()
```

## ⚙️ Configuración de Entornos

### Generar Variables de Entorno

```bash
# Generar archivos .env para todos los entornos
python setup_environment.py

# Esto crea:
# - .env.development
# - .env.testing
# - .env.production
# - .env.example
```

### Usar Variables de Entorno

```bash
# Copiar archivo apropiado
cp .env.development .env

# O para producción
cp .env.production .env
```

### Configuración por Entorno

- **Development**: Debug activado, logging detallado, BD local
- **Testing**: Configuración de pruebas, BD de test
- **Production**: Configuración optimizada, BD de producción

## 🛠️ Instalación y Configuración

### Prerrequisitos

- Python 3.8+
- MySQL/MariaDB o PostgreSQL
- PySide6 (Qt6 para Python)
- PyMySQL (para MySQL/MariaDB) o psycopg2 (para PostgreSQL)

### Instalación

```bash
# 1. Clonar repositorio
git clone <repository-url>
cd creative_erp

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# o
.venv\Scripts\activate     # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
python setup_environment.py
cp .env.development .env  # o .env.production para producción

# 5. Configurar bases de datos
python create_main_database.py     # Crear BD principal
python create_artstudio3d_database.py  # Crear BD ArtStudio3D

# 6. Ejecutar aplicación
python main.py

# 7. Probar integración Qt (opcional)
python qt_company_integration_example.py
```

### Configuración de Empresas

Después de crear las bases de datos, configurar las empresas en la BD principal:

```python
from core.db import set_current_database, get_session
from core.models import Empresa

set_current_database('main')
session = get_session()

# Crear empresa de ejemplo
empresa = Empresa(
    codigo_empresa="ART001",
    nombre_fiscal="ArtStudio3D S.L.",
    motor_base_datos="mariadb",
    nombre_base_datos_maria_db="artstudio3d",
    host_mariadb="localhost",
    puerto_mariadb=3306,
    usuario_mariadb="erp_user",
    password_mariadb="password",
    activa=1
)

session.add(empresa)
session.commit()
```

## 📁 Estructura del Proyecto

```
creative_erp/
├── README.md
├── requirements.txt
├── main.py                     # Punto de entrada
├── setup_environment.py        # Configuración de variables de entorno
├── qt_company_integration_example.py  # Ejemplo integración Qt
├── .env.example               # Ejemplo de variables de entorno
├── app/                        # Interfaz de usuario Qt6
│   ├── app.py                 # Arranque de la aplicación
│   ├── ui/                    # Archivos UI de Qt Designer
│   └── views/                 # Vistas Python
├── core/                       # Lógica de negocio
│   ├── db.py                  # Gestión de bases de datos
│   ├── models.py              # Modelos SQLAlchemy
│   ├── business.py            # Lógica de negocio
│   ├── config.py              # Configuración de entornos
│   └── company_manager.py     # Gestión de empresas y BD
├── modules/                    # Módulos específicos
│   ├── clientes/              # Gestión de clientes
│   ├── facturas/              # Facturación
│   └── contabilidad/          # Contabilidad
├── scripts/                    # Scripts de utilidad
│   ├── create_main_database.py
│   ├── create_artstudio3d_database.py
│   ├── test_clientes_databases.py
│   └── migrate.py             # Migraciones de BD
├── tests/                      # Tests
│   ├── test_main_database.py
│   └── test_artstudio3d_database.py
├── datos/                      # Datos de ejemplo
├── xml_templates/              # Plantillas XML
└── alembic/                    # Migraciones de BD
    ├── alembic.ini
    ├── env.py
    └── versions/
```

## 🧪 Testing

### Probar Sistema Multi-Base de Datos

```bash
# Probar sistema de cambio entre bases de datos
python test_clientes_databases.py

# Ver ejemplo de uso básico
python ejemplo_bases_datos.py
```

### Probar Base de Datos Específica

```bash
# Probar base de datos principal
python test_main_database.py

# Probar base de datos ArtStudio3D
python test_artstudio3d_database.py
```

### Probar Integración Qt

```bash
# Probar widget de selección de empresa
python qt_company_integration_example.py

# Esto abre una ventana Qt con:
# - Lista de empresas disponibles
# - Validación de configuración de BD
# - Cambio automático de base de datos
# - Logging de operaciones
```

### Probar Gestión de Empresas

```python
from core.company_manager import company_manager

# Listar empresas
companies = company_manager.get_available_companies()
print(f"Empresas disponibles: {len(companies)}")

# Seleccionar empresa
if companies:
    success = company_manager.select_company(companies[0]['id'])
    print(f"Selección exitosa: {success}")
```

## 📚 Uso Programático

### Operaciones Básicas con Múltiples Bases de Datos

```python
from core.db import set_current_database, get_session
from modules.clientes.models import Cliente

# Cambiar a base de datos ArtStudio3D
set_current_database('artstudio3d')

# Obtener sesión
session = get_session()

# Consultar clientes
clientes = session.query(Cliente).all()

# Cerrar sesión
session.close()
```

### Gestión de Empresas y Bases de Datos

```python
from core.company_manager import company_manager

# Obtener lista de empresas
companies = company_manager.get_available_companies()
for company in companies:
    print(f"Empresa: {company['codigo']} - {company['nombre']}")

# Seleccionar empresa (cambia automáticamente la BD)
if companies:
    success = company_manager.select_company(companies[0]['id'])
    if success:
        # La BD ya está configurada para esta empresa
        from core.db import get_session
        session = get_session()
        # Realizar operaciones en la BD de la empresa
        session.close()
```

### Context Manager para Bases de Datos

```python
from contextlib import contextmanager
from core.db import set_current_database, get_current_database

@contextmanager
def usar_base_datos(db_name):
    db_actual = get_current_database()
    try:
        set_current_database(db_name)
        yield
    finally:
        set_current_database(db_actual)

# Uso
with usar_base_datos('artstudio3d'):
    # Operaciones en ArtStudio3D
    pass
```

### Integración con Qt - Selección de Empresa

```python
from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from core.company_manager import company_manager, setup_company_selection_combo

class MiVentana(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Crear combo de empresas
        self.company_combo = QComboBox()
        setup_company_selection_combo(self.company_combo)
        self.company_combo.currentIndexChanged.connect(self.on_company_changed)

        layout.addWidget(self.company_combo)
        self.setLayout(layout)

    def on_company_changed(self, index):
        company_id = self.company_combo.itemData(index)
        if company_id:
            success = company_manager.select_company(company_id)
            if success:
                print("Empresa seleccionada - BD configurada")
                # Actualizar UI con datos de la nueva empresa
```

### Configuración de Entornos

```python
from core.config import EnvironmentConfig

# Obtener configuración del entorno actual
config = EnvironmentConfig()

# Obtener entorno actual
print(f"Entorno: {config.get_current_env()}")

# Acceder a configuración de BD
main_db_url = config.get_database_url('main')
print(f"URL BD principal: {main_db_url}")

# Configuración personalizada
config.set_custom_config('ui.theme', 'dark')
theme = config.get('ui.theme')
print(f"Tema: {theme}")
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Soporte

Para soporte técnico o preguntas:
- Email: support@creative-erp.com
- Issues: [GitHub Issues](https://github.com/your-repo/issues)


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
