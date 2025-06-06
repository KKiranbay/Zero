import pygame

# My code
from camera import Camera
from character import Character
from game import Game
from npc import NPC, NPC_Type
from playground import Playground
from time_handler import Time_Handler
from ui import User_Interface

import game_events_dictionary
from game_events_dictionary import GameEventsDictionary

import resources.colors as colors

# Initialize Pygame
pygame.init()

MAX_HZ: int = 0  # 240 Hz update rate
desired_framerate: float = 0
if MAX_HZ != 0:
	desired_framerate = 1.0 / MAX_HZ

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
playground = Playground(user_interface.getWindow(), playground_width, playground_height, colors.BEIGE)
game.add_playground(playground)

player = Character(playground.m_game_world_rect.width // 2, playground.m_game_world_rect.height // 2, pygame.Vector2(50,50), 500)
game.add_char_object(player)

camera = Camera(player.rect.centerx, player.rect.centery, user_interface.getWindow().get_width(), user_interface.getWindow().get_height())
game.add_camera(camera)

target = NPC(NPC_Type.ENEMY, 100, 100, pygame.Vector2(20,20))
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
	user_interface.resetWindowFill()
	game.draw()
	user_interface.update(player.m_health, game.m_score)

	# Update the display
	pygame.display.flip()

if restart:
    print("Restarted!")

# Quit Pygame
pygame.quit()

