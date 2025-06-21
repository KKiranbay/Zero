import pygame

from game.game_objects.equippables.equippable import Equippable

class Inventory(pygame.sprite.Sprite):
	def __init__(self) -> None:
		self.m_weapon_inventory: dict[int, Equippable] = {}
		self.m_main_equipped: Equippable | None = None
		pass

	def update(self):
		for key, weapon in self.m_weapon_inventory.items():
			weapon.update()

	def add_equipped_weapon(self, key: int, weapon: Equippable):
		self.m_weapon_inventory[key] =  weapon

	def add_main_equipped(self, equipped: Equippable):
		self.m_main_equipped =  equipped

	def updated_equipped_weapon_pos_and_direction(self, pos: pygame.Vector2, direction: pygame.Vector2):
		for key, weapon in self.m_weapon_inventory.items():
			weapon.update_pos_and_direction(pos, direction)

	def main_triggered(self):
		if self.m_main_equipped is None:
			return

		self.m_main_equipped.trigger()

	def inventory_key_triggered(self, key: int):
		if key not in self.m_weapon_inventory:
			return

		self.m_weapon_inventory[key].trigger()