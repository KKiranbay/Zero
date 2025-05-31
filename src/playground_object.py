import pygame

from game import Game

class Playground_Object(pygame.sprite.Sprite):
	def __init__(self, pos_x: float, pos_y: float, size: float) -> None:
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((size, size))
		self.image.fill((255, 255, 255))

		self.m_size: float = size
		self.m_half_size: float = size // 2

		rect_left_top_x: float = pos_x - self.m_half_size
		rect_left_top_y: float = pos_y - self.m_half_size

		self.rect: pygame.Rect = pygame.Rect(rect_left_top_x, rect_left_top_y, self.m_size, self.m_size)
		self.m_pos = pygame.math.Vector2(pos_x, pos_y)

	def update(self, dt: float, game: Game):
		pass

	def setCenter(self, center: pygame.math.Vector2):
		self.rect.center = round(center)

	def setPos(self, x: float, y: float):
		self.m_pos = pygame.math.Vector2(x, y)
		self.setCenter(self.m_pos)

	def setDisplacement(self, displacement: pygame.math.Vector2):
		self.m_pos += displacement
		self.setCenter(self.m_pos)

	def check_and_clamp_ip_with_playground(self, playground_rect: pygame.Rect) :
		self.rect.clamp_ip(playground_rect)