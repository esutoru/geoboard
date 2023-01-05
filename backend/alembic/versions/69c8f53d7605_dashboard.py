"""dashboard

Revision ID: 69c8f53d7605
Revises: 366e560ea3ed
Create Date: 2023-01-05 21:02:12.077550

"""
from typing import Any

import sqlalchemy as sa
from alembic import op
from sqlalchemy import orm
from sqlalchemy.sql import column, insert, table

# revision identifiers, used by Alembic.
revision = "69c8f53d7605"
down_revision = "366e560ea3ed"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    dashboard_table = op.create_table(
        "dashboard",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.Column(
            "temperature_scale",
            sa.Enum("celsius", "fahrenheit", name="temperaturescale"),
            nullable=False,
        ),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_dashboard_id"), "dashboard", ["id"], unique=False)
    # ### end Alembic commands ###

    _generate_dashboards_for_existed_users(dashboard_table)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_dashboard_id"), table_name="dashboard")
    op.drop_table("dashboard")
    # ### end Alembic commands ###


def _generate_dashboards_for_existed_users(dashboard_table: Any) -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for row in session.query(table("user", column("id"))):
        data = {
            "location": "moscow-moscow-city-russia",
            "user_id": row[0],
            "temperature_scale": "celsius",
        }
        session.execute(insert(dashboard_table).values(data))
    session.commit()
