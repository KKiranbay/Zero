import pygame

event_id: int = pygame.USEREVENT
def generateEventId():
	global event_id
	event_id += 1
	return event_id

RESTART_EVENT: int		=	generateEventId()
SPAWN_NPC_EVENT: int	=	generateEventId()
CHAR_NO_DIED_EVENT: int	=	generateEventId()


class GameEventsDictionary:
	def __init__(self):
		self.m_events: dict = {}
		self.resetEvents()

	def exists(self, event: int) -> bool:
		return event in self.m_events

	def resetEvents(self):
		self.m_events[pygame.MOUSEBUTTONDOWN] = False
		self.m_events[pygame.MOUSEBUTTONUP] = False

		self.m_events[SPAWN_NPC_EVENT] = False
		self.m_events[CHAR_NO_DIED_EVENT] = []
		self.m_events[RESTART_EVENT] = False

	def changeEvent(self, event: int, value):
		self.m_events[event] = value

	def getEvent(self, event: int):
		return self.m_events[event]