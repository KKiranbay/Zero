from enum import Enum
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
	from game.game import Game

from game.game_objects.playground_object import PlaygroundObject

class NPC_Type(Enum):
	ENEMY = 1
	FRIENDLY = 2

class NPC(PlaygroundObject):
	def __init__(self, game: 'Game', npc_type: NPC_Type, npc_pos: pygame.Vector2, npc_size: pygame.Vector2):
		super().__init__(game, npc_pos, npc_size)

		self.m_type: NPC_Type = npc_type
		self.m_health: int = 100
		self.m_speed: float = 100
		self.m_move_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)
		self.m_look_direction: pygame.math.Vector2 = pygame.math.Vector2(0, -1)

		loaded_image: pygame.Surface = pygame.image.load("enemy_triangle.png").convert_alpha()
		self.original_image = pygame.transform.scale(loaded_image, npc_size)
		self.image = self.original_image
		self.rect = self.image.get_rect(center=self.m_pos)

		self.mask = pygame.mask.from_surface(self.image)

	def update(self,):
		self.move_towards_closest_target()

	def move_towards_closest_target(self):
		closest_target: PlaygroundObject | None = None
		min_distance: float = float('inf')
		chars = self.m_game.m_chars
		my_pos = self.m_pos
		for target in chars:
			distance: float = my_pos.distance_to(target.m_pos)
			if distance < min_distance:
				min_distance = distance
				closest_target = target

		if closest_target:
			self.m_move_direction = closest_target.m_pos - self.m_pos
			if self.m_move_direction.length() > self.rect.width / 2.0:
				self.m_move_direction = self.m_move_direction.normalize() * self.m_speed * self.m_time_handler.get_delta_time_s()

				self.update_look_direction()
				self.update_draw_polygon_and_mask()

				self.setDisplacement(self.m_move_direction)

	def update_look_direction(self):
		self.m_look_direction = self.m_move_direction

	def update_draw_polygon_and_mask(self):
		reference_vector = pygame.Vector2(0, -1)
		current_angle = reference_vector.angle_to(self.m_look_direction)

		self.image = pygame.transform.rotate(self.original_image, -current_angle)
		self.rect = self.image.get_rect(center=self.rect.center)
		self.mask = pygame.mask.from_surface(self.image)

	def on_collision_with_projectile(self, collided_projectile):
		self.m_health -= collided_projectile.m_damage
		if self.m_health <= 0:
			self.m_game.m_score += 1
			self.kill()

		collided_projectile.kill()

	def on_collision_with_char(self, char_hit: pygame.sprite.Sprite):
		pass