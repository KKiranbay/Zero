from states_enum import StatesEnum

class State:
	def __init__(self):
		self.done: bool = False
		self.quit: bool = False

		self.next_state: StatesEnum
		self.previous_state: StatesEnum

	def startup(self, persistent):
		self.persist = persistent

	def get_event(self, event):
		pass

	def update(self, dt):
		pass

	def draw(self, surface):
		pass