import pygame

import resources.colors as colors

from game_objects.playground_object import Playground_Object
from game import Game

class GrowingBarbedChain(Playground_Object):
	def __init__(self, direction: pygame.Vector2, spawn_pos: pygame.Vector2,  projectile_size: pygame.Vector2) -> None:
		super().__init__(spawn_pos, projectile_size)

		self.m_direction: pygame.math.Vector2 = pygame.math.Vector2(direction)
		self.m_damage: int = 100
		self.m_growth_per_sec: float = 100
		self.m_growth: float = 1

		self.image.fill(colors.DARK_GREY)
		self.image.set_colorkey(colors.WHITE) # transparent

		self.m_original_image = self.image.copy()

		reference_vector = pygame.Vector2(0, -1)
		self.m_current_angle = reference_vector.angle_to(self.m_direction)

		self.image = pygame.transform.rotate(self.image, self.m_current_angle)
		self.rect = self.image.get_rect(center=self.m_pos)
		self.mask = pygame.mask.from_surface(self.image)

	def update(self, dt_s: float, game: Game):
		player_mask_rect = self.mask.get_rect(center=self.rect.center)
		if game.m_playground.m_game_world_rect.contains(player_mask_rect):
			self.m_growth += self.m_growth_per_sec * dt_s

			self.image = pygame.transform.scale_by(self.m_original_image, (1, self.m_growth))
			self.image = pygame.transform.rotate(self.image, self.m_current_angle)
			self.rect = self.image.get_rect(center=self.m_pos)
			self.mask = pygame.mask.from_surface(self.image)

	def on_collision_with_npcs(self, game, npcs_hit: set[pygame.sprite.Sprite]):
		pass
