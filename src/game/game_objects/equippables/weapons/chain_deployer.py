from pygame import Vector2

from game.game_objects.equippables.weapons.weapon import Weapon

from game.game_objects.projectiles.growing_barbed_chain import GrowingBarbedChain

from game.game import Game

class ChainDeployer(Weapon):
	def __init__(self, game: Game, pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int]) -> None:
		super().__init__(game, "Chain", pos, size, attack_rpm, direction, color)

	def create_projectile(self):
		mine: GrowingBarbedChain = GrowingBarbedChain(self.m_game, self.m_direction, self.m_pos, Vector2(30, 10))
		self.m_game.add_projectile_object(mine)