from app import db


class MakeOrigin(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   auto_increment=True, nullable=False)
    make_origin = db.Column(db.String(100), nullable=False)
    relativity = db.Column(db.Float, nullable=False)

    def __init__(self, make_origin, relativity):
        self.make_origin = make_origin
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