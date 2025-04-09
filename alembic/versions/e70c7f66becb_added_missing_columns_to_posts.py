"""Added missing columns to posts

Revision ID: e70c7f66becb
Revises: 1b12cf08e34f
Create Date: 2025-04-05 23:13:44.574636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e70c7f66becb'
down_revision: Union[str, None] = '1b12cf08e34f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.drop_constraint('posts_user_id_fkey', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['owner_id'], ['user_id'], ondelete='CASCADE')
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_user_id_fkey', 'posts', 'users', ['user_id'], ['user_id'], ondelete='CASCADE')
    op.drop_column('posts', 'owner_id')
    # ### end Alembic commands ###
