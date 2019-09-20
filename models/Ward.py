from database.db import db


class Ward(db.Model):
    __tablename__ = 'ward'

    id = db.Column(db.Integer, primary_key=True,
                   auto_increment=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    constituency_id = db.Column(db.Integer, db.ForeignKey(
        'constituency.id', ondelete='CASCADE', onupdate='CASCADE'))
    county_id = db.Column(db.Integer, db.ForeignKey(
        'county.id', ondelete='CASCADE', onupdate='CASCADE'))

    def __init__(self, name, constituency, county):
        self.name = name
        self.constituency = constituency
        self.county = county

    def serialize(self):
        return{
            "constituency": self.constituency.name,
            "id": self.id,
            "name": self.name
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_ward_id_by_name(cls, name):
        ward = cls.query.filter_by(name=name).first()
        return ward.id

    @classmethod
    def get_all_wards(cls):
        return [ward.serialize() for ward in cls.query.all()]

