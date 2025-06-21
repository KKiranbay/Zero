from pygame import Vector2

from game.game_objects.playground_object import Playground_Object

from game.game_objects.equippables.weapons.weapon import Weapon

from game.game_objects.projectiles.bullet import Bullet


class Rifle(Weapon):
	def __init__(self, pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int],
			  parent: Playground_Object | None = None,
			  attach_to_parent: bool = False) -> None:
		super().__init__("Rifle", pos, size, attack_rpm, direction, color, parent, attach_to_parent)

	def create_projectile(self):
		bullet: Bullet = Bullet(self.m_direction, self.m_pos, Vector2(10, 10))
		self.m_game.add_projectile_object(bullet)