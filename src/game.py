import pygame

# My code
from camera import Camera
from character import Character
from npc import NPC, NPC_Type
from screen import Screen

import colors

# Initialize Pygame
pygame.init()

# Screen
screen = Screen(800, 600, "Movable Character with Toggleable Camera")

# Game instances
player = Character(50, 1, screen.m_screen_width, screen.m_screen_height)
camera = Camera()
target = NPC(NPC_Type.ENEMY, 100, 100, 20)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get all pressed keys
    keys = pygame.key.get_pressed()

    # Logic
    # Keep character within some bounds (optional, for a larger world)
    # For this example, let's just let it move freely for camera demonstration
    player.move_char(keys)
    camera.move_cam(player.m_char_x, player.m_char_y, player.m_char_size, screen.m_screen_width, screen.m_screen_height)

    # Clear the screen
    screen.m_surface.fill(colors.BLACK)

    # Draw a larger world background (optional, to visualize camera movement)
    pygame.draw.rect(screen.m_surface, colors.GREEN, (-camera.m_cam_pos_x, -camera.m_cam_pos_y, 2000, 2000)) # A large green background

    # Draw the character relative to the camera
    # Character's screen position = actual_position - camera_offset
    player.draw_char(screen.m_surface, camera.m_cam_pos_x, camera.m_cam_pos_y)

    # Draw a small "target" or "origin" indicator for reference
    target.draw_npc(screen.m_surface, camera.m_cam_pos_x, camera.m_cam_pos_y)

    pygame.draw.circle(screen.m_surface, colors.WHITE, (screen.m_screen_width // 2, screen.m_screen_height // 2), 5) # Screen center

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()