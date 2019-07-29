from app import db


class TAStaff(db.Model):
    __tablename__ = 'ta_staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    agent_id = db.Column(db.Integer, db.ForeignKey('tied_agent.id', ondelete='CASCADE', onupdate='CASCADE'))
    ta_customer = db.relationship("TACustomer", backref="ta_customer_member")

    def __init__(self, user_id, agent_id):
        self.user_id = user_id
        self.agent_id = agent_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def fetch_staff_by_id(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id).first()

    @classmethod
    def fetch_agent_by_staff(cls, staff_id):
        agent = cls.query.filter_by(staff_id=staff_id).first()

        return agent.user_id