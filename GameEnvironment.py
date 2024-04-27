import numpy as np
import pygame
import sys
from abc import ABC, abstractmethod
from GameState import *

class GameEnvironment(ABC):
    @abstractmethod
    def step(self, action):
        pass

    @abstractmethod
    def get_state(self):
        pass

    @abstractmethod
    def get_reward(self):
        pass

class PongEnvironment(GameEnvironment):
    def __init__(self, width, height, ball_radius, paddle_width, paddle_height, ball_speed, paddle_speed):
        self.state = GameState(width, height, ball_radius, paddle_width, paddle_height, ball_speed, paddle_speed)
        self.previous_state = np.zeros((width, height))

    def reset(self):
        self.state.reset()
        self.previous_state = np.zeros((self.state.width, self.state.height))
        return self.get_true_state()
    
    def step(self, action):
        print(f"move paddle: {action}")
        self.move_paddle(action)
        self.move_ball()
        reward = self.get_reward()
        self.check_collision()
        done = self.state.done
        true_state = self.get_true_state()
        return true_state, reward, done

    def get_state(self):
        return self.state

    def get_reward(self):
        if self.state.ball_pos[0] <= 0:
            self.state.player2_score += 1
            self.state.done = True
            return -1
        elif self.state.ball_pos[0] >= self.state.width:
            self.state.player1_score += 1
            self.state.done = True
            return 1
        else:
            return 0

    def get_true_state(self):
        new_state = self.state.get_state_as_image()
        mask = new_state == 0
        mask_int = mask.astype(int)
        true_state = new_state - self.previous_state * mask_int
        self.previous_state = new_state
        return true_state // 16777215 #normalise

    def move_paddle(self, action):
        #up
        if action == 0:
            self.state.player1_pos[1] = max(self.state.player1_pos[1] - self.state.paddle_speed, 0)
        #down
        elif action == 1:
            self.state.player1_pos[1] = min(self.state.player1_pos[1] + self.state.paddle_speed, self.state.height - self.state.paddle_height)
            
    def autoMove_paddle(self):
        if self.state.ball_pos[1] < self.state.player2_pos[1]:
            self.state.player2_pos[1] = max(self.state.player2_pos[1] - self.state.paddle_speed, 0)
        elif self.state.ball_pos[1] > self.state.player2_pos[1]:
            self.state.player2_pos[1] = min(self.state.player2_pos[1] + self.state.paddle_speed, self.state.height - self.state.paddle_height)
        

    def move_ball(self):
        self.state.ball_pos += self.state.ball_velocity
        if self.state.ball_pos[1] <= 0 or self.state.ball_pos[1] >= self.state.height:
            self.state.ball_velocity[1] *= -1

    def check_collision(self):
        if self.state.ball_pos[0] <= self.state.paddle_width and self.state.player1_pos[1] <= self.state.ball_pos[1] <= self.state.player1_pos[1] + self.state.paddle_height:
            self.state.ball_velocity[0] *= -1
        elif self.state.ball_pos[0] >= self.state.width - 2 * self.state.paddle_width and self.state.player2_pos[1] <= self.state.ball_pos[1] <= self.state.player2_pos[1] + self.state.paddle_height:
            self.state.ball_velocity[0] *= -1