import random
import matplotlib.pyplot as plt
import numpy as np
import sys
import pickle
import gymnasium as gym

env = gym.make("Taxi-v3")

epsilon = float(sys.argv[1])
lr = float(sys.argv[2])
discount_factor = float(sys.argv[3])
episodes = 5000
max_episode_length = 100
actions = 6
states = 500
rewards = []

observation, info = env.reset()

policy = {state: None for state in range(states)}
action_values = np.zeros((states, actions))

def choose_action(state, epsilon):
    if random.random() < epsilon:
        return env.action_space.sample()
    else:
        return np.argmax(action_values[state,:])

for _ in range(episodes):
    total = 0
    for i in range(max_episode_length):
        state = observation
        action = choose_action(observation, epsilon)
        observation, reward, terminated, truncated, info = env.step(action)
        total += reward

        action_values[state, action] += lr * (reward + discount_factor * np.max(action_values[observation, :]) - action_values[state, action])

        if truncated or terminated or i == max_episode_length - 1:
            observation, info = env.reset()
            break

        policy[state] = np.argmax(action_values[state, :])

    rewards.append(total)

env.close()
row = action_values.shape[0]
column = action_values.shape[1]
action_values_dict = {}
for i in range(row):
    inner_dict = {}
    for j in range(column):
        inner_dict[j] = action_values[i, j]
    action_values_dict[i] = inner_dict

policy_path = '/Users/hardikgupta/Downloads/hero/qlearning_policy.pickle'
with open(policy_path, 'wb') as f:
    pickle.dump(policy, f)
vals_path = '/Users/hardikgupta/Downloads/hero/qlearning_q_vals.pickle'
with open(vals_path, 'wb') as f:
    pickle.dump(action_values_dict, f)

plt.plot(rewards)
plt.title('Rewards per Episode')
plt.xlabel('Episode')
plt.ylabel('Reward')
plt.savefig('/Users/hardikgupta/Downloads/hero/qlearning_total_reward.png')
plt.show()