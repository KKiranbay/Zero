import pygame

class Camera:
	def __init__(self, cam_pos_x: float, cam_pos_y: float):
		self.m_cam_locked = False
		self.m_pos_x = cam_pos_x
		self.m_pos_y = cam_pos_y

	def check_focus_on_player_move_cam(self, char_pos_x: float, char_pos_y: float):
		mouse_buttons = pygame.mouse.get_pressed()

		# Right mouse button
		m_cam_locked = mouse_buttons[2]

		if m_cam_locked:
			self.m_pos_x = char_pos_x
			self.m_pos_y = char_pos_y
		else:
			# If camera is not locked, we can demonstrate moving the camera independently
			# For simplicity, let's make the camera "follow" the character slowly
			# or you could add separate camera movement controls here.
			# For this example, we'll keep it simple and just not update m_pos_x, m_pos_y
			# if not locked, making it effectively fixed until locked.
			pass