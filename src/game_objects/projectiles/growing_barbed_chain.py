import pygame

from game_objects.playground_object import Playground_Object

class GrowingBarbedChain(Playground_Object):
	def __init__(self, spawn_pos: pygame.Vector2, direction: pygame.Vector2, projectile_width) -> None:
		super().__init__(spawn_pos, pygame.Vector2(1, 1))
