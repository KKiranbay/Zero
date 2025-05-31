import pygame

import colors

from playground_object import Playground_Object

class Projectile(Playground_Object):
	def __init__(self, direction: pygame.math.Vector2, projectile_x, projectile_y, projectile_size) -> None:
		super().__init__(projectile_x, projectile_y, projectile_size)
		self.m_direction: pygame.math.Vector2 = direction
		self.image.fill(colors.PINK_RED)
		pass

	def update(self, dt: float, game):
		displacement = self.m_direction * 1000 * dt
		self.setDisplacement(displacement)