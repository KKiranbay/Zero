import pygame

from systems.save_game_system import SaveGameSystem

from ui.components.button import Button
from screen import Screen

import resources.colors as colors

class Main_Menu_UI:
	def __init__(self) -> None:
		self.m_save_game_system_main_menu = SaveGameSystem()

		try:
			self.m_menu_font = pygame.font.SysFont("Consolas", 50)
		except pygame.error:
			self.m_menu_font = pygame.font.Font(None, 50)

		self.m_screen: Screen = Screen()
		self.m_button_width = 300
		self.m_button_height = 100
		self.m_button_spacing = 20
		self.m_center_x = (self.m_screen.m_window.get_width() - self.m_button_width) // 2

		self.m_load_button = None

		load_button_available: bool = self.m_save_game_system_main_menu.has_save_file()
		number_of_buttons = 2
		if load_button_available:
			number_of_buttons += 1

		self.m_center_y = (self.m_screen.m_window.get_height() - (self.m_button_height * number_of_buttons + self.m_button_spacing * (number_of_buttons - 1))) // 2

		self.m_start_button: Button = Button(
			x=self.m_center_x, y=self.m_center_y,
			width=self.m_button_width, height=self.m_button_height,
			text="Start Game",
			base_color=colors.DARK_NAVY,
			hover_color=colors.NAVY,
			text_color=colors.WHITE,
			font=self.m_menu_font
		)

		button_y_jump = self.m_button_height + self.m_button_spacing

		if load_button_available:

			self.m_load_button = Button(
				x=self.m_center_x, y=self.m_center_y + button_y_jump,
				width=self.m_button_width, height=self.m_button_height,
				text="Load Game",
				base_color=colors.DARK_NAVY,
				hover_color=colors.NAVY,
				text_color=colors.WHITE,
				font=self.m_menu_font
			)

		if load_button_available:
			exit_button_y = self.m_center_y + button_y_jump * 2
		else:
			exit_button_y = self.m_center_y + button_y_jump

		self.m_exit_button: Button = Button(
			x=self.m_center_x, y=exit_button_y,
			width=self.m_button_width, height=self.m_button_height,
			text="Exit",
			base_color=colors.DARK_NAVY,
			hover_color=colors.NAVY,
			text_color=colors.WHITE,
			font=self.m_menu_font
		)

		self.m_buttons: list[Button] = [self.m_start_button, self.m_exit_button]
		if load_button_available:
			assert self.m_load_button is not None
			self.m_buttons.insert(1, self.m_load_button)

	def draw(self):
		for button in self.m_buttons:
			button.draw()

	def check_ui_events(self):
		for button in self.m_buttons:
			button.check_button_events()

	def is_start_button_clicked(self):
		return self.m_start_button.m_is_clicked

	def is_load_button_clicked(self):
		return self.m_load_button and self.m_load_button.m_is_clicked

	def is_exit_button_clicked(self):
		return self.m_exit_button.m_is_clicked