"""empty message

Revision ID: 6535b8d5f7e5
Revises: 2c0afe941463
Create Date: 2019-09-21 06:53:41.564355

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6535b8d5f7e5'
down_revision = '2c0afe941463'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_profile', sa.Column('country', sa.String(length=30), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user_profile', 'country')
    # ### end Alembic commands ###
