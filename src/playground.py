import pygame

class Playground:
	def __init__(self, parent: pygame.Surface, width: int, height: int, color: tuple):
		self.m_screen_rect: pygame.Rect = pygame.Rect(0, 0, width, height)
		self.m_game_rect: pygame.Rect = pygame.Rect(0, 0, width, height)
		self.m_surface: pygame.Surface = pygame.Surface((width, height))
		self.m_color: tuple = color

		self.m_surface.fill(color)

		self.m_parent: pygame.Surface = parent


	def draw_playground(self):
		self.m_parent.blit(self.m_surface, self.m_screen_rect.topleft)

	def move_relative_to_cam(self, cam_x: float, cam_y: float):
		self.m_screen_rect.x = self.m_parent.width // 2 - cam_x
		self.m_screen_rect.y = self.m_parent.height // 2 - cam_y