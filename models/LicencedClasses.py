from app import db

licenced_classes = db.Table('licenced_classes',
                            db.Column('company', db.Integer,
                                      db.ForeignKey('company_details.id')),
                            db.Column('class', db.Integer,
                                      db.ForeignKey('insurance_class.class_id'))
                            )