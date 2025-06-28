import pygame

import events_dictionary as events_dictionary

from game.camera import Camera
from game.game import Game
from game.playground import Playground

from game.game_objects.characters.character import Character
from game.game_objects.npcs.npc import NPC, NPC_Type

from systems.save_game_system import SaveGameSystem

from ui.game_ui import Game_UI
from ui.menu_uis.pause_menu_ui import PauseMenuUI, PauseMenuRequestEnum

import resources.colors as colors

from states_enum import StatesEnum

from states.state import State


class GameState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.MAIN_MENU

		self.m_game: Game = Game()

		self.m_is_paused = False
		self.m_pause_menu_ui = None
		self.m_save_game_system = SaveGameSystem()

	def startup(self, persistent):
		self.persist = persistent
		self.m_is_paused = False

		if self.previous_state == StatesEnum.MAIN_MENU:
			self.initialize_game_objects()
		elif self.previous_state == StatesEnum.LOAD_GAME_STATE:
			self.game_loaded_successfully = self.persist.get('game_loaded', None)
			if not self.game_loaded_successfully:
				self.initialize_game_objects()

		self.m_game_ui : Game_UI = Game_UI()

	def initialize_game_objects(self):
		self.m_game.reinitialize()

		playground_width = 500
		playground_height = 500
		playground = Playground(self.screen.m_window, playground_width, playground_height, colors.BEIGE)
		self.m_game.add_playground(playground)

		player = Character(pygame.Vector2(playground.m_game_world_rect.width // 2, playground.m_game_world_rect.height // 2), pygame.Vector2(50,50), 500)
		self.m_game.add_char_object(player)

		camera = Camera(pygame.Vector2(player.rect.center), self.screen.m_window.get_width(), self.screen.m_window.get_height())
		self.m_game.add_camera(camera)

		target = NPC(NPC_Type.ENEMY, pygame.Vector2(100, 100), pygame.Vector2(20,20))
		self.m_game.add_npc_object(target)

		self.m_game.start_spawn_system()

	def check_events(self):
		if self.events.get_event(pygame.KEYDOWN) is None:
			return

		key_pressed = self.events.get_event(pygame.KEYDOWN).key

		if key_pressed == pygame.K_ESCAPE:
			if self.m_is_paused:
				self.resume_game()
			else:
				self.pause_game()

		if not self.m_is_paused:
			pass

	def pause_game(self):
		self.m_is_paused = True
		if self.m_pause_menu_ui is None:
			self.m_pause_menu_ui = PauseMenuUI()

	def resume_game(self):
		self.m_is_paused = False

	def save_game(self):
		success = self.m_save_game_system.save_game_state(self.m_game)

	def update(self):
		if self.m_is_paused:
			self.handle_pause_menu()
			return

		if self.m_game is None:
			return

		if self.m_game.m_game_events.get_event(events_dictionary.RESTART_GAME_EVENT):
			self.m_game.m_game_events.clear_persistent_event(events_dictionary.RESTART_GAME_EVENT)
			self.persist = {
				'game_data': self.m_game,
			}
			self.next_state = StatesEnum.GAME_OVER
			self.done = True
			return

		self.m_game.update()

	def handle_pause_menu(self):
		if self.m_pause_menu_ui is None:
			return

		request = self.m_pause_menu_ui.get_ui_requests()

		if request == PauseMenuRequestEnum.RESUME:
			self.resume_game()
		elif request == PauseMenuRequestEnum.SAVE:
			self.save_game()
		elif request == PauseMenuRequestEnum.MAIN_MENU:
			self.persist = {
				'game_data': self.m_game,
			}
			self.next_state = StatesEnum.MAIN_MENU
			self.done = True
		elif request == PauseMenuRequestEnum.EXIT_CONFIRMED:
			self.events.change_event(events_dictionary.EXIT_GAME_EVENT, True)

	def draw(self):
		self.screen.reset_window_fill()

		if self.m_game is None:
			return

		self.m_game.draw()
		self.m_game_ui.update(self.m_game.m_chars.sprites()[0], self.m_game.m_score)

		if self.m_is_paused and self.m_pause_menu_ui:
			self.m_pause_menu_ui.draw()