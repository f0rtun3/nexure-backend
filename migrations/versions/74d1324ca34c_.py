"""empty message

Revision ID: 74d1324ca34c
Revises: 01b5c3faa6f9
Create Date: 2019-09-25 15:59:20.541811

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74d1324ca34c'
down_revision = '01b5c3faa6f9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_complete')
    # ### end Alembic commands ###