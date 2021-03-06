"""empty message

Revision ID: 605703ccb96b
Revises: ffaa798632a7
Create Date: 2017-02-26 18:07:59.023880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '605703ccb96b'
down_revision = 'ffaa798632a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('nickname', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'nickname')
    # ### end Alembic commands ###
