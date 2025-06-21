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

		self.m_font_source: str = "sys"
		self.m_inventory_font: pygame.font.Font | None = None
		self.m_default_font_size: int = 48
		self.set_font()

		self.m_cached_text_surfaces = {}

	def set_font(self):
		try:
			self.m_font_name = "Consolas"
			self.m_font = pygame.font.SysFont(self.m_font_name, self.m_default_font_size) # Has to be monospace
		except pygame.error:
			print("Default font not found, trying a system font.")
			self.m_font_name = pygame.font.match_font('dejavusans', bold=True) or \
						pygame.font.match_font('arial', bold=True) or \
						pygame.font.match_font('sans', bold=True)
			if self.m_font_name:
				self.m_font = pygame.font.Font(self.m_font_name, self.m_default_font_size)
				self.m_font_source = "file"
			else:
				print("No suitable font found! Text rendering might fail.")
				self.m_font_name = None
				self.m_font = pygame.font.SysFont(None, self.m_default_font_size)

		current_size = self.m_font.get_height()
		is_bold = self.m_font.get_bold()
		is_italic = self.m_font.get_italic()
		new_size = max(1, current_size // 2)

		if self.m_font_source == 'file':
			self.m_inventory_font = pygame.font.Font(self.m_font_name, new_size)
		else:
			self.m_inventory_font = pygame.font.SysFont(self.m_font_name, new_size, bold=is_bold, italic=is_italic)

	def update(self, player: Character, score: int):
		self.update_FPS()

		self.write_FPS(self.m_fps_str)

		healthRectTopLeft: pygame.Vector2 = self.write_health(player.m_health)

		lastRectTopLeft: pygame.Vector2 = healthRectTopLeft
		for key, weapon in player.m_inventory.m_weapon_inventory.items():
			inventoryRectTopLeft: pygame.Vector2 = self.write_weapon_cooldown_s(lastRectTopLeft, weapon.m_equippable_name, 1, weapon.m_current_cooldown_s, pygame.key.name(key))
			lastRectTopLeft = inventoryRectTopLeft

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
		if not self.m_inventory_font:
			return pygame.Vector2(0, 0)

		formatted_name = f"{current_weapon[:6]:<6}"
		if button != "":
			formatted_name += "("+ button + ")"

		formatted_name = f"{formatted_name[:9]:<9}"

		cd: str
		if cooldown == 0:
			cd = f"{'READY':>5}"
		else:
			cd = f"{cooldown:5.2f}"

		text: str = f"{formatted_name} | {cd}"

		if text not in self.m_cached_text_surfaces:
			text_surface = self.m_inventory_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			self.m_cached_text_surfaces[text] = (text_surface, text_rect)
		else:
			text_surface, text_rect = self.m_cached_text_surfaces[text]

		padding = 10

		blit_rect = text_rect.copy()
		blit_rect.bottomleft = (padding, bottom_left.y)
		self.m_screen.m_window.blit(text_surface, blit_rect)

		return pygame.Vector2(blit_rect.topleft)

	def write_score(self, score: int):
		if not self.m_font:
			return

		text: str = f"Score: {score}"

		if text not in self.m_cached_text_surfaces:
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			self.m_cached_text_surfaces[text] = (text_surface, text_rect)
		else:
			text_surface, text_rect = self.m_cached_text_surfaces[text]

		padding = 10
		blit_rect = text_rect.copy()
		blit_rect.center = (self.m_screen.m_window.get_width() / 2, padding + text_rect.height / 2)
		self.m_screen.m_window.blit(text_surface, blit_rect)

	def update_FPS(self):
		current_time: float = self.m_timer_handler.get_total_duration_ms()
		if current_time - self.m_fps_start_timer >= self.m_FPS_UPDATE_INTERVAL:
			fps: int = self.m_timer_handler.get_fps()
			self.m_fps_str = f"FPS: {fps}"
			self.m_fps_start_timer = current_time

	def write_FPS(self, text: str):
		if not self.m_font:
			return

		if text not in self.m_cached_text_surfaces:
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			self.m_cached_text_surfaces[text] = (text_surface, text_rect)
		else:
			text_surface, text_rect = self.m_cached_text_surfaces[text]

		padding = 10
		blit_rect = text_rect.copy()
		blit_rect.topleft = (padding, padding)
		self.m_screen.m_window.blit(text_surface, blit_rect)