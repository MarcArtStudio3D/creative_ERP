"""add_tipocliente_tables

Revision ID: bd1e450d06f8
Revises: ebabfdc0ca54
Create Date: 2025-11-24 00:40:55.246439

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bd1e450d06f8"
down_revision: Union[str, Sequence[str], None] = "ebabfdc0ca54"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create tipocliente_def table
    op.create_table(
        "tipocliente_def",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("desc", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )

    # Create tiposubcliente_def table
    op.create_table(
        "tiposubcliente_def",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("id_tipocliente", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("desc", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(
            ["id_tipocliente"],
            ["tipocliente_def.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sqlite_autoincrement=True,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("tiposubcliente_def")
    op.drop_table("tipocliente_def")
