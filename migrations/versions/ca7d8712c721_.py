"""empty message

Revision ID: ca7d8712c721
Revises: de4bf6718891
Create Date: 2019-09-26 12:47:40.506890

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca7d8712c721'
down_revision = 'de4bf6718891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('independent_agent', sa.Column('ira_license_number', sa.String(length=15), nullable=True))
    op.add_column('independent_agent', sa.Column('website', sa.String(length=150), nullable=True))
    op.create_unique_constraint(None, 'independent_agent', ['website'])
    op.drop_column('independent_agent', 'ira_licence_number')
    op.add_column('user', sa.Column('is_complete', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'is_complete')
    op.add_column('independent_agent', sa.Column('ira_licence_number', sa.VARCHAR(length=15), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'independent_agent', type_='unique')
    op.drop_column('independent_agent', 'website')
    op.drop_column('independent_agent', 'ira_license_number')
    # ### end Alembic commands ###
