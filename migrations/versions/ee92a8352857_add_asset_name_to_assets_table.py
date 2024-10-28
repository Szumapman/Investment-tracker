"""add asset_name to assets table

Revision ID: ee92a8352857
Revises: 39d3ed70d308
Create Date: 2024-10-28 11:52:19.586356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee92a8352857'
down_revision: Union[str, None] = '39d3ed70d308'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('assets', sa.Column('asset_name', sa.String(length=10), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('assets', 'asset_name')
    # ### end Alembic commands ###