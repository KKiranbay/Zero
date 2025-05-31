import pygame

import colors

class Character:
	def __init__(self, char_x: float, char_y: float, char_size: int, char_speed: float):
		self.m_char_size: int = char_size
		self.m_char_speed: float = char_speed

		self.m_pos_x: float = char_x
		self.m_pos_y: float = char_y

		self.m_char_size_half = self.m_char_size // 2

		start_char_rect_left_top_x: float = self.m_pos_x - self.m_char_size_half
		start_char_rect_left_top_y: float = self.m_pos_y - self.m_char_size_half

		self.m_rect = pygame.Rect(start_char_rect_left_top_x, start_char_rect_left_top_y, self.m_char_size, self.m_char_size)

	def move_char(self, keys, dt: float):
		if keys[pygame.K_a]:
			self.m_pos_x -= self.m_char_speed * dt
		if keys[pygame.K_d]:
			self.m_pos_x += self.m_char_speed * dt

		if keys[pygame.K_w]:
			self.m_pos_y -= self.m_char_speed * dt
		if keys[pygame.K_s]:
			self.m_pos_y += self.m_char_speed * dt

		self.m_rect.x = self.m_pos_x - self.m_char_size_half
		self.m_rect.y = self.m_pos_y - self.m_char_size_half

	def check_and_clamp_ip(self, playground_rect: pygame.Rect):
		self.m_rect.clamp_ip(playground_rect)

		self.m_pos_x = self.m_rect.x + self.m_char_size_half
		self.m_pos_y = self.m_rect.y + self.m_char_size_half

	def draw_char(self, ground: pygame.Surface):
		pygame.draw.rect(ground, colors.DARK_GREEN, (self.m_rect.x, self.m_rect.y, self.m_char_size, self.m_char_size))
