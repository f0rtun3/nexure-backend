"""empty message

Revision ID: 1aae715e7889
Revises: de4bf6718891
Create Date: 2019-09-27 11:37:30.461476

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1aae715e7889'
down_revision = 'de4bf6718891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organization_customer', sa.Column('org_reg_number', sa.String(length=50), nullable=True))
    op.drop_column('organization_customer', 'org_registration_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('organization_customer', sa.Column('org_registration_number', sa.VARCHAR(length=50), autoincrement=False, nullable=True))
    op.drop_column('organization_customer', 'org_reg_number')
    # ### end Alembic commands ###