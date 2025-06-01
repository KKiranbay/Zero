import pygame

import resources.colors as colors
import helper

from game import Game
from playground import Playground
from playground_object import Playground_Object
from projectile import Projectile

class Character(Playground_Object):
	def __init__(self, char_x: float, char_y: float, char_size: int, char_speed: float):
		super().__init__(char_x, char_y, char_size)
		self.m_char_speed: float = char_speed
		self.image.fill(colors.DARK_GREEN)

	def update(self, dt: float, game: Game):
		self.checkShoot(game)
		self.move_char(dt, game)
		pass

	def move_char(self, dt: float, game: Game):
		original_x = self.rect.centerx
		original_y = self.rect.centery

		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.rect.centerx -= self.m_char_speed * dt
		if keys[pygame.K_d]:
			self.rect.centerx += self.m_char_speed * dt

		if keys[pygame.K_w]:
			self.rect.centery -= self.m_char_speed * dt
		if keys[pygame.K_s]:
			self.rect.centery += self.m_char_speed * dt

	def checkShoot(self, game: Game):
		for event in game.m_events:
			if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
				self.shoot(game)

	def shoot(self, game: Game):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - game.get_screen_offset()
		direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.rect.center
		norm_direction: pygame.math.Vector2 = helper.normalize_vector(direction)

		projectile: Projectile = Projectile(norm_direction, self.rect.centerx, self.rect.centery, 10)
		game.add_projectile_object(projectile)