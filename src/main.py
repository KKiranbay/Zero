import random
import time

import pygame

# My code
from camera import Camera
from character import Character
from game import Game
from npc import NPC, NPC_Type
from playground import Playground

import resources.colors as colors

# Initialize Pygame
pygame.init()

MAX_HZ = 240  # 240 Hz update rate
clock = pygame.time.Clock()

# Delta Time
dt: float = 0.0
prev_time: float = 0.0

def update_delta_time():
	global dt, prev_time
	now = time.time()
	dt = now - prev_time
	prev_time = now

# Screen
window: pygame.Surface = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Movable Character with Toggleable Camera")

# Game instances
game = Game()

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


SPAWN_NPC_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_NPC_EVENT, 2500)
spawn = False

# Game loop
running = True
while running:
	# Time management
	update_delta_time()

	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running = False
		if event.type == SPAWN_NPC_EVENT:
			spawn = True

	if running == False:
		break

	game.update(dt, events)

	if spawn:
		random_x: float = random.uniform(playground.m_game_world_rect.left, playground.m_game_world_rect.right)
		random_y: float = random.uniform(playground.m_game_world_rect.top, playground.m_game_world_rect.bottom)
		game.add_npc_object(NPC(NPC_Type.ENEMY, random_x, random_y, 20))
		spawn = False
		pygame.time.set_timer(SPAWN_NPC_EVENT, round(random.uniform(1000, 5000)))

	# Clear main window
	window.fill(colors.BLACK)

	# Draw game stuff
	game.draw()

	# Update the display
	pygame.display.flip()

	# --- Frame Rate Control ---
	clock.tick(MAX_HZ)

# Quit Pygame
pygame.quit()