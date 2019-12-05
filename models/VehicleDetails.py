from flask import current_app as app
from database.db import db
from helpers.file_handler import S3FileHandler

class VehicleDetails(db.Model):
    """
    Describes the vehicle details that a policy holder intends to insure
    """
    __tablename__ = 'vehicle_details'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_number = db.Column(db.String(8))
    model = db.Column(db.Integer, db.ForeignKey(
        'car_model.model_id', ondelete='CASCADE', onupdate='CASCADE'))
    color = db.Column(db.String(20))
    body_type = db.Column(db.String(20))
    origin = db.Column(db.String(20), nullable=True)
    sum_insured = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey(
        'driver.id', ondelete='CASCADE', onupdate='CASCADE'))
    no_of_seats = db.Column(db.Integer, nullable=False)
    manufacture_year = db.Column(db.Integer, nullable=False)
    engine_capacity = db.Column(db.Integer, nullable=False)
    national_id_file = db.Column(db.String(150), unique=True)
    logbook_file = db.Column(db.String(150), unique=True) 
    # link to vehicle modifications
    modifications = db.relationship("VehicleModifications", backref="vehicle_details")
    child_policy = db.relationship("ChildPolicy", backref="vehicle_details")

    def __init__(self, reg_number, model, color, body_type, origin, sum_insured, driver_id,
                 no_of_seats, manufacture_year, engine_capacity, national_id_file, logbook_file):
        self.reg_number = reg_number
        self.model = model
        self.color = color
        self.body_type = body_type
        self.origin = origin
        self.sum_insured = sum_insured
        self.driver_id = driver_id
        self.no_of_seats = no_of_seats
        self.manufacture_year = manufacture_year
        self.engine_capacity = engine_capacity
        self.national_id_file = national_id_file
        self.logbook_file = logbook_file

    def serialize(self):
        national_id = ""
        logbook = ""
        if self.national_id_file:
            s3_handler_id = S3FileHandler(app.config['S3_BUCKET'], self.national_id_file)
            national_id = s3_handler_id.generate_pre_signed_url()
        if self.logbook_file:
            s3_handler_logbook = S3FileHandler(app.config['S3_BUCKET'], self.logbook_file)
            logbook = s3_handler_logbook.generate_pre_signed_url()
        return {
            "id": self.id,
            "reg_number": self.reg_number,
            "model": self.car_model.model_name,
            "color": self.color,
            "body_type": self.body_type,
            "origin": self.origin,
            "sum_insured": self.sum_insured,
            "national_id": national_id,
            "logbook": logbook,
            "driver": self.driver.serialize(),
            "no_of_seats": self.no_of_seats,
            "manufacture_year": self.manufacture_year,
            "engine_capacity": self.engine_capacity,
            "vehicle_modifications": [modification.serialize() for modification in
                                      self.modifications]
        }

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
    def get_details(cls, id):
        vehicle = cls.query.filter_by(id=id).first()
        return vehicle
