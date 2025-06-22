import pygame

import events_dictionary as events_dictionary
from events_dictionary import EventsDictionary

from screen import Screen

from states_enum import StatesEnum
from states.state import State
from states.game_state import GameState
from states.main_menu_state import MainMenuState

from time_handler import Time_Handler


class GameController:
	def __init__(self):
		pygame.init()
		self.m_screen: Screen = Screen(800, 600)
		pygame.display.set_caption("Movable Character with Toggleable Camera")

		self.time_handler: Time_Handler = Time_Handler()
		self.MAX_HZ: int = 0
		self.desired_framerate: float = 0

		self.set_desired_hz(10000)

		self.quit: bool = False
		self.states: dict[StatesEnum, State] = {
			StatesEnum.MAIN_MENU:	MainMenuState(),
			StatesEnum.GAME_STATE:	GameState()
		}

		self.current_state: StatesEnum = StatesEnum.MAIN_MENU
		self.state: State = self.states[self.current_state]
		self.state.startup({})

		self.game_events: EventsDictionary = EventsDictionary()

	def event_loop(self):
		pygame_events = pygame.event.get()
		for pygame_event in pygame_events:
			if pygame_event.type == pygame.QUIT:
				self.quit = True
			elif self.game_events.exists(pygame_event.type):
				self.game_events.change_event(pygame_event.type, pygame_event)

		self.state.check_events()

		if self.game_events.get_event(events_dictionary.EXIT_GAME_EVENT):
			self.quit = True

	def update(self):
		if self.state.done:
			self.change_state()
		self.state.update()

	def draw(self):
		self.m_screen.reset_window_fill()
		self.state.draw()
		pygame.display.flip()

	def change_state(self):
		previous_state: StatesEnum = self.current_state
		self.current_state = self.state.next_state
		persistent_data = self.state.persist
		self.state.done = False
		self.state = self.states[self.current_state]
		self.state.startup(persistent_data)
		self.state.previous_state = previous_state

	def run(self):
		while not self.quit:
			self.time_handler.tick(self.desired_framerate)
			self.game_events.reset_events()
			self.event_loop()
			self.update()
			self.draw()

	def set_desired_hz(self, hz: int):
		self.MAX_HZ = hz
		if self.MAX_HZ != 0:
			self.desired_framerate = 1.0 / self.MAX_HZ
		else:
			self.desired_framerate = 0

if __name__ == "__main__":
	app = GameController()
	app.run()
	pygame.quit()
