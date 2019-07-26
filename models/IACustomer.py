from app import db


class IACustomer(db.Model):
    """
    Affiliation between customers and tied agents
    """
    __tablename__ = 'ia_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    customer_number = db.Column(db.String(50), unique=True, nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('independent_agent.id', onupdate='CASCADE', ondelete='CASCADE'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', onupdate='CASCADE'))
    date_affiliated = db.Column(db.DateTime, default=db.func.now())
    # we need to know whether the affiliation is active or not
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, customer_number, agent_id, staff_id=None):
        self.customer_number = customer_number
        self.agent_id = agent_id
        self.staff_id = staff_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_affiliation(cls, agent_id):
        agent_data = cls.query.filter_by(agent_id=agent_id).all()
        return agent_data
