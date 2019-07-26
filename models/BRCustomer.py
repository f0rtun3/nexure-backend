from app import db


class BRCustomer(db.Model):
    """
    Affiliation between customers and brokers
    """
    __tablename__ = 'br_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    customer_number = db.Column(db.String(50), unique=True, nullable=True)
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.broker_id', onupdate='CASCADE', ondelete='CASCADE'))
    staff_id = db.Column(db.Integer, db.ForeignKey('staff.id', onupdate='CASCADE'))
    date_affiliated = db.Column(db.DateTime, default=db.func.now())
    # we need to know whether the affiliation is active or not
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self, customer_number, broker_id, staff_id=None):
        self.customer_number = customer_number
        self.broker_id = broker_id
        self.staff_id = staff_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_affiliation(cls, broker_id):
        broker_data = cls.query.filter_by(broker_id=broker_id).all()
        return broker_data
