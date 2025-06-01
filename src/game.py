import pygame

from playground import Playground
from playground_object import Playground_Object
from camera import Camera

class Game:
	def __init__(self):
		self.m_char: pygame.sprite.GroupSingle = pygame.sprite.GroupSingle()
		self.m_projectiles: pygame.sprite.Group = pygame.sprite.Group()
		self.m_npcs: pygame.sprite.Group = pygame.sprite.Group()

		self.m_events: list[pygame.Event]
		self.m_playground: Playground

	def update(self, dt: float, event: list[pygame.Event]):
		self.m_events = event
		self.m_char.update(dt, self)
		self.m_projectiles.update(dt, self)

		self.check_collisions()

		self.m_camera.update(self.m_char.sprite.rect.center)

	def add_playground(self, playground: Playground):
		self.m_playground = playground

	def add_camera(self, camera: Camera):
		self.m_camera = camera

	def add_char_object(self, char_obj: pygame.sprite.Sprite):
		self.m_char.add(char_obj)

	def add_projectile_object(self, projectile_obj: pygame.sprite.Sprite):
		self.m_projectiles.add(projectile_obj)

	def add_npc_object(self, sprite_obj: pygame.sprite.Sprite):
		self.m_npcs.add(sprite_obj)

	def draw(self):
		self.m_playground.refill_playground()

		for sprite in self.m_npcs:
			self.m_playground.m_surface.blit(sprite.image, sprite.rect.topleft)

		for sprite in self.m_projectiles:
			self.m_playground.m_surface.blit(sprite.image, sprite.rect.topleft)

		if self.m_char.sprite:
			self.m_playground.m_surface.blit(self.m_char.sprite.image, self.m_char.sprite.rect.topleft)

		self.m_playground.draw_playground(self.m_camera.m_screen_offset)

	def check_collisions(self):
		collisions = pygame.sprite.groupcollide(self.m_projectiles, self.m_npcs, False, False)

		for projectile, npcs_hit in collisions.items():
			projectile.on_collision_with_npc(game=self, collided_with=npcs_hit)
			for npc in npcs_hit:
				npc.on_collision_with_projectile(game=self, collided_with=[projectile])

		if self.m_char.sprite:
			p_o: Playground_Object = self.m_char.sprite
			p_o.check_and_clamp_ip_with_playground(self.m_playground.m_game_world_rect)

	def get_screen_offset(self) -> pygame.math.Vector2:
		return self.m_camera.m_screen_offset
