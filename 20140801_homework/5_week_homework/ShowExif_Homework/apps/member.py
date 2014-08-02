class Member(object):
	info = {}
	def __init__(self):
		self.info['id'] = ""
		self.info['pass'] = ""
	def set(self, user_id, user_pw):
		self.info['id'] = user_id
		self.info['pass'] = user_pw
	def get_id(self):
		return self.info['id']
	def get_pw(self):
		return self.info['pass']