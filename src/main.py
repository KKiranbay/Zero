import pygame
from states_enum import StatesEnum
from states.state import State
from states.game_state import GameState
from states.main_menu_state import MainMenuState

from time_handler import Time_Handler

import game.game_events_dictionary as game_events_dictionary
from game.game_events_dictionary import GameEventsDictionary

class GameController:
	def __init__(self):
		pygame.init()
		self.screen: pygame.Surface = pygame.display.set_mode((800, 600))

		self.time_handler: Time_Handler = Time_Handler()
		self.MAX_HZ: int = 0  # 240 Hz update rate
		self.desired_framerate: float = 0
		if self.MAX_HZ != 0:
			self.desired_framerate = 1.0 / self.MAX_HZ

		self.quit: bool = False
		self.states: dict[StatesEnum, State] = {
			StatesEnum.MAIN_MENU:	MainMenuState(),
			StatesEnum.GAME_STATE:	GameState()
		}

		self.current_state: StatesEnum = StatesEnum.MAIN_MENU
		self.state: State = self.states[self.current_state]
		self.state.startup({})

		self.game_events: GameEventsDictionary = GameEventsDictionary()

	def event_loop(self):
		pygame_events = pygame.event.get()

		for pygame_event in pygame_events:
			if pygame_event.type == pygame.QUIT:
				self.quit = True
			elif self.game_events.exists(pygame_event.type):
				self.game_events.changeEvent(pygame_event.type, True)

			self.state.get_event(pygame_event)

	def update(self, dt):
		if self.state.done:
			self.change_state()
		self.state.update(dt)

	def draw(self):
		self.state.draw(self.screen)
		pygame.display.flip()

	def change_state(self):
		previous_state = self.current_state
		self.current_state = self.state.next_state
		persistent_data = self.state.persist
		self.state.done = False
		self.state = self.states[self.current_state]
		self.state.startup(persistent_data)
		self.state.previous_state = previous_state

	def run(self):
		while not self.quit:
			self.time_handler.tick(self.desired_framerate)
			self.event_loop()
			self.update(self.desired_framerate)
			self.draw()

if __name__ == "__main__":
	app = GameController()
	app.run()
	pygame.quit()


import pygame

# My code
from game.camera import Camera
from game.game import Game
from game.playground import Playground
from time_handler import Time_Handler
from ui.ui import User_Interface

from game.game_objects.characters.character import Character
from game.game_objects.npcs.npc import NPC, NPC_Type

import resources.colors as colors
from resources.shape_png_factory import create_triangle_png


# Initialize Pygame
pygame.init()

MAX_HZ: int = 0  # 240 Hz update rate
desired_framerate: float = 0
if MAX_HZ != 0:
	desired_framerate = 1.0 / MAX_HZ

# Triangle PNG
image_filename = "enemy_triangle.png"
create_triangle_png(image_filename, (100, 100), colors.PURPLE)

# Time Handler
time_handler: Time_Handler = Time_Handler()

# UI
user_interface: User_Interface = User_Interface((800, 600), time_handler)

# Mouse
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

# Game instances
game: Game = Game(time_handler)
game_events: GameEventsDictionary = GameEventsDictionary()

playground_width = 500
playground_height = 500
playground = Playground(user_interface.get_window(), playground_width, playground_height, colors.BEIGE)
game.add_playground(playground)

player = Character(pygame.Vector2(playground.m_game_world_rect.width // 2, playground.m_game_world_rect.height // 2), pygame.Vector2(50,50), 500)
game.add_char_object(player)

camera = Camera(pygame.Vector2(player.rect.center), user_interface.get_window().get_width(), user_interface.get_window().get_height())
game.add_camera(camera)

target = NPC(NPC_Type.ENEMY, pygame.Vector2(100, 100), pygame.Vector2(20,20))
game.add_npc_object(target)

pygame.time.set_timer(game_events_dictionary.SPAWN_NPC_EVENT, 2500)

restart = False
running = True
def check_pygame_events(game_events: GameEventsDictionary):
	global running
	pygame_events = pygame.event.get()

	for pygame_event in pygame_events:
		if pygame_event.type == pygame.QUIT:
			running = False
		elif game_events.exists(pygame_event.type):
			game_events.changeEvent(pygame_event.type, True)


# Game loop
game_events.resetEvents()
time_handler.tick(desired_framerate)

while running:
	check_pygame_events(game_events)

	if running == False:
		break

	time_handler.tick(desired_framerate)

	game.update(game_events)

	if game_events.getEvent(game_events_dictionary.RESTART_EVENT):
		restart = True
		game_events.resetEvents()
		break

	game_events.resetEvents()

	# Draw game stuff
	user_interface.reset_window_fill()
	game.draw()
	user_interface.update(player.m_health, player.m_current_weapon_str, game.m_score)

	# Update the display
	pygame.display.flip()

if restart:
    print("Restarted!")

# Quit Pygame
pygame.quit()