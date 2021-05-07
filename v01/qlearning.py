# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 22:58:43 2021

@author: phill
"""

import sixwinters

import tensorflow as tf
import numpy as np

from collections import deque

import matplotlib.pyplot as plt

def epsilon_greedy_policy(model, state, num_actions, epsilon = 0.0):
    if np.random.rand() < epsilon or state == None:
        return np.random.randint(num_actions)
    else:
        state = np.array(state)[np.newaxis]
        Q_values = model.predict(state)
        return np.argmax(Q_values[0])

def play_step(replay_buffer, model, num_actions, env, state, epsilon):
    action = epsilon_greedy_policy(model, state, num_actions, epsilon)
    next_state, reward, done, info = env.step(action)
    replay_buffer.append((state, action, reward, next_state, done))
    return next_state, reward, done, info, replay_buffer

def play_game(replay_buffer, model, num_actions, obs, env,
              episode, max_steps = 200):
    total_rewards = 0
    for step in range(max_steps):
        epsilon = max(1 - (episode / 1000), 0.01)
        obs, reward, done, info, replay_buffer = play_step(replay_buffer, 
                                                           model, 
                                                           num_actions, env, 
                                                           obs, epsilon)
        total_rewards = total_rewards + reward
        if done:
            return replay_buffer, total_rewards
    return replay_buffer, total_rewards

def sample_experiences(replay_buffer, batch_size):    
    indices = np.random.randint(len(replay_buffer), size = batch_size)

    batch = [replay_buffer[index] for index in indices]
    
    states, actions, rewards, next_states, dones = [
        np.array([experience[field_index] for experience in batch])
        for field_index in range(5)]
    
    return states, actions, rewards, next_states, dones

def train(model, num_actions, replay_buffer, optimizer):
    
    batch_size = 32
    discount_factor = 0.95
    loss_fn = tf.keras.losses.mean_squared_error
    
    experiences = sample_experiences(replay_buffer, batch_size)
    states, actions, rewards, next_states, dones = experiences

    next_Q_values = model.predict(next_states)
    
    max_next_Q_values = np.max(next_Q_values, axis = 1)
    target_Q_values = (rewards + ((1 - dones) * discount_factor * max_next_Q_values))    
    
    mask = tf.one_hot(actions, num_actions)
    
    with tf.GradientTape() as tape:
        all_Q_values = model(states)
        Q_values = tf.reduce_sum(all_Q_values * mask, 
                                 axis = 1, keepdims = True)
        loss = tf.reduce_mean(loss_fn(target_Q_values, Q_values))
    grads = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(grads, model.trainable_variables))
    return model
    
# Train a simple Q learning algorithm to play Six Winters
def qlearn(model_name = 'sw_dqn.h5'):
    
    env = sixwinters.SixWinters()
    
    input_shape = env.observation_space.shape
    num_actions = env.action_space.n
    
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(64, activation = 'elu', input_shape = input_shape),
        tf.keras.layers.Dense(32, activation = 'elu'),
        tf.keras.layers.Dense(16, activation = 'elu'),        
        tf.keras.layers.Dense(num_actions)
        ])
    
    # TODO: Tried 1e-3
    optimizer = tf.keras.optimizers.Adam(lr = 1e-4)
    
    replay_buffer = deque(maxlen = 8000)
    
    num_episodes = 5000
    
    reward_history = []
        
    # Play a game, returning the updated Q table, along with the number
    # of turns the game lasted, and the total reward
    for episode in range(num_episodes):
        obs = env.reset()
        replay_buffer, total_rewards = play_game(replay_buffer, model, 
                                                 num_actions, obs, env, 
                                                 episode)        
        if episode >= 100:
            model = train(model, num_actions, replay_buffer, optimizer)
            print(episode, ': Training Score', total_rewards, 
                  np.average(reward_history[:-100]))
        else:
            print(episode, ': Exploration Score', total_rewards)
            
        reward_history.append(total_rewards)
    
    window_size = 200
    window = np.ones(window_size) / float(window_size)
    xc = np.convolve(reward_history, window)
    plt.plot(xc[window_size:-window_size])
    plt.title('Six Winters v01 Deep Q Learning')
    plt.xlabel('Games Played')
    plt.ylabel('Score')

if __name__ ==  "__main__":
    qlearn()