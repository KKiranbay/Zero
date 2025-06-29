import pygame

import events_dictionary as events_dictionary

from controllers.game_controller import GameController

from ui.menu_uis.pause_menu_ui import PauseMenuUI, PauseMenuRequestEnum

from states_enum import StatesEnum

from states.state import State


class GameState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.MAIN_MENU

		self.m_game_controller: GameController | None = None

		self.m_is_paused = False
		self.m_pause_menu_ui = None

	def startup(self, persistent):
		super().startup(persistent)
		self.m_game_controller = GameController(self.screen)

		existing_game = self.persist.get("game")
		if existing_game:
			self.m_game_controller.set_game(existing_game)

			existing_spawn_controller = self.persist.get("spawn_controller")
			if existing_spawn_controller:
				self.m_game_controller.set_spawn_controller(existing_spawn_controller)
		else:
			self.m_game_controller.create_game()

		self.m_is_paused = False

		if self.previous_state == StatesEnum.MAIN_MENU:
			self.initialize_game_objects()
		elif self.previous_state == StatesEnum.LOAD_GAME_STATE:
			self.game_loaded_successfully = self.persist.get('game_loaded', None)
			if not self.game_loaded_successfully:
				self.initialize_game_objects()

	def initialize_game_objects(self):
		assert self.m_game_controller is not None

		self.m_game_controller.initialize_game_objects()
		self.m_game_controller.start_spawn_system()

	def check_events(self):
		if self.events.get_event(pygame.KEYDOWN) is None:
			return

		key_pressed = self.events.get_event(pygame.KEYDOWN).key

		if key_pressed == pygame.K_ESCAPE:
			if self.m_is_paused:
				self.resume_game()
			else:
				self.pause_game()

		if not self.m_is_paused:
			pass

	def pause_game(self):
		self.m_is_paused = True
		if self.m_pause_menu_ui is None:
			self.m_pause_menu_ui = PauseMenuUI()

	def resume_game(self):
		self.m_is_paused = False

	def save_game(self):
		if self.m_game_controller:
			self.m_game_controller.save_game()

	def update(self):
		if self.m_is_paused:
			self.handle_pause_menu()
			return

		if self.m_game_controller is None:
			return

		self.m_game_controller.update()

		if self.m_game_controller.has_game_restart_event():
			self.m_game_controller.clear_restart_event()
			self.persist = {
				'game_data': self.m_game_controller.get_game(),
			}
			self.next_state = StatesEnum.GAME_OVER
			self.done = True
			return



	def handle_pause_menu(self):
		if self.m_pause_menu_ui is None:
			return

		request = self.m_pause_menu_ui.get_ui_requests()

		if request == PauseMenuRequestEnum.RESUME:
			self.resume_game()
		elif request == PauseMenuRequestEnum.SAVE:
			self.save_game()
		elif request == PauseMenuRequestEnum.MAIN_MENU:
			self.persist = {
				'game_data': self.m_game_controller.get_game() if self.m_game_controller else None,
			}
			self.next_state = StatesEnum.MAIN_MENU
			self.done = True
		elif request == PauseMenuRequestEnum.EXIT_CONFIRMED:
			self.events.change_event(events_dictionary.EXIT_GAME_EVENT, True)

	def draw(self):
		self.screen.reset_window_fill()

		if self.m_game_controller is None:
			return

		self.m_game_controller.draw_game()

		if self.m_is_paused and self.m_pause_menu_ui:
			self.m_pause_menu_ui.draw()