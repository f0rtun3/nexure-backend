from app import db


class PolicyExtensions(db.Model):
    """
    Links benefits offered by the insurance company to a particular child policy.
    Also contains the limit and the premium paid by the customer for the benefit
    """
    __tablename__ = 'policy_extension'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))
    ic_extension = db.Column(db.Integer, db.ForeignKey('ic_extension.id', ondelete='CASCADE', onupdate='CASCADE'))
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, policy_id, ic_extension, amount):
        self.policy_id = policy_id
        self.ic_benefit = ic_extension
        self.amount = amount
    
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
