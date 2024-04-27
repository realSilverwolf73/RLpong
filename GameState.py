import numpy as np
import pygame
import sys
from abc import ABC, abstractmethod

class GameState:
    def __init__(self, width, height, ball_radius, paddle_width, paddle_height, ball_speed, paddle_speed):
        self.width = width
        self.height = height
        self.ball_radius = ball_radius
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.ball_speed = ball_speed
        self.paddle_speed = paddle_speed
        self.player1_score = 0
        self.player2_score = 0
        
        self.reset()

    def reset(self):
        
        self.player1_pos = [self.paddle_width, self.height // 2 - self.paddle_height // 2]
        self.player2_pos = [self.width - 2 * self.paddle_width, self.height // 2 - self.paddle_height // 2]
        self.ball_pos = [self.width // 2, self.height // 2]
        self.ball_direction = np.random.choice([np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4])
        self.ball_velocity = np.array([self.ball_speed * np.cos(self.ball_direction),
                                       self.ball_speed * np.sin(self.ball_direction)])
        self.done = False

    def get_state_as_image(self):
        # Render the environment to an image surface
        surface = pygame.Surface((self.width, self.height))
        surface.fill((0, 0, 0))

        pygame.draw.rect(surface, (255, 255, 255),
                         (self.player1_pos[0], self.player1_pos[1], self.paddle_width, self.paddle_height))
        pygame.draw.rect(surface, (255, 255, 255),
                         (self.player2_pos[0], self.player2_pos[1], self.paddle_width, self.paddle_height))

        pygame.draw.circle(surface, (255, 255, 255), (int(self.ball_pos[0]), int(self.ball_pos[1])), self.ball_radius)

        # Convert the image surface to image data
        image_data = pygame.surfarray.array2d(surface)
        return np.array(image_data)