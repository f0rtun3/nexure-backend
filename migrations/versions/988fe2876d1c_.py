"""empty message

Revision ID: 988fe2876d1c
Revises: 
Create Date: 2019-07-01 18:01:47.206267

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '988fe2876d1c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=2), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('user_id')
    )
    op.create_table('broker',
    sa.Column('broker_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('broker_name', sa.String(length=100), nullable=False),
    sa.Column('broker_phone_number', sa.BIGINT(), nullable=False),
    sa.Column('broker_email', sa.String(length=100), nullable=False),
    sa.Column('b_contact_person', sa.Integer(), nullable=False),
    sa.Column('b_contact_number', sa.BIGINT(), nullable=False),
    sa.Column('b_contact_email', sa.String(length=100), nullable=False),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_license_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['b_contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('broker_id'),
    sa.UniqueConstraint('b_contact_email'),
    sa.UniqueConstraint('b_contact_number'),
    sa.UniqueConstraint('broker_email'),
    sa.UniqueConstraint('broker_name'),
    sa.UniqueConstraint('broker_phone_number'),
    sa.UniqueConstraint('ira_license_number'),
    sa.UniqueConstraint('ira_registration_number'),
    sa.UniqueConstraint('kra_pin'),
    sa.UniqueConstraint('website')
    )
    op.create_table('independent_agent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('agency_name', sa.String(length=100), nullable=False),
    sa.Column('agency_phone', sa.BIGINT(), nullable=False),
    sa.Column('agency_email', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('contact_first_name', sa.String(length=50), nullable=False),
    sa.Column('contact_last_name', sa.String(length=50), nullable=False),
    sa.Column('contact_phone', sa.BIGINT(), nullable=False),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_licence_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agency_email'),
    sa.UniqueConstraint('agency_phone')
    )
    op.create_table('individual_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance_company',
    sa.Column('insurance_company_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('contact_first_name', sa.String(length=50), nullable=False),
    sa.Column('contact_last_name', sa.String(length=50), nullable=False),
    sa.Column('contact_phone', sa.BIGINT(), nullable=False),
    sa.Column('company_phone', sa.BIGINT(), nullable=False),
    sa.Column('company_email', sa.String(length=100), nullable=False),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_license_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('insurance_company_id'),
    sa.UniqueConstraint('company_email'),
    sa.UniqueConstraint('company_name'),
    sa.UniqueConstraint('company_phone'),
    sa.UniqueConstraint('ira_license_number'),
    sa.UniqueConstraint('ira_registration_number'),
    sa.UniqueConstraint('kra_pin'),
    sa.UniqueConstraint('website')
    )
    op.create_table('organization_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('org_customer_number', sa.String(length=50), nullable=True),
    sa.Column('org_name', sa.String(length=100), nullable=True),
    sa.Column('org_phone', sa.BIGINT(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('org_registration_number', sa.String(length=50), nullable=True),
    sa.Column('physical_address', sa.String(length=100), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('postal_town', sa.String(length=30), nullable=True),
    sa.Column('county', sa.String(length=30), nullable=True),
    sa.Column('constituency', sa.String(length=30), nullable=True),
    sa.Column('ward', sa.String(length=30), nullable=True),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('org_customer_number'),
    sa.UniqueConstraint('org_name')
    )
    op.create_table('tied_agent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_profile',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('phone', sa.BIGINT(), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.Column('occupation', sa.String(length=100), nullable=True),
    sa.Column('id_passport', sa.String(length=30), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.Column('address_line_1', sa.String(length=100), nullable=True),
    sa.Column('address_line_2', sa.String(length=100), nullable=True),
    sa.Column('postal_code', sa.Integer(), nullable=True),
    sa.Column('postal_town', sa.String(length=30), nullable=True),
    sa.Column('county', sa.String(length=30), nullable=True),
    sa.Column('constituency', sa.String(length=30), nullable=True),
    sa.Column('ward', sa.String(length=30), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('updated_on', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id_passport'),
    sa.UniqueConstraint('kra_pin'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_role')
    op.drop_table('user_profile')
    op.drop_table('tied_agent')
    op.drop_table('organization_customer')
    op.drop_table('insurance_company')
    op.drop_table('individual_customer')
    op.drop_table('independent_agent')
    op.drop_table('broker')
    op.drop_table('user')
    op.drop_table('role')
    # ### end Alembic commands ###