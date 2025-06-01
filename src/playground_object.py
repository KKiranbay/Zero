import pygame

import resources.colors as colors

class Playground_Object(pygame.sprite.Sprite):
	def __init__(self, pos_x: float, pos_y: float, size: float) -> None:
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((size, size))
		self.image.fill(colors.WHITE)

		self.m_size: float = size
		self.m_half_size: float = size // 2

		self.m_pos = pygame.math.Vector2()
		self.rect: pygame.Rect = self.image.get_rect()
		self.setPos(pos_x, pos_y)

	def update(self, dt: float, game):
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

	def check_collide_with_playground(self, playground_rect: pygame.Rect) -> bool :
		return self.rect.colliderect(playground_rect)

	def check_fully_left_playground(self, playground_rect: pygame.Rect) -> bool :
		top_check: bool = playground_rect.top > self.rect.bottom
		bottom_check: bool = playground_rect.bottom < self.rect.top
		left_check: bool = playground_rect.left > self.rect.right
		right_check: bool = playground_rect.right < self.rect.left
		return top_check or bottom_check or left_check or right_check