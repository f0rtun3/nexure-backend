import datetime

class PolicyNoGenerator(object):
    """
    Defines a standard format to generate the policy numbers
    the class is able to generate master policy number with format: MS/MPI/SN/YEAR
    or chile policy number with format CH/PCI/SN/YEAR
    @param policy_type {String}    the type of policy number to generate
    @param mpi {String}     policy class code
    @param pci {String}     policy child code
    @param prev_index       the serial numbers are generated sequentially, the last index of the policy must be entered
    """
    def __init__(self, policy_type, prev_index=0):
        self.policy_type = policy_type
        self.prev_index = prev_index
        self.pci = None
        self.mpi = None

    def set_mpi(self, mpi):
        """
        add the class code if the policy number to generate
        is a master policy
        :param mpi:
        :return:
        """
        self.mpi = mpi

    def set_pci(self, pci):
        """
        add the product code if the number to generate
        is a child policy
        :param pci:
        :return:
        """
        self.pci = pci

    @staticmethod
    def get_curr_year():
        """
        this is a static method to return the current year
        in which the policy number is generated
        :return {String}    current year
        """
        today = datetime.datetime.now()
        return str(today.year)

    def generate_serial(self):
        """
        returns the serial number to which a policy number is generated
        :return {String}    serial number
        """
        serial_no = int(self.prev_index)+1
        return str(serial_no).zfill(8)

    def generate_policy_no(self):
        """
        generate the policy number (master/child)
        :return {String}    policy number
        """
        policy_no = []
        serial_no = self.generate_serial()
        curr_year = self.get_curr_year()
        if self.policy_type == "MS":
            policy_no.extend([self.policy_type, self.mpi, serial_no, curr_year])
        elif self.policy_type == "CH":
            policy_no.extend([self.policy_type, self.pci, serial_no, curr_year])
        else:
            return

        separator = '/'

        return separator.join(policy_no)
