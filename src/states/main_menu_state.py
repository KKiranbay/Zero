import pygame

from states_enum import StatesEnum

from states.state import State

class MainMenuState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.GAME_STATE

	def startup(self, persistent):
		self.persist = persistent
		print("Main Menu is up!")

	def check_events(self):
		if not self.events.exists(pygame.KEYDOWN):
			return

		if self.events.get_event(pygame.KEYDOWN) == None:
			return

		if self.events.get_event(pygame.KEYDOWN).key == pygame.K_RETURN:
			self.done = True

	def draw(self):
		self.screen.get_window().fill((0, 255, 0))