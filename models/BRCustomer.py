from app import db


class BRCustomer(db.Model):
    """
    Affiliation between customers and brokers
    """
    __tablename__ = 'br_customer'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
<<<<<<< HEAD
    customer_number = db.Column(db.String(50))
=======
    customer_number = db.Column(db.String(50), nullable=True)
>>>>>>> ca63987386e14df66130c1b18b45c2cf659df541
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.broker_id', onupdate='CASCADE', ondelete='CASCADE'))
    staff_id = db.Column(db.Integer, db.ForeignKey('br_staff.id', onupdate='CASCADE'), nullable=True)
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

    @classmethod
    def check_duplicate_affiliation(cls, broker_id, customer_number):
        if cls.query.filter_by(broker_id=broker_id, customer_number=customer_number).first():
            return True
        return False
