# This UI displays a sleek, metal-design game over screen with restart and exit options.
# Key Pygame-ce elements:
# - pygame.Surface: For creating overlay backgrounds and metallic effects
# - pygame.draw: For drawing metallic borders and gradients
# - pygame.font.Font: For rendering game over text
# - Button class: Custom button components for user interaction

import pygame

from ui.components.button import Button

import resources.colors as colors

from screen import Screen

from time_handler import Time_Handler


class GameOverUI:
	def __init__(self):
		self.m_screen: Screen = Screen()
		self.m_time_handler: Time_Handler = Time_Handler()

		# Metal color palette for sleek design
		self.m_metal_dark = (45, 45, 50)
		self.m_metal_light = (120, 125, 130)
		self.m_metal_accent = (180, 185, 190)
		self.m_metal_highlight = (220, 225, 230)
		self.m_overlay_color = (0, 0, 0, 180)  # Semi-transparent black

		# Fonts
		self.m_title_font = pygame.font.SysFont("Arial", 72, bold=True)
		self.m_button_font = pygame.font.SysFont("Arial", 36, bold=True)

		# UI dimensions
		self.m_panel_width = 400
		self.m_panel_height = 300
		screen_width = self.m_screen.m_window.get_width()
		screen_height = self.m_screen.m_window.get_height()

		# Center the panel
		self.m_panel_x = (screen_width - self.m_panel_width) // 2
		self.m_panel_y = (screen_height - self.m_panel_height) // 2

		# Button dimensions
		button_width = 200
		button_height = 50
		button_spacing = 20

		# Create buttons centered in the panel
		restart_x = self.m_panel_x + (self.m_panel_width - button_width) // 2
		restart_y = self.m_panel_y + 150

		main_menu_x = restart_x
		main_menu_y = restart_y + button_height + button_spacing

		self.m_restart_button = Button(
			restart_x, restart_y, button_width, button_height,
			"RESTART",
			self.m_metal_dark, self.m_metal_light, colors.WHITE, self.m_button_font
		)

		self.m_main_menu_button = Button(
			main_menu_x, main_menu_y, button_width, button_height,
			"MAIN MENU",
			self.m_metal_dark, self.m_metal_light, colors.WHITE, self.m_button_font
		)

		# Game over text
		self.m_title_text = self.m_title_font.render("GAME OVER", True, self.m_metal_highlight)
		title_rect = self.m_title_text.get_rect()
		self.m_title_x = self.m_panel_x + (self.m_panel_width - title_rect.width) // 2
		self.m_title_y = self.m_panel_y + 40

		# Animation variables
		self.m_glow_intensity_f: float = 0.0
		self.m_glow_intensity_i: int = 0
		self.m_glow_direction: int = 1

	def update(self):
		# Update glow animation
		self.m_glow_intensity_f += self.m_glow_direction * (self.m_time_handler.get_delta_time_ms() / 10.0)
		if self.m_glow_intensity_f >= 50:
			self.m_glow_direction = -1
		elif self.m_glow_intensity_f <= 0:
			self.m_glow_direction = 1

		self.m_glow_intensity_i = int(self.m_glow_intensity_f)

		self.m_restart_button.check_button_events()
		self.m_main_menu_button.check_button_events()

		restart_clicked = self.m_restart_button.m_is_clicked
		main_menu_clicked = self.m_main_menu_button.m_is_clicked

		return restart_clicked, main_menu_clicked

	def draw(self):
		overlay = pygame.Surface((self.m_screen.m_window.get_width(), self.m_screen.m_window.get_height()))
		overlay.set_alpha(180)
		overlay.fill((0, 0, 0))
		self.m_screen.m_window.blit(overlay, (0, 0))

		self.draw_metallic_panel()

		self.draw_glow_border()

		self.draw_title()

		self.m_restart_button.draw()
		self.m_main_menu_button.draw()

	def draw_metallic_panel(self):
		panel_rect = pygame.Rect(self.m_panel_x, self.m_panel_y, self.m_panel_width, self.m_panel_height)

		# Create gradient effect
		for i in range(self.m_panel_height):
			ratio = i / self.m_panel_height
			# Create metallic gradient from dark to light
			r = int(self.m_metal_dark[0] + (self.m_metal_light[0] - self.m_metal_dark[0]) * ratio)
			g = int(self.m_metal_dark[1] + (self.m_metal_light[1] - self.m_metal_dark[1]) * ratio)
			b = int(self.m_metal_dark[2] + (self.m_metal_light[2] - self.m_metal_dark[2]) * ratio)

			line_rect = pygame.Rect(self.m_panel_x, self.m_panel_y + i, self.m_panel_width, 1)
			pygame.draw.rect(self.m_screen.m_window, (r, g, b), line_rect)

		# Add metallic border
		pygame.draw.rect(self.m_screen.m_window, self.m_metal_accent, panel_rect, 3)

	def draw_glow_border(self):
		glow_color_intensity = min(255, 100 + self.m_glow_intensity_i)
		glow_color = (glow_color_intensity, glow_color_intensity, glow_color_intensity)

		# Draw multiple border lines for glow effect
		for thickness in range(1, 4):
			border_rect = pygame.Rect(
				self.m_panel_x - thickness,
				self.m_panel_y - thickness,
				self.m_panel_width + thickness * 2,
				self.m_panel_height + thickness * 2
			)

			alpha_value = 100 - (thickness * 25)

			# Create temporary surface for alpha blending
			glow_surface = pygame.Surface((border_rect.width, border_rect.height))
			glow_surface.set_alpha(alpha_value)
			pygame.draw.rect(glow_surface, glow_color, (0, 0, border_rect.width, border_rect.height), thickness)
			self.m_screen.m_window.blit(glow_surface, (border_rect.x, border_rect.y))

	def draw_title(self):
		# Draw shadow first
		shadow_surface = self.m_title_font.render("GAME OVER", True, self.m_metal_dark)
		self.m_screen.m_window.blit(shadow_surface, (self.m_title_x + 3, self.m_title_y + 3))

		# Draw main title
		self.m_screen.m_window.blit(self.m_title_text, (self.m_title_x, self.m_title_y))

		# Add highlight effect
		highlight_surface = self.m_title_font.render("GAME OVER", True, self.m_metal_highlight)
		highlight_surface.set_alpha(50 + self.m_glow_intensity_i)
		self.m_screen.m_window.blit(highlight_surface, (self.m_title_x - 1, self.m_title_y - 1))
