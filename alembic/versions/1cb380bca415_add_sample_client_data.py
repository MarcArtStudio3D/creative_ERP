"""Add sample client data

Revision ID: 1cb380bca415
Revises: 6271f8dcd28d
Create Date: 2025-11-18 14:22:31.454854

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1cb380bca415'
down_revision: Union[str, Sequence[str], None] = '6271f8dcd28d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Insertar clientes de ejemplo
    op.execute("""
        INSERT INTO clients (id, name, email, country, vat_number, address, created_at) VALUES
        (1, 'Empresa Ejemplo SL', 'contacto@empresa-ejemplo.com', 'ES', 'B12345678', 'Calle Mayor 123, Madrid', '2025-01-15 10:00:00'),
        (2, 'Tech Solutions SARL', 'info@techsolutions.fr', 'FR', 'FR12345678901', '15 Rue de la Paix, Paris', '2025-02-01 09:30:00'),
        (3, 'Industria Manufacturera SA', 'ventas@manufacturera.es', 'ES', 'A98765432', 'Polígono Industrial 45, Barcelona', '2025-02-15 11:15:00'),
        (4, 'Consulting Group Ltd', 'hello@consulting.fr', 'FR', 'FR98765432109', '8 Avenue des Champs, Lyon', '2025-03-01 14:20:00'),
        (5, 'Distribuciones Norte SL', 'pedidos@distribuciones.es', 'ES', 'B55566677', 'Calle Comercio 67, Bilbao', '2025-03-10 16:45:00'),
        (6, 'Boutique Mode Paris', 'contact@boutique.fr', 'FR', 'FR11122233344', '22 Boulevard Saint-Germain, Paris', '2025-04-01 12:00:00'),
        (7, 'Construcciones del Sur SA', 'obra@construcciones.es', 'ES', 'A44455566', 'Avenida Andalucia 89, Sevilla', '2025-04-15 08:30:00'),
        (8, 'IT Services Marseille', 'support@itservices.fr', 'FR', 'FR77788899900', '45 Rue de la République, Marseille', '2025-05-01 13:15:00'),
        (9, 'Comercial Valencia SL', 'info@comercialvalencia.es', 'ES', 'B33344455', 'Plaza de la Reina 12, Valencia', '2025-05-20 10:45:00'),
        (10, 'Agence Marketing Toulouse', 'marketing@agence.fr', 'FR', 'FR66677788811', '18 Place du Capitole, Toulouse', '2025-06-01 15:30:00')
    """)

    # Insertar algunas facturas de ejemplo
    op.execute("""
        INSERT INTO invoices (id, number, client_id, date, status, total, currency) VALUES
        (1, 'INV-2025-001', 1, '2025-06-15', 'paid', 1250.50, 'EUR'),
        (2, 'INV-2025-002', 2, '2025-06-20', 'pending', 890.75, 'EUR'),
        (3, 'INV-2025-003', 3, '2025-07-01', 'draft', 2100.00, 'EUR'),
        (4, 'INV-2025-004', 4, '2025-07-05', 'paid', 675.25, 'EUR'),
        (5, 'INV-2025-005', 5, '2025-07-10', 'sent', 445.80, 'EUR')
    """)

    # Insertar líneas de factura de ejemplo
    op.execute("""
        INSERT INTO invoice_lines (id, invoice_id, description, qty, unit_price, vat) VALUES
        (1, 1, 'Desarrollo software personalizado', 40.0, 25.00, 21.0),
        (2, 1, 'Instalación y configuración', 8.0, 15.00, 21.0),
        (3, 2, 'Consultoría técnica mensual', 1.0, 750.00, 20.0),
        (4, 2, 'Licencias software', 5.0, 28.15, 20.0),
        (5, 3, 'Proyecto de automatización industrial', 1.0, 1800.00, 21.0),
        (6, 3, 'Materiales y componentes', 1.0, 300.00, 21.0),
        (7, 4, 'Auditoría de sistemas', 15.0, 35.00, 20.0),
        (8, 4, 'Informe técnico', 1.0, 175.25, 20.0),
        (9, 5, 'Suministro de equipos', 2.0, 180.00, 21.0),
        (10, 5, 'Instalación in situ', 1.0, 85.80, 21.0)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar datos de ejemplo
    op.execute("DELETE FROM invoice_lines")
    op.execute("DELETE FROM invoices")
    op.execute("DELETE FROM clients")
