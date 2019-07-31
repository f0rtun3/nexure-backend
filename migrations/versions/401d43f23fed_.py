"""empty message

Revision ID: 401d43f23fed
Revises: 
Create Date: 2019-07-29 18:17:07.174285

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '401d43f23fed'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('car_make',
    sa.Column('make_id', sa.Integer(), nullable=False),
    sa.Column('make_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('make_id'),
    sa.UniqueConstraint('make_name')
    )
    op.create_table('county',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('county_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('county_name')
    )
    op.create_table('insurance_class',
    sa.Column('class_id', sa.Integer(), nullable=False),
    sa.Column('class_name', sa.String(length=50), nullable=False),
    sa.Column('acronym', sa.String(length=3), nullable=False),
    sa.Column('sector', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('class_id'),
    sa.UniqueConstraint('acronym'),
    sa.UniqueConstraint('class_name')
    )
    op.create_table('organization_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.Column('type_acronym', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_acronym'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=3), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('role_name')
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
    sa.Column('contact_person', sa.Integer(), nullable=False),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_license_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('mpesa_paybill', sa.BIGINT(), nullable=False),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('broker_id'),
    sa.UniqueConstraint('broker_email'),
    sa.UniqueConstraint('broker_name'),
    sa.UniqueConstraint('broker_phone_number'),
    sa.UniqueConstraint('ira_license_number'),
    sa.UniqueConstraint('ira_registration_number'),
    sa.UniqueConstraint('kra_pin'),
    sa.UniqueConstraint('website')
    )
    op.create_table('car_model',
    sa.Column('model_id', sa.Integer(), nullable=False),
    sa.Column('model_name', sa.String(length=300), nullable=False),
    sa.Column('series', sa.String(length=100), nullable=False),
    sa.Column('make', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['make'], ['car_make.make_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('model_id')
    )
    op.create_table('constituency',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('county', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['county'], ['county.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('independent_agent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('agency_name', sa.String(length=100), nullable=False),
    sa.Column('agency_phone', sa.BIGINT(), nullable=False),
    sa.Column('agency_email', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_licence_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('mpesa_paybill', sa.BIGINT(), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.Column('avatar_url', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agency_email'),
    sa.UniqueConstraint('agency_phone'),
    sa.UniqueConstraint('mpesa_paybill')
    )
    op.create_table('individual_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('salutation', sa.String(length=4), nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance_company',
    sa.Column('insurance_company_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('company_phone', sa.BIGINT(), nullable=False),
    sa.Column('company_email', sa.String(length=100), nullable=False),
    sa.Column('ira_registration_number', sa.String(length=15), nullable=True),
    sa.Column('ira_license_number', sa.String(length=15), nullable=True),
    sa.Column('kra_pin', sa.String(length=15), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('bank_account', sa.BIGINT(), nullable=True),
    sa.Column('mpesa_paybill', sa.BIGINT(), nullable=True),
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
    sa.UniqueConstraint('mpesa_paybill'),
    sa.UniqueConstraint('website')
    )
    op.create_table('insurance_subclass',
    sa.Column('class_code', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('parent_class', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['parent_class'], ['insurance_class.class_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('class_code')
    )
    op.create_table('organization_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('org_type', sa.String(length=100), nullable=False),
    sa.Column('org_name', sa.String(length=100), nullable=True),
    sa.Column('org_phone', sa.BIGINT(), nullable=True),
    sa.Column('org_email', sa.String(length=100), nullable=True),
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
    sa.UniqueConstraint('org_name')
    )
    op.create_table('tied_agent',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
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
    sa.Column('physical_address', sa.String(length=100), nullable=True),
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
    op.create_table('br_staff',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('broker_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['broker_id'], ['broker.broker_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ia_staff',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['independent_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ta_staff',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['tied_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ward',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('constituency', sa.Integer(), nullable=True),
    sa.Column('county', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['constituency'], ['constituency.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['county'], ['county.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('br_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('broker_id', sa.Integer(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('date_affiliated', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['broker_id'], ['broker.broker_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['br_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('customer_number')
    )
    op.create_table('ia_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('date_affiliated', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['independent_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['ia_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('customer_number')
    )
    op.create_table('ta_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('date_affiliated', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['tied_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['ta_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('customer_number')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ta_customer')
    op.drop_table('ia_customer')
    op.drop_table('br_customer')
    op.drop_table('ward')
    op.drop_table('ta_staff')
    op.drop_table('ia_staff')
    op.drop_table('br_staff')
    op.drop_table('user_role')
    op.drop_table('user_profile')
    op.drop_table('tied_agent')
    op.drop_table('organization_customer')
    op.drop_table('insurance_subclass')
    op.drop_table('insurance_company')
    op.drop_table('individual_customer')
    op.drop_table('independent_agent')
    op.drop_table('constituency')
    op.drop_table('car_model')
    op.drop_table('broker')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('organization_type')
    op.drop_table('insurance_class')
    op.drop_table('county')
    op.drop_table('car_make')
    # ### end Alembic commands ###
