import pygame

import resources.colors as colors

from game.game_objects.playground_object import Playground_Object

from game.game import Game

class Bullet(Playground_Object):
	def __init__(self, game: Game, direction: pygame.math.Vector2, projectile_pos:  pygame.Vector2, projectile_size: pygame.Vector2) -> None:
		super().__init__(game, projectile_pos, projectile_size)
		self.m_direction: pygame.math.Vector2 = pygame.math.Vector2(direction)
		self.m_damage: int = 20
		self.m_speed: float = 500.0

		reference_vector = pygame.Vector2(0, -1)
		current_angle = reference_vector.angle_to(self.m_direction)

		self.image = self.image.copy()
		self.image.fill(colors.PINK_RED)
		self.image.set_colorkey(colors.WHITE) # transparent

		self.image = pygame.transform.rotate(self.image, current_angle)
		self.rect = self.image.get_rect(center=self.m_pos)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self):
		displacement = self.m_direction * self.m_speed * self.m_time_handler.get_delta_time_s()
		self.setDisplacement(displacement)

		game_world_rect = self.m_game.m_playground.m_game_world_rect
		if self.check_fully_left_rect(game_world_rect):
			self.kill()

	def on_collision_with_npcs(self, npcs_hit: set[pygame.sprite.Sprite]):
		pass