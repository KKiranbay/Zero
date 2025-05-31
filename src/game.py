import pygame

from playground import Playground

class Game:
	def __init__(self):
		self.m_npcs: pygame.sprite.Group = pygame.sprite.Group()
		self.m_chars: pygame.sprite.Group = pygame.sprite.Group()
		self.m_playground: Playground

	def update(self, dt):
		self.m_chars.update(dt, self.m_playground)
		# self.m_npcs.update()

	def add_playground(self, playground: Playground):
		self.m_playground = playground

	def add_char_object(self, char_obj: pygame.sprite.Sprite):
		if isinstance(char_obj, pygame.sprite.Sprite):
			self.m_chars.add(char_obj)
		else:
			print("Warning: Only Pygame Sprites should be added to this group.")

	def add_playground_object(self, sprite_obj: pygame.sprite.Sprite):
		if isinstance(sprite_obj, pygame.sprite.Sprite):
			self.m_npcs.add(sprite_obj)
		else:
			print("Warning: Only Pygame Sprites should be added to this group.")

	def draw(self):
		self.m_playground.refill_playground()

		self.m_npcs.draw(self.m_playground.m_surface)
		self.m_chars.draw(self.m_playground.m_surface)

		self.m_playground.draw_playground()