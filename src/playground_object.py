import pygame

import resources.colors as colors

class Playground_Object(pygame.sprite.Sprite):
	def __init__(self, pos_x: float, pos_y: float, size: float) -> None:
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((size, size))
		self.image.fill(colors.WHITE)

		self.m_size: float = size
		self.m_half_size: float = size // 2

		self.m_pos = pygame.math.Vector2(pos_x, pos_y)
		self.rect: pygame.Rect = self.image.get_rect()
		self.rect.centerx = round(pos_x)
		self.rect.centery = round(pos_y)

	def update(self, dt_s: float, game):
		pass

	def setCenter(self, center: pygame.math.Vector2):
		self.rect.centerx = round(center.x)
		self.rect.centery = round(center.y)

	def setPos(self, x: float, y: float):
		self.m_pos.update(x, y)
		self.setCenter(self.m_pos)

	def setDisplacement(self, displacement: pygame.math.Vector2):
		self.m_pos += displacement
		self.setCenter(self.m_pos)

	def check_and_clamp_ip_with_playground(self, playground_rect: pygame.Rect) :
		top_check: bool = playground_rect.top >= self.m_pos.y - self.m_half_size
		bottom_check: bool = playground_rect.bottom <= self.m_pos.y + self.m_half_size
		left_check: bool = playground_rect.left >= self.m_pos.x - self.m_half_size
		right_check: bool = playground_rect.right <= self.m_pos.x + self.m_half_size

		if (top_check or bottom_check or left_check or right_check):
			self.rect.clamp_ip(playground_rect)
			self.m_pos.update(self.rect.centerx, self.rect.centery)

	def check_fully_left_playground(self, playground_rect: pygame.Rect) -> bool :
		top_check: bool = playground_rect.top > self.m_pos.y + self.m_half_size
		bottom_check: bool = playground_rect.bottom < self.m_pos.y - self.m_half_size
		left_check: bool = playground_rect.left > self.m_pos.x + self.m_half_size
		right_check: bool = playground_rect.right < self.m_pos.x - self.m_half_size
		return top_check or bottom_check or left_check or right_check