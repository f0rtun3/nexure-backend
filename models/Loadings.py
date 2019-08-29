from app import db


class Loadings(db.Model):
    __tablename__ = 'loading'
    """Contains loadings for a particular child policy"""
    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"{self.name}"

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

    @classmethod
    def get_loading_id_by_name(cls, loading_name):
        loading = cls.query.filter_by(name=loading_name).first()
        return loading.id

    @classmethod
    def get_name_by_id(cls, loading_id):
        loading = cls.query.filter_by(id=loading_id).first()
        return loading.name

    @classmethod
    def get_all_loadings(cls):
        loading_rows = cls.query.all()
        return loading_rows
