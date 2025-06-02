import random
import time

import pygame

# My code
from camera import Camera
from character import Character
from game import Game
from npc import NPC, NPC_Type
from playground import Playground

import game_events_dictionary
from game_events_dictionary import GameEventsDictionary

import resources.colors as colors

# Initialize Pygame
pygame.init()

fps = 0
fps_display_timer = 0
FPS_UPDATE_INTERVAL = 0.5

MAX_HZ = 240  # 240 Hz update rate
clock = pygame.time.Clock()

# Delta Time
dt: float = 0
prev_time: float = time.time()

def update_delta_time():
	global dt, prev_time
	now = time.time()
	dt = now - prev_time
	prev_time = now

# Mouse
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

# Screen
window: pygame.Surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movable Character with Toggleable Camera")

# Font
try:
	font = pygame.font.Font(None, 48)
except pygame.error:
	print("Default font not found, trying a system font.")
	font_name = pygame.font.match_font('dejavusans', bold=True) or \
				pygame.font.match_font('arial', bold=True) or \
				pygame.font.match_font('sans', bold=True)
	if font_name:
		font = pygame.font.Font(font_name, 48)
	else:
		print("No suitable font found! Text rendering might fail.")
		font = None

# Game instances
game: Game = Game()
game_events: GameEventsDictionary = GameEventsDictionary()

playground_width = 500
playground_height = 500
playground = Playground(window, playground_width, playground_height, colors.BEIGE)

game.add_playground(playground)

player = Character(playground.m_game_world_rect.width // 2, playground.m_game_world_rect.height // 2, 50, 500)
game.add_char_object(player)

camera = Camera(player.rect.centerx, player.rect.centery, window.get_width(), window.get_height())
game.add_camera(camera)

target = NPC(NPC_Type.ENEMY, 100, 100, 20)
game.add_npc_object(target)


pygame.time.set_timer(game_events_dictionary.SPAWN_NPC_EVENT, 2500)
spawn = False

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

def writeHealth(text: str):
	global window, font
	if font:
		text_surface = font.render(text, True, colors.WHITE)
		text_rect = text_surface.get_rect()
		padding = 10
		text_rect.bottomleft = (padding, window.get_height() - padding)
		window.blit(text_surface, text_rect)

def writeScore(text: str):
	global window, font
	if font:
		text_surface = font.render(text, True, colors.WHITE)
		text_rect = text_surface.get_rect()
		padding = 10
		text_rect.center = (window.get_width() / 2, padding + text_rect.height / 2)
		window.blit(text_surface, text_rect)

def writeFPS(text: str):
	global window, font
	if font:
		text_surface = font.render(text, True, colors.WHITE)
		text_rect = text_surface.get_rect()
		padding = 10
		text_rect.topleft = (padding, padding)
		window.blit(text_surface, text_rect)

# Game loop
game_events.resetEvents()

while running:
	# Time management
	update_delta_time()

	check_pygame_events(game_events)

	if running == False:
		break

	game.update(dt, game_events)

	if game_events.getEvent(game_events_dictionary.RESTART_EVENT):
		restart = True
		game_events.resetEvents()
		break

	game_events.resetEvents()

	# Clear main window
	window.fill(colors.BLACK)

	# Draw game stuff
	game.draw()

	# UI
	health: str = f"HP: {player.m_health}"
	writeHealth(health)

	score: str = f"Score: {game.m_score}"
	writeScore(score)

	fps_display_timer += dt
	if fps_display_timer >= FPS_UPDATE_INTERVAL:
		fps = 1 / dt
		fps_display_timer = 0

	fpsStr: str = f"FPS: {int(fps)}"
	writeFPS(fpsStr)

	# Update the display
	pygame.display.flip()

	# --- Frame Rate Control ---
	clock.tick(MAX_HZ)

if restart:
    print("Restarted!")

# Quit Pygame
pygame.quit()

