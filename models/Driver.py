from database.db import db
from datetime import datetime

class Driver(db.Model):
    """
    Store driver details linked to a particular vehicle
    """
    __tablename__ = 'driver'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(1))
    # we need to store the user mobile number
    # for subsequent communication
    phone = db.Column(db.BIGINT, unique=True)
    birth_date = db.Column(db.DateTime)
    driver = db.relationship("VehicleDetails", backref="driver")

    def __init__(self, first_name, last_name, gender, phone, birth_date):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone = phone
        self.birth_date = birth_date

    def serialize(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "birth_date": self.birth_date.strftime('%m/%d/%Y')
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
    def get_driver_by_id(cls, id):
        driver = cls.query.filter_by(id=id).first()
        return driver
