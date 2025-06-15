import pygame

import events_dictionary as events_dictionary

from states_enum import StatesEnum

from states.state import State

from ui.main_menu_ui import Main_Menu_UI

class MainMenuState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.GAME_STATE
		self.m_main_menu_ui: Main_Menu_UI = Main_Menu_UI()

	def startup(self, persistent):
		self.persist = persistent

	def check_events(self):
		self.m_main_menu_ui.check_ui_events()

		if self.m_main_menu_ui.is_start_button_clicked():
			self.done = True
			self.next_state = StatesEnum.GAME_STATE

		if self.m_main_menu_ui.is_exit_button_clicked():
			self.events.change_event(events_dictionary.EXIT_GAME_EVENT, True)

	def update(self):
		pass

	def draw(self):
		self.screen.reset_window_fill()
		self.m_main_menu_ui.draw()