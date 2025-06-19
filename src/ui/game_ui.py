import pygame

from game.game_objects.characters.character import Character

import resources.colors as colors

from screen import Screen
from time_handler import Time_Handler


class Game_UI:
	def __init__(self):
		self.m_screen: Screen = Screen()

		self.m_timer_handler: Time_Handler = Time_Handler()

		self.m_fps_str: str = "FPS: 0"
		self.m_fps_start_timer: float = self.m_timer_handler.get_total_duration_ms()
		self.m_FPS_UPDATE_INTERVAL: float = 0.5

		self.m_font: pygame.font.Font | None = None
		self.m_default_font_size: int = 48
		self.set_font()

	def set_font(self):
		try:
			self.m_font = pygame.font.SysFont("Consolas", self.m_default_font_size) # Has to be monospace
		except pygame.error:
			print("Default font not found, trying a system font.")
			font_name = pygame.font.match_font('dejavusans', bold=True) or \
						pygame.font.match_font('arial', bold=True) or \
						pygame.font.match_font('sans', bold=True)
			if font_name:
				self.m_font = pygame.font.Font(font_name, self.m_default_font_size)
			else:
				print("No suitable font found! Text rendering might fail.")
				self.m_font = pygame.font.SysFont(None, self.m_default_font_size)

	def update(self, player: Character, score: int):
		self.update_FPS()

		self.write_FPS(self.m_fps_str)

		healthRectTopLeft: pygame.Vector2 = self.write_health(player.m_health)

		currentWeaponRectTopLeft: pygame.Vector2 = self.write_current_weapon(healthRectTopLeft, player.m_current_weapon_str)
		cdMineDeployerRectTopLeft: pygame.Vector2 = self.write_weapon_cooldown_s(currentWeaponRectTopLeft, player.mine_deployer.m_weapon_name, 1, player.mine_deployer.m_current_cooldown_s, "E")
		cdChainDeployerRectTopLeft: pygame.Vector2 = self.write_weapon_cooldown_s(cdMineDeployerRectTopLeft, player.chain_deployer.m_weapon_name, 2, player.chain_deployer.m_current_cooldown_s, "R")

		self.write_score(score)

	def write_health(self, health: int) -> pygame.Vector2:
		if self.m_font:
			text: str = f"HP: {health}"
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.bottomleft = (padding, self.m_screen.m_window.get_height() - padding)
			self.m_screen.m_window.blit(text_surface, text_rect)
			return pygame.Vector2(text_rect.topleft)
		else:
			return pygame.Vector2(0, 0)

	def write_weapon_cooldown_s(self, bottom_left: pygame.Vector2, current_weapon: str, index: int, cooldown: float, button: str)-> pygame.Vector2:
		if self.m_font:
			self.m_font.set_point_size(self.m_default_font_size // 2)

			formatted_name = "(" + button + ") " + current_weapon
			formatted_name = f"{formatted_name[:10]:<10}"

			cd: str
			if cooldown == 0:
				cd = f"{'READY':>5}"
			else:
				cd = f"{cooldown:5.2f}"

			text: str = f"{formatted_name} | {cd}"
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.bottomleft = (padding, bottom_left.y)
			self.m_screen.m_window.blit(text_surface, text_rect)

			self.m_font.set_point_size(self.m_default_font_size)

			return pygame.Vector2(text_rect.topleft)
		else:
			return pygame.Vector2(0, 0)

	def write_current_weapon(self, bottom_left: pygame.Vector2, current_weapon: str)-> pygame.Vector2:
		if self.m_font:
			self.m_font.set_point_size(self.m_default_font_size // 2)

			text_surface = self.m_font.render(current_weapon, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.bottomleft = (padding, bottom_left.y)
			self.m_screen.m_window.blit(text_surface, text_rect)

			self.m_font.set_point_size(self.m_default_font_size)
			return pygame.Vector2(text_rect.topleft)
		else:
			return pygame.Vector2(0, 0)

	def write_score(self, score: int):
		if self.m_font:
			text: str = f"Score: {score}"
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.center = (self.m_screen.m_window.get_width() / 2, padding + text_rect.height / 2)
			self.m_screen.m_window.blit(text_surface, text_rect)

	def update_FPS(self):
		current_time: float = self.m_timer_handler.get_total_duration_ms()
		if current_time - self.m_fps_start_timer >= self.m_FPS_UPDATE_INTERVAL:
			fps: int = self.m_timer_handler.get_fps()
			self.m_fps_str = f"FPS: {fps}"
			self.m_fps_start_timer = current_time

	def write_FPS(self, text: str):
		if self.m_font:
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.topleft = (padding, padding)
			self.m_screen.m_window.blit(text_surface, text_rect)