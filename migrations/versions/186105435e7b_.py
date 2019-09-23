"""empty message

Revision ID: 186105435e7b
Revises: 49b83cacc07b
Create Date: 2019-09-23 10:05:05.770729

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '186105435e7b'
down_revision = '49b83cacc07b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurance_company', sa.Column('associated_company', sa.Integer(), nullable=True))
    op.drop_constraint('insurance_company_company_fkey', 'insurance_company', type_='foreignkey')
    op.create_foreign_key(None, 'insurance_company', 'company_details', ['associated_company'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('insurance_company', 'company')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('insurance_company', sa.Column('company', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'insurance_company', type_='foreignkey')
    op.create_foreign_key('insurance_company_company_fkey', 'insurance_company', 'company_details', ['company'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('insurance_company', 'associated_company')
    # ### end Alembic commands ###
