from enum import Enum

import pygame

import resources.colors as colors

from game.game_objects.playground_object import Playground_Object

class NPC_Type(Enum):
	ENEMY = 1
	FRIENDLY = 2

class NPC(Playground_Object):
	def __init__(self, npc_type: NPC_Type, npc_pos: pygame.Vector2, npc_size: pygame.Vector2):
		super().__init__(npc_pos, npc_size)

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

	def update(self, dt_s: float, game):
		self.move_towards_closest_target(dt_s, game)

	def move_towards_closest_target(self, dt_s: float, game):
		closest_target: Playground_Object | None = None

		min_distance: float = float('inf')
		for target in game.m_chars:
			distance: float = self.m_pos.distance_to(target.m_pos)
			if distance < min_distance:
				min_distance = distance
				closest_target = target

		if closest_target:
			self.m_move_direction = closest_target.m_pos - self.m_pos
			if self.m_move_direction.length() > self.rect.width / 2.0:
				self.m_move_direction = self.m_move_direction.normalize() * self.m_speed * dt_s

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


	def on_collision_with_projectile(self, game, collided_projectile):
		self.m_health -= collided_projectile.m_damage
		if self.m_health <= 0:
			game.m_score += 1
			self.kill()

		collided_projectile.kill()

	def on_collision_with_char(self, game, char_hit: pygame.sprite.Sprite):
		pass