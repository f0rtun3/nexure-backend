from app import db


class TiedAgents(db.Model):
    """
    Tied Agents model
    """
    __tablename__ = 'tied_agent'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # The tied agent is linked to a user profile since they have common details
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    ta_customer = db.relationship("TACustomer", backref="ta_affiliation")
    ta_staff = db.relationship("TAStaff", backref="ta_member")

    def __init__(self, user_id):
        self.user_id = user_id

    def __repr__(self):
        return f"{self.id}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
        }, 200

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
    def get_all_tied_agents(cls):
        tied_agents_rows = cls.query.all()
        tied_agents = [{
            "id": agent.id,
            "user": agent.user
        } for agent in tied_agents_rows]

        return tied_agents

    @classmethod
    def get_tied_agent_by_id(cls, agent_id):
        return cls.query.filter_by(id=agent_id).first()
    
    @classmethod
    def get_tied_agent_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()