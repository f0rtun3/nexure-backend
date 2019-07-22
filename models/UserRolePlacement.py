from app import db


class UserRolePlacement(db.Model):
    """
    Place users to a specified role
    """
    __tablename__ = 'user_role'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', onupdate='CASCADE', ondelete='CASCADE'))
    role_id = db.Column(db.Integer, db.ForeignKey(
        'role.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id

    def __repr__(self):
        return f"{self.user_id}"

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
    def fetch_role_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()