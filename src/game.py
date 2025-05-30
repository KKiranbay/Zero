import time

import pygame

# My code
from camera import Camera
from character import Character
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
playground_width = 500
playground_height = 500
playground = Playground(window, playground_width, playground_height, colors.BEIGE) 

player = Character(playground.m_game_rect.width // 2, playground.m_game_rect.height // 2, 50, 500)
camera = Camera(player.m_pos_x, player.m_pos_y)
target = NPC(NPC_Type.ENEMY, 100, 100, 20)

# Game loop
running = True
while running:
    # Time management
    update_delta_time()
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get all pressed keys
    keys = pygame.key.get_pressed()

    # Logic
    # Keep character within some bounds (optional, for a larger world)
    # For this example, let's just let it move freely for camera demonstration
    player.move_char(keys, dt)
    player.check_and_clamp_ip(playground.m_game_rect)

    camera.check_focus_on_player_move_cam(player.m_pos_x, player.m_pos_y)

    playground.move_relative_to_cam(camera.m_pos_x, camera.m_pos_y)

    # Shoot
    player.shoot()

    # Clear the playground
    playground.m_surface.fill(playground.m_color)
    
    # Draw the character relative to the camera
    player.draw_char(playground.m_surface)

    # Draw the target NPC relative to the camera
    target.draw_npc(playground.m_surface)

    # Clear main window
    window.fill(colors.BLACK)

    # Draw playground
    playground.draw_playground()

    # Draw a small "origin" indicator for reference
    pygame.draw.circle(window, colors.GREEN, (window.width // 2, window.height // 2), 5)

    # Update the display
    pygame.display.flip()

    # --- Frame Rate Control ---
    clock.tick(MAX_HZ)

# Quit Pygame
pygame.quit()