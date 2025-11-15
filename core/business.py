"""
Modelos para la gestión multi-empresa.

Soporta grupos empresariales con múltiples empresas.
Cada empresa tiene su propia contabilidad, clientes, facturas, etc.
Los proyectos pueden ser compartidos entre empresas del mismo grupo.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class BusinessGroup:
    """
    Grupo empresarial.
    
    Un grupo puede contener múltiples empresas que comparten
    ciertos recursos (como proyectos) pero mantienen contabilidades separadas.
    
    Ejemplo: "ArtStudio" contiene "ArtStudio Software" y "ArtStudio Music"
    """
    id: int
    name: str                          # Nombre del grupo (ej: "ArtStudio")
    code: str                          # Código corto (ej: "AS")
    description: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    # Logo del grupo
    logo_path: Optional[str] = None
    
    # Configuración
    default_currency: str = "EUR"
    default_country: str = "ES"        # País principal (ES, FR, etc)


@dataclass
class Company:
    """
    Empresa dentro de un grupo.
    
    Cada empresa tiene su propia identidad fiscal, clientes, facturas, etc.
    pero puede compartir proyectos con otras empresas del grupo.
    
    Ejemplo: 
    - "ARTSTUDIOPRUEBAS" (Software y Diseño 3D)
    - "ArtStudio Music" (Sonido y Música)
    """
    id: int
    group_id: int                      # ID del grupo al que pertenece
    name: str                          # Nombre comercial
    legal_name: str                    # Razón social legal
    
    # Identificación fiscal
    vat_number: str                    # NIF/CIF
    tax_id: str = ""                   # Otros identificadores fiscales
    
    # Dirección
    address: str = ""
    city: str = ""
    postal_code: str = ""
    state: str = ""
    country: str = "ES"
    
    # Contacto
    phone: str = ""
    email: str = ""
    website: str = ""
    
    # Logo e imagen corporativa
    logo_path: Optional[str] = None
    brand_image_path: Optional[str] = None
    
    # Configuración contable
    accounting_start_date: Optional[datetime] = None
    fiscal_year_start: int = 1         # Mes de inicio del ejercicio fiscal (1-12)
    
    # Series de numeración
    invoice_series: str = "A"          # Serie por defecto de facturas
    quote_series: str = "P"            # Serie de presupuestos
    delivery_note_series: str = "ALB"  # Serie de albaranes
    
    # Estado
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    
    # Notas
    notes: str = ""


@dataclass
class CompanyContext:
    """
    Contexto de empresa activo en la sesión.
    
    Cuando un usuario inicia sesión, selecciona:
    - Un grupo empresarial
    - Una empresa dentro de ese grupo
    
    Todos los datos (clientes, facturas, etc) se filtran por esta empresa.
    """
    group: BusinessGroup
    company: Company
    
    def get_invoice_number_prefix(self) -> str:
        """Genera el prefijo para números de factura."""
        return f"{self.company.invoice_series}/{datetime.now().year}/"
    
    def can_share_projects_with(self, other_company_id: int) -> bool:
        """
        Verifica si esta empresa puede compartir proyectos con otra.
        Solo se pueden compartir proyectos dentro del mismo grupo.
        """
        # TODO: Consultar si la otra empresa pertenece al mismo grupo
        return True  # Por ahora siempre true
    
    def __str__(self):
        return f"{self.group.name} - {self.company.name}"


# Funciones helper para trabajar con contextos multi-empresa

def filter_by_company(query, company_id: int):
    """
    Filtra una query de SQLAlchemy por empresa.
    
    Uso:
        companies = filter_by_company(
            db.query(Client), 
            session.company_context.company.id
        ).all()
    """
    return query.filter_by(company_id=company_id)


def get_shared_projects(group_id: int):
    """
    Obtiene proyectos compartidos dentro de un grupo.
    
    Los proyectos pueden ser de una empresa específica o compartidos
    entre varias empresas del mismo grupo.
    """
    # TODO: Implementar consulta de proyectos compartidos
    pass
