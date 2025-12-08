"""
Sistema de gestión de módulos del ERP.

Cada módulo representa una funcionalidad del sistema (facturas, clientes, etc.)
y puede ser habilitado/deshabilitado según los permisos del usuario.
"""

from enum import Enum
from typing import Dict, List, Optional

from PySide6.QtCore import QCoreApplication


class Permission(Enum):
    """
    Permisos disponibles en el sistema.
    Cada permiso controla el acceso a operaciones específicas.
    """

    # Permisos básicos CRUD (Create, Read, Update, Delete)
    READ = "read"  # Ver datos
    CREATE = "create"  # Crear nuevos registros
    UPDATE = "update"  # Modificar registros existentes
    DELETE = "delete"  # Eliminar registros

    # Permisos especiales
    ADMIN = "admin"  # Acceso total al módulo
    EXPORT = "export"  # Exportar datos
    IMPORT = "import"  # Importar datos
    PRINT = "print"  # Imprimir documentos


class ModuleCategory(Enum):
    """Categorías de módulos para organizar el menú."""

    VENTAS = "ventas"
    COMPRAS = "compras"
    ALMACEN = "almacen"
    FINANCIERO = "financiero"
    PROYECTOS = "proyectos"
    ADMINISTRACION = "administracion"


class Module:
    """
    Define un módulo del sistema.

    Cada módulo tiene:
    - Identificador único
    - Nombre visible (traducible)
    - Icono para el menú
    - Permisos requeridos
    - Categoría
    - Dependencias de otros módulos
    """

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        icon: str,
        category: ModuleCategory,
        required_permissions: List[Permission],
        dependencies: Optional[List[str]] = None,
        enabled: bool = True,
    ):
        self.id = id
        self._name = name
        self._description = description
        self.icon = icon
        self.category = category
        self.required_permissions = required_permissions
        self.dependencies = dependencies or []
        self.enabled = enabled

    @property
    def name(self) -> str:
        """Retorna el nombre traducido del módulo."""
        return QCoreApplication.translate("Modules", self._name)

    @property
    def description(self) -> str:
        """Retorna la descripción traducida del módulo."""
        return QCoreApplication.translate("Modules", self._description)


def _tr(text: str) -> str:
    """Helper para traducir strings de módulos."""
    return QCoreApplication.translate("Modules", text)


# Definición de todos los módulos del sistema
AVAILABLE_MODULES = {
    # MÓDULOS DE VENTAS
    "clientes": Module(
        id="clientes",
        name="Clientes",
        description="Gestión de clientes y contactos",
        icon="",
        category=ModuleCategory.VENTAS,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "presupuestos": Module(
        id="presupuestos",
        name="Presupuestos",
        description="Creación de presupuestos",
        icon="",
        category=ModuleCategory.VENTAS,
        required_permissions=[Permission.READ],
        dependencies=["clientes", "articulos"],
    ),
    "albaranes": Module(
        id="albaranes",
        name="Albaranes",
        description="Albaranes de entrega",
        icon="",
        category=ModuleCategory.VENTAS,
        required_permissions=[Permission.READ],
        dependencies=["clientes", "articulos"],
    ),
    "facturas": Module(
        id="facturas",
        name="Facturas",
        description="Emisión y gestión de facturas",
        icon="",
        category=ModuleCategory.VENTAS,
        required_permissions=[Permission.READ],
        dependencies=["clientes", "articulos"],
    ),
    # MÓDULOS DE COMPRAS
    "proveedores": Module(
        id="proveedores",
        name="Proveedores",
        description="Gestión de proveedores",
        icon="",
        category=ModuleCategory.COMPRAS,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "facturas_compra": Module(
        id="facturas_compra",
        name="Facturas de Compra",
        description="Registro de facturas de proveedores",
        icon="",
        category=ModuleCategory.COMPRAS,
        required_permissions=[Permission.READ],
        dependencies=["proveedores", "articulos"],
    ),
    # MÓDULOS DE ALMACÉN
    "articulos": Module(
        id="articulos",
        name="Artículos",
        description="Catálogo de productos y servicios",
        icon="",
        category=ModuleCategory.ALMACEN,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "tarifas_maestras": Module(
        id="tarifas_maestras",
        name="Tarifas maestras",
        description="Gestión de tarifas maestras",
        icon="",
        category=ModuleCategory.ALMACEN,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "almacen": Module(
        id="almacen",
        name="Almacén",
        description="Control de inventario y stock",
        icon="",
        category=ModuleCategory.ALMACEN,
        required_permissions=[Permission.READ],
        dependencies=["articulos"],
    ),
    "divisiones_almacen": Module(
        id="divisiones_almacen",
        name="Secciones Almacén",
        description="Gestión de Secciones, Familias y Subfamilias",
        icon="",
        category=ModuleCategory.ALMACEN,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    # MÓDULOS FINANCIEROS
    "contabilidad": Module(
        id="contabilidad",
        name="Contabilidad",
        description="Asientos contables y balance",
        icon="",
        category=ModuleCategory.FINANCIERO,
        required_permissions=[Permission.READ, Permission.ADMIN],
        dependencies=["facturas", "facturas_compra"],
    ),
    "tesoreria": Module(
        id="tesoreria",
        name="Tesorería",
        description="Gestión de cobros y pagos",
        icon="",
        category=ModuleCategory.FINANCIERO,
        required_permissions=[Permission.READ],
        dependencies=["facturas", "facturas_compra"],
    ),
    # MÓDULOS DE PROYECTOS (específico para creativos)
    "proyectos": Module(
        id="proyectos",
        name="Proyectos",
        description="Gestión de proyectos creativos",
        icon="",
        category=ModuleCategory.PROYECTOS,
        required_permissions=[Permission.READ],
        dependencies=["clientes"],
    ),
    "tiempo": Module(
        id="tiempo",
        name="Control de Tiempo",
        description="Registro de horas trabajadas",
        icon="",
        category=ModuleCategory.PROYECTOS,
        required_permissions=[Permission.READ],
        dependencies=["proyectos"],
    ),
    # MÓDULOS DE ADMINISTRACIÓN
    "empresas": Module(
        id="empresas",
        name="Empresas",
        description="Gestión de empresas y multi-empresa",
        icon="",
        category=ModuleCategory.ADMINISTRACION,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "usuarios": Module(
        id="usuarios",
        name="Usuarios",
        description="Gestión de usuarios y permisos",
        icon="",
        category=ModuleCategory.ADMINISTRACION,
        required_permissions=[Permission.ADMIN],
        dependencies=[],
    ),
    "configuracion": Module(
        id="configuracion",
        name="Configuración",
        description="Configuración general del sistema",
        icon="",
        category=ModuleCategory.ADMINISTRACION,
        required_permissions=[Permission.ADMIN],
        dependencies=[],
    ),
    "informes": Module(
        id="informes",
        name="Informes",
        description="Informes y estadísticas",
        icon="",
        category=ModuleCategory.ADMINISTRACION,
        required_permissions=[Permission.READ],
        dependencies=[],
    ),
    "gestor_modulos": Module(
        id="gestor_modulos",
        name="Gestor Módulos",
        description="Ver módulos y otorgar permisos por rol",
        icon="",
        category=ModuleCategory.ADMINISTRACION,
        required_permissions=[Permission.ADMIN],
        dependencies=[],
    ),
}


class ModuleManager:
    """
    Gestor de módulos del sistema.
    Controla qué módulos están disponibles para cada usuario.
    """

    def __init__(self):
        self._user_modules: Dict[str, List[str]] = {}
        self._user_permissions: Dict[str, Dict[str, List[Permission]]] = {}

    def get_available_modules(
        self, user_permissions: Dict[str, List[Permission]]
    ) -> List[Module]:
        """
        Obtiene los módulos disponibles según los permisos del usuario.

        Args:
            user_permissions: Diccionario {module_id: [permissions]}

        Returns:
            Lista de módulos a los que el usuario tiene acceso
        """
        available = []

        for module_id, module in AVAILABLE_MODULES.items():
            if not module.enabled:
                continue

            # Verificar si el usuario tiene permisos para este módulo
            user_perms = user_permissions.get(module_id, [])

            # Si tiene algún permiso requerido, puede acceder
            if any(perm in user_perms for perm in module.required_permissions):
                available.append(module)

            # Si es admin del módulo, siempre tiene acceso
            elif Permission.ADMIN in user_perms:
                available.append(module)

        return available

    def get_modules_by_category(
        self, modules: List[Module]
    ) -> Dict[ModuleCategory, List[Module]]:
        """
        Agrupa los módulos por categoría para construir el menú.

        Returns:
            Diccionario {categoria: [modulos]}
        """
        categorized = {}
        for module in modules:
            if module.category not in categorized:
                categorized[module.category] = []
            categorized[module.category].append(module)

        return categorized

    def check_dependencies(self, module_id: str, available_modules: List[str]) -> bool:
        """
        Verifica si las dependencias de un módulo están disponibles.

        Args:
            module_id: ID del módulo a verificar
            available_modules: Lista de IDs de módulos disponibles

        Returns:
            True si todas las dependencias están disponibles
        """
        module = AVAILABLE_MODULES.get(module_id)
        if not module:
            return False

        # module.dependencies puede ser None en tipos estáticos; usar lista vacía como fallback
        return all(dep in available_modules for dep in (module.dependencies or []))

    def get_module(self, module_id: str) -> Optional[Module]:
        """Obtiene un módulo por su ID."""
        return AVAILABLE_MODULES.get(module_id)


# Bloque dummy para que lupdate detecte las cadenas traducibles
# Bloque dummy para que lupdate detecte las cadenas traducibles
def _dummy_translations():
    # Nombres de módulos
    QCoreApplication.translate("Modules", "Clientes")
    QCoreApplication.translate("Modules", "Presupuestos")
    QCoreApplication.translate("Modules", "Albaranes")
    QCoreApplication.translate("Modules", "Facturas")
    QCoreApplication.translate("Modules", "Proveedores")
    QCoreApplication.translate("Modules", "Facturas de Compra")
    QCoreApplication.translate("Modules", "Artículos")
    QCoreApplication.translate("Modules", "Almacén")
    QCoreApplication.translate("Modules", "Contabilidad")
    QCoreApplication.translate("Modules", "Tesorería")
    QCoreApplication.translate("Modules", "Proyectos")
    QCoreApplication.translate("Modules", "Control de Tiempo")
    QCoreApplication.translate("Modules", "Empresas")
    QCoreApplication.translate("Modules", "Usuarios")
    QCoreApplication.translate("Modules", "Configuración")
    QCoreApplication.translate("Modules", "Informes")
    QCoreApplication.translate("Modules", "Gestor Módulos")

    # Descripciones
    QCoreApplication.translate("Modules", "Gestión de clientes y contactos")
    QCoreApplication.translate("Modules", "Creación de presupuestos")
    QCoreApplication.translate("Modules", "Albaranes de entrega")
    QCoreApplication.translate("Modules", "Emisión y gestión de facturas")
    QCoreApplication.translate("Modules", "Gestión de proveedores")
    QCoreApplication.translate("Modules", "Registro de facturas de proveedores")
    QCoreApplication.translate("Modules", "Catálogo de productos y servicios")
    QCoreApplication.translate("Modules", "Control de inventario y stock")
    QCoreApplication.translate("Modules", "Secciones Almacén")
    QCoreApplication.translate("Modules", "Asientos contables y balance")
    QCoreApplication.translate("Modules", "Gestión de cobros y pagos")
    QCoreApplication.translate("Modules", "Gestión de proyectos creativos")
    QCoreApplication.translate("Modules", "Registro de horas trabajadas")
    QCoreApplication.translate("Modules", "Gestión de empresas y multi-empresa")
    QCoreApplication.translate("Modules", "Gestión de usuarios y permisos")
    QCoreApplication.translate("Modules", "Configuración general del sistema")
    QCoreApplication.translate("Modules", "Informes y estadísticas")
    QCoreApplication.translate("Modules", "Ver módulos y otorgar permisos por rol")
    QCoreApplication.translate(
        "Modules", "Gestión de Secciones, Familias y Subfamilias"
    )
    QCoreApplication.translate("Modules", "Tarifas maestras")
    QCoreApplication.translate("Modules", "Gestión de tarifas maestras")
