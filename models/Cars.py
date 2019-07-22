from app import db

class CarMake(db.Model):
    """
    Stores the car make and the make id
    """
    __tablename__ = 'car_make'
    make_id = db.Column(db.Integer, primary_key=True, nullable=False)
    make_name = db.Column(db.String(50), unique=True, nullable=False)

    def __init__(self, make_id, make_name):
        self.make_id = make_id
        self.make_name = make_name
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def get_car_make_by_name(cls, name):
        car = cls.query.get(make_name=name)
        return car.id

class CarModel(db.Model):
    """
    Stores car model
    """
    __tablename__ = "car_model"

    model_id = db.Column(db.Integer, primary_key=True, nullable=False)
    model_name = db.Column(db.String(100), unique=True, nullable=False)
    series = db.Column(db.String(100), unique=True, nullable=False)
    make = db.Column(db.Integer, db.ForeignKey('car_make.make_id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, model_name, series, make):
        self. model_name = model_name
        self.series = series
        self.make = make

    def save(self):
        db.session.add(self)
        db.session.commit()
