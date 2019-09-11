from app import db


class ChildPolicy(db.Model):
    """Stores all information regarding a particular child policy to which a customer is enrolled, linking all their details as well"""

    __tablename__ = 'child_policy'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vehicle = db.Column(db.Integer, db.ForeignKey('vehicle_details.id', ondelete='CASCADE', onupdate='CASCADE'))
    # links to the association table for benefits
    benefits = db.relationship("PolicyBenefits", backref="benefits")
    # links to the association table for extensions
    extensions = db.relationship("PolicyExtensions", backref="extensions")
    cp_number = db.Column(db.String(22), nullable=False, unique=True)
    # links to the association table for loadings
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
    date_activated = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())
    is_active = db.Column(db.Boolean, default=False)
    subclass = db.Column(db.String(22), nullable=True)

    def __init__(self, cp_number, vehicle, customer_number, rate, date_expiry, premium_amount, transaction_type,
                 agency_id, company, pricing_model, master_policy, subclass):
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

    def add_benefit(self, benefit, amount_paid):
        self.benefits.append(benefit, amount_paid)
        self.save()

    def add_loading(self, loading_id, amount_paid):
        self.loadings.append(loading_id, amount_paid)
        self.save()

    def add_extension(self, extension_id, amount_paid):
        self.extensions.append(extension_id, amount_paid)
        self.save()
    
    @classmethod
    def get_child_by_id(cls, id):
        child = cls.query.filter_by(id=id).first()
        return child
