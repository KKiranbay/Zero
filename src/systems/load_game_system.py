import json
import os

import pygame
from pygame import Vector2

from game.camera import Camera
from game.playground import Playground

from game.game_objects.characters.character import Character
from game.game_objects.npcs.npc import NPC, NPC_Type
from game.game_objects.projectiles.bullet import Bullet
from game.game_objects.projectiles.mine import Mine
from game.game_objects.projectiles.growing_barbed_chain import GrowingBarbedChain

import resources.colors as colors

from screen import Screen

from systems.game_data_system import GameDataSystem

class LoadGameSystem(GameDataSystem):
	def __init__(self):
		super().__init__()
		self.screen: Screen = Screen()

	def load_game_data(self):
		try:
			save_path = os.path.join(self.m_save_directory, self.m_save_filename)

			if not os.path.exists(save_path):
				print("No save file found")
				return None

			with open(save_path, 'r') as f:
				save_data = json.load(f)

			print("Game loaded successfully")
			return save_data

		except Exception as e:
			print(f"Failed to load game: {e}")
			return None

	def restore_game_state(self, save_data, game):
		try:
			game.reinitialize()

			game_data = save_data["game"]
			game.m_score = game_data["score"]
			game.m_time_handler.m_total_duration_ms = game_data["total_duration_ms"]

			self.restore_playground(game)

			self.restore_player(save_data["player"], game)

			game.m_npcs.empty()
			game.m_projectiles.empty()

			self.restore_npcs(save_data["npcs"], game)

			self.restore_projectiles(save_data["projectiles"], game)

			print("Game state restored successfully")
			return True

		except Exception as e:
			print(f"Failed to restore game state: {e}")
			return False

	def restore_playground(self, game):
		playground_width = 500
		playground_height = 500
		playground = Playground(self.screen.m_window, playground_width, playground_height, colors.BEIGE)
		game.add_playground(playground)

	def restore_player(self, player_data, game):
		pos_data = player_data["position"]
		player = Character(pygame.Vector2(pos_data["x"], pos_data["y"]), pygame.Vector2(50,50), 500)

		player.m_health = player_data["health"]

		look_data = player_data["look_direction"]
		player.m_look_direction = pygame.Vector2(look_data["x"], look_data["y"])
		game.add_char_object(player)

		self.restore_camera(player, game)

		self.restore_inventory(player_data["inventory"], player.m_inventory)

	def restore_camera(self, player, game):
		self.m_camera = Camera(pygame.Vector2(game.m_playground.m_game_world_rect.width // 2, game.m_playground.m_game_world_rect.height // 2), self.screen.m_window.get_width(), self.screen.m_window.get_height())
		game.add_camera(self.m_camera)

	def restore_inventory(self, inventory_data, inventory):
		weapons_data = inventory_data["weapons"]
		for key_str, weapon_data in weapons_data.items():
			key = int(key_str)
			if key in inventory.m_weapon_inventory:
				weapon = inventory.m_weapon_inventory[key]
				weapon.m_current_cooldown_s = weapon_data["cooldown_remaining"]
				weapon.m_last_attack_time_ms = weapon_data["last_attack_time"]

		if inventory_data["main_equipped"] and inventory.m_main_equipped:
			main_data = inventory_data["main_equipped"]
			inventory.m_main_equipped.m_current_cooldown_s = main_data["cooldown_remaining"]
			inventory.m_main_equipped.m_last_attack_time_ms = main_data["last_attack_time"]

	def restore_npcs(self, npcs_data, game):
		for npc_data in npcs_data:
			pos = Vector2(npc_data["position"]["x"], npc_data["position"]["y"])
			size = Vector2(npc_data["size"]["x"], npc_data["size"]["y"])
			npc_type = NPC_Type(npc_data["npc_type"])

			npc = NPC(npc_type, pos, size)
			npc.m_health = npc_data["health"]

			look_data = npc_data["look_direction"]
			npc.m_look_direction = Vector2(look_data["x"], look_data["y"])

			game.add_npc_object(npc)

	def restore_projectiles(self, projectiles_data, game):
		for proj_data in projectiles_data:
			pos = Vector2(proj_data["position"]["x"], proj_data["position"]["y"])
			size = Vector2(proj_data["size"]["x"], proj_data["size"]["y"])

			projectile = None

			if proj_data["type"] == "Bullet":
				direction = Vector2(proj_data["direction"]["x"], proj_data["direction"]["y"])
				projectile = Bullet(direction, pos, size)
				if "speed" in proj_data:
					projectile.m_speed = proj_data["speed"]

			elif proj_data["type"] == "Mine":
				projectile = Mine(pos, size)

			elif proj_data["type"] == "GrowingBarbedChain":
				direction = Vector2(proj_data["direction"]["x"], proj_data["direction"]["y"])
				projectile = GrowingBarbedChain(direction, pos, size)
				if "growth" in proj_data:
					projectile.m_growth = proj_data["growth"]

			if projectile:
				projectile.m_damage = proj_data["damage"]
				game.add_projectile_object(projectile)