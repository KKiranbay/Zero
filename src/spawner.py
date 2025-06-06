import random

import pygame

import game_events_dictionary

from playground import Playground
from game_objects.npc import NPC, NPC_Type


last_spawn: int = 0

def spawnNPC(playground: Playground, sprites: pygame.sprite.Group, min_time: int, max_time: int) -> NPC | None:
	max_attempts = 100  # Prevent infinite loops in case no suitable spot is found
	attempts = 0

	while attempts < max_attempts:
		size_int = random.randint(20, 40)
		enemy_size: pygame.Vector2 = pygame.Vector2(size_int, size_int)
		enemy_size_half: pygame.Vector2 = enemy_size / 2
		random_x: float = random.uniform(playground.m_game_world_rect.left + enemy_size_half.x, playground.m_game_world_rect.right - enemy_size_half.x)
		random_y: float = random.uniform(playground.m_game_world_rect.top + enemy_size_half.y, playground.m_game_world_rect.bottom - enemy_size_half.y)
		random_pos: pygame.Vector2 = pygame.Vector2(random_x, random_y)

		temp_npc_rect = pygame.Rect(0, 0, enemy_size.x, enemy_size.y)
		temp_npc_rect.center = (random_x, random_y)

		collision_found = False
		for sprite in sprites:
			temp_sprite_rect: pygame.Rect = sprite.rect.scale_by(3, 3)
			if temp_npc_rect.colliderect(temp_sprite_rect):
				collision_found = True
				break

		if not collision_found:
			pygame.time.set_timer(game_events_dictionary.SPAWN_NPC_EVENT, round(random.uniform(min_time, max_time)))
			return NPC(NPC_Type.ENEMY, random_pos, enemy_size)

		attempts += 1

	pygame.time.set_timer(game_events_dictionary.SPAWN_NPC_EVENT, round(random.uniform(min_time, max_time)))
	return None


