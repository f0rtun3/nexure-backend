from app import db


class VehicleModifications(db.Model):
    """
    Contains records of any modifications made to a vehicle
    """
    __tablename__ = "vehicle_modifications"
    # modifications: accessory, make, estimated_value, serial_no
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    accessory_name = db.Column(db.String(200))
    make = db.Column(db.String(100))
    estimated_value = db.Column(db.Float)
    serial_no = db.Column(db.String(200))
    vehicle = db.Column(db.Integer, db.ForeignKey(
        'vehicle_details.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, accessory_name, make, estimated_value, serial_no, vehicle):
        self.accessory_name = accessory_name
        self.make = make
        self.estimated_value = estimated_value
        self.serial_no = serial_no
        self.vehicle = vehicle

    def serialize(self):
        return {
            "accessory_name": self.accessory_name,
            "make": self.make,
            "estimated_value": self.estimated_value,
            "serial_no": self.serial_no
        }

    def save(self):
        db.session.add(self)
        db.session.commit(self)

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()
