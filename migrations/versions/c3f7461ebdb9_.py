"""empty message

Revision ID: c3f7461ebdb9
Revises: 
Create Date: 2019-09-10 14:48:19.452151

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3f7461ebdb9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ic_benefit', sa.Column('insurance_company_id', sa.Integer(), nullable=True))
    op.drop_constraint('ic_benefit_insurance_company_fkey', 'ic_benefit', type_='foreignkey')
    op.create_foreign_key(None, 'ic_benefit', 'insurance_company', ['insurance_company_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('ic_benefit', 'insurance_company')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ic_benefit', sa.Column('insurance_company', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'ic_benefit', type_='foreignkey')
    op.create_foreign_key('ic_benefit_insurance_company_fkey', 'ic_benefit', 'insurance_company', ['insurance_company'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('ic_benefit', 'insurance_company_id')
    # ### end Alembic commands ###
