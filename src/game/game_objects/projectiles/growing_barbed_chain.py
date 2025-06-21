import pygame

import resources.colors as colors

from game.game_objects.playground_object import Playground_Object

class GrowingBarbedChain(Playground_Object):
	def __init__(self, direction: pygame.Vector2, spawn_pos: pygame.Vector2,  projectile_size: pygame.Vector2) -> None:
		super().__init__(spawn_pos, projectile_size)

		self.m_direction: pygame.math.Vector2 = pygame.math.Vector2(direction)
		self.m_damage: int = 100

		self.m_growth_per_sec: float = 10
		self.m_growth: float = 1
		self.m_height_limit: int = 100

		self.image.fill(colors.DARK_GREY)

		self.m_original_image: pygame.Surface = self.image.copy()
		self.m_original_height = self.m_original_image.get_height()
		self.m_scaled_image: pygame.Surface= self.image.copy()

		reference_vector: pygame.Vector2 = pygame.Vector2(0, -1)
		self.m_current_angle: float = self.m_direction.angle_to(reference_vector)

		self.image = pygame.transform.rotate(self.m_original_image, self.m_current_angle)
		self.rect = self.image.get_rect(center=self.m_pos)
		self.mask = pygame.mask.from_surface(self.image)

		self.m_anchor_pos: pygame.Vector2 = pygame.Vector2(self.rect.midbottom)

	def update(self):
		if self.m_scaled_image.get_height() > self.m_height_limit:
			return

		player_mask_rect: pygame.Rect = self.mask.get_rect(center=self.rect.center)
		if self.m_game.m_playground.m_game_world_rect.contains(player_mask_rect):
			current_growth: float = self.m_growth_per_sec * self.m_time_handler.get_delta_time_s()
			self.m_growth += current_growth

			new_pixel_height = self.m_original_height * self.m_growth

			self.m_scaled_image = pygame.transform.scale(self.m_original_image, (self.m_original_image.get_width(), new_pixel_height))
			self.image = pygame.transform.rotate(self.m_scaled_image, self.m_current_angle)

			offset = self.m_direction * (new_pixel_height / 2)
			new_center = self.m_anchor_pos + offset

			self.rect = self.image.get_rect(center=new_center)
			self.mask = pygame.mask.from_surface(self.image)

	def on_collision_with_npcs(self, npcs_hit: set[pygame.sprite.Sprite]):
		pass
