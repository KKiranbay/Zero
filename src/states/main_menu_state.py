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

	def get_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RETURN:
				self.done = True

	def draw(self, surface):
		surface.fill((0, 255, 0))