import pygame

from playground import Playground

class Game:
	def __init__(self):
		self.m_events: list[pygame.Event]
		self.m_char: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
		self.m_projectiles: pygame.sprite.Group = pygame.sprite.Group()
		self.m_npcs: pygame.sprite.Group = pygame.sprite.Group()

		self.m_playground: Playground

	def update(self, dt: float, event: list[pygame.Event]):
		self.m_events = event
		self.m_char.update(dt, self)
		# self.m_npcs.update()
		self.m_projectiles.update(dt, self)

	def add_playground(self, playground: Playground):
		self.m_playground = playground

	def add_char_object(self, char_obj: pygame.sprite.Sprite):
		self.m_char.add(char_obj)

	def add_projectile_object(self, projectile_obj: pygame.sprite.Sprite):
		self.m_projectiles.add(projectile_obj)

	def add_playground_object(self, sprite_obj: pygame.sprite.Sprite):
		self.m_npcs.add(sprite_obj)

	def draw(self):
		self.m_playground.refill_playground()

		self.m_npcs.draw(self.m_playground.m_surface)
		self.m_projectiles.draw(self.m_playground.m_surface)
		self.m_char.draw(self.m_playground.m_surface)

		self.m_playground.draw_playground()