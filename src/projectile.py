import pygame

from playground_object import Playground_Object

class Projectile(Playground_Object):
	def __init__(self, projectile_x, projectile_y, projectile_size) -> None:
		super().__init__(projectile_x, projectile_y, projectile_size)
		pass