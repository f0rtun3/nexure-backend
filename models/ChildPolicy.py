from app import db


class ChildPolicy(db.Model):
    """Stores all information regarding a particular child policy to which a customer is enrolled, linking all their details as well"""

    __tablename__ = 'child_policy'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    vehicle = db.Column(db.Integer, db.ForeignKey(
        'vehicle_details.id', ondelete='CASCADE', onupdate='CASCADE'))
    # links to the association table for benefits
    benefits = db.relationship('ICBenefits', secondary='policy_benefits',
                               lazy='dynamic', backref=db.backref('benefits', lazy='dynamic'))
    # links to the association table for extensions
    extensions = db.relationship('ICExtensions', secondary='policy_extensions',
                                 lazy='dynamic', backref=db.backref('extensions', lazy='dynamic'))
    # links to the association table for loadings
    loadings = db.relationship('ICLoadings', secondary='policy_loadings',
                               lazy='dynamic', backref=db.backref('loadings', lazy='dynamic'))
    customer_number = db.Column(db.String(50))
    rate = db.Column(db.Float, nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())
    date_expiry = db.Column(db.DateTime)
    premium_amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    # the agency id is stored as an integer rather than a foreign key since it could be a brokerage, IA, or TA
    # the role is used to match the ID to it's table
    agency_id = db.Column(db.Integer, nullable=False)
    agency_role = db.Column(db.Integer, db.ForeignKey(
        'role.id', onupdate='CASCADE', ondelete='CASCADE'))
    master_policy = db.Column(db.Integer, db.ForeignKey(
        'master_policy.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, vehicle, customer_number, rate, date_created, date_expiry, premium_amount, transaction_type,
                agency_id, agency_role, master_policy):
        self.vehicle = vehicle
        self.customer_number = customer_number
        self.rate = rate
        self.date_created = date_created
        self.date_expiry = date_expiry
        self.premium_amount = premium_amount
        self.transaction_type = transaction_type
        self.agency_id = agency_id
        self.agency_role = agency_role
        self.master_policy = master_policy

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def add_benefits(self):
        pass
    
    def add_loadings(self):
        pass
    
    def add_extension(self):
        pass
