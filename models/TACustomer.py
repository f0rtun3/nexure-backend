from database.db import db
from helpers import helpers as helper
from models.IndividualCustomer import IndividualCustomer
from models.OrganizationCustomer import OrganizationCustomer


class TACustomer(db.Model):
    """
    Affiliation between customers and tied agents
    """
    __tablename__ = 'ta_customer'

    id = db.Column(db.Integer, autoincrement=True,
                   primary_key=True, nullable=False)
    customer_number = db.Column(db.String(50))
    agent_id = db.Column(db.Integer, db.ForeignKey(
        'tied_agent.id', onupdate='CASCADE', ondelete='CASCADE'))
    staff_id = db.Column(db.Integer, db.ForeignKey(
        'ta_staff.id', onupdate='CASCADE'), nullable=True)
    date_affiliated = db.Column(db.DateTime, default=db.func.now())
    # we need to know whether the affiliation is active or not
    status = db.Column(db.Boolean, default=True)

    def __init__(self, customer_number, agent_id, staff_id=None):
        self.customer_number = customer_number
        self.agent_id = agent_id
        self.staff_id = staff_id

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @classmethod
    def get_affiliation(cls, agent_id):
        agent_data = cls.query.filter_by(agent_id=agent_id).all()
        return agent_data

    @classmethod
    def check_duplicate_affiliation(cls, agent_id, customer_number):
        if cls.query.filter_by(agent_id=agent_id, customer_number=customer_number).first():
            return True
        return False

    @classmethod
    def get_affiliation_by_customer(cls, cust_no):
        return cls.query.filter_by(customer_number=cust_no).first()

    @classmethod
    def get_customers(cls, agent_id):
        """
        Get broker specific customer details according to the Tied Agent Details
        :param agent_id:
        :return:
        """
        customer_numbers = [str(customer.customer_number)
                            for customer in cls.query.filter_by(agent_id=agent_id).all()]
        customer_data = {'individual':[], 'organization':[]}
        for customer_number in customer_numbers:
            customer_type = helper.get_customer_type(customer_number)
            if customer_type == 'IN':
                customer_details = IndividualCustomer.query.filter_by(
                    customer_number=customer_number).first()
                customer_data['individual'].append(customer_details.serialize())
            else:
                customer_details = OrganizationCustomer.query.filter_by(
                    customer_number=customer_number).first()
                customer_data['organization'].append(customer_details.serialize())

        return customer_data

    @classmethod
    def get_number_by_customer_id(cls, customer_id, agent_id=None, staff_id=None):
        customer_numbers = [customer.customer_number for customer in cls.query.filter_by(agent_id=agent_id, staff_id=staff_id).all() if type(
            customer.customer_number) is str and int(customer.customer_number.split("/")[2]) == customer_id]

        return customer_numbers[0]
