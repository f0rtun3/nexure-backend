from database.db import db


class CarMake(db.Model):
    """
    Stores the car make and the make id
    """
    __tablename__ = 'car_make'
    make_id = db.Column(db.Integer, primary_key=True, nullable=False)
    make_name = db.Column(db.String(50), unique=True, nullable=False)
    car_model = db.relationship('CarModel', backref='car_make', cascade="all, delete,"
                                                                        " delete-orphan")

    def __init__(self, make_id, make_name):
        self.make_id = make_id
        self.make_name = make_name

    def save(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return {
            "make_id": self.make_id,
            "make_name": self.make_name,
            "models": [m.serialize() for m in self.car_model]
        }

    @classmethod
    def get_car_make_by_name(cls, name):
        car = cls.query.filter_by(make_name=name).first()
        return car.make_id

    @classmethod
    def get_all_car_makes(cls):
        cars = [car.serialize() for car in cls.query.all()]
        return cars
