from app import db


class VehicleDetails(db.Model):
    """
    Describes the vehicle details that a policy holder intends to insure
    """
    __tablename__ = 'vehicle_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_number = db.Column(db.String(8))
    model = db.Column(db.Integer, db.ForeignKey('car_model.model_id', ondelete='CASCADE', onupdate='CASCADE'))
    color = db.Column(db.String(20))
    body_type = db.Column(db.String(20))
    origin = db.Column(db.String(20), nullable=True)
    sum_insured = db.Column(db.Integer, nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, reg_number, model, color, body_type, origin, policy_id, sum_insured):
        self.reg_number = reg_number
        self.model = model
        self.color = color
        self.body_type = body_type
        self.origin = origin
        self.policy_id = policy_id
        self.sum_insured = sum_insured

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
