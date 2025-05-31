import pygame

import colors

from playground import Playground
from playground_object import Playground_Object

class Character(Playground_Object):
	def __init__(self, char_x: float, char_y: float, char_size: int, char_speed: float):
		super().__init__(char_x, char_y, char_size)
		self.m_char_speed: float = char_speed
		self.image.fill(colors.DARK_GREEN)

	def update(self, dt, playground):
		keys = pygame.key.get_pressed()

		self.move_char(keys, dt, playground)
		pass

	def move_char(self, keys, dt: float, playground: Playground):
		original_x = self.m_pos_x
		original_y = self.m_pos_y

		if keys[pygame.K_a]:
			self.m_pos_x -= self.m_char_speed * dt
		if keys[pygame.K_d]:
			self.m_pos_x += self.m_char_speed * dt

		if keys[pygame.K_w]:
			self.m_pos_y -= self.m_char_speed * dt
		if keys[pygame.K_s]:
			self.m_pos_y += self.m_char_speed * dt

		self.rect.x = self.m_pos_x - self.m_half_size
		self.rect.y = self.m_pos_y - self.m_half_size

		self.check_and_clamp_ip_with_playground(playground.m_game_rect)
