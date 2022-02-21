"""create_main_tables

Revision ID: 3f833b29f554
Revises: 
Create Date: 2022-02-06 17:07:44.064148

"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '3f833b29f554'
down_revision = None
branch_labels = None
depends_on = None


def created_updated_at_trigger() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
        """
    )


def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column("created_at", sa.DateTime,
                  server_default=sa.func.now(), nullable=False, index=indexed),
        sa.Column("updated_at", sa.DateTime,
                  server_default=sa.func.now(), nullable=False, index=indexed),
    )


def create_cleanings_table() -> None:
    op.create_table(
        "cleanings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False, index=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("cleaning_type", sa.Text, nullable=False,
                  server_default="spot_clean"),
        sa.Column("price", sa.Numeric(10, 2), nullable=False),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_cleanings_modtime
        BEFORE UPDATE ON cleanings
        FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.Text, nullable=False),
        sa.Column("email", sa.Text, nullable=False, unique=True),
        sa.Column("email_verified", sa.Boolean, nullable=False,
                  unique=True, server_default="false"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("is_active", sa.Boolean,
                  nullable=False, server_default="false"),
        sa.Column("is_superuser", sa.Boolean,
                  nullable=False, server_default="false"),
        *timestamps()
    )
    op.execute(
        """
        CREATE TRIGGER update_users_modtime
        BEFORE UPDATE ON users
        FOR EACH ROW EXECUTE PROCEDURE update_updated_at_column();
        """
    )


def upgrade() -> None:
    created_updated_at_trigger()
    create_cleanings_table()
    create_users_table()


def downgrade() -> None:
    op.drop_table("cleanings")
    op.drop_table("users")
    op.execute("DROP FUNCTION update_updated_at_column()")
