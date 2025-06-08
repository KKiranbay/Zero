import pygame

import resources.colors as colors

class Playground_Object(pygame.sprite.Sprite):
	def __init__(self, pos: pygame.Vector2, size: pygame.Vector2) -> None:
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((size.x, size.y), pygame.SRCALPHA)
		self.image.fill(colors.WHITE)

		self.m_size: pygame.Vector2 = pygame.Vector2(size)
		self.m_half_size: pygame.Vector2 = self.m_size / 2

		self.m_pos = pygame.math.Vector2(pos)
		self.rect: pygame.Rect = self.image.get_rect()
		self.rect.centerx = round(pos.x)
		self.rect.centery = round(pos.y)

	def update(self, dt_s: float, game):
		pass

	def updateCenterDependingOnPos(self):
		self.rect.centerx = round(self.m_pos.x)
		self.rect.centery = round(self.m_pos.y)

	def setCenter(self, center: pygame.math.Vector2):
		self.rect.centerx = round(center.x)
		self.rect.centery = round(center.y)

	def setPos(self, x: float, y: float):
		self.m_pos.update(x, y)
		self.updateCenterDependingOnPos()

	def setDisplacement(self, displacement: pygame.math.Vector2):
		self.m_pos += displacement
		self.updateCenterDependingOnPos()

	def check_and_clamp_ip_with_rect(self, rect: pygame.Rect) :
		top_check: bool = rect.top > self.m_pos.y - self.m_half_size.y
		bottom_check: bool = rect.bottom < self.m_pos.y + self.m_half_size.y
		left_check: bool = rect.left > self.m_pos.x - self.m_half_size.x
		right_check: bool = rect.right < self.m_pos.x + self.m_half_size.x

		if (top_check):
			self.m_pos.y = rect.top + self.m_half_size.y

		if (bottom_check):
			self.m_pos.y = rect.bottom - self.m_half_size.y

		if (left_check):
			self.m_pos.x = rect.left + self.m_half_size.x

		if (right_check):
			self.m_pos.x = rect.right - self.m_half_size.x

		if (top_check or bottom_check or left_check or right_check):
			self.updateCenterDependingOnPos()

	def check_fully_left_rect(self, rect: pygame.Rect) -> bool :
		top_check: bool = rect.top > self.m_pos.y + self.m_half_size.y
		bottom_check: bool = rect.bottom < self.m_pos.y - self.m_half_size.y
		left_check: bool = rect.left > self.m_pos.x + self.m_half_size.x
		right_check: bool = rect.right < self.m_pos.x - self.m_half_size.x
		return top_check or bottom_check or left_check or right_check