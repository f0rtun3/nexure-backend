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
    "mob",
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

# change password
user_parser.add_argument(
    "new_password",
    type=str
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


