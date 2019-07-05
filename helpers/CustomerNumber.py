import datetime


class CustomerNumber(object):
	def __init__(self, type_acronym, user_id, country_short_code):
		self.type_acronym = type_acronym
		self.user_id = user_id
		self.country_short_code = country_short_code

	def convert_user_id(self, user_id):
		user_id_str = str(self.user_id)
		return user_id_str.zfill(6)

	@staticmethod
	def get_current_year():
		today = datetime.datetime.now()
		return str(today.year)

	def generate_customer_number(self):
		cust_num_tuple = []
		cust_num_tuple.append(self.type_acronym)
		cust_num_tuple.append(self.get_current_year())
		cust_num_tuple.append(self.convert_user_id(self.user_id))
		cust_num_tuple.append(self.country_short_code)
		separator = '/'
		return separator.join(cust_num_tuple)
