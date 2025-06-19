import pygame
from pygame import Vector2

import resources.colors as colors

from game.game import Game

from game.game_objects.playground_object import Playground_Object

from time_handler import Time_Handler


class Weapon(Playground_Object):
	def __init__(self, name: str,
			  pos: Vector2, size: Vector2,
			  attack_rpm: float,
			  direction: Vector2,
			  color: tuple[int, int, int],
			  parent: Playground_Object | None = None,
			  attach_to_parent: bool = False) -> None:
		super().__init__(pos, size)

		self.m_time_handler: Time_Handler = Time_Handler()

		self.m_weapon_name: str = name

		self.m_direction: Vector2 = direction

		self.image = self.image.copy()
		self.image.fill(color)

		reference_vector = Vector2(0, -1)
		self.m_current_angle = reference_vector.angle_to(self.m_direction)

		self.image = pygame.transform.rotate(self.image, self.m_current_angle)
		self.rect = self.image.get_rect(center=self.m_pos)
		self.mask = pygame.mask.from_surface(self.image)

		self.m_attack_rpm: float = attack_rpm
		self.m_attack_cooldown_ms: float = (60.0 / self.m_attack_rpm) * 1000.0

		self.m_current_cooldown_s: float = 0

		self.m_total_duration_ms: float = self.m_time_handler.get_total_duration_ms()
		self.m_last_attack_time_ms: float = self.m_total_duration_ms - self.m_attack_cooldown_ms

		self.m_parent = parent
		self.m_attach_to_parent = attach_to_parent

	def update(self, dt_s: float, game: Game):
		self.m_total_duration_ms = self.m_time_handler.get_total_duration_ms()
		time_since_last_attack_ms = self.m_total_duration_ms - self.m_last_attack_time_ms
		remaining_cooldown_ms = self.m_attack_cooldown_ms - time_since_last_attack_ms
		self.m_current_cooldown_s = max(0, remaining_cooldown_ms * 0.001)

		if self.m_attach_to_parent and self.m_parent != None:
			self.m_pos = self.m_parent.get_attach_anchor_pos()
			self.m_direction = self.m_parent.m_look_direction

	def update_attack_rpm(self, new_rpm: float):
		self.m_attack_rpm = new_rpm
		self.m_attack_cooldown_ms = (60.0 / self.m_attack_rpm) * 1000.0

	def attack(self, game: Game):
		if self.m_current_cooldown_s == 0:
			self.m_last_attack_time_ms = self.m_total_duration_ms
			self.create_projectile(game)

	def create_projectile(self, game: Game):
		pass