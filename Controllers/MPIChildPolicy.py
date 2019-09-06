from models.ChildPolicy import ChildPolicy


class ChildController:
    """
    Controller for creating, updating, renewing and cancelling child policy
    """

    def __init__(self, cp_number):
        self.cp_number = cp_number
        self.child_policy_id = None

    def add_new_policy(self, data):
        """
        Create a new policy.
        """
        new_child = ChildPolicy(data)
        new_child.save()
        return new_child.id

    def extend(self):
        """
        Add new provision for losses outside the original circumstances
        """
        
        pass

    def add_extensions(self):
        """
        Append extensions
        """
        pass

    def add_benefits(self):
        """
        Append benefits
        """
        pass

    def renew(self):
        """
        Renew policy if expired 
        """
        pass

    def cancel(self):
        """
        Cancel existing policy and return a refund if needed
        """
        pass

    def generate_policy_number():
        pass
