from database.db import db


class PolicyExtensions(db.Model):
    """
    Links benefits offered by the insurance company to a particular child policy.
    Also contains the limit and the premium paid by the customer for the benefit
    """
    __tablename__ = 'policy_extension'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey(
        'child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))
    ic_extension_id = db.Column(db.Integer, db.ForeignKey(
        'ic_extension.id', ondelete='CASCADE', onupdate='CASCADE'))
    amount = db.Column(db.Float, nullable=False)

    def __init__(self, policy_id, ic_extension_id, amount):
        self.policy_id = policy_id
        self.ic_extension_id = ic_extension_id
        self.amount = amount

    def serialize(self):
        #  We use the PolicyExtensions ID instead of the ICExtensions
        #  ID to return a unique extension for each child policy
        data = self.ic_extension.serialize()
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
    def get_policy_ext_by_policy(cls, child_policy_id):
        extension_set = set()
        extensions = cls.query.filter_by(policy_id=child_policy_id)
        if extensions is None:
            return None

        for ext in extensions:
            extensions.add(ext.ic_extension_id)

        return extension_set
