"""empty message

Revision ID: 50f03fbd58b9
Revises: 
Create Date: 2019-08-29 14:36:12.174169

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '50f03fbd58b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('benefit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('car_make',
    sa.Column('make_id', sa.Integer(), nullable=False),
    sa.Column('make_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('make_id'),
    sa.UniqueConstraint('make_name')
    )
    op.create_table('company_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company_name', sa.String(length=100), nullable=False),
    sa.Column('company_email', sa.String(length=100), nullable=False),
    sa.Column('physical_address', sa.String(length=300), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('company_email'),
    sa.UniqueConstraint('company_name')
    )
    op.create_table('county',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('county_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('county_name')
    )
    op.create_table('driver',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('gender', sa.String(length=1), nullable=True),
    sa.Column('phone', sa.BIGINT(), nullable=True),
    sa.Column('birth_date', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('phone')
    )
    op.create_table('extension',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
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
    op.create_table('levies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('loading',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('organization_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=False),
    sa.Column('type_acronym', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('type_acronym'),
    sa.UniqueConstraint('type_name')
    )
    op.create_table('permission',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('permission_name', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('role',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('role_name', sa.String(length=7), nullable=False),
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
    sa.Column('mpesa_paybill', sa.BIGINT(), nullable=True),
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
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('salutation', sa.String(length=4), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('insurance_company',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('contact_person', sa.Integer(), nullable=True),
    sa.Column('company_phone', sa.BIGINT(), nullable=True),
    sa.Column('ira_registration_number', sa.String(length=50), nullable=True),
    sa.Column('ira_license_number', sa.String(length=50), nullable=True),
    sa.Column('kra_pin', sa.String(length=50), nullable=True),
    sa.Column('website', sa.String(length=150), nullable=True),
    sa.Column('bank_account', sa.String(length=50), nullable=True),
    sa.Column('mpesa_paybill', sa.String(length=50), nullable=True),
    sa.Column('company_details', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=True),
    sa.Column('year', sa.Float(), nullable=True),
    sa.Column('facebook', sa.String(length=150), nullable=True),
    sa.Column('instagram', sa.String(length=150), nullable=True),
    sa.Column('twitter', sa.String(length=150), nullable=True),
    sa.ForeignKeyConstraint(['company_details'], ['company_details.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['contact_person'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('bank_account'),
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
    op.create_table('licenced_classes',
    sa.Column('company', sa.Integer(), nullable=True),
    sa.Column('class', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['class'], ['insurance_class.class_id'], ),
    sa.ForeignKeyConstraint(['company'], ['company_details.id'], )
    )
    op.create_table('organization_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('org_type', sa.String(length=100), nullable=False),
    sa.Column('org_name', sa.String(length=100), nullable=True),
    sa.Column('org_phone', sa.BIGINT(), nullable=True),
    sa.Column('org_email', sa.String(length=100), nullable=True),
    sa.Column('org_registration_number', sa.String(length=50), nullable=True),
    sa.Column('physical_address', sa.String(length=100), nullable=True),
    sa.Column('postal_address', sa.String(length=100), nullable=True),
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
    op.create_table('user_permission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('permission_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['permission_id'], ['permission.id'], onupdate='CASCADE', ondelete='CASCADE'),
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
    sa.Column('postal_address', sa.String(length=100), nullable=True),
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
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['broker_id'], ['broker.broker_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ia_staff',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['independent_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ic_benefit',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('insurance_company', sa.Integer(), nullable=True),
    sa.Column('benefit', sa.Integer(), nullable=True),
    sa.Column('free_limit', sa.Float(), nullable=False),
    sa.Column('max_limit', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['benefit'], ['benefit.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['insurance_company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ic_extension',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('insurance_company', sa.Integer(), nullable=True),
    sa.Column('extension', sa.Integer(), nullable=True),
    sa.Column('free_limit', sa.Float(), nullable=False),
    sa.Column('max_limit', sa.Float(), nullable=False),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['extension'], ['extension.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['insurance_company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ic_loadings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('insurance_company', sa.Integer(), nullable=True),
    sa.Column('loading', sa.Integer(), nullable=True),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['insurance_company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['loading'], ['loading.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ic_products',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('company', sa.Integer(), nullable=True),
    sa.Column('insurance_class', sa.Integer(), nullable=True),
    sa.Column('sub_class', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['insurance_class'], ['insurance_class.class_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sub_class'], ['insurance_subclass.class_code'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('master_policy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('mp_number', sa.String(length=22), nullable=False),
    sa.Column('customer', sa.String(length=22), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('date_expiry', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('company', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('mp_number')
    )
    op.create_table('ta_staff',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['tied_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle_details',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('reg_number', sa.String(length=8), nullable=True),
    sa.Column('model', sa.Integer(), nullable=True),
    sa.Column('color', sa.String(length=20), nullable=True),
    sa.Column('body_type', sa.String(length=20), nullable=True),
    sa.Column('origin', sa.String(length=20), nullable=True),
    sa.Column('sum_insured', sa.Integer(), nullable=False),
    sa.Column('driver', sa.Integer(), nullable=True),
    sa.Column('no_of_seats', sa.Integer(), nullable=False),
    sa.Column('manufacture_year', sa.Integer(), nullable=False),
    sa.Column('engine_capacity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['driver'], ['driver.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['model'], ['car_model.model_id'], onupdate='CASCADE', ondelete='CASCADE'),
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
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['broker_id'], ['broker.broker_id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['br_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('child_policy',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('vehicle', sa.Integer(), nullable=True),
    sa.Column('cp_number', sa.String(length=22), nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('rate', sa.Float(), nullable=False),
    sa.Column('date_registered', sa.DateTime(), nullable=True),
    sa.Column('date_expiry', sa.DateTime(), nullable=True),
    sa.Column('premium_amount', sa.Float(), nullable=False),
    sa.Column('transaction_type', sa.String(length=50), nullable=False),
    sa.Column('agency_id', sa.Integer(), nullable=False),
    sa.Column('master_policy', sa.Integer(), nullable=True),
    sa.Column('company', sa.Integer(), nullable=True),
    sa.Column('pricing_model', sa.String(length=50), nullable=False),
    sa.Column('date_activated', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['company'], ['insurance_company.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['master_policy'], ['master_policy.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['vehicle'], ['vehicle_details.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('cp_number')
    )
    op.create_table('ia_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('date_affiliated', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['independent_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['ia_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ta_customer',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_number', sa.String(length=50), nullable=True),
    sa.Column('agent_id', sa.Integer(), nullable=True),
    sa.Column('staff_id', sa.Integer(), nullable=True),
    sa.Column('date_affiliated', sa.DateTime(), nullable=True),
    sa.Column('status', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['agent_id'], ['tied_agent.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['staff_id'], ['ta_staff.id'], onupdate='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('vehicle_modifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('accessory_name', sa.String(length=200), nullable=True),
    sa.Column('make', sa.String(length=100), nullable=True),
    sa.Column('estimated_value', sa.Float(), nullable=True),
    sa.Column('serial_no', sa.String(length=200), nullable=True),
    sa.Column('vehicle', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['vehicle'], ['vehicle_details.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('policy_benefits',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('policy_id', sa.Integer(), nullable=True),
    sa.Column('ic_benefit', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['ic_benefit'], ['ic_benefit.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['policy_id'], ['child_policy.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('policy_extension',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('policy_id', sa.Integer(), nullable=True),
    sa.Column('ic_extension', sa.Integer(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['ic_extension'], ['ic_extension.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['policy_id'], ['child_policy.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('policy_extension')
    op.drop_table('policy_benefits')
    op.drop_table('vehicle_modifications')
    op.drop_table('ta_customer')
    op.drop_table('ia_customer')
    op.drop_table('child_policy')
    op.drop_table('br_customer')
    op.drop_table('ward')
    op.drop_table('vehicle_details')
    op.drop_table('ta_staff')
    op.drop_table('master_policy')
    op.drop_table('ic_products')
    op.drop_table('ic_loadings')
    op.drop_table('ic_extension')
    op.drop_table('ic_benefit')
    op.drop_table('ia_staff')
    op.drop_table('br_staff')
    op.drop_table('user_role')
    op.drop_table('user_profile')
    op.drop_table('user_permission')
    op.drop_table('tied_agent')
    op.drop_table('organization_customer')
    op.drop_table('licenced_classes')
    op.drop_table('insurance_subclass')
    op.drop_table('insurance_company')
    op.drop_table('individual_customer')
    op.drop_table('independent_agent')
    op.drop_table('constituency')
    op.drop_table('car_model')
    op.drop_table('broker')
    op.drop_table('user')
    op.drop_table('role')
    op.drop_table('permission')
    op.drop_table('organization_type')
    op.drop_table('loading')
    op.drop_table('levies')
    op.drop_table('insurance_class')
    op.drop_table('extension')
    op.drop_table('driver')
    op.drop_table('county')
    op.drop_table('company_details')
    op.drop_table('car_make')
    op.drop_table('benefit')
    # ### end Alembic commands ###