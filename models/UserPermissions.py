from database.db import db


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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_permission_by_user_id(cls, uid):
        permissions_list = cls.query.filter_by(user_id=uid).all()
        permission_ids = []
        for i in permissions_list:
            permission_ids.append(str(i.permission_id))
        return ''.join(permission_ids)

    @classmethod
    def get_specific_permission(cls, permission_id, user_id):
        permission = cls.query.filter_by(
            user_id=user_id, permission_id=permission_id).first()
        return permission

    @classmethod
    def delete_user_permissions(cls, user_id, permissions):
        """
        delete user permissions where id matches in array
        :param user_id {Int} user id whom we are deleting permissions
        :param permissions {IntSet}
        """
        user_acc =  cls.query.filter(cls.permission_id.in_(permissions), cls.user_id==user_id)\
                    .delete(synchronize_session='fetch')
        db.session.commit()
