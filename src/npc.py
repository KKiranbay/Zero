from enum import Enum

import pygame

import resources.colors as colors

from playground_object import Playground_Object

class NPC_Type(Enum):
	ENEMY = 1
	FRIENDLY = 2

class NPC(Playground_Object):
	def __init__(self, npc_type: NPC_Type, npc_pos_x: float, npc_pos_y: float, npc_size: pygame.Vector2):
		super().__init__(npc_pos_x, npc_pos_y, npc_size)
		self.m_type: NPC_Type = npc_type
		self.image.fill(colors.PURPLE)
		self.m_health: int = 100
		self.m_direction: pygame.math.Vector2 = pygame.math.Vector2(0, 0)

	def update(self, dt_s: float, game):
		closest_target: Playground_Object | None = None

		min_distance: float = float('inf')
		for target in game.m_chars:
			distance: float = self.m_pos.distance_to(target.m_pos)
			if distance < min_distance:
				min_distance = distance
				closest_target = target

		if closest_target:
			self.m_direction = closest_target.m_pos - self.m_pos
			if self.m_direction.length() > self.rect.width / 2.0:
				self.m_direction = self.m_direction.normalize() * 100.0 * dt_s
				self.setDisplacement(self.m_direction)

	def on_collision_with_projectile(self, game, collided_with: list[pygame.sprite.Sprite]):
		for projectile in collided_with:
				projectile.kill()
				self.m_health -= 20
				if self.m_health <= 0:
					game.m_score += 1
					self.kill()

	def on_collision_with_char(self, game, collided_with: list[pygame.sprite.Sprite]):
		pass