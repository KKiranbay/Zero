import time

import pygame

# My code
from camera import Camera
from character import Character
from game import Game
from npc import NPC, NPC_Type
from playground import Playground

import colors

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

player = Character(playground.m_game_rect.width // 2, playground.m_game_rect.height // 2, 50, 500)
game.add_char_object(player)

camera = Camera(player.rect.centerx, player.rect.centery)

target = NPC(NPC_Type.ENEMY, 100, 100, 20)
game.add_playground_object(target)

# Game loop
running = True
while running:
	# Time management
	update_delta_time()

	events = pygame.event.get()
	# Event handling
	for event in events:
		if event.type == pygame.QUIT:
			running = False

	game.update(dt, events)

	# Logic
	camera.check_focus_on_player_move_cam(player.rect.centerx, player.rect.centery)

	playground.move_relative_to_cam(camera.m_pos_x, camera.m_pos_y)

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