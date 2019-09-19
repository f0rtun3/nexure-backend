"""empty message

Revision ID: c659fc9ffbe5
Revises: 
Create Date: 2019-09-18 11:57:13.753961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c659fc9ffbe5'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ic_rate_discount')
    op.add_column('insurance_company', sa.Column('ncd_rate', sa.Float(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('insurance_company', 'ncd_rate')
    op.create_table('ic_rate_discount',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('rates', sa.VARCHAR(length=20), autoincrement=False, nullable=False),
    sa.Column('ic_company_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['ic_company_id'], ['insurance_company.id'], name='ic_rate_discount_ic_company_id_fkey', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='ic_rate_discount_pkey')
    )
    # ### end Alembic commands ###