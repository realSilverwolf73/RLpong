import numpy as np
import pygame
import sys
from abc import ABC, abstractmethod

from PolicyNetwork import PolicyNetwork, PolicyGradientAgent
from GameEnvironment import *
from GameState import *
from GameRender import *

class InputHandler(ABC):
    @abstractmethod
    def get_action(self):
        pass

class KeyboardInputHandler(InputHandler):
    def get_action(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            return -1
        elif keys[pygame.K_DOWN]:
            return 1
        else:
            return 0

# Dependency Inversion Principle
def main():
    width, height = 320, 256
    paddle_width = 5
    paddle_height = 32
    ball_radius = 5
    ball_speed = 3
    paddle_speed = 3
    action = 0

    env = PongEnvironment(width, height, ball_radius, paddle_width, paddle_height, ball_speed, paddle_speed)
    renderer = PygameRenderer(width, height)
    input_handler = KeyboardInputHandler()
    ninja = PolicyGradientAgent(width * height, 2)

    while True:
        episode_states = []
        episode_actions = []
        episode_rewards = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        
        true_state, reward, done = env.step(action)
        episode_states.append(true_state)
        action = ninja.get_action(true_state)
        episode_actions.append(action)
        episode_rewards.append(reward)

        renderer.render(env.get_state())
        env.autoMove_paddle()
        
        if done:
            env.state.reset()
            ninja.update(episode_states, episode_actions, episode_rewards)
            episode_states = []
            episode_actions = []
            episode_rewards = []
            

if __name__ == "__main__":
    main()