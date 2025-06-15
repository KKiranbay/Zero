import pygame

import events_dictionary as events_dictionary

from game.camera import Camera
from game.game import Game
from game.playground import Playground

from game.game_objects.characters.character import Character
from game.game_objects.npcs.npc import NPC, NPC_Type

from ui.game_ui import Game_UI

import resources.colors as colors

from screen import Screen

from states_enum import StatesEnum

from states.state import State


class GameState(State):
	def __init__(self):
		super().__init__()
		self.next_state = StatesEnum.MAIN_MENU

	def startup(self, persistent):
		self.persist = persistent

		# init
		self.m_game: Game = Game()

		playground_width = 500
		playground_height = 500
		self.m_playground = Playground(self.screen.m_window, playground_width, playground_height, colors.BEIGE)
		self.m_game.add_playground(self.m_playground)

		self.m_player = Character(pygame.Vector2(self.m_playground.m_game_world_rect.width // 2, self.m_playground.m_game_world_rect.height // 2), pygame.Vector2(50,50), 500)
		self.m_game.add_char_object(self.m_player)

		self.m_camera = Camera(pygame.Vector2(self.m_player.rect.center), self.screen.m_window.get_width(), self.screen.m_window.get_height())
		self.m_game.add_camera(self.m_camera)

		self.m_target = NPC(NPC_Type.ENEMY, pygame.Vector2(100, 100), pygame.Vector2(20,20))
		self.m_game.add_npc_object(self.m_target)

		pygame.time.set_timer(events_dictionary.SPAWN_NPC_EVENT, 2500)

		self.m_game_ui : Game_UI = Game_UI()

	def check_events(self):
		if self.events.get_event(pygame.KEYDOWN) == None:
			return

		if self.events.get_event(pygame.KEYDOWN).key == pygame.K_ESCAPE:
			self.done = True

	def update(self):
		self.m_game.update()
		pass

	def draw(self):
		self.screen.reset_window_fill()
		self.m_game.draw()
		self.m_game_ui.update(self.m_player.m_health, self.m_player.m_current_weapon_str, self.m_game.m_score)