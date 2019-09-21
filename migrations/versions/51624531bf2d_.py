"""empty message

Revision ID: 51624531bf2d
Revises: 2bed2120e88b
Create Date: 2019-09-21 07:56:17.742165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '51624531bf2d'
down_revision = '70c569483518'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurance_company', sa.Column('company', sa.Integer(), nullable=True))
    op.drop_constraint('insurance_company_company_details_fkey', 'insurance_company', type_='foreignkey')
    op.create_foreign_key(None, 'insurance_company', 'company_details', ['company'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('insurance_company', 'company_details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurance_company', sa.Column('company_details', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'insurance_company', type_='foreignkey')
    op.create_foreign_key('insurance_company_company_details_fkey', 'insurance_company', 'company_details', ['company_details'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('insurance_company', 'company')
    # ### end Alembic commands ###