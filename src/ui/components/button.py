import pygame

from events_dictionary import EventsDictionary
from screen import Screen

class Button:
	def __init__(self, x, y, width, height, text,
				base_color, hover_color, text_color, font: pygame.Font) -> None:

		self.m_rect: pygame.Rect = pygame.Rect(x, y, width, height)

		self.m_base_color = base_color
		self.m_hover_color = hover_color

		self.m_text_color = text_color

		self.m_font: pygame.Font = font

		self.m_text_surface: pygame.Surface = self.m_font.render(text, True, self.m_text_color)
		self.m_text_rect: pygame.Rect = self.m_text_surface.get_rect(center=self.m_rect.center)

		self.m_is_hovered = False
		self.m_is_clicked = False

		self.m_screen: Screen = Screen()
		self.m_events: EventsDictionary = EventsDictionary()

	def draw(self):
		current_color = self.m_hover_color if self.m_is_hovered else self.m_base_color

		pygame.draw.rect(self.m_screen.m_window, current_color, self.m_rect, border_radius=12)

		self.m_screen.m_window.blit(self.m_text_surface, self.m_text_rect)

	def check_button_events(self):
		self.m_is_hovered = self.m_rect.collidepoint(pygame.mouse.get_pos())

		event: pygame.Event = self.m_events.get_event(pygame.MOUSEBUTTONDOWN)
		if event != None:
			self.m_is_clicked = (event.button == 1 and self.m_is_hovered)
		else:
			self.m_is_clicked = False
