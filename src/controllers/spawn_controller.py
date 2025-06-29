# SpawnController manages NPC spawning logic and timing.
# Key Pygame-ce elements:
# - pygame.sprite.Group: Container for managing multiple sprites.
# - pygame.Vector2: 2D vector for positioning.
# Manages exponential spawn timing and NPC creation.

import math
import pygame

import events_dictionary as events_dictionary
from game.game_objects.npcs.npc_factory import create_npc, NPC_Type
import game.spawner as spawner


class SpawnController:
	def __init__(self, game_instance):
		self.m_game = game_instance
		self.m_next_spawn_total_time_ms: float = 0
		self.m_spawn_system_active: bool = False

	def start_spawn_system(self) -> None:
		"""Initialize the spawn system with initial spawn timing."""
		self.m_spawn_system_active = True
		self.m_next_spawn_total_time_ms = self.m_game.m_time_handler.get_total_duration_ms() + 2500

	def update(self) -> None:
		"""Check and handle spawn events during game update cycle."""
		self.check_spawn_event(self.m_game.m_game_events.get_event(events_dictionary.SPAWN_NPC_EVENT))

	def check_spawn_event(self, spawn: bool) -> None:
		"""Handle NPC spawning based on events and timing."""
		should_spawn = spawn

		if self.m_spawn_system_active:
			current_time = self.m_game.m_time_handler.get_total_duration_ms()
			if current_time >= self.m_next_spawn_total_time_ms:
				should_spawn = True

		if not should_spawn:
			return

		exp_time_ms = self.get_exponential_spawn_interval()

		def npc_factory_func(npc_type: NPC_Type, pos: pygame.Vector2, size: pygame.Vector2):
			return create_npc(self.m_game, npc_type, pos, size)

		npc_time_tuple = spawner.spawn_npc(npc_factory_func, self.m_game.m_playground, self.m_game.m_chars, 200, exp_time_ms)
		if npc_time_tuple[0] is not None:
			self.m_game.add_npc_object(npc_time_tuple[0])

		self.m_next_spawn_total_time_ms = self.m_game.m_time_handler.get_total_duration_ms() + npc_time_tuple[1]

	def get_exponential_spawn_interval(self) -> int:
		"""Calculate spawn interval that decreases exponentially over time."""
		BASE_SPAWN_INTERVAL_MS: int = 3000
		DECAY_RATE: float = 0.01
		MIN_SPAWN_INTERVAL_MS: int = 200
		game_duration_seconds = self.m_game.m_time_handler.get_total_duration_ms() / 1000.0
		raw_interval = BASE_SPAWN_INTERVAL_MS * math.exp(-DECAY_RATE * game_duration_seconds)
		return int(max(MIN_SPAWN_INTERVAL_MS, raw_interval))
