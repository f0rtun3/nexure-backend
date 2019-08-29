"""empty message

Revision ID: 1b4478ad464d
Revises: 1995e9d6953d
Create Date: 2019-08-29 13:10:39.912125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1b4478ad464d'
down_revision = '1995e9d6953d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('location_data',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('constituency', sa.Integer(), nullable=True),
    sa.Column('ward', sa.Integer(), nullable=True),
    sa.Column('relativity', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['constituency'], ['constituency.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['ward'], ['ward.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('location_data')
    # ### end Alembic commands ###
