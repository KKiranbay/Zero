from states.state import State
from states_enum import StatesEnum

class LoadGameState(State):
	def __init__(self):
		self.next_state: StatesEnum = StatesEnum.LOAD_GAME_STATE
		self.persist = None

	def startup(self, persistent):
		self.persist = persistent

	def check_events(self):
		pass

	def update(self):
		self.done = True
		self.next_state = StatesEnum.GAME_STATE
		pass

	def draw(self):
		pass