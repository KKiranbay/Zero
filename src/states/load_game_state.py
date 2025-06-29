from states.state import State
from states_enum import StatesEnum

from controllers.game_controller import GameController
from systems.load_game_system import LoadGameSystem

class LoadGameState(State):
	def __init__(self):
		super().__init__()
		self.next_state: StatesEnum = StatesEnum.LOAD_GAME_STATE

		self.m_game_controller: GameController | None = None
		self.m_load_game_system = LoadGameSystem()

	def startup(self, persistent):
		super().startup(persistent)

		self.m_game_controller = GameController(self.screen)

	def check_events(self):
		pass

	def update(self):
		self.done = True
		self.next_state = StatesEnum.GAME_STATE

		if self.m_game_controller is None:
			self.persist = {
				'game_loaded': False,
			}
			return

		game_data = self.m_load_game_system.load_game_data()
		if game_data is None:
			self.persist = {
				'game_loaded': False,
			}
			return

		# Use GameController to load game state (includes spawn controller restoration)
		successful = self.m_game_controller.load_game_from_save_data(game_data)

		self.persist = {
			'game_loaded': successful,
			'game': self.m_game_controller.get_game(),
			'spawn_controller': self.m_game_controller.get_spawn_controller(),
		}

	def draw(self):
		pass