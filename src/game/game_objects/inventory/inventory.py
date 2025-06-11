from game.game_objects.weapons.weapon import Weapon

class Inventory:
	def __init__(self) -> None:
		self.m_weapon_inventory: dict[int, Weapon] = {}
		pass