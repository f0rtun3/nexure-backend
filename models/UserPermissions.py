from app import db

class UserPermissions(db.Model):
    __tablename__ = 'user_permission'

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', onupdate='CASCADE', ondelete='CASCADE'))
    permission_id = db.Column(db.Integer, db.ForeignKey(
        'permission.id', onupdate='CASCADE', ondelete='CASCADE'))

    def __init__(self, user_id, permission_id):
        self.user_id = user_id
        self.permission_id = permission_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        db.session.commit()

    @classmethod
    def get_permission_by_user_id(cls, id):
        permissions_list = cls.query.filter_by(user_id=id).all()
        permission_ids = []
        for i in permissions_list:
            permission_ids.append(str(i.permission_id))
        return ''.join(permission_ids)