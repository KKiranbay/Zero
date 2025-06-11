import pygame

from states_enum import StatesEnum

from states.state import State

class GameState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.MAIN_MENU

	def startup(self, persistent):
		self.persist = persistent

		# init

		print("Starting a new game!")

	def get_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				self.done = True

	def update(self, dt):
		pass

	def draw(self, surface):
		surface.fill((0, 0, 255)) # Blue screen for the game