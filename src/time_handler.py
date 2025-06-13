import time

import pygame

from singleton import singleton

# Singleton Time Handler
@singleton
class Time_Handler:
	def __init__(self):
		self.m_pygame_clock: pygame.time.Clock = pygame.time.Clock()

		self.m_current_time_ns: int = time.perf_counter_ns()
		self.m_last_time_ns: int = self.m_current_time_ns
		self.m_frame_start_time_ns: int = self.m_current_time_ns

		self.m_delta_time_ns: int = 0
		self.m_delta_time_ms: float = 0
		self.m_delta_time_s: float = 0
		self.m_total_duration_ms: float = 0

		self.m_fps: int = 0
		self.m_current_fps: int = 0
		self.m_current_fps_check_time_duration_s: float = 0
		self.CHECK_FPS_PERIOD_s: float = 0.5

	def tick(self, frame_time: float):
		if frame_time != 0:
			self.m_current_time_ns = time.perf_counter_ns()

			time_to_wait_s = frame_time - (self.m_current_time_ns - self.m_frame_start_time_ns) / 1_000_000_000.0
			if time_to_wait_s > 0:
				time.sleep(time_to_wait_s)

		self.m_last_time_ns = self.m_frame_start_time_ns
		self.m_frame_start_time_ns = time.perf_counter_ns()

		self.m_delta_time_ns = self.m_frame_start_time_ns - self.m_last_time_ns
		self.m_delta_time_ms = self.m_delta_time_ns / 1_000_000.0
		self.m_delta_time_s = self.m_delta_time_ms / 1000.0
		self.m_total_duration_ms += self.m_delta_time_ms

		self.m_fps += 1
		self.m_current_fps_check_time_duration_s += self.m_delta_time_s
		if (self.m_current_fps_check_time_duration_s > self.CHECK_FPS_PERIOD_s):
			self.m_current_fps = int(self.m_fps / self.m_current_fps_check_time_duration_s)
			self.m_current_fps_check_time_duration_s = 0
			self.m_fps = 0

	def get_delta_time_ms(self) -> float:
		return self.m_delta_time_ms

	def get_delta_time_s(self) -> float:
		return self.m_delta_time_s

	def get_fps(self) -> int:
		return self.m_current_fps

	def get_total_duration_ms(self) -> float:
		return self.m_total_duration_ms

	def reset_total_duration(self) -> None:
		self.m_total_duration_ms = 0