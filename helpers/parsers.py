from flask_restful import reqparse

user_parser = reqparse.RequestParser()

# contact person info
user_parser.add_argument(
    "first_name",
    type=str
)
user_parser.add_argument(
    "last_name",
    type=str
)
user_parser.add_argument(
    "password",
    type=str
)
user_parser.add_argument(
    "phone",
    type=int
)
user_parser.add_argument(
    "email",
    type=str
)
user_parser.add_argument(
    "birth_date",
    type=str
)
user_parser.add_argument(
    "gender",
    type=str
)
user_parser.add_argument(
    "physical_address",
    type=str
)
user_parser.add_argument(
    "postal_code",
    type=int
)
user_parser.add_argument(
    "postal_town",
    type=str
)
user_parser.add_argument(
    "postal_address",
    type=str
)
user_parser.add_argument(
    "country",
    type=str
)
user_parser.add_argument(
    "county",
    type=str
)
user_parser.add_argument(
    "constituency",
    type=str
)
user_parser.add_argument(
    "ward",
    type=str
)
user_parser.add_argument(
    "id_passport",
    type=str
)
user_parser.add_argument(
    "update_type",
    type=str
)
user_parser.add_argument(
    "kra_pin",
    type=str
)
user_parser.add_argument(
    "occupation",
    type=str
)
user_parser.add_argument(
    "role",
    type=str
)
user_parser.add_argument(
    "permissions",
    type=str
)

# Organization details
user_parser.add_argument(
    "org_name",
    type=str
)
user_parser.add_argument(
    "org_email",
    type=str
)
user_parser.add_argument(
    "org_phone",
    type=int
)
user_parser.add_argument(
    "ira_reg_no",
    type=str
)
user_parser.add_argument(
    "ira_license_no",
    type=str
)
user_parser.add_argument(
    "org_kra_pin",
    type=str
)
user_parser.add_argument(
    "website",
    type=str
)
user_parser.add_argument(
    "bank_account_number",
    type=str
)
user_parser.add_argument(
    "mpesa_paybill",
    type=str
)

# social media info
user_parser.add_argument(
    "facebook",
    type=str
)
user_parser.add_argument(
    "twitter",
    type=str
)
user_parser.add_argument(
    "instagram",
    type=str
)
user_parser.add_argument(
    "avatar_url",
    type=str
)
user_parser.add_argument(
    "company_id",
    type=int
)
user_parser.add_argument(
    "staff_id",
    type=str
)
# change password
user_parser.add_argument(
    "new_password",
    type=str
)

user_parser.add_argument(
    "customer_id",
    type=int
)

user_parser.add_argument(
    "is_active",
    type=bool
)

user_parser.add_argument(
    "staff_id",
    type=int
)

"""Contains customer details"""
customer_parser = reqparse.RequestParser()

customer_parser.add_argument(
    # Individual or organization
    "type",
    type=str
)
customer_parser.add_argument(
    # If organization
    "org_type",
    type=str
)

customer_parser.add_argument(
    "phone_2",
    type=int
)

customer_parser.add_argument(
    "email_2",
    type=str
)

customer_parser.add_argument(
    "customer_id",
    type=int
)

# For individuals
customer_parser.add_argument(
    "first_name",
    type=str
)
customer_parser.add_argument(
    "last_name",
    type=str
)
customer_parser.add_argument(
    "phone",
    type=int
)
customer_parser.add_argument(
    "email",
    type=str
)
customer_parser.add_argument(
    "birth_date",
    type=str
)
customer_parser.add_argument(
    "gender",
    type=str
)
customer_parser.add_argument(
    "physical_address",
    type=str
)
customer_parser.add_argument(
    "postal_code",
    type=int
)
customer_parser.add_argument(
    "postal_town",
    type=str
)
customer_parser.add_argument(
    "postal_address",
    type=str
)
customer_parser.add_argument(
    "county",
    type=str
)
customer_parser.add_argument(
    "constituency",
    type=str
)
customer_parser.add_argument(
    "ward",
    type=str
)
customer_parser.add_argument(
    "country",
    type=str
)
customer_parser.add_argument(
    "id_passport",
    type=str
)
customer_parser.add_argument(
    "kra_pin",
    type=str
)
customer_parser.add_argument(
    "occupation",
    type=str
)
customer_parser.add_argument(
    "salutation",
    type=str
)
customer_parser.add_argument(
    "is_active",
    type=bool
)

# organization details
customer_parser.add_argument(
    "org_phone",
    type=int
)
customer_parser.add_argument(
    "org_name",
    type=str
)
customer_parser.add_argument(
    "org_email",
    type=str
)
customer_parser.add_argument(
    "reg_number",
    type=str
)
customer_parser.add_argument(
    "cust_no",
    type=str
)
customer_parser.add_argument(
    "status",
    type=bool
)
# social media info
customer_parser.add_argument(
    "facebook",
    type=str
)
customer_parser.add_argument(
    "twitter",
    type=str
)
customer_parser.add_argument(
    "instagram",
    type=str
)
customer_parser.add_argument(
    "avatar_url",
    type=str
)
# Underwriting parser
"""Contains customer details"""
underwriting_parser = reqparse.RequestParser()

underwriting_parser.add_argument(
    "transaction_type",
    type=str
)

underwriting_parser.add_argument(
    "modifications",
    type=list,
    action='append'
)
underwriting_parser.add_argument(
    "premium_amount",
    type=int
)
underwriting_parser.add_argument(
    "customer_number",
    type=str
)
underwriting_parser.add_argument(
    "class_id",
    type=str
)
underwriting_parser.add_argument(
    "subclass_id",
    type=str
)
underwriting_parser.add_argument(
    "pricing_model",
    type=str
)
underwriting_parser.add_argument(
    "driver_details",
    type=dict
)
underwriting_parser.add_argument(
    "vehicle_details",
    type=dict
)
underwriting_parser.add_argument(
    "insurance_company",
    type=int
)
underwriting_parser.add_argument(
    "benefits",
    type=dict,
    action='append'
)
underwriting_parser.add_argument(
    "extensions",
    type=dict,
    action='append'
)
underwriting_parser.add_argument(
    "master_policy_id",
    type=int
)
underwriting_parser.add_argument(
    "child_policy_id",
    type=int
)
underwriting_parser.add_argument(
    "date_expiry",
    type=str
)
underwriting_parser.add_argument(
    "rate",
    type=str
)
# for refunds
underwriting_parser.add_argument(
    "refund_type",
    type=str
)

underwriting_parser.add_argument(
    "vehicle_id",
    type=int
)

underwriting_parser.add_argument(
    "benefit_id",
    type=int
)

underwriting_parser.add_argument(
    "national_id",
    type=str
)

underwriting_parser.add_argument(
    "logbook",
    type=str
)


# Insurance Policy products handler parser
"""Contains details that are specific to a particular company for a particular policy such as benefits, extensions, loadings"""

policy_parser = reqparse.RequestParser()
policy_parser.add_argument(
    "rate",
    type=str
)
policy_parser.add_argument(
    "name",
    type=str
)
policy_parser.add_argument(
    "free_limit",
    type=str
)
policy_parser.add_argument(
    "max_limit",
    type=str
)
policy_parser.add_argument(
    "insurance_class",
    type=int
)
policy_parser.add_argument(
    "sub_class",
    type=list,
    action='append'
)
policy_parser.add_argument(
    "expiry_date",
    type=str
)
policy_parser.add_argument(
    "master_policy_id",
    type=int
)
policy_parser.add_argument(
    "child_policy_id",
    type=int
)
policy_parser.add_argument(
    "transaction_type",
    type=str
)
policy_parser.add_argument(
    "ncd_rate",
    type=str
)

# Payments parser: Handles all payments attributes
payments_parser = reqparse.RequestParser()
payments_parser.add_argument(
    "child_policy_id",
    type=int
)
payments_parser.add_argument(
    "amount",
    type=float
)
payments_parser.add_argument(
    "transaction_type",
    type=str
)
payments_parser.add_argument(
    "customer_no",
    type=str
)
payments_parser.add_argument(
    "next_date",
    type=str
)
payments_parser.add_argument(
    "amount_due",
    type=float
)
payments_parser.add_argument(
    "transaction_code",
    type=str
)

# aws_parser = reqparse.RequestParser()
# aws_parser.add_argument(
#     "file_name",
#     type=str
# )