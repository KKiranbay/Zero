from states_enum import StatesEnum

from events_dictionary import EventsDictionary
from screen import Screen

class State:
	def __init__(self):
		self.done: bool = False

		self.next_state: StatesEnum
		self.previous_state: StatesEnum

		self.events: EventsDictionary = EventsDictionary()
		self.screen: Screen = Screen()
		self.persist = {}

	def startup(self, persistent):
		self.persist = persistent

	def check_events(self):
		pass

	def update(self):
		pass

	def draw(self):
		pass