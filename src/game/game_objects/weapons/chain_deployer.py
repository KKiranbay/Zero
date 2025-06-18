from pygame import Vector2

from game.game import Game

from game.game_objects.weapons.weapon import Weapon

from game.game_objects.projectiles.growing_barbed_chain import GrowingBarbedChain

class ChainDeployer(Weapon):
	def __init__(self, pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int]) -> None:
		super().__init__("Chain", pos, size, attack_rpm, direction, color)

	def create_projectile(self, game: Game):
		mine: GrowingBarbedChain = GrowingBarbedChain(self.m_direction, self.m_pos, Vector2(30, 10))
		game.add_projectile_object(mine)