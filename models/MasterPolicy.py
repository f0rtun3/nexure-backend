from database.db import db
from sqlalchemy import desc


class MasterPolicy(db.Model):
    """
    describes the master policy details
    once an policy holder registers a new business/risk item
    a master policy is automatically created for them
    """
    __tablename__ = 'master_policy'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    # the master policy number which is created upon registration
    mp_number = db.Column(db.String(22), nullable=False, unique=True)
    # the customer number of the policy holder
    customer = db.Column(db.String(22), nullable=False)
    # the date in which the policy; master policy number was created
    date_created = db.Column(db.DateTime, default=db.func.now())
    # the date in which the master policy will expire
    # this date may be altered upon renewal
    date_expiry = db.Column(db.DateTime)
    # the status of the policy holder's policy
    # it may be changed depending on various circumstances
    status = db.Column(db.Boolean, nullable=False, default=True)
    # insurance company that covers this master policy
    company = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    child = db.relationship("ChildPolicy", backref="master")

    def __init__(self, mp_number, customer, date_expiry, company):
        self.mp_number = mp_number
        self.customer = customer
        self.date_expiry = date_expiry
        self.company = company

    def serialize(self):
        return {
            "id": self.id,
            "mp_number": self.mp_number,
            "customer_number": self.customer,
            "date_created": self.date_created.strftime('%m/%d/%Y'),
            "date_expiry": self.date_expiry.strftime('%m/%d/%Y'),
            "status": self.status,
            "company": self.insurance_company.company_details.company_name,
            "child_policies": [child_policy.serialize() for child_policy in self.child]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def get_policy_by_customer_no(cls, number):
        policy = cls.query.filter_by(customer=number).all()
        return policy

    @classmethod
    def get_policy_by_mp_number(cls, mp_number):
        policy = cls.query.filter_by(mp_number=mp_number).first()
        return policy

    @classmethod
    def get_policy_by_id(cls, id):
        policy = cls.query.filter_by(id=id).first()
        return policy

    @classmethod
    def get_latest_policy_details(cls, mp_number):
        policy_details = cls.query.order_by(cls.id.desc()).filter_by(mp_number=mp_number).first()
        if policy_details:
            return policy_details.serialize()

        return None
