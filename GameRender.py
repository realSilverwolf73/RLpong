import numpy as np
import pygame
import sys
from abc import ABC, abstractmethod

class GameRenderer(ABC):
    @abstractmethod
    def render(self, state):
        pass

class PygameRenderer(GameRenderer):
    def __init__(self, width, height):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

    def render(self, state):
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (state.player1_pos[0], state.player1_pos[1], state.paddle_width, state.paddle_height))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (state.player2_pos[0], state.player2_pos[1], state.paddle_width, state.paddle_height))

        pygame.draw.circle(self.screen, (255, 255, 255), (int(state.ball_pos[0]), int(state.ball_pos[1])), state.ball_radius)

        player1_score_text = self.font.render(str(state.player1_score), True, (255, 255, 255))
        player2_score_text = self.font.render(str(state.player2_score), True, (255, 255, 255))
        self.screen.blit(player1_score_text, (10, 10))
        self.screen.blit(player2_score_text, (state.width - 40, 10))
        
        pygame.display.flip()
        self.clock.tick(60)
