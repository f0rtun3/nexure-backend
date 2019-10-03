from database.db import db


class PolicyTransactions(db.Model):
    """
    Describes all the transactions for a particular child policy, for both credit(payments) and debit(refunds)
    """
    __tablename__ = 'policy_transactions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # transaction type can either be debit or credit
    transaction_type = db.Column(db.String(10))
    amount = db.Column(db.Float, nullable=False)
    customer_no = db.Column(db.String(50))
    child_policy = db.Column(db.Integer, db.ForeignKey(
        'child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))
    date_due = db.Column(db.DateTime)
    date_paid = db.Column(db.DateTime)
    is_paid = db.Column(db.Boolean, default=False)

    def __init__(self, transaction_type, amount, customer_no, child_policy, date_due):
        self.transaction_type = transaction_type
        self.amount = amount
        self.customer_no = customer_no
        self.child_policy = child_policy
        self.date_due = date_due

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    @classmethod
    def total_amount_paid(cls, child_id):
        """
        Get total amount paid for a particular child policy
        """
        amounts = [t.amount for t in cls.query.filter_by(child_policy=child_id).all() if t.is_paid]
        return sum(amounts)
    
    @classmethod
    def extend_date_paid(cls):
        """In case of a refund, add the amount to be refunded to the policy transaction
            and extend the date due for the next payment"""
        pass
            
