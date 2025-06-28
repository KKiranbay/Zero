# This UI displays a pause menu with pre-rendered surfaces for optimal performance.
# Key Pygame-ce elements:
# - pygame.Surface: Pre-created overlay and title surfaces
# - pygame.Rect: Panel positioning and drawing
# - Button class: Custom button components for user interaction

from enum import Enum

import pygame

from ui.components.button import Button
from screen import Screen
import resources.colors as colors

class PauseMenuRequestEnum(Enum):
	NONE = 1
	RESUME = 2
	SAVE = 3
	MAIN_MENU = 4
	EXIT_CONFIRMED = 5

class PauseMenuUI:
	def __init__(self):
		self.m_screen: Screen = Screen()

		# Font setup
		try:
			self.m_menu_font = pygame.font.SysFont("Consolas", 42)
		except pygame.error:
			self.m_menu_font = pygame.font.Font(None, 42)

		# UI dimensions
		self.m_panel_width = 350
		self.m_panel_height = 400
		screen_width = self.m_screen.m_window.get_width()
		screen_height = self.m_screen.m_window.get_height()

		# Center panel
		self.m_panel_x = (screen_width - self.m_panel_width) // 2
		self.m_panel_y = (screen_height - self.m_panel_height) // 2

		# Pre-create panel rect
		self.m_panel_rect = pygame.Rect(self.m_panel_x, self.m_panel_y, self.m_panel_width, self.m_panel_height)

		# Pre-create overlay surface
		self.m_overlay_surface = pygame.Surface((screen_width, screen_height))
		self.m_overlay_surface.set_alpha(150)
		self.m_overlay_surface.fill((0, 0, 0))

		# Pre-render title
		self.m_title_surface = self.m_menu_font.render("PAUSED", True, colors.WHITE)
		title_rect = self.m_title_surface.get_rect()
		self.m_title_x = self.m_panel_x + (self.m_panel_width - title_rect.width) // 2
		self.m_title_y = self.m_panel_y + 20

		# Button setup
		self.m_button_width = 250
		self.m_button_height = 60
		self.m_button_spacing = 20
		button_x = self.m_panel_x + (self.m_panel_width - self.m_button_width) // 2

		# Create buttons
		self.m_resume_button = Button(
			x=button_x, y=self.m_panel_y + self.m_button_height + self.m_button_spacing,
			width=self.m_button_width, height=self.m_button_height,
			text="Resume",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_menu_font
		)

		self.m_save_button = Button(
			x=button_x, y=self.m_panel_y + (self.m_button_height + self.m_button_spacing) * 2,
			width=self.m_button_width, height=self.m_button_height,
			text="Save Game",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_menu_font
		)

		self.m_main_menu_button = Button(
			x=button_x, y=self.m_panel_y + (self.m_button_height + self.m_button_spacing) * 3,
			width=self.m_button_width, height=self.m_button_height,
			text="Main Menu",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_menu_font
		)

		self.m_exit_button = Button(
			x=button_x, y=self.m_panel_y + (self.m_button_height + self.m_button_spacing) * 4,
			width=self.m_button_width, height=self.m_button_height,
			text="Exit Game",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_menu_font
		)

		self.m_buttons = [self.m_resume_button, self.m_save_button, self.m_main_menu_button, self.m_exit_button]

		# Confirmation dialog state
		self.m_show_exit_confirmation = False
		self.m_confirmation_font = pygame.font.SysFont("Consolas", 28)

		self.setup_exit_confirmation_dialog()

	def setup_exit_confirmation_dialog(self):
		self.m_dialog_width = 350
		self.m_dialog_height = 150
		self.m_dialog_x = (self.m_screen.m_window.get_width() - self.m_dialog_width) // 2
		self.m_dialog_y = (self.m_screen.m_window.get_height() - self.m_dialog_height) // 2

		self.m_dialog_rect = pygame.Rect(self.m_dialog_x, self.m_dialog_y, self.m_dialog_width, self.m_dialog_height)

		self.m_confirmation_text_surface = self.m_confirmation_font.render("Exit without saving?", True, colors.WHITE)
		text_rect = self.m_confirmation_text_surface.get_rect()
		self.m_confirmation_text_x = self.m_dialog_x + (self.m_dialog_width - text_rect.width) // 2
		self.m_confirmation_text_y = self.m_dialog_y + 30

		button_width = 80
		button_height = 40
		button_y = self.m_dialog_y + 90

		self.m_yes_button = Button(
			x=self.m_dialog_x + 50, y=button_y,
			width=button_width, height=button_height,
			text="Yes",
			base_color=colors.RED, hover_color=colors.PINK_RED,
			text_color=colors.WHITE, font=self.m_confirmation_font
		)

		self.m_no_button = Button(
			x=self.m_dialog_x + 170, y=button_y,
			width=button_width, height=button_height,
			text="No",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_confirmation_font
		)

	def draw(self):
		self.m_screen.m_window.blit(self.m_overlay_surface, (0, 0))

		pygame.draw.rect(self.m_screen.m_window, colors.DARK_GREY, self.m_panel_rect)
		pygame.draw.rect(self.m_screen.m_window, colors.WHITE, self.m_panel_rect, 3)

		self.m_screen.m_window.blit(self.m_title_surface, (self.m_title_x, self.m_title_y))

		# Draw buttons
		for button in self.m_buttons:
			button.draw()

		# Draw exit confirmation if needed
		if self.m_show_exit_confirmation:
			self.draw_exit_confirmation()

	def draw_exit_confirmation(self):
		pygame.draw.rect(self.m_screen.m_window, colors.DARK_GREY, self.m_dialog_rect)
		pygame.draw.rect(self.m_screen.m_window, colors.RED, self.m_dialog_rect, 2)

		self.m_screen.m_window.blit(self.m_confirmation_text_surface, (self.m_confirmation_text_x, self.m_confirmation_text_y))

		self.m_yes_button.draw()
		self.m_no_button.draw()

	def get_ui_requests(self):
		if self.m_show_exit_confirmation:
			return self.handle_exit_confirmation()

		for button in self.m_buttons:
			button.check_button_events()

		if self.m_exit_button.m_is_clicked:
			self.m_show_exit_confirmation = True
			return PauseMenuRequestEnum.NONE

		if self.m_resume_button.m_is_clicked:
			return PauseMenuRequestEnum.RESUME
		elif self.m_save_button.m_is_clicked:
			return PauseMenuRequestEnum.SAVE
		elif self.m_main_menu_button.m_is_clicked:
			return PauseMenuRequestEnum.MAIN_MENU

		return PauseMenuRequestEnum.NONE

	def handle_exit_confirmation(self):
		self.m_yes_button.check_button_events()
		self.m_no_button.check_button_events()

		if self.m_yes_button.m_is_clicked:
			return PauseMenuRequestEnum.EXIT_CONFIRMED
		elif self.m_no_button.m_is_clicked:
			self.m_show_exit_confirmation = False
			return PauseMenuRequestEnum.NONE

		return PauseMenuRequestEnum.NONE