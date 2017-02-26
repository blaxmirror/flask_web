"""basic SQL

Revision ID: ac7ca276ca8f
Revises: 605703ccb96b
Create Date: 2017-02-26 18:09:15.203326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac7ca276ca8f'
down_revision = '605703ccb96b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.VARCHAR(length=64), nullable=True))
    # ### end Alembic commands ###