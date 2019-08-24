from app import db


"""Links benefits offered by the insurance company to a particular child policy. 
    Also contains the limit and the premium paid by the customer for the benefit"""
policy_benefits = db.Table('policy_benefits',
                           db.Column('policy_id', db.Integer,
                                     db.ForeignKey('child_policy.id')),
                           db.Column('ic_benefit_id', db.Integer,
                                     db.ForeignKey('ic_benefit.id')),
                           db.Column('amount', db.Float, nullable=False),
                           )
