from app import db


class LocationData(db.Model):
    """
    Stores ward, constituency and the relativity
    """
    __tablename__ = "location_data"
    
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    constituency = db.Column(db.Integer, db.ForeignKey(
        'constituency.id', onupdate='CASCADE', ondelete='CASCADE'))
    ward = db.Column(db.Integer, db.ForeignKey(
        'ward.id', onupdate='CASCADE', ondelete='CASCADE'))
    relativity = db.Column(db.Float, nullable=False)

    def __init__(self, constituency, ward, relativity):
        self.constituency = constituency
        self.ward = ward
        self.relativity = relativity

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
