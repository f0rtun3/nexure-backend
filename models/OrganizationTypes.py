from app import db


class OrganizationTypes(db.Model):
    """
    Holds the customer organization types
    """
    __tablename__ = 'organization_type'

    id = db.Column(db.Integer, autoincrement=True, nullable=False, primary_key=True)
    type_name = db.Column(db.String(20), nullable=False, unique=True)
    type_acronym = db.Column(db.String(5), nullable=False, unique=True)

    def __init__(self, type_name, type_acronym):
        self.type_name = type_name
        self.type_acronym = type_acronym

    def serialize(self):
        return {
            "label": self.type_name,
            "value": self.type_acronym
        }, 200

    def save(self):
        db.session.add(self)
        db.session.comit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_organization_customer_types(cls):
        all_types = [types.serialize() for types in cls.query.all()]
        return all_types
