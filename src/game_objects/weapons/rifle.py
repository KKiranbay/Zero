from pygame import Vector2

from game import Game
from game_objects.weapons.weapon import Weapon

from game_objects.projectiles.bullet import Bullet

class Rifle(Weapon):
	def __init__(self, pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int]) -> None:
		super().__init__("Rifle", pos, size, attack_rpm, direction, color)

	def create_projectile(self, game: Game):
		bullet: Bullet = Bullet(self.m_direction, self.m_pos, Vector2(10, 10))
		game.add_projectile_object(bullet)