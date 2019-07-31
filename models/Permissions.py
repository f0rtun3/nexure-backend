from app import db


class Permissions(db.Model):

    __tablename__ = 'permission'
    #  stores the list of permissions
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    permission_name = db.Column(db.String(100))
    user_permission = db.relationship('UserPermissions', backref='permissions')

    def __init__(self, permission_name, user_id):
        self.permission_name = permission_name
        self.user_id = user_id

    def __str__(self):
        return f"{self.id}"
