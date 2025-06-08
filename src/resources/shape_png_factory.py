import os

import pygame

def create_triangle_png(filename: str, size: tuple[int, int], color: tuple[int, int, int]):
	if os.path.exists(filename):
		return

	print(f"Creating dummy image: {filename}")
	temp_surface = pygame.Surface(size, pygame.SRCALPHA)
	temp_surface.fill((0, 0, 0, 0))

	points = [
		(size[0] // 2, 0),
		(0, size[1]),
		(size[0], size[1])
	]

	pygame.draw.polygon(temp_surface, color, points)
	pygame.image.save(temp_surface, filename)