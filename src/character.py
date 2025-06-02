import pygame

import game_events_dictionary
import helper
import resources.colors as colors

from game import Game
from playground import Playground
from playground_object import Playground_Object
from projectile import Projectile

class Character(Playground_Object):
	def __init__(self, char_x: float, char_y: float, char_size: int, char_speed: float):
		super().__init__(char_x, char_y, char_size)
		self.m_char_speed: float = char_speed
		self.image.fill(colors.DARK_GREEN)

		self.m_left_click: bool = False
		self.m_last_shoot_time: int = 0

		self.m_health = 30

		shot_rpm = 300
		self.m_shot_delay_ms = (60 / shot_rpm) * 1000 #  ms

		self.m_in_collision_with_npc: list[pygame.sprite.Sprite] = []
		self.m_last_npc_collision_time: int = 0
		damage_rpm = 60
		self.m_damage_delay_ms = (60 / damage_rpm) * 1000

	def update(self, dt: float, game: Game):
		self.checkShoot(game)
		self.move_char(dt, game)

	def move_char(self, dt: float, game: Game):
		original_x = self.rect.centerx
		original_y = self.rect.centery

		keys = pygame.key.get_pressed()

		direction = pygame.Vector2(0,0)
		if keys[pygame.K_a]:
			direction.x -= self.m_char_speed * dt
		if keys[pygame.K_d]:
			direction.x += self.m_char_speed * dt

		if keys[pygame.K_w]:
			direction.y -= self.m_char_speed * dt
		if keys[pygame.K_s]:
			direction.y += self.m_char_speed * dt

		self.setDisplacement(direction)

	def checkShoot(self, game: Game):
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
			self.m_left_click = True
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONUP) and not pygame.mouse.get_pressed()[0]:
			self.m_left_click = False

		if self.m_left_click and (game.m_current_time_ms - self.m_last_shoot_time) >= self.m_shot_delay_ms:
			self.m_last_shoot_time = game.m_current_time_ms
			self.shoot(game)

	def shoot(self, game: Game):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - game.get_screen_offset()
		direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.m_pos
		norm_direction: pygame.math.Vector2 = helper.normalize_vector(direction)

		projectile: Projectile = Projectile(norm_direction, self.m_pos.x, self.m_pos.y, 10)
		game.add_projectile_object(projectile)

	def on_collision_with_npc(self, game: Game, collided_with: list[pygame.sprite.Sprite]):
		already_collided = False
		for npc in collided_with:
			if npc in self.m_in_collision_with_npc:
				already_collided = True
				break

		self.m_in_collision_with_npc = collided_with

		if not already_collided or (already_collided and (game.m_current_time_ms - self.m_last_npc_collision_time) >= self.m_damage_delay_ms):
			self.m_last_npc_collision_time = game.m_current_time_ms
			self.damaged(game)

	def damaged(self, game: Game):
		self.m_health -= 1
		print(f"Health: {self.m_health}")
		if (self.m_health == 0):
			chars_died: list[int] = game.m_game_events.getEvent(game_events_dictionary.CHAR_NO_DIED_EVENT)
			chars_died.append(1)
			game.m_game_events.changeEvent(game_events_dictionary.CHAR_NO_DIED_EVENT, chars_died)
			print("Dead!")