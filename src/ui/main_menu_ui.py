import pygame

from ui.components.button import Button
from screen import Screen

import resources.colors as colors

class Main_Menu_UI:
	def __init__(self) -> None:
		try:
			self.m_menu_font = pygame.font.SysFont("Segoe UI", 50)
		except pygame.error:
			self.m_menu_font = pygame.font.Font(None, 50)

		self.m_screen: Screen = Screen()
		self.m_button_width = 250
		self.m_button_height = 70
		self.m_center_x = (self.m_screen.m_window.get_width() - self.m_button_width) // 2

		self.m_start_button: Button = Button(
			x=self.m_center_x, y=200,
			width=self.m_button_width, height=self.m_button_height,
			text="Start Game",
			base_color=colors.DARK_NAVY,
			hover_color=colors.NAVY,
			text_color=colors.WHITE,
			font=self.m_menu_font
		)

		self.m_exit_button: Button = Button(
			x=self.m_center_x, y=300,
			width=self.m_button_width, height=self.m_button_height,
			text="Exit",
			base_color=colors.DARK_NAVY,
			hover_color=colors.NAVY,
			text_color=colors.WHITE,
			font=self.m_menu_font
		)

		self.m_buttons: list[Button] = [self.m_start_button, self.m_exit_button]

	def draw(self):
		for button in self.m_buttons:
			button.draw()

	def check_ui_events(self):
		for button in self.m_buttons:
			button.check_button_events()

	def is_start_button_clicked(self):
		return self.m_start_button.m_is_clicked

	def is_exit_button_clicked(self):
		return self.m_exit_button.m_is_clicked