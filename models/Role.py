from app import db


class Role(db.Model):
    """
    Pre defined list of roles in nexure for permission throttling
    """
    __tablename__ = 'role'

    # the role name will help us know what permissions to grant the user
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    role_name = db.Column(db.String(3), nullable=False, unique=True)
    # define the relationship to the user role placement
    user_role = db.relationship("UserRolePlacement", backref="role")

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return f"{self.role_name}"

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
    def fetch_all_roles(cls):
        role_rows = cls.query.all()
        roles = [{
            "role_name": role.role_name
        } for role in role_rows]

        return roles

    @classmethod
    def fetch_role_by_id(cls, role_id):
        # Get user role by id
        role_row = cls.query.filter_by(id=role_id).first()
        return role_row.role_name

    @classmethod
    def fetch_role_by_name(cls, role_name):
        # Get user role by name
        role_row = cls.query.filter_by(role_name=role_name).first()
        return role_row.id
