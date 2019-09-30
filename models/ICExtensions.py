from database.db import db


class ICExtensions(db.Model):
    """
    Stores the extensions
    that offered by a company, for a particular policy, together with the rate and limits for them"""

    __tablename__ = 'ic_extension'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    insurance_company_id = db.Column(db.Integer, db.ForeignKey(
        'insurance_company.id', onupdate='CASCADE', ondelete='CASCADE'))
    extension_id = db.Column(db.Integer, db.ForeignKey(
        'extension.id', onupdate='CASCADE', ondelete='CASCADE'))
    free_limit = db.Column(db.Float, nullable=False)
    max_limit = db.Column(db.Float, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    policy_extension_id = db.relationship('PolicyExtensions', backref="ic_extension")

    def __init__(self, insurance_company_id, extension_id, free_limit, max_limit, rate):
        self.insurance_company_id = insurance_company_id
        self.extension_id = extension_id
        self.free_limit = free_limit
        self.max_limit = max_limit
        self.rate = rate

    def serialize(self):
        return {
            "insurance_company": self.insurance_company.company_details.company_name,
            "name": self.extension.name,
            "free_limit": self.free_limit,
            "max_limit": self.max_limit,
            "rate": self.rate
        }

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
    def get_extensions_by_company_id(cls, company_id):
        """
        Returns id, extension_id, free_limit, max_limit and rate for
        every list of extensions under a particular company 
        """
        extension_rows = [ extension.serialize() for extension in cls.query.filter_by(
            insurance_company_id=company_id).all()]
        return extension_rows

    @classmethod
    def get_ic_extension(cls, extension_id):
        extension = cls.query.filter_by(extension_id=extension_id).first()
        return extension

    @classmethod
    def get_extension_id(cls, id):
        """
        Gets the IC Extension given the object id
        """
        ic_extension = cls.query.filter_by(id=id).first()
        return ic_extension

    @classmethod
    def get_unselected_extensions(cls, excluded_extensions):
        extensions = cls.query.filter(cls.id.notin_(excluded_extensions))
        return [extension.serialize() for extension in extensions]
