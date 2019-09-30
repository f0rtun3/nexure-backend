from database.db import db


class PolicyBenefits(db.Model):
    """
    Links benefits offered by the insurance company to a particular child policy.
    Also contains the limit and the premium paid by the customer for the benefit
    """
    __tablename__ = 'policy_benefits'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey(
        'child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))
    ic_benefit_id = db.Column(db.Integer, db.ForeignKey(
        'ic_benefit.id', ondelete='CASCADE', onupdate='CASCADE'))
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, policy_id, ic_benefit_id, amount):
        self.policy_id = policy_id
        self.ic_benefit_id = ic_benefit_id
        self.amount = amount

    def serialize(self):
        #  We use the PolicyBenefits ID instead of the ICBenefits
        #  ID to return a unique benefit for each child policy
        data = self.ic_benefit.serialize()
        data.update({"id": self.id})
        return data

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
    def get_policy_benefit_by_policy(cls, child_policy_id):
        benefit_set = set()
        benefits = cls.query.filter_by(policy_id=child_policy_id)
        for benefit in benefits:
            benefit_set.add(benefit.ic_benefit_id)

        return benefit_set
