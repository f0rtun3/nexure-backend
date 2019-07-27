from app import db


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    agent_broker_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, user_id, agent_broker_id):
        self.user_id = user_id
        self.agent_broker_id = agent_broker_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    

    @classmethod
    def fetch_staff_by_id(cls, id):
        return cls.query.filter_by(user_id=id).first()
