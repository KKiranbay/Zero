import pygame

from singleton import singleton
import resources.colors as colors

@singleton
class Screen:
	def __init__(self, width: int = 0, height: int = 0) -> None:
		self.m_window: pygame.Surface = pygame.display.set_mode((width, height))

	def reset_window_fill(self):
		self.m_window.fill(colors.BLACK)