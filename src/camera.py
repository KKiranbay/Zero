import pygame


class Camera:
    def __init__(self):
        self.m_cam_locked = False
        self.m_cam_pos_x = 0
        self.m_cam_pos_y = 0

    def move_cam(self, char_pos_x: float, char_pos_y: float, char_size: int, screen_width: int, screen_height: int):
        mouse_buttons = pygame.mouse.get_pressed()

        # Right mouse button
        m_cam_locked = mouse_buttons[2]

        if m_cam_locked:
            self.m_cam_pos_x = char_pos_x - screen_width // 2 + char_size // 2
            self.m_cam_pos_y = char_pos_y - screen_height // 2 + char_size // 2
        else:
            # If camera is not locked, we can demonstrate moving the camera independently
            # For simplicity, let's make the camera "follow" the character slowly
            # or you could add separate camera movement controls here.
            # For this example, we'll keep it simple and just not update camera_x, camera_y
            # if not locked, making it effectively fixed until locked.
            pass