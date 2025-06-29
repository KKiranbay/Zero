from pygame import Vector2

from game.game_objects.equippables.weapons.weapon import Weapon

from game.game_objects.projectiles.mine import Mine

from game.game import Game

class MineDeployer(Weapon):
	def __init__(self, game: Game, pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int]) -> None:
		super().__init__(game, "Mine", pos, size, attack_rpm, direction, color)

	def create_projectile(self):
		mine: Mine = Mine(self.m_game, self.m_pos, Vector2(50, 50))
		self.m_game.add_projectile_object(mine)