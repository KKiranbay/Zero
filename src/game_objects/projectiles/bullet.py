import pygame

import resources.colors as colors

from game_objects.playground_object import Playground_Object
from game import Game

class Bullet(Playground_Object):
	def __init__(self, direction: pygame.math.Vector2, projectile_pos:  pygame.Vector2, projectile_size: pygame.Vector2) -> None:
		super().__init__(projectile_pos, projectile_size)
		self.m_direction: pygame.math.Vector2 = pygame.math.Vector2(direction)
		self.image.fill(colors.PINK_RED)
		pass

	def update(self, dt_s: float, game: Game):
		displacement = self.m_direction * 1000.0 * dt_s
		self.setDisplacement(displacement)

		if self.check_fully_left_rect(game.m_playground.m_game_world_rect):
			self.kill()

	def on_collision_with_npc(self, game, collided_with: list[pygame.sprite.Sprite]):
		pass
