import pygame

import colors
import helper

from game import Game
from playground import Playground
from playground_object import Playground_Object
from projectile import Projectile

class Character(Playground_Object):
	def __init__(self, char_x: float, char_y: float, char_size: int, char_speed: float):
		super().__init__(char_x, char_y, char_size)
		self.m_char_speed: float = char_speed
		self.image.fill(colors.DARK_GREEN)

	def update(self, dt: float, game: Game):
		self.move_char(dt, game)
		self.shoot(game)
		pass

	def move_char(self, dt: float, game: Game):
		playground: Playground = game.m_playground
		original_x = self.rect.centerx
		original_y = self.rect.centery

		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.rect.centerx -= self.m_char_speed * dt
		if keys[pygame.K_d]:
			self.rect.centerx += self.m_char_speed * dt

		if keys[pygame.K_w]:
			self.rect.centery -= self.m_char_speed * dt
		if keys[pygame.K_s]:
			self.rect.centery += self.m_char_speed * dt

		self.check_and_clamp_ip_with_playground(playground.m_game_rect)

	def shoot(self, game: Game):
		shoot: bool = False

		for event in game.m_events:
			if event.type == pygame.MOUSEBUTTONDOWN:
				shoot = True

		# mouse_buttons = pygame.mouse.get_pressed()
		# shoot = mouse_buttons[0]

		if shoot:
			playground: Playground = game.m_playground

			mousePos: tuple[int, int] = pygame.mouse.get_pos()

			mouse_pos_relative_to_playground_x = mousePos[0] - playground.m_screen_rect.topleft[0]
			mouse_pos_relative_to_playground_y = mousePos[1] - playground.m_screen_rect.topleft[1]

			direction_x = mouse_pos_relative_to_playground_x - self.rect.centerx
			direction_y = mouse_pos_relative_to_playground_y - self.rect.centery

			norm_direction: pygame.math.Vector2 = helper.normalize_vector(direction_x, direction_y)

			projectile: Projectile = Projectile(norm_direction, self.rect.centerx, self.rect.centery, 10)
			game.add_projectile_object(projectile)