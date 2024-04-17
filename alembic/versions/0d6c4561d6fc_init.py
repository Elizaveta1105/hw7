"""Init

Revision ID: 0d6c4561d6fc
Revises: 
Create Date: 2024-04-17 13:07:59.409244

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0d6c4561d6fc'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notes', 'note',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('notes', 'note_date',
               existing_type=sa.DATE(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('notes', 'note_date',
               existing_type=sa.DATE(),
               nullable=False)
    op.alter_column('notes', 'note',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
