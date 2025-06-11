import pygame

class Camera:
	def __init__(self, cam_pos: pygame.math.Vector2, screen_width: int, screen_height: int):
		self.m_cam_locked = False
		self.m_pos: pygame.math.Vector2 = pygame.math.Vector2(cam_pos)
		self.m_screen_width = screen_width
		self.m_screen_height = screen_height

		self.m_screen_offset = pygame.math.Vector2(self.m_screen_width // 2 - self.m_pos.x, self.m_screen_height // 2 - self.m_pos.y)

	def update(self, char_pos: tuple[int, int]):
		# self.check_cam_lock(char_pos)

		self.update_screen_offset()

	def check_cam_pos_depending_on_char(self, char_pos: tuple[int, int]):
		pass

	def check_cam_lock(self, char_pos: tuple[int, int]):
		mouse_buttons = pygame.mouse.get_pressed()

		# Right mouse button
		self.m_cam_locked = mouse_buttons[2]

		if self.m_cam_locked:
			self.m_pos.update(char_pos)

	def update_screen_offset(self):
		screen_offset_x: float = self.m_screen_width // 2 - self.m_pos.x
		screen_offset_y: float = self.m_screen_height // 2 - self.m_pos.y
		self.m_screen_offset.update(screen_offset_x, screen_offset_y)