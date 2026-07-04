"""add stage scoring rules

Revision ID: 5b8c2327106d
Revises: 52b20ff59887
Create Date: 2026-07-04 12:16:25.613833

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5b8c2327106d'
down_revision: Union[str, Sequence[str], None] = '52b20ff59887'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table(
        "stage_scoring_rules",
        sa.Column("rule_id", sa.Integer(), primary_key=True, index=True),
        sa.Column("stage", sa.String(), nullable=False, unique=True),
        sa.Column("exact_score_points", sa.Integer(), nullable=False),
        sa.Column("winner_diff_points", sa.Integer(), nullable=False),
        sa.Column("winner_only_points", sa.Integer(), nullable=False),
        sa.Column("qualified_team_points", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    stage_scoring_rules_table = sa.table(
        "stage_scoring_rules",
        sa.column("stage", sa.String),
        sa.column("exact_score_points", sa.Integer),
        sa.column("winner_diff_points", sa.Integer),
        sa.column("winner_only_points", sa.Integer),
        sa.column("qualified_team_points", sa.Integer),
        sa.column("is_active", sa.Boolean),
    )

    op.bulk_insert(
        stage_scoring_rules_table,
        [
            {
                "stage": "مرحله گروهی",
                "exact_score_points": 12,
                "winner_diff_points": 8,
                "winner_only_points": 4,
                "qualified_team_points": 0,
                "is_active": True,
            },
            {
                "stage": "1/32 نهایی",
                "exact_score_points": 12,
                "winner_diff_points": 8,
                "winner_only_points": 4,
                "qualified_team_points": 3,
                "is_active": True,
            },
            {
                "stage": "1/8 نهایی",
                "exact_score_points": 16,
                "winner_diff_points": 10,
                "winner_only_points": 5,
                "qualified_team_points": 4,
                "is_active": True,
            },
        ],
    )


def downgrade():

    op.drop_table("stage_scoring_rules")