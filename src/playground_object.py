import pygame

class Playground_Object(pygame.sprite.Sprite):
	def __init__(self, pos_x: float, pos_y: float, size: float) -> None:
		super().__init__()

		self.image: pygame.Surface = pygame.Surface((size, size))
		self.image.fill((255, 255, 255))


		self.m_pos_x: float = pos_x
		self.m_pos_y: float = pos_y
		self.m_size: float = size
		self.m_half_size: float = size // 2

		rect_left_top_x: float = self.m_pos_x - self.m_half_size
		rect_left_top_y: float = self.m_pos_x - self.m_half_size

		self.rect: pygame.Rect = pygame.Rect(rect_left_top_x, rect_left_top_y, self.m_size, self.m_size)

	def update(self, dt, playground):
		pass

	def setPos(self, x, y):
		self.m_pos_x = x
		self.m_pos_y = y

		self.rect.x = self.m_pos_x - self.m_half_size
		self.rect.y = self.m_pos_y - self.m_half_size

	def check_and_clamp_ip_with_playground(self, playground_rect: pygame.Rect) :
		self.rect.clamp_ip(playground_rect)

		self.m_pos_x = self.rect.x + self.m_half_size
		self.m_pos_y = self.rect.y + self.m_half_size
