import pygame

class Playground:
	def __init__(self, parent: pygame.Surface, width: int, height: int, color: tuple):
		self.m_game_world_rect: pygame.Rect = pygame.Rect(0, 0, width, height)
		self.m_color: tuple = color

		self.m_surface: pygame.Surface = pygame.Surface((width, height))
		self.m_surface.fill(color)

		self.m_parent: pygame.Surface = parent

	def refill_playground(self):
		self.m_surface.fill(self.m_color)

	def draw_playground(self, camera_offset: pygame.math.Vector2):
		self.m_parent.blit(self.m_surface, camera_offset)
