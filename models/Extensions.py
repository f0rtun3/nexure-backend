from app import db

class Extension(db.Model):
    __tablename__ = 'extension'
    """Contains extensions for a particular child polict"""
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    name = db.Column(db.String(100))
    # class_code = db.Column(db.Integer, db.ForeignKey('insurance_class.class_id', onupdate='CASCADE', ondelete='CASCADE'))

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
    def get_extension_id_by_name(cls, extension_name):
        extension = cls.query.filter_by(name=extension_name).first()
        return extension.id
    
    @classmethod
    def get_name_by_id(cls, extension_id):
        extension = cls.query.filter_by(id=extension_id).first()
        return extension.name
        
    @classmethod
    def get_all_extensions(cls):
        extension_rows = cls.query.all()
        extensions = []
        for i in extension_rows:
            extensions.append(i.name)
        return extensions
