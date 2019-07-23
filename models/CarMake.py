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
