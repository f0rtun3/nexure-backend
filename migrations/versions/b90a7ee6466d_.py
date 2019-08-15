"""empty message

Revision ID: b90a7ee6466d
Revises: 4e4f7f6b46c9
Create Date: 2019-08-09 13:04:50.165386

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b90a7ee6466d'
down_revision = '4e4f7f6b46c9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('company_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('company_email', sa.String(length=100), nullable=False),
    sa.Column('physical_address', sa.String(length=300), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('avatar'),
    sa.UniqueConstraint('company_email'),
    sa.UniqueConstraint('company_name')
    )
    op.add_column('br_staff', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('ia_staff', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('insurance_company', sa.Column('company_details', sa.Integer(), nullable=True))
    op.drop_constraint('insurance_company_company_email_key', 'insurance_company', type_='unique')
    op.drop_constraint('insurance_company_company_name_key', 'insurance_company', type_='unique')
    op.create_foreign_key(None, 'insurance_company', 'company_details', ['company_details'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('insurance_company', 'company_name')
    op.drop_column('insurance_company', 'company_email')
    op.drop_column('insurance_company', 'avatar_url')
    op.add_column('ta_staff', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ta_staff', 'active')
    op.add_column('insurance_company', sa.Column('avatar_url', sa.VARCHAR(length=150), autoincrement=False, nullable=True))
    op.add_column('insurance_company', sa.Column('company_email', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.add_column('insurance_company', sa.Column('company_name', sa.VARCHAR(length=100), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'insurance_company', type_='foreignkey')
    op.create_unique_constraint('insurance_company_company_name_key', 'insurance_company', ['company_name'])
    op.create_unique_constraint('insurance_company_company_email_key', 'insurance_company', ['company_email'])
    op.drop_column('insurance_company', 'company_details')
    op.drop_column('ia_staff', 'active')
    op.drop_column('br_staff', 'active')
    op.drop_table('company_details')
    # ### end Alembic commands ###
