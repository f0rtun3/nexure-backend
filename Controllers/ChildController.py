"""
This controller should create a child policy, update it and extend it
"""
from models.ChildPolicy import ChildPolicy
from models.Driver import Driver
from models.VehicleDetails import VehicleDetails
from models.VehicleModifications import VehicleModifications
from models.ICBenefits import ICBenefits
from models.ICExtensions import ICExtensions
from models.PolicyBenefits import PolicyBenefits
from models.PolicyExtensions import PolicyExtensions
from models.Benefits import Benefit
from models.Extensions import Extension
from models.InsuranceCompany import InsuranceCompany


class ChildController:
    def __init__(self):
        self.vehicle_id = None
        self.driver_id = None

    def add_driver_details(self, first_name, last_name, gender, phone, birth_date):
        """
        Handles the driver details related to a particular vehicle
        """
        driver = Driver(first_name, last_name, gender, phone, birth_date)
        driver.save()
        self.driver_id = driver.id

    def add_vehicle_details(self, reg_number, model, color, body_type, origin, sum_insured, no_of_seats,
                            manufacture_year, engine_capacity):
        """
        Creates a vehicle object tied to a particular child policy.
        Uses the 'driver_id' to identify the vehicle driver
        """
        new_car = VehicleDetails(reg_number, model, color, body_type, origin, sum_insured,
                                 self.driver_id, no_of_seats, manufacture_year, engine_capacity)
        new_car.save()
        self.vehicle_id = new_car.id

    def add_modifications(self, accessory_name, make, estimated_value, serial_no):
        new_modification = VehicleModifications(
            accessory_name, make, estimated_value. serial_no, self.vehicle_id)
        new_modification.save()

    def create_child_policy(self, policy_number, customer_number, rate, date_expiry, premium_amount, transaction_type,
                            agency_id, associated_company, pricing_model, master_id, subclass):
        # Get insurance company given the company details
        new_company = InsuranceCompany.get_by_associated_company(
            associated_company)

        # create child policy
        new_child = ChildPolicy(
            policy_number,
            self.vehicle_id,
            customer_number,
            rate,
            date_expiry,
            premium_amount,
            transaction_type,
            agency_id,
            new_company.id,
            pricing_model,
            master_id,
            subclass
        )
        new_child.save()
        return new_child.id

    @staticmethod
    def add_benefits(data, child_id):
        for i in data:
            benefit = Benefit.get_benefit_by_name(
                i["name"])
            ic_benefit = ICBenefits.get_ic_benefit(benefit.id)
            policy_benefit = PolicyBenefits(
                child_id, ic_benefit.id, i["value"])
            policy_benefit.save()

    @staticmethod
    def add_extensions(data, child_id):
        for i in data:
            extension = Extension.get_extension_id_by_name(
                i["name"])
            ic_extension = ICExtensions.get_ic_extension(
                extension.id)
            policy_extension = PolicyExtensions(
                child_id, ic_extension, i["value"])
            policy_extension.save()
