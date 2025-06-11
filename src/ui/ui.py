import pygame

import resources.colors as colors

from time_handler import Time_Handler


class User_Interface:
	def __init__(self, window_size: tuple[int, int], time_handler: Time_Handler):
		self.m_window: pygame.Surface = pygame.display.set_mode(window_size)
		pygame.display.set_caption("Movable Character with Toggleable Camera")

		self.m_timer_handler: Time_Handler = time_handler

		self.m_fps_str: str = "FPS: 0"
		self.m_fps_start_timer: float = self.m_timer_handler.get_total_duration_ms()
		self.m_FPS_UPDATE_INTERVAL: float = 0.5

		self.m_font: pygame.font.Font | None = None
		self.set_font()

	def get_window(self) -> pygame.Surface:
		return self.m_window

	def reset_window_fill(self):
		self.m_window.fill(colors.BLACK)

	def set_font(self):
		try:
			self.m_font = pygame.font.Font(None, 48)
		except pygame.error:
			print("Default font not found, trying a system font.")
			font_name = pygame.font.match_font('dejavusans', bold=True) or \
						pygame.font.match_font('arial', bold=True) or \
						pygame.font.match_font('sans', bold=True)
			if font_name:
				self.m_font = pygame.font.Font(font_name, 48)
			else:
				print("No suitable font found! Text rendering might fail.")
				self.m_font = None

	def update(self, health: int, current_weapon: str, score: int):
		self.update_FPS()

		self.write_FPS(self.m_fps_str)

		healthRectSize: pygame.Vector2 = self.write_health(health)
		self.write_current_weapon(healthRectSize, current_weapon)

		self.write_score(score)

	def write_health(self, health: int) -> pygame.Vector2:
		if self.m_font:
			text: str = f"HP: {health}"
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.bottomleft = (padding, self.m_window.get_height() - padding)
			self.m_window.blit(text_surface, text_rect)
			return pygame.Vector2(text_rect.size)
		else:
			return pygame.Vector2(0, 0)

	def write_current_weapon(self, healthRectSize: pygame.Vector2, current_weapon: str):
		if self.m_font:
			text_surface = self.m_font.render(current_weapon, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.bottomleft = (padding, self.m_window.get_height() - padding - healthRectSize.y)
			self.m_window.blit(text_surface, text_rect)

	def write_score(self, score: int):
		if self.m_font:
			text: str = f"Score: {score}"
			text_surface = self.m_font.render(text, True, colors.WHITE)
			text_rect = text_surface.get_rect()
			padding = 10
			text_rect.center = (self.m_window.get_width() / 2, padding + text_rect.height / 2)
			self.m_window.blit(text_surface, text_rect)

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
			self.m_window.blit(text_surface, text_rect)