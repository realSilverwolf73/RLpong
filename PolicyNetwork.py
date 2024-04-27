import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class PolicyNetwork(nn.Module):
    def __init__(self, state_size, action_size, hidden_size=64):
        super(PolicyNetwork, self).__init__()
        self.fc1 = nn.Linear(state_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, action_size)

    def forward(self, state):
        x = torch.relu(self.fc1(state))
        probs = torch.softmax(self.fc2(x), dim=-1)
        print(f"probs: {probs}")
        
        return probs
    
    def backward(self, loss):
        loss.backward()
    
    
class PolicyGradientAgent:
    def __init__(self, state_dim, action_dim, gamma=0.99, learning_rate=1e-3):
        self.gamma = gamma
        self.policy = PolicyNetwork(state_dim, action_dim)
        self.optimizer = optim.Adam(self.policy.parameters(), lr=learning_rate)
        self.action_dim = action_dim

    def get_action(self, state):
        state = torch.from_numpy(state).float().unsqueeze(0).view(-1)
        action_probs = self.policy(state)
        action_dist = torch.distributions.Categorical(action_probs)
        action = action_dist.sample()
        the_action = action.item()
        print(f"action: {the_action}")
        return the_action

    def update(self, states, actions, rewards):
        returns = []
        discounted_return = 0
        for reward in reversed(rewards):
            discounted_return = reward + self.gamma * discounted_return
            returns.insert(0, discounted_return)

        returns = torch.tensor(returns)
        std = returns.std()
        num_elements = len(returns)

        if num_elements < 2:
            # Skip normalization if there is only one element
            pass
        else:
            if std > 0:
                eps = 1e-8  # Small constant to prevent division by zero
                returns = (returns - returns.mean()) / (std + eps)
            else:
                pass

        log_probs = []
        for state, action in zip(states, actions):
            state = torch.from_numpy(state).float().unsqueeze(0).view(-1)
            action_probs = self.policy(state)
            dist = torch.distributions.Categorical(action_probs)
            log_prob = dist.log_prob(torch.tensor([action]))
            log_probs.append(log_prob)

        log_probs = torch.cat(log_probs)
        loss = (-log_probs * returns).mean()

        self.optimizer.zero_grad()
        self.policy.backward(loss)
        self.optimizer.step()