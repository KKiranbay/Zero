from states.state import State
from states_enum import StatesEnum

from systems.load_game_system import LoadGameSystem

class LoadGameState(State):
	def __init__(self):
		self.next_state: StatesEnum = StatesEnum.LOAD_GAME_STATE
		self.persist = None

		self.m_load_game_system = LoadGameSystem()

	def startup(self, persistent):
		self.persist = persistent

	def check_events(self):
		pass

	def update(self):
		self.done = True
		self.next_state = StatesEnum.GAME_STATE

		game_data = self.m_load_game_system.load_game_data()
		if game_data is None:
			return

		successful = self.m_load_game_system.restore_game_state(game_data)

		self.persist = {
			'game_loaded': successful,
		}

		pass

	def draw(self):
		pass