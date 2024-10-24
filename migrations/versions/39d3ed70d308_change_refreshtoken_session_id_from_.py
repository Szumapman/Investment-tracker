"""change RefreshToken session_id from JSON to String

Revision ID: 39d3ed70d308
Revises: 860f6f990daa
Create Date: 2024-10-21 18:14:38.407283

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '39d3ed70d308'
down_revision: Union[str, None] = '860f6f990daa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('refresh_tokens', 'session_id',
               existing_type=postgresql.JSON(astext_type=sa.Text()),
               type_=sa.String(length=350),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('refresh_tokens', 'session_id',
               existing_type=sa.String(length=350),
               type_=postgresql.JSON(astext_type=sa.Text()),
               existing_nullable=False)
    # ### end Alembic commands ###
