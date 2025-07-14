# GameController manages game initialization, coordination, and high-level operations.
# Coordinates Game instance, UI, saving, and spawn control.

import pygame

import events_dictionary as events_dictionary

from game.camera import Camera
from game.game import Game
from game.playground import Playground

from game.map.polygon_data import PolygonData
from game.map.map import Map

from game.game_objects.characters.character import Character
from game.game_objects.npcs.npc import NPC, NPC_Type

from systems.save_game_system import SaveGameSystem
from controllers.spawn_controller import SpawnController

from ui.game_ui import Game_UI

import resources.colors as colors


class GameController:
	def __init__(self, screen):
		self.m_screen = screen
		self.m_game = Game()
		self.m_game_ui = Game_UI()
		self.m_save_game_system: SaveGameSystem = SaveGameSystem()

	def create_game(self) -> Game:
		"""Create and return a new Game instance."""
		self.m_game = Game()
		self.m_spawn_controller = SpawnController(self.m_game)
		self.m_game_ui = Game_UI()
		return self.m_game

	def initialize_game_objects(self) -> None:
		"""Initialize all game objects including playground, player, camera, and initial NPCs."""
		self.m_game.reset_game_duration()

		playground_width = 3500
		playground_height = 3500
		playground = Playground(self.m_screen.m_window, playground_width, playground_height, colors.BEIGE)
		self.m_game.add_playground(playground)

		main_polygon_data = PolygonData(
			vertices=[(200, 200), (600, 200), (600, 600), (200, 600)],
			fill_color=colors.LIGHT_BLUE,
			outline_color=colors.WHITE,
			outline_width=2
		)
		self.m_game_map = Map(main_polygon_data)
		self.m_game.add_map(self.m_game_map)

		player = Character(self.m_game, pygame.Vector2(self.m_game_map.get_main_polygon().get_middle_point()), pygame.Vector2(50,50), 500)
		self.m_game.add_char_object(player)

		camera = Camera(pygame.Vector2(player.rect.center), self.m_screen.m_window.get_width(), self.m_screen.m_window.get_height())
		self.m_game.add_camera(camera)

		target = NPC(self.m_game, NPC_Type.ENEMY, pygame.Vector2(100, 100), pygame.Vector2(20,20))
		self.m_game.add_npc_object(target)

	def start_spawn_system(self) -> None:
		"""Start the NPC spawn system."""
		if self.m_spawn_controller:
			self.m_spawn_controller.start_spawn_system()

	def update(self) -> None:
		"""Update all game systems including spawn controller."""
		self.m_game.update()
		self.m_spawn_controller.update()

	def save_game(self) -> None:
		"""Save the current game state."""
		self.m_save_game_system.save_game_state(self.m_game, self.m_spawn_controller)

	def update_ui(self) -> None:
		"""Update the game UI with current player and score information."""
		self.m_game_ui.update(self.m_game.m_chars.sprites()[0], self.m_game.m_score)

	def get_game(self) -> Game | None:
		"""Get the current game instance."""
		return self.m_game

	def get_spawn_controller(self) -> SpawnController | None:
		return self.m_spawn_controller

	def set_game(self, game: Game) -> None:
		"""Set the game instance (used when loading from save)."""
		self.m_game = game
		self.m_spawn_controller = SpawnController(self.m_game)
		self.m_game_ui = Game_UI()

	def set_spawn_controller(self, spawn_controller: SpawnController) -> None:
		self.m_spawn_controller = spawn_controller

	def has_game_restart_event(self) -> bool:
		"""Check if the game has a restart event."""
		return self.m_game.m_game_events.get_event(events_dictionary.RESTART_GAME_EVENT)

	def clear_restart_event(self) -> None:
		"""Clear the restart game event."""
		self.m_game.m_game_events.clear_persistent_event(events_dictionary.RESTART_GAME_EVENT)

	def draw_game(self) -> None:
		"""Draw the game and UI."""
		self.m_game.draw()
		self.update_ui()

	def restore_spawn_controller_from_save_data(self, save_data) -> bool:
		"""Restore spawn controller state from save data."""
		return False

		spawn_data = save_data.get("spawn_controller")
		if spawn_data:
			self.m_spawn_controller.m_next_spawn_total_time_ms = spawn_data.get("next_spawn_total_time_ms", 0)
			self.m_spawn_controller.m_spawn_system_active = spawn_data.get("spawn_system_active", False)
			return True
		return False

	def load_game_from_save_data(self, save_data) -> bool:
		"""Load game state from save data using LoadGameSystem."""
		from systems.load_game_system import LoadGameSystem

		self.create_game()

		load_system = LoadGameSystem()

		# Restore the game state
		success = load_system.restore_game_state(save_data, self.m_game)

		if success:
			# Restore spawn controller state
			load_system.restore_spawn_controller_state(save_data, self.m_spawn_controller)

		return success
