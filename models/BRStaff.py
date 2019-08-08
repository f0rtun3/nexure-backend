from app import db


class BRStaff(db.Model):
    __tablename__ = 'br_staff'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'))
    broker_id = db.Column(db.Integer, db.ForeignKey('broker.broker_id', ondelete='CASCADE', onupdate='CASCADE'))
    br_customer = db.relationship("BRCustomer", backref="br_customer_member")
    active = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, broker_id):
        self.user_id = user_id
        self.broker_id = broker_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def deactivate_staff(self, company_id, staff_id):
        staff = self.query.filter_by(user_id=staff_id, broker_id=company_id)
        staff.active = False
        self.save()

    @classmethod
    def fetch_staff_by_id(cls, broker_id):
        return cls.query.filter_by(broker_id=broker_id, active=True).first()

    @classmethod
    def fetch_broker_by_staff(cls, staff_id):
        broker = cls.query.filter_by(user_id=staff_id, active=True).first()
        return broker.user_id

    @classmethod
    def fetch_all_staff_ids(cls, agency_id):
        staff = cls.query.filter_by(broker_id=agency_id, active=True)
        staff_ids = []
        for i in staff:
            staff_ids.append(i.user_id)
        return staff_ids
