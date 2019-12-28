from database.db import db


class IndividualCustomer(db.Model):
    """
    Individual customer user
    linked to the UserProfile
    """
    # ToDo: Serialize the individual customer data
    __tablename__ = 'individual_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    customer_number = db.Column(db.String(50))
    phone_2 = db.Column(db.BIGINT, unique=True)
    email_2 = db.Column(db.String(100), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    salutation = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f"{self.user}"

    def __init__(self, user_id, customer_number, salutation, phone_2=None, email_2=None):
        self.user_id = user_id
        self.salutation = salutation
        self.phone_2 = phone_2
        self.email_2 = email_2
        self.customer_number = customer_number

    def serialize(self):
        customer_profile = {
            "customer_number": self.customer_number,
            "salutation": self.salutation,
            "phone_2": self.phone_2,
            "email_2": self.email_2
        }
        customer_profile.update(self.user.serialize())
        return customer_profile

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_customer_by_user_id(cls, uid):
        return cls.query.filter_by(user_id=uid).first()

    @classmethod
    def get_customer_number(cls, uid):
        customer = cls.query.filter_by(user_id=uid).first()
        return customer.customer_number
