import pygame

import game_events_dictionary
import resources.colors as colors

from game import Game
from game_objects.playground_object import Playground_Object

from game_objects.projectiles.bullet import Bullet
from game_objects.projectiles.mine import Mine
from game_objects.projectiles.growing_barbed_chain import GrowingBarbedChain

class Character(Playground_Object):
	def __init__(self, char_pos: pygame.Vector2, char_size: pygame.Vector2, char_speed: float):
		super().__init__(char_pos, char_size)

		self.m_health: int = 30
		self.m_char_speed: float = char_speed
		self.m_look_direction: pygame.Vector2 = pygame.Vector2(1, 0)
		self.m_color: tuple[int, int, int] = colors.DARK_GREEN

		# Enemy NPC collision
		self.m_in_collision_with_npc: set[pygame.sprite.Sprite] = set()
		self.m_last_npc_collision_time: float = 0
		damage_rpm: int = 60
		self.m_damage_delay_ms: float = (60.0 / damage_rpm) * 1000.0

		# Triangle Draw
		self.m_hitbox_multiplier: float = 1.5
		self.m_half_hitbox_multiplier: float = self.m_hitbox_multiplier / 2
		self.m_hitbox_size = self.m_size * self.m_hitbox_multiplier
		self.m_half_hitbox_size = self.m_size * self.m_half_hitbox_multiplier
		self.m_original_image = pygame.Surface(self.m_hitbox_size, pygame.SRCALPHA)
		self.image = self.m_original_image.copy()
		self.image.fill((0, 0, 0, 0)) # transparent background
		self.rect = self.image.get_rect(center=(self.m_pos))

		self.m_points: list[pygame.Vector2] = [
			pygame.Vector2(0, -self.m_half_size.y),
			pygame.Vector2(-self.m_half_size.x, self.m_half_size.y),
			pygame.Vector2(self.m_half_size.x, self.m_half_size.y)
		]

		self.update_draw_polygon_and_mask()

		# Weapon
		self.m_current_weapon: int = 1
		self.m_current_weapon_str: str = "Bullets"
		self.m_left_click: bool = False

		# Bullet
		self.m_last_shoot_time: float = 0
		shoot_rpm: int = 300
		self.m_shoot_delay_ms: float = (60.0 / shoot_rpm) * 1000.0 # ms

		# Mine
		self.m_last_deploy_time: float = 0
		shot_rpm: int = 30
		self.m_deploy_delay_ms: float = (60.0 / shot_rpm) * 1000.0 # ms

		# Mine
		self.m_last_throw_time: float = 0
		throw_rpm: int = 10
		self.m_throw_delay_ms: float = (60.0 / throw_rpm) * 1000.0 # ms

		self.m_total_duration: float = 0

	def update(self, dt_s: float, game: Game):
		self.m_total_duration = game.m_time_handler.get_total_duration_ms()

		self.update_look_direction(game)
		self.update_draw_polygon_and_mask()

		keys = pygame.key.get_pressed()

		self.check_shoot(game)

		self.move_char(keys, dt_s, game)

		self.check_weapon_select(keys, game)
		self.try_to_deploy_mines(keys, game)
		self.try_to_throw_barbed_chain(keys, game)

	def update_look_direction(self, game: Game):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - game.get_screen_offset()
		self.m_look_direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.m_pos
		if self.m_look_direction.length() == 0:
			self.m_look_direction.update(1, 0)  # Default direction if no movement
		else:
			self.m_look_direction.normalize_ip()

	def update_draw_polygon_and_mask(self):
		self.image.fill((0, 0, 0, 0))

		reference_vector: pygame.Vector2 = pygame.Vector2(0, -1) # up
		current_angle = reference_vector.angle_to(self.m_look_direction)

		rotated_points = []
		for point in self.m_points:
			# Rotate around (0,0) (the center of our conceptual sprite)
			rotated_point = point.rotate(current_angle)
			# Translate back to image coordinates (add half_width/height to move origin to top-left)
			translated_point = (rotated_point.x + self.m_half_hitbox_size.x,
								rotated_point.y + self.m_half_hitbox_size.y)
			rotated_points.append(translated_point)

		pygame.draw.polygon(self.image, self.m_color, rotated_points)

		self.mask = pygame.mask.from_surface(self.image)

	def move_char(self, keys, dt_s: float, game: Game):
		movement_direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
		if movement_direction.length() == 0:
			return

		movement_direction = movement_direction.normalize() * self.m_char_speed * dt_s

		self.setDisplacement(movement_direction)

	def check_shoot(self, game: Game):
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
			self.m_left_click = True
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONUP) and not pygame.mouse.get_pressed()[0]:
			self.m_left_click = False

		if not self.m_left_click:
			return

		self.current_weapon_triggered(game)

	def shoot_bullet(self, game: Game):
		bullet: Bullet = Bullet(self.m_look_direction, self.m_pos, pygame.Vector2(10, 10))
		game.add_projectile_object(bullet)

	def deploy_mine(self, game: Game):
		mine: Mine = Mine(self.m_pos, pygame.Vector2(25, 25))
		game.add_projectile_object(mine)

	def deploy_barbed_chain(self, game: Game):
		barbed_chain: GrowingBarbedChain = GrowingBarbedChain(self.m_look_direction, self.m_pos, pygame.Vector2(30, 10))
		game.add_projectile_object(barbed_chain)

	def on_collision_with_npcs(self, game: Game, npcs_hit: set[pygame.sprite.Sprite]):
		already_collided = False
		for npc in npcs_hit:
			if npc in self.m_in_collision_with_npc:
				already_collided = True

		self.m_in_collision_with_npc = npcs_hit

		total_duration: float = game.m_time_handler.get_total_duration_ms()
		if not already_collided or (already_collided and (total_duration - self.m_last_npc_collision_time) >= self.m_damage_delay_ms):
			self.m_last_npc_collision_time = total_duration
			self.damaged(game)

	def damaged(self, game: Game):
		self.m_health -= 1
		if (self.m_health == 0):
			chars_died: list[int] = game.m_game_events.getEvent(game_events_dictionary.CHAR_NO_DIED_EVENT)
			chars_died.append(1)
			game.m_game_events.changeEvent(game_events_dictionary.CHAR_NO_DIED_EVENT, chars_died)
			print("Dead!")

	def check_weapon_select(self, keys, game: Game):
		if keys[pygame.K_q]:
			self.change_current_weapon(1)

	def change_current_weapon(self, weapon_index: int):
		self.m_current_weapon = weapon_index
		match self.m_current_weapon:
			case 1:
				self.m_current_weapon_str: str = "Bullets"

	def current_weapon_triggered(self, game: Game):
		match self.m_current_weapon:
			case 1:
				if (self.m_total_duration - self.m_last_shoot_time) >= self.m_shoot_delay_ms:
					self.m_last_shoot_time = self.m_total_duration
					self.shoot_bullet(game)

	def try_to_deploy_mines(self, keys, game: Game):
		if not keys[pygame.K_e]:
			return

		if (self.m_total_duration - self.m_last_deploy_time) >= self.m_deploy_delay_ms:
					self.m_last_deploy_time = self.m_total_duration
					self.deploy_mine(game)

	def try_to_throw_barbed_chain(self, keys, game: Game):
		if not keys[pygame.K_r]:
			return

		if (self.m_total_duration - self.m_last_throw_time) >= self.m_throw_delay_ms:
					self.m_last_throw_time = self.m_total_duration
					self.deploy_barbed_chain(game)