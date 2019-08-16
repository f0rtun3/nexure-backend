from app import db

class ChildPolicy(db.Model):
    """Stores all information regarding a particular child policy to which a customer is enrolled, linking all their details as well"""
    id = db.Column(
        db.Integer, autoincrement=True, primary_key=True)