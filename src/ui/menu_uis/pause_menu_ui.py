from enum import Enum

import pygame

from ui.components.button import Button
from screen import Screen
import resources.colors as colors

class PauseMenuRequestEnum(Enum):
	NONE = 1
	RESUME = 2
	SAVE = 3
	EXIT_CONFIRMED = 4

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

		self.m_exit_button = Button(
			x=button_x, y=self.m_panel_y + (self.m_button_height + self.m_button_spacing) * 3,
			width=self.m_button_width, height=self.m_button_height,
			text="Exit Game",
			base_color=colors.DARK_NAVY, hover_color=colors.NAVY,
			text_color=colors.WHITE, font=self.m_menu_font
		)

		self.m_buttons = [self.m_resume_button, self.m_save_button, self.m_exit_button]

		# Confirmation dialog state
		self.m_show_exit_confirmation = False
		self.m_confirmation_font = pygame.font.SysFont("Consolas", 28)

	def draw(self):
		# Semi-transparent overlay
		overlay = pygame.Surface((self.m_screen.m_window.get_width(), self.m_screen.m_window.get_height()))
		overlay.set_alpha(150)
		overlay.fill((0, 0, 0))
		self.m_screen.m_window.blit(overlay, (0, 0))

		# Draw panel background
		panel_rect = pygame.Rect(self.m_panel_x, self.m_panel_y, self.m_panel_width, self.m_panel_height)
		pygame.draw.rect(self.m_screen.m_window, colors.DARK_GREY, panel_rect)
		pygame.draw.rect(self.m_screen.m_window, colors.WHITE, panel_rect, 3)

		# Draw title
		title_surface = self.m_menu_font.render("PAUSED", True, colors.WHITE)
		title_rect = title_surface.get_rect()
		title_x = self.m_panel_x + (self.m_panel_width - title_rect.width) // 2
		title_y = self.m_panel_y + 20
		self.m_screen.m_window.blit(title_surface, (title_x, title_y))

		# Draw buttons
		for button in self.m_buttons:
			button.draw()

		# Draw exit confirmation if needed
		if self.m_show_exit_confirmation:
			self.draw_exit_confirmation()

	def draw_exit_confirmation(self):
		# Confirmation dialog background
		dialog_width = 300
		dialog_height = 150
		dialog_x = (self.m_screen.m_window.get_width() - dialog_width) // 2
		dialog_y = (self.m_screen.m_window.get_height() - dialog_height) // 2

		dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
		pygame.draw.rect(self.m_screen.m_window, colors.DARK_GREY, dialog_rect)
		pygame.draw.rect(self.m_screen.m_window, colors.RED, dialog_rect, 2)

		# Confirmation text
		text_surface = self.m_confirmation_font.render("Exit without saving?", True, colors.WHITE)
		text_rect = text_surface.get_rect()
		text_x = dialog_x + (dialog_width - text_rect.width) // 2
		text_y = dialog_y + 30
		self.m_screen.m_window.blit(text_surface, (text_x, text_y))

		# Yes/No buttons (simplified drawing)
		yes_rect = pygame.Rect(dialog_x + 50, dialog_y + 90, 80, 40)
		no_rect = pygame.Rect(dialog_x + 170, dialog_y + 90, 80, 40)

		pygame.draw.rect(self.m_screen.m_window, colors.RED, yes_rect)
		pygame.draw.rect(self.m_screen.m_window, colors.DARK_NAVY, no_rect)

		yes_text = self.m_confirmation_font.render("Yes", True, colors.WHITE)
		no_text = self.m_confirmation_font.render("No", True, colors.WHITE)

		self.m_screen.m_window.blit(yes_text, yes_rect.center)
		self.m_screen.m_window.blit(no_text, no_rect.center)

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

		return PauseMenuRequestEnum.NONE

	def handle_exit_confirmation(self):
		mouse_pos = pygame.mouse.get_pos()
		mouse_clicked = pygame.mouse.get_pressed()[0]

		dialog_width = 300
		dialog_height = 150
		dialog_x = (self.m_screen.m_window.get_width() - dialog_width) // 2
		dialog_y = (self.m_screen.m_window.get_height() - dialog_height) // 2

		yes_rect = pygame.Rect(dialog_x + 50, dialog_y + 90, 80, 40)
		no_rect = pygame.Rect(dialog_x + 170, dialog_y + 90, 80, 40)

		if mouse_clicked:
			if yes_rect.collidepoint(mouse_pos):
				return PauseMenuRequestEnum.EXIT_CONFIRMED
			elif no_rect.collidepoint(mouse_pos):
				self.m_show_exit_confirmation = False
				return PauseMenuRequestEnum.NONE

		return PauseMenuRequestEnum.NONE