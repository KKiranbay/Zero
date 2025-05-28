import time

import pygame

# My code
from camera import Camera
from character import Character
from npc import NPC, NPC_Type
from screen import Screen
from playground import Playground

import colors

# Initialize Pygame
pygame.init()

five_hundred_hz = 1.0 / 500.0  # 500 Hz update rate

# Delta Time
dt: float = 0.0
prev_time: float = 0.0

def delta_time():
    global dt, prev_time
    now = time.time()
    dt = now - prev_time
    prev_time = now

# Screen
screen = Screen(800, 600, "Movable Character with Toggleable Camera")

# Game instances
player = Character(50, 500, screen.m_screen_width, screen.m_screen_height)
camera = Camera()
target = NPC(NPC_Type.ENEMY, 100, 100, 20)
playground = Playground(2000, 2000) 

# Game loop
running = True
while running:
    # Time management
    delta_time()
    
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
    camera.move_cam(player.m_char_x, player.m_char_y, player.m_char_size, screen.m_screen_width, screen.m_screen_height)

    # Clear the screen
    screen.m_surface.fill(colors.BLACK)

    # Draw the playground relative to the camera
    playground.draw_playground(screen.m_surface, colors.GREEN, camera.m_cam_pos_x, camera.m_cam_pos_y)

    # Draw the character relative to the camera
    player.draw_char(screen.m_surface, camera.m_cam_pos_x, camera.m_cam_pos_y)

    # Draw the target NPC relative to the camera
    target.draw_npc(screen.m_surface, camera.m_cam_pos_x, camera.m_cam_pos_y)

    # Draw a small "origin" indicator for reference
    pygame.draw.circle(screen.m_surface, colors.WHITE, (screen.m_screen_width // 2, screen.m_screen_height // 2), 5)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()