import random
from typing import Callable

import pygame

from game.playground import Playground
from game.game_objects.npcs.npc import NPC, NPC_Type

from game.map.polygon_data import PolygonData

last_spawn: int = 0

def _check_for_collision_with_sprites(npc_rect: pygame.Rect, sprites: pygame.sprite.Group) -> bool:
	"""Check if the NPC rectangle collides with any sprite in the group."""
	for sprite in sprites:
		temp_sprite_rect: pygame.Rect = sprite.rect.scale_by(3, 3)
		if npc_rect.colliderect(temp_sprite_rect):
			return True
	return False

def spawn_npc_on_playground(npc_factory: Callable[[NPC_Type, pygame.Vector2, pygame.Vector2], NPC], playground: Playground, sprites: pygame.sprite.Group, min_time: int, max_time: int) -> tuple[NPC | None, int]:
	max_attempts = 100  # Prevent infinite loops in case no suitable spot is found
	attempts = 0

	spawn_time = round(random.uniform(min_time, max_time))

	while attempts < max_attempts:
		size_int = random.randint(20, 40)
		enemy_size: pygame.Vector2 = pygame.Vector2(size_int, size_int)
		enemy_size_half: pygame.Vector2 = enemy_size / 2

		random_spawn_edge: int = random.choice([1, 2, 3, 4])
		random_x: float = 0
		random_y: float = 0

		match random_spawn_edge:
			case 1: # TOP
				random_x = random.uniform(playground.m_game_world_rect.left + enemy_size_half.x, playground.m_game_world_rect.right - enemy_size_half.x)
				random_y = playground.m_game_world_rect.top + enemy_size_half.y

			case 2: # RIGHT
				random_x = playground.m_game_world_rect.right - enemy_size_half.x
				random_y = random.uniform(playground.m_game_world_rect.top + enemy_size_half.y, playground.m_game_world_rect.bottom - enemy_size_half.y)

			case 3: # BOTTOM
				random_x = random.uniform(playground.m_game_world_rect.left + enemy_size_half.x, playground.m_game_world_rect.right - enemy_size_half.x)
				random_y = playground.m_game_world_rect.bottom - enemy_size_half.y

			case 4: # LEFT
				random_x = playground.m_game_world_rect.left + enemy_size_half.x
				random_y = random.uniform(playground.m_game_world_rect.top + enemy_size_half.y, playground.m_game_world_rect.bottom - enemy_size_half.y)

		random_pos: pygame.Vector2 = pygame.Vector2(random_x, random_y)

		temp_npc_rect = pygame.Rect(0, 0, enemy_size.x, enemy_size.y)
		temp_npc_rect.center = (random_x, random_y)

		collision_found = _check_for_collision_with_sprites(temp_npc_rect, sprites)

		if not collision_found:
			return (npc_factory(NPC_Type.ENEMY, random_pos, enemy_size), spawn_time)

		attempts += 1

	return (None, spawn_time)

def spawn_npc_on_polygon_vertices(npc_factory: Callable[[NPC_Type, pygame.Vector2, pygame.Vector2], NPC], map_polygon: 'PolygonData', sprites: pygame.sprite.Group, min_time: int, max_time: int) -> tuple[NPC | None, int]:
	"""Spawn an NPC on the map polygon."""
	if not map_polygon.get_vertices():
		return (None, 0)

	max_attempts = 100
	attempts = 0

	spawn_time = round(random.uniform(min_time, max_time))

	while attempts < max_attempts:
		random_point = map_polygon.select_a_point_randomly_on_vertices()

		size_int = random.randint(20, 40)
		enemy_size: pygame.Vector2 = pygame.Vector2(size_int, size_int)
		temp_npc_rect = pygame.Rect(0, 0, enemy_size.x, enemy_size.y)
		temp_npc_rect.center = random_point

		"""Move temp_npc_rect towards map_polygon's middle point"""
		polygon_middle = map_polygon.get_middle_point()
		temp_npc_rect_direction = pygame.Vector2(polygon_middle) - pygame.Vector2(random_point)
		new_temp_npc_rect_center = pygame.Vector2(random_point) + temp_npc_rect_direction.normalize() * (enemy_size.length() / 2)

		"""Check if the new center collides with map_polygon."""
		temp_npc_rect.center = new_temp_npc_rect_center
		if map_polygon.check_if_given_rect_collides_with_polygon_s_vertices(temp_npc_rect) or _check_for_collision_with_sprites(temp_npc_rect, sprites):
			attempts += 1
			continue

		return (npc_factory(NPC_Type.ENEMY, pygame.Vector2(temp_npc_rect.center), enemy_size), spawn_time)

	return  (None, spawn_time)