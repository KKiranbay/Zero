import json
import os
from datetime import datetime

from systems.game_data_system import GameDataSystem

class SaveGameSystem(GameDataSystem):
	def __init__(self):
		super().__init__()

	def save_game_state(self, game, spawn_controller=None):
		try:
			save_data = {
				"metadata": {
					"save_time": datetime.now().isoformat(),
					"version": "1.0"
				},
				"game": self.serialize_game(game),
				"player": self.serialize_player(game.m_chars.sprites()[0]),
				"npcs": self.serialize_npcs(game.m_npcs),
				"projectiles": self.serialize_projectiles(game.m_projectiles),
				"spawn_controller": self.serialize_spawn_controller(spawn_controller)
			}

			save_path = os.path.join(self.m_save_directory, self.m_save_filename)
			with open(save_path, 'w') as f:
				json.dump(save_data, f, indent=2)

			print(f"Game saved successfully to {save_path}")
			return True

		except Exception as e:
			print(f"Failed to save game: {e}")
			return False

	def serialize_game(self, game):
		return {
			"score": game.m_score,
			"total_duration_ms": game.m_time_handler.get_total_duration_ms()
		}

	def serialize_player(self, player):
		return {
			"position": {"x": player.m_pos.x, "y": player.m_pos.y},
			"health": player.m_health,
			"look_direction": {"x": player.m_look_direction.x, "y": player.m_look_direction.y},
			"inventory": self.serialize_inventory(player.m_inventory)
		}

	def serialize_inventory(self, inventory):
		weapons = {}
		for key, weapon in inventory.m_weapon_inventory.items():
			weapons[str(key)] = {
				"name": weapon.m_equippable_name,
				"cooldown_remaining": weapon.m_current_cooldown_s,
				"last_attack_time": weapon.m_last_attack_time_ms
			}

		main_equipped = None
		if inventory.m_main_equipped:
			main_equipped = {
				"name": inventory.m_main_equipped.m_equippable_name,
				"cooldown_remaining": inventory.m_main_equipped.m_current_cooldown_s,
				"last_attack_time": inventory.m_main_equipped.m_last_attack_time_ms
			}

		return {
			"weapons": weapons,
			"main_equipped": main_equipped
		}

	def serialize_npcs(self, npcs_group):
		npcs_data = []
		for npc in npcs_group:
			npcs_data.append({
				"position": {"x": npc.m_pos.x, "y": npc.m_pos.y},
				"size": {"x": npc.m_size.x, "y": npc.m_size.y},
				"health": npc.m_health,
				"npc_type": npc.m_type.value,
				"look_direction": {"x": npc.m_look_direction.x, "y": npc.m_look_direction.y}
			})
		return npcs_data

	def serialize_projectiles(self, projectiles_group):
		projectiles_data = []
		for projectile in projectiles_group:
			projectile_data = {
				"type": projectile.__class__.__name__,
				"position": {"x": projectile.m_pos.x, "y": projectile.m_pos.y},
				"size": {"x": projectile.m_size.x, "y": projectile.m_size.y},
				"damage": projectile.m_damage
			}

			if hasattr(projectile, 'm_direction'):
				projectile_data["direction"] = {"x": projectile.m_direction.x, "y": projectile.m_direction.y}
			if hasattr(projectile, 'm_speed'):
				projectile_data["speed"] = projectile.m_speed
			if hasattr(projectile, 'm_growth'):
				projectile_data["growth"] = projectile.m_growth

			projectiles_data.append(projectile_data)

		return projectiles_data

	def serialize_spawn_controller(self, spawn_controller):
		"""Serialize spawn controller data for saving."""
		if spawn_controller is None:
			return None

		return {
			"next_spawn_total_time_ms": spawn_controller.m_next_spawn_total_time_ms,
			"spawn_system_active": spawn_controller.m_spawn_system_active
		}