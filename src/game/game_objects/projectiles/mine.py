import pygame

import resources.colors as colors

from game.game_objects.playground_object import Playground_Object

class Mine(Playground_Object):
	def __init__(self, projectile_pos:  pygame.Vector2, projectile_size: pygame.Vector2) -> None:
		super().__init__(projectile_pos, projectile_size)
		self.m_damage = 50

		self.image.fill(colors.SOFT_GREEN)

	def update(self):
		if self.check_fully_left_rect(self.m_game.m_playground.m_game_world_rect):
			self.kill()

	def on_collision_with_npcs(self, npcs_hit: set[pygame.sprite.Sprite]):
		pass
