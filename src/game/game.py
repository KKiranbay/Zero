import math

import pygame

import events_dictionary as events_dictionary
from events_dictionary import EventsDictionary

from game.camera import Camera
from game.playground import Playground
import game.spawner as spawner

from time_handler import Time_Handler

from resources.shape_png_factory import create_triangle_png
import resources.colors as colors

from singleton import singleton

@singleton
class Game:
	def __init__(self):
		self.m_time_handler: Time_Handler = Time_Handler()
		self.m_game_events: EventsDictionary = EventsDictionary()

		self.m_playground: Playground

		self.reinitialize()

		create_triangle_png("enemy_triangle.png", (100, 100), color=colors.YELLOW_ORANGE)

	def reinitialize(self):
		self.m_time_handler.reset_total_duration()

		self.m_chars: pygame.sprite.Group = pygame.sprite.Group()
		self.m_projectiles: pygame.sprite.Group = pygame.sprite.Group()
		self.m_npcs: pygame.sprite.Group = pygame.sprite.Group()

		self.m_score: int = 0

	def update(self):
		self.m_chars.update()
		self.m_npcs.update()
		self.m_projectiles.update()

		self.check_collisions()
		self.check_game_events()

		chars_sprites = self.m_chars.sprites()
		if chars_sprites:
			self.m_camera.update(chars_sprites[0].rect.center)

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

			projectile.on_collision_with_npcs(npcs_hit=npcs_hit_forreal)
			for npc in npcs_hit:
				npc.on_collision_with_projectile(collided_projectile=projectile)

		char_npc_collisions = pygame.sprite.groupcollide(self.m_chars, self.m_npcs, False, False)
		for char, npcs_hit in char_npc_collisions.items():
			npcs_hit_forreal: set[pygame.sprite.Sprite] = set()
			for npc in npcs_hit:
				if pygame.sprite.collide_mask(char, npc):
					npcs_hit_forreal.add(npc)

			if len(npcs_hit_forreal) == 0:
				continue

			char.on_collision_with_npcs(npcs_hit=npcs_hit_forreal)
			for npc in npcs_hit:
				npc.on_collision_with_char(char_hit=char)

		chars_sprites = self.m_chars.sprites()
		npcs_sprites = self.m_npcs.sprites()
		game_world_rect = self.m_playground.m_game_world_rect
		for sprite in chars_sprites:
			sprite.check_and_clamp_ip_with_rect(game_world_rect)

		for sprite in npcs_sprites:
			sprite.check_and_clamp_ip_with_rect(game_world_rect)

	def get_screen_offset(self) -> pygame.math.Vector2:
		return self.m_camera.m_screen_offset

	def check_game_events(self):
		self.check_spawn_event(self.m_game_events.get_event(events_dictionary.SPAWN_NPC_EVENT))
		self.check_chars_died_event(self.m_game_events.get_event(events_dictionary.CHAR_NO_DIED_EVENT))

	def check_spawn_event(self, spawn: bool):
		if not spawn:
			return

		npc = spawner.spawnNPC(self.m_playground, self.m_chars, 200, self.get_exponential_spawn_interval())
		if (npc is not None):
			self.add_npc_object(npc)

	def get_exponential_spawn_interval(self) -> int:
		BASE_SPAWN_INTERVAL_MS: int = 3000
		DECAY_RATE: float = 0.01
		MIN_SPAWN_INTERVAL_MS: int = 200
		game_duration_seconds = self.m_time_handler.get_total_duration_ms() / 1000.0
		raw_interval = BASE_SPAWN_INTERVAL_MS * math.exp(-DECAY_RATE * game_duration_seconds)
		return int(max(MIN_SPAWN_INTERVAL_MS, raw_interval))

	def check_chars_died_event(self, chars_died):
		if not chars_died:
			return

		if chars_died[0] == 1:
			self.m_game_events.change_event(events_dictionary.RESTART_GAME_EVENT, True)
			self.m_game_events.clear_persistent_event(events_dictionary.CHAR_NO_DIED_EVENT)
