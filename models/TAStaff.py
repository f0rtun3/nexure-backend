from database.db import db
from models.UserPermissions import UserPermissions

class TAStaff(db.Model):
    __tablename__ = 'ta_staff'

    id = db.Column(db.Integer, primary_key=True,
                   autoincrement=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE', onupdate='CASCADE'))
    agent_id = db.Column(db.Integer, db.ForeignKey(
        'tied_agent.id', ondelete='CASCADE', onupdate='CASCADE'))
    ta_customer = db.relationship("TACustomer", backref="ta_customer_member")
    active = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, agent_id):
        self.user_id = user_id
        self.agent_id = agent_id

    def serialize(self):
        result = self.user.serialize()
        return {
            "id": self.user_id,
            "first_name": result['profile_details']['first_name'],
            "last_name": result['profile_details']['last_name'],
            "email": result['profile_details']['email'],
            "phone": result['profile_details']['phone'],
            "is_active": self.active,
            "permissions": UserPermissions.get_permission_by_user_id(self.user_id)
        }

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
    def fetch_staff_by_id(cls, agent_id):
        return cls.query.filter_by(agent_id=agent_id, active=True).first()

    @classmethod
    def fetch_agent_by_staff(cls, staff_id):
        agent = cls.query.filter_by(user_id=staff_id, active=True).first()
        return agent.user_id

    @classmethod
    def fetch_all_staff_ids(cls, agency_id):
        staff = cls.query.filter_by(agent_id=agency_id, active=True)
        staff_ids = []
        for i in staff:
            staff_ids.append(i.user_id)
        return staff_ids

    @classmethod
    def fetch_staff_by_agency_id(cls, agency_id):
        return [staff.serialize() for staff in cls.query.filter_by(agency_id).all()]
    
    @classmethod
    def get_staff_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()
    
    @classmethod
    def check_account(cls, staff_id):
        # fetch staff account by the staff account user id
        # check if staff status is active
        staff = cls.query.filter_by(user_id=staff_id).first()
        return staff.active
