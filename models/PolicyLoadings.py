from app import db

policy_extensions = db.Table('policy_loadings',
                           db.Column('policy_id', db.Integer,
                                     db.ForeignKey('child_policy.id')),
                           db.Column('ic_loadings_id', db.Integer,
                                     db.ForeignKey('ic_loadings.id')),
                           db.Column('amount', db.Float, nullable=False)
                           )
    