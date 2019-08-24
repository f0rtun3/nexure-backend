from app import db

policy_extensions = db.Table('policy_extensions',
                             db.Column('policy_id', db.Integer,
                                       db.ForeignKey('child_policy.id')),
                             db.Column('ic_extension_id', db.Integer,
                                       db.ForeignKey('ic_extension.id')),
                             db.Column('amount', db.Float, nullable=False)
                             )
