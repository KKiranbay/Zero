import pygame

import game_events_dictionary
import resources.colors as colors

from game import Game
from game_objects.playground_object import Playground_Object
from game_objects.projectiles.bullet import Bullet
from game_objects.projectiles.mine import Mine

class Character(Playground_Object):
	def __init__(self, char_pos: pygame.Vector2, char_size: pygame.Vector2, char_speed: float):
		super().__init__(char_pos, char_size)

		self.m_health: int = 30
		self.m_char_speed: float = char_speed

		# Enemy NPC collision
		self.m_in_collision_with_npc: set[pygame.sprite.Sprite] = set()
		self.m_last_npc_collision_time: float = 0
		damage_rpm: int = 60
		self.m_damage_delay_ms: float = (60.0 / damage_rpm) * 1000.0

		# Triangle Draw
		self.image = pygame.Surface(self.m_size, pygame.SRCALPHA)
		self.image.fill((0, 0, 0, 0)) # transparent background
		self.rect = self.image.get_rect(center=(self.m_pos))

		self.m_points: list[pygame.Vector2] = [
			pygame.Vector2(self.m_size.x // 2, 0),
			pygame.Vector2(0, self.m_size.y),
			pygame.Vector2(self.m_size.x, self.m_size.y)
		]

		pygame.draw.polygon(self.image, colors.DARK_GREEN, self.m_points)

		self.mask = pygame.mask.from_surface(self.image)

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

	def update(self, dt_s: float, game: Game):
		keys = pygame.key.get_pressed()

		self.check_shoot(game)

		self.move_char(keys, dt_s, game)

		self.check_weapon_select(keys, game)

	def move_char(self, keys, dt_s: float, game: Game):
		original_x = self.rect.centerx
		original_y = self.rect.centery

		direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
		if direction.length() == 0:
			return

		direction = direction.normalize() * self.m_char_speed * dt_s

		self.setDisplacement(direction)

	def check_shoot(self, game: Game):
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
			self.m_left_click = True
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONUP) and not pygame.mouse.get_pressed()[0]:
			self.m_left_click = False

		self.current_weapon_triggered(game)

	def shoot_bullet(self, game: Game):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - game.get_screen_offset()
		direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.m_pos
		if direction.length() == 0:
			direction.update(1, 0)  # Default direction if no movement

		bullet: Bullet = Bullet(direction.normalize(), self.m_pos, pygame.Vector2(10, 10))
		game.add_projectile_object(bullet)

	def deploy_mine(self, game: Game):
		mine: Mine = Mine(self.m_pos, pygame.Vector2(25, 25))
		game.add_projectile_object(mine)

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
		print(f"Health: {self.m_health}")
		if (self.m_health == 0):
			chars_died: list[int] = game.m_game_events.getEvent(game_events_dictionary.CHAR_NO_DIED_EVENT)
			chars_died.append(1)
			game.m_game_events.changeEvent(game_events_dictionary.CHAR_NO_DIED_EVENT, chars_died)
			print("Dead!")

	def check_weapon_select(self, keys, game: Game):
		if keys[pygame.K_1]:
			self.change_current_weapon(1)
		if keys[pygame.K_2]:
			self.change_current_weapon(2)

	def change_current_weapon(self, weapon_index: int):
		self.m_current_weapon = weapon_index
		match self.m_current_weapon:
			case 1:
				self.m_current_weapon_str: str = "Bullets"
			case 2:
				self.m_current_weapon_str: str = "Mines"

	def current_weapon_triggered(self, game: Game):
		match self.m_current_weapon:
			case 1:
				total_duration = game.m_time_handler.get_total_duration_ms()
				if self.m_left_click and (total_duration - self.m_last_shoot_time) >= self.m_shoot_delay_ms:
					self.m_last_shoot_time = total_duration
					self.shoot_bullet(game)

			case 2:
				total_duration = game.m_time_handler.get_total_duration_ms()
				if self.m_left_click and (total_duration - self.m_last_deploy_time) >= self.m_deploy_delay_ms:
					self.m_last_deploy_time = total_duration
					self.deploy_mine(game)