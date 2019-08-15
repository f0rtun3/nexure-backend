from app import db


class MasterPolicy(db.Model):
    """
    describes the master policy details
    once an policy holder registers a new business/risk item
    a master policy is automatically created for them
    """
    __tablename__ = 'master_policy'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
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

    def __init__(self, mp_number, customer, date_expiry):
        self.mp_number = mp_number
        self.customer = customer
        self.date_expiry = date_expiry

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


