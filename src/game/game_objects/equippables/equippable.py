import pygame

from game.game_objects.playground_object import Playground_Object

class Equippable(Playground_Object):
	def __init__(self,
			  name: str, pos: pygame.Vector2, size: pygame.Vector2,
			  direction: pygame.Vector2,
			  parent: Playground_Object | None = None,
			  ) -> None:
		super().__init__(pos, size)

		self.m_equippable_name: str = name
		self.m_parent = parent

		self.m_direction: pygame.Vector2 = direction

		self.m_attack_cooldown_ms: float = 0
		self.m_current_cooldown_s: float = 0

	def update(self):
		pass

	def update_pos_and_direction(self, pos: pygame.Vector2, direction: pygame.Vector2):
		self.m_pos = pos
		self.m_direction = direction

	def trigger(self):
		return
