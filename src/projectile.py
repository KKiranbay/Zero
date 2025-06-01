import pygame

import resources.colors as colors

from playground_object import Playground_Object
from game import Game

class Projectile(Playground_Object):
	def __init__(self, direction: pygame.math.Vector2, projectile_x, projectile_y, projectile_size) -> None:
		super().__init__(projectile_x, projectile_y, projectile_size)
		self.m_direction: pygame.math.Vector2 = direction
		self.image.fill(colors.PINK_RED)
		pass

	def update(self, dt: float, game: Game):
		displacement = self.m_direction * 1000 * dt
		self.setDisplacement(displacement)

		if self.check_fully_left_playground(game.m_playground.m_game_world_rect):
			print("killed")
			self.kill()

	def on_collision_with_npc(self, game, collided_with: list[pygame.sprite.Sprite]):
		print(f"Projectile collided with: {collided_with}")
