from app import db

class CarModel(db.Model):
    """
    Stores car model
    """
    __tablename__ = "car_model"

    model_id = db.Column(db.Integer, primary_key=True, nullable=False)
    model_name = db.Column(db.String(300), nullable=False)
    series = db.Column(db.String(100), nullable=False)
    make = db.Column(db.Integer, db.ForeignKey('car_make.make_id', ondelete='CASCADE', onupdate='CASCADE'))

    # describe the relationship with the vehicle_details of a policy holder
    vehicle_details = db.relationship("VehicleDetails", backref="car_model")

    def __init__(self, model_name, series, make):
        self. model_name = model_name
        self.series = series
        self.make = make

    def save(self):
        db.session.add(self)
        db.session.commit()
