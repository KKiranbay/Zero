import pygame
from pygame import Vector2

import events_dictionary as events_dictionary
import resources.colors as colors

from game.game_objects.playground_object import Playground_Object

from game.game_objects.inventory.inventory import Inventory

from game.game_objects.projectiles.bullet import Bullet
from game.game_objects.projectiles.mine import Mine
from game.game_objects.projectiles.growing_barbed_chain import GrowingBarbedChain

from game.game_objects.equippables.weapons.weapon import Weapon
from game.game_objects.equippables.weapons.rifle import Rifle
from game.game_objects.equippables.weapons.mine_deployer import MineDeployer
from game.game_objects.equippables.weapons.chain_deployer import ChainDeployer

class Character(Playground_Object):
	def __init__(self, char_pos: pygame.Vector2, char_size: pygame.Vector2, char_speed: float):
		super().__init__(char_pos, char_size)

		self.m_health: int = 30
		self.m_char_speed: float = char_speed
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
			pygame.Vector2(0, -self.m_half_size.y),						# top
			pygame.Vector2(-self.m_half_size.x, self.m_half_size.y),	# bottom right
			pygame.Vector2(self.m_half_size.x, self.m_half_size.y)		# bottom left
		]

		self.update_draw_polygon_and_mask()

		# Weapon
		self.m_current_weapon: int = 1
		self.m_current_weapon_str: str = "Bullets"
		self.m_left_click: bool = False

		# Weapon Inventory
		rifle: Weapon = Rifle(self.m_pos, Vector2(5, 10),
							  300, self.m_look_direction, colors.PINK_RED, self, True)
		mine_deployer: Weapon = MineDeployer(self.m_pos, Vector2(5, 10),
							  30, self.m_look_direction, colors.SOFT_GREEN)
		chain_deployer: Weapon = ChainDeployer(self.m_pos, Vector2(5,10),
							  10, self.m_look_direction, colors.DARK_GREY)

		self.m_inventory: Inventory = Inventory()
		self.m_inventory.add_main_equipped(rifle)
		self.m_inventory.add_equipped_weapon(pygame.MOUSEBUTTONDOWN, rifle)
		self.m_inventory.add_equipped_weapon(pygame.K_e, mine_deployer)
		self.m_inventory.add_equipped_weapon(pygame.K_r, chain_deployer)

	def update(self):
		self.m_total_duration = self.m_time_handler.get_total_duration_ms()

		self.update_look_direction()
		self.update_draw_polygon_and_mask()
		self.update_equipped_pos_direction()

		self.m_inventory.update()

		keys = pygame.key.get_pressed()

		self.check_shoot()

		self.move_char(keys)

		self.try_to_deploy_mines(keys)
		self.try_to_throw_barbed_chain(keys)

	def update_look_direction(self):
		mousePos: tuple[int, int] = pygame.mouse.get_pos()

		mouse_pos_relative_to_playground: pygame.math.Vector2 = mousePos - self.m_game.get_screen_offset()
		self.m_look_direction: pygame.math.Vector2 = mouse_pos_relative_to_playground - self.m_pos

		if self.m_look_direction.length() == 0:
			self.m_look_direction.update(1, 0)  # Default direction if no movement
		else:
			self.m_look_direction.normalize_ip()

		self.m_look_angle = self.m_reference_vector.angle_to(self.m_look_direction)

	def update_draw_polygon_and_mask(self):
		self.image.fill((0, 0, 0, 0))

		rotated_points = []
		for point in self.m_points:
			# Rotate around (0,0) (the center of our conceptual sprite)
			rotated_point = point.rotate(self.m_look_angle)
			# Translate back to image coordinates (add half_width/height to move origin to top-left)
			translated_point = (rotated_point.x + self.m_half_hitbox_size.x,
								rotated_point.y + self.m_half_hitbox_size.y)
			rotated_points.append(translated_point)

		pygame.draw.polygon(self.image, self.m_color, rotated_points)

		self.mask = pygame.mask.from_surface(self.image)

	def update_equipped_pos_direction(self):
		self.m_inventory.updated_equipped_weapon_pos_and_direction(self.m_pos, self.m_look_direction)

	def move_char(self, keys):
		movement_direction = pygame.Vector2(keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
		if movement_direction.length() == 0:
			return

		movement_direction = movement_direction.normalize() * self.m_char_speed * self.m_time_handler.get_delta_time_s()

		self.setDisplacement(movement_direction)

	def check_shoot(self):
		if self.m_game.m_game_events.get_event(pygame.MOUSEBUTTONDOWN) and pygame.mouse.get_pressed()[0]:
			self.m_left_click = True
		if self.m_game.m_game_events.get_event(pygame.MOUSEBUTTONUP) and not pygame.mouse.get_pressed()[0]:
			self.m_left_click = False

		if not self.m_left_click:
			return

		self.m_inventory.main_triggered()

	def shoot_bullet(self):
		bullet: Bullet = Bullet(self.m_look_direction, self.m_pos, pygame.Vector2(10, 10))
		self.m_game.add_projectile_object(bullet)

	def deploy_mine(self):
		mine: Mine = Mine(self.m_pos, pygame.Vector2(25, 25))
		self.m_game.add_projectile_object(mine)

	def deploy_barbed_chain(self):
		barbed_chain: GrowingBarbedChain = GrowingBarbedChain(self.m_look_direction, self.m_pos, pygame.Vector2(30, 10))
		self.m_game.add_projectile_object(barbed_chain)

	def on_collision_with_npcs(self, npcs_hit: set[pygame.sprite.Sprite]):
		already_collided = False
		for npc in npcs_hit:
			if npc in self.m_in_collision_with_npc:
				already_collided = True

		self.m_in_collision_with_npc = npcs_hit

		total_duration: float = self.m_game.m_time_handler.get_total_duration_ms()
		if not already_collided or (already_collided and (total_duration - self.m_last_npc_collision_time) >= self.m_damage_delay_ms):
			self.m_last_npc_collision_time = total_duration
			self.damaged()

	def damaged(self):
		self.m_health -= 1
		if (self.m_health == 0):
			chars_died: list[int] = self.m_game.m_game_events.get_event(events_dictionary.CHAR_NO_DIED_EVENT)
			chars_died.append(1)
			self.m_game.m_game_events.change_event(events_dictionary.CHAR_NO_DIED_EVENT, chars_died)
			print("Dead!")

	def change_current_weapon(self, weapon_index: int):
		self.m_current_weapon = weapon_index
		match self.m_current_weapon:
			case 1:
				self.m_current_weapon_str: str = "Bullets"

	def try_to_deploy_mines(self, keys):
		if not keys[pygame.K_e]:
			return

		self.m_inventory.inventory_key_triggered(pygame.K_e)

	def try_to_throw_barbed_chain(self, keys):
		if not keys[pygame.K_r]:
			return

		self.m_inventory.inventory_key_triggered(pygame.K_r)


	def get_attach_anchor_pos(self) -> Vector2:
		top: Vector2 = Vector2(self.m_points[0]) # up

		top.rotate_ip(self.m_look_angle)

		top.x = top.x + self.m_pos.x
		top.y = top.y + self.m_pos.y

		return top