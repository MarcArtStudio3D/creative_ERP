"""add_clientes_tipos_table

Revision ID: 3bf5bd205a0f
Revises: bd1e450d06f8
Create Date: 2025-11-24 01:04:02.893558

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3bf5bd205a0f"
down_revision: Union[str, Sequence[str], None] = "bd1e450d06f8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "clientes_tipos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_cliente", sa.Integer(), nullable=False),
        sa.Column("id_tipo", sa.Integer(), nullable=False),
        sa.Column("id_subtipo", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["id_cliente"], ["clientes.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["id_tipo"], ["tipocliente_def.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["id_subtipo"], ["tiposubcliente_def.id"], ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("clientes_tipos")
