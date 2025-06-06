import pygame

import game_events_dictionary
import resources.colors as colors

from game import Game
from game_objects.playground_object import Playground_Object
from game_objects.projectiles.bullet import Bullet

class Character(Playground_Object):
	def __init__(self, char_pos: pygame.Vector2, char_size: pygame.Vector2, char_speed: float):
		super().__init__(char_pos, char_size)
		self.m_char_speed: float = char_speed

		self.m_left_click: bool = False
		self.m_last_shoot_time: float = 0

		self.m_health: int = 30

		shot_rpm: int = 300
		self.m_shot_delay_ms: float = (60.0 / shot_rpm) * 1000.0 #  ms

		self.m_in_collision_with_npc: set[pygame.sprite.Sprite] = set()
		self.m_last_npc_collision_time: float = 0
		damage_rpm: int = 60
		self.m_damage_delay_ms: float = (60.0 / damage_rpm) * 1000.0

		# Triangle
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

	def update(self, dt_s: float, game: Game):
		self.checkShoot(game)
		self.move_char(dt_s, game)

	def move_char(self, dt_s: float, game: Game):
		original_x = self.rect.centerx
		original_y = self.rect.centery

		keys = pygame.key.get_pressed()

		direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
		if direction.length() == 0:
			return

		direction = direction.normalize() * self.m_char_speed * dt_s

		self.setDisplacement(direction)

	def checkShoot(self, game: Game):
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
			self.m_left_click = True
		if game.m_game_events.getEvent(pygame.MOUSEBUTTONUP) and not pygame.mouse.get_pressed()[0]:
			self.m_left_click = False

		total_duration = game.m_time_handler.get_total_duration_ms()
		if self.m_left_click and (total_duration - self.m_last_shoot_time) >= self.m_shot_delay_ms:
			self.m_last_shoot_time = total_duration
			self.shoot(game)

	def shoot(self, game: Game):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - game.get_screen_offset()
		direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.m_pos
		if direction.length() == 0:
			direction.update(1, 0)  # Default direction if no movement

		bullet: Bullet = Bullet(direction.normalize(), self.m_pos, pygame.Vector2(10,10))
		game.add_projectile_object(bullet)

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