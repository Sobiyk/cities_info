"""empty message

Revision ID: 15fa4e9ee9ff
Revises: 8c24fbd73af1
Create Date: 2024-08-16 18:17:40.737162

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15fa4e9ee9ff'
down_revision: Union[str, None] = '8c24fbd73af1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'city', ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'city', type_='unique')
    # ### end Alembic commands ###
