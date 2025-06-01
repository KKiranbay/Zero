from enum import Enum

import pygame

import resources.colors as colors

from playground_object import Playground_Object

class NPC_Type(Enum):
	ENEMY = 1
	FRIENDLY = 2

class NPC(Playground_Object):
	def __init__(self, npc_type: NPC_Type, npc_pos_x: float, npc_pos_y: float, npc_size: float):
		super().__init__(npc_pos_x, npc_pos_y, npc_size)
		self.m_type: NPC_Type = npc_type
		self.image.fill(colors.PURPLE)
		self.m_health: int = 100

	def on_collision_with_projectile(self, game, collided_with: list[pygame.sprite.Sprite]):
		print(f"NPC collided with: {collided_with}")
		for projectile in collided_with:
				projectile.kill()
				self.m_health -= 20
				print(f"NPC hit by projectile! Health: {self.m_health}")
				if self.m_health <= 0:
					print("NPC defeated!")
					self.kill()