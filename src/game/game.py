import math

import pygame

import events_dictionary as events_dictionary
from events_dictionary import EventsDictionary

from game.camera import Camera
from game.playground import Playground
import game.spawner as spawner

from time_handler import Time_Handler

class Game:
	def __init__(self):
		self.m_time_handler: Time_Handler = Time_Handler()

		self.m_chars: pygame.sprite.Group = pygame.sprite.Group()
		self.m_projectiles: pygame.sprite.Group = pygame.sprite.Group()
		self.m_npcs: pygame.sprite.Group = pygame.sprite.Group()

		self.m_game_events: EventsDictionary = EventsDictionary()
		self.m_playground: Playground

		self.m_score: int = 0

	def update(self):
		dt_s: float = self.m_time_handler.get_delta_time_s()

		self.m_chars.update(dt_s, self)
		self.m_npcs.update(dt_s, self)
		self.m_projectiles.update(dt_s, self)

		self.check_collisions()

		self.check_game_events()

		self.m_camera.update(self.m_chars.sprites()[0].rect.center)

	def add_playground(self, playground: Playground):
		self.m_playground = playground

	def add_camera(self, camera: Camera):
		self.m_camera = camera

	def add_char_object(self, char_obj: pygame.sprite.Sprite):
		self.m_chars.add(char_obj)

	def add_projectile_object(self, projectile_obj: pygame.sprite.Sprite):
		self.m_projectiles.add(projectile_obj)

	def add_npc_object(self, sprite_obj: pygame.sprite.Sprite):
		self.m_npcs.add(sprite_obj)

	def draw(self):
		self.m_playground.refill_playground()

		self.m_npcs.draw(self.m_playground.m_surface)
		self.m_projectiles.draw(self.m_playground.m_surface)
		self.m_chars.draw(self.m_playground.m_surface)

		self.m_playground.draw_playground(self.m_camera.m_screen_offset)

	def check_collisions(self):
		projectile_npc_collisions = pygame.sprite.groupcollide(self.m_projectiles, self.m_npcs, False, False)
		for projectile, npcs_hit in projectile_npc_collisions.items():
			npcs_hit_forreal: set[pygame.sprite.Sprite] = set()
			for npc in npcs_hit:
				if pygame.sprite.collide_mask(projectile, npc):
					npcs_hit_forreal.add(npc)

			if len(npcs_hit_forreal) == 0:
				continue

			projectile.on_collision_with_npcs(game=self, npcs_hit=npcs_hit_forreal)
			for npc in npcs_hit:
				npc.on_collision_with_projectile(game=self, collided_projectile=projectile)

		char_npc_collisions = pygame.sprite.groupcollide(self.m_chars, self.m_npcs, False, False)
		for char, npcs_hit in char_npc_collisions.items():
			npcs_hit_forreal: set[pygame.sprite.Sprite] = set()
			for npc in npcs_hit:
				if pygame.sprite.collide_mask(char, npc):
					npcs_hit_forreal.add(npc)

			if len(npcs_hit_forreal) == 0:
				continue

			char.on_collision_with_npcs(game=self, npcs_hit=npcs_hit_forreal)
			for npc in npcs_hit:
				npc.on_collision_with_char(game=self, char_hit=char)

		for sprite in self.m_chars.sprites():
			sprite.check_and_clamp_ip_with_rect(self.m_playground.m_game_world_rect)

		for sprite in self.m_npcs.sprites():
			sprite.check_and_clamp_ip_with_rect(self.m_playground.m_game_world_rect)

	def get_screen_offset(self) -> pygame.math.Vector2:
		return self.m_camera.m_screen_offset

	def check_game_events(self):
		self.check_spawn_event(self.m_game_events.get_event(events_dictionary.SPAWN_NPC_EVENT))
		self.check_chars_died_event(self.m_game_events.get_event(events_dictionary.CHAR_NO_DIED_EVENT))

	def check_spawn_event(self, spawn: bool):
		if not spawn:
			return

		npc = spawner.spawnNPC(self.m_playground, self.m_chars, 200, self.get_exponential_spawn_interval())
		if (npc != None):
			self.add_npc_object(npc)

	def get_exponential_spawn_interval(self) -> int:
		BASE_SPAWN_INTERVAL_MS: int = 3000
		DECAY_RATE: float = 0.01
		MIN_SPAWN_INTERVAL_MS: int = 200
		game_duration_seconds = self.m_time_handler.get_total_duration_ms() / 1000.0
		raw_interval = BASE_SPAWN_INTERVAL_MS * math.exp(-DECAY_RATE * game_duration_seconds) + 200
		return int(max(MIN_SPAWN_INTERVAL_MS, raw_interval))

	def check_chars_died_event(self, chars_died: list[int]):
		if not chars_died:
			return

		if isinstance(chars_died[0], int) and chars_died[0] == 1:
			self.m_game_events.change_event(events_dictionary.RESTART_EVENT, True)