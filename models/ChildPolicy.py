from database.db import db
from sqlalchemy import desc


class ChildPolicy(db.Model):
    """
        Stores all information regarding a particular child policy to which a customer is enrolled,
        linking all their details as well
    """

    __tablename__ = 'child_policy'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vehicle = db.Column(db.Integer, db.ForeignKey(
        'vehicle_details.id', ondelete='CASCADE', onupdate='CASCADE'))
    cp_number = db.Column(db.String(22), nullable=False, unique=True)
    customer_number = db.Column(db.String(50))
    rate = db.Column(db.Float, nullable=True)
    date_registered = db.Column(db.DateTime, default=db.func.now())
    date_expiry = db.Column(db.DateTime)
    premium_amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    # the agency id is stored as an integer rather than a foreign key since it could be a brokerage, IA, or TA
    agency_id = db.Column(db.Integer, nullable=False)
    master_policy = db.Column(db.Integer, db.ForeignKey(
        'master_policy.id', onupdate='CASCADE', ondelete='CASCADE'))
    company = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    pricing_model = db.Column(db.String(50), nullable=False)
    date_activated = db.Column(
        db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=False)
    subclass = db.Column(db.String(22), nullable=True)
    reason = db.Column(db.String(10), nullable=True)
    # links to the association table for benefits
    benefits = db.relationship("PolicyBenefits", backref="child_policy")
    # links to the association table for extensions
    extensions = db.relationship("PolicyExtensions", backref="child_policy")

    def __init__(self, cp_number, vehicle, customer_number, rate, date_expiry, premium_amount, transaction_type,
                 agency_id, company, pricing_model, master_policy, subclass, reason=None):
        self.vehicle = vehicle
        self.cp_number = cp_number
        self.customer_number = customer_number
        self.rate = rate
        self.date_expiry = date_expiry
        self.premium_amount = premium_amount
        self.transaction_type = transaction_type
        self.agency_id = agency_id
        self.master_policy = master_policy
        self.company = company
        self.pricing_model = pricing_model
        self.subclass = subclass
        self.reason = reason

    def serialize(self, types=None):
        # todo: when other products are added, make vehicles parent to child policy table and dynamically
        # todo: add the item

        if types is None:
            types = ['benefits', 'extensions']

        child_policy = {
            "vehicle": self.vehicle_details.serialize(),
            "cp_number": self.cp_number,
            "rate": self.rate,
            "date_expiry": self.date_expiry.strftime('%m/%d/%Y'),
            "premium_amount": self.premium_amount,
            "transaction_type": self.transaction_type,
            "agency_id": self.agency_id,
            "master_policy": self.master_policy,
            "pricing_model": self.pricing_model,
            "date_activated": self.date_activated.strftime('%m/%d/%Y'),
            "subclass": self.subclass
        }

        if 'benefits' in types:
            child_policy.update({'benefits': [benefit.serialize() for benefit in self.benefits if self.benefits]})

        if 'extensions' in types:
            child_policy.update({'extensions': [extension.serialize() for extension in self.extensions
                                                if self.extensions]})

        return child_policy

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
    def get_child_by_id(cls, child_id, status=None):
        if status is None:
            status = True
        child = cls.query.filter_by(
            id=child_id, is_active=status).first()
        return child

    @classmethod
    def get_child_by_master_policy(cls, id):
        return [policy.serialize() for policy in cls.query.filter_by(master_policy=id).all()]

    @classmethod
    def get_child_policies(cls, customer_number):
        """
        for payments tracking, we need to get all the child policies of a customer which are active
        :param customer_number:
        :return {Array}:
        """
        return [child_policy.serialize('no_benefits_and_extensions')
                for child_policy in cls.query.filter_by(customer_number=customer_number, is_active=True)]
