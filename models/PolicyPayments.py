from database.db import db


class PolicyPayments(db.Model):
    """
    Describes all the transactions for a particular child policy, for both credit(payments) and debit(refunds)
    """
    __tablename__ = 'policy_payments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # transaction type can either be mpesa, bankers cheque, refund
    transaction_type = db.Column(db.String(10))
    amount = db.Column(db.Float, nullable=False)
    customer_no = db.Column(db.String(50))
    child_policy_id = db.Column(db.Integer, db.ForeignKey(
        'child_policy.id', ondelete='CASCADE', onupdate='CASCADE'))
    next_date = db.Column(db.DateTime)
    amount_due = db.Column(db.Float, nullable=False, default=0)
    # could be the mpesa code, or cheque number
    transaction_code = db.Column(db.String(25))
    date_paid = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, transaction_type, amount, customer_no, child_policy_id, next_date, amount_due, transaction_code):
        self.transaction_type = transaction_type
        self.amount = amount
        self.customer_no = customer_no
        self.child_policy_id = child_policy_id
        self.next_date = next_date
        self.amount_due = amount_due
        self.transaction_code = transaction_code

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
        amounts = [t.amount for t in cls.query.filter_by(child_policy=child_id).all()]
        return sum(amounts)

    @classmethod
    def get_payments_history(cls, child_id):
        return [installment.serialize() for installment in cls.query.filter_by(child_id=child_id).all()]