# Game Over State handles the end-game UI and user decisions for restart/exit.
# Key Pygame-ce elements:
# - State pattern implementation following the existing architecture
# - UI rendering and event handling for game over screen
# - State transitions back to game or main menu

import pygame

from ui.game_over_ui import GameOverUI
from states_enum import StatesEnum
from states.state import State


class GameOverState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.MAIN_MENU

	def startup(self, persistent):
		self.persist = persistent

		self.m_game_data = persistent.get('game_data', None)

		self.m_game_over_ui = GameOverUI()

	def check_events(self):
		if self.events.get_event(pygame.KEYDOWN) is None:
			return

		if self.events.get_event(pygame.KEYDOWN).key == pygame.K_ESCAPE:
			self.next_state = StatesEnum.MAIN_MENU
			self.done = True

	def update(self):
		restart_clicked, main_menu_clicked = self.m_game_over_ui.update()

		if restart_clicked:
			self.next_state = StatesEnum.GAME_STATE
			self.done = True
		elif main_menu_clicked:
			self.next_state = StatesEnum.MAIN_MENU
			self.done = True

	def draw(self):
		self.screen.reset_window_fill()

		if self.m_game_data:
			self.m_game_data.draw()

		self.m_game_over_ui.draw()
