import pygame

from singleton import singleton

event_id: int = pygame.USEREVENT
def generateEventId():
	global event_id
	event_id += 1
	return event_id

EXIT_GAME_EVENT: int	=	generateEventId()
RESTART_GAME_EVENT: int	=	generateEventId()

SPAWN_NPC_EVENT: int	=	generateEventId()
CHAR_NO_DIED_EVENT: int	=	generateEventId()

# Holds the current frames events inside a dictionary. Singleton
@singleton
class EventsDictionary:
	def __init__(self):
		self.m_events: dict = {}
		self.reset_events()

	def exists(self, event: int) -> bool:
		return event in self.m_events

	def reset_events(self):
		# pygame events
		self.m_events[pygame.MOUSEBUTTONDOWN] = None
		self.m_events[pygame.MOUSEBUTTONUP] = None

		self.m_events[pygame.KEYDOWN] = None

		# custom events - only reset if not active
		if not self.m_events.get(EXIT_GAME_EVENT, False):
			self.m_events[EXIT_GAME_EVENT] = False

		if not self.m_events.get(RESTART_GAME_EVENT, False):
			self.m_events[RESTART_GAME_EVENT] = False

		self.m_events[SPAWN_NPC_EVENT] = False

		if not self.m_events.get(CHAR_NO_DIED_EVENT, []):
			self.m_events[CHAR_NO_DIED_EVENT] = []

	def change_event(self, event: int, value):
		self.m_events[event] = value

	def get_event(self, event: int):
		return self.m_events[event]

	def clear_persistent_event(self, event: int):
		"""Explicitly clear a persistent event after it has been processed"""
		if event == EXIT_GAME_EVENT or event == RESTART_GAME_EVENT or event == CHAR_NO_DIED_EVENT:
			self.m_events[event] = False