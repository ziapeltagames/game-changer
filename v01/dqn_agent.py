# -*- coding: utf-8 -*-
"""
An agent for playing Six Winters using the TensorFlow Agents library.
TF Agents works well with games which conform to the OpenAI Gym standard.
This version uses a somewhat cumbersome way to calculate metrics. Had
difficulty using the standard TF Agents library calls to handle that.

For this simple version of Six Winters, this just uses a shallow DQN and no
prioritized experience replay.

@author: phill
"""

import sixwinters

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tf_agents.agents.dqn.dqn_agent import DqnAgent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.networks.q_network import QNetwork
from tf_agents.policies import random_tf_policy
from tf_agents.trajectories import trajectory
from tf_agents.utils import common
from tf_agents.replay_buffers import tf_uniform_replay_buffer

def compute_metrics(environment, policy, num_actions, num_episodes=10):
    """
    Computes the average reward, average number of turns, and
    a tree of strategies, and a histogram of different actions on an
    OpenAI Gym RL Environment.

    Parameters
    ----------
    environment : Open AI Gym
    policy : TF Agents Policy
    num_episodes : INT, optional
        Number of episodes to collect metrics on. The default is 10.

    Returns
    -------
    dict
    
    """

    total_rewards = 0.0
    total_turns = 0.0
    strategies = []
    
    # This will need to change if the action space ever moves from
    # a long categorical list of options
    action_hist = np.zeros((num_actions))
    
    for _ in range(num_episodes):
  
      time_step = environment.reset()
      episode_reward = 0.0
      episode_turns = 0.0
      game_tree = []
  
      while not time_step.is_last():
        action_step = policy.action(time_step)
        action = action_step.action.numpy()[0]
        game_tree.append(action)
        action_hist[action] += 1.0
        time_step = environment.step(action_step.action)
        episode_reward += time_step.reward
        episode_turns += 1.0
      total_rewards += episode_reward
      total_turns += episode_turns
      strategies.append(game_tree)
  
    avg_reward = total_rewards / num_episodes
    avg_turns = total_turns / num_episodes
    action_hist = action_hist / num_episodes
  
    return {"reward": avg_reward.numpy()[0],
            "turns": avg_turns,
            "strategies": strategies, 
            "actions": action_hist}

def collect_data(env, policy, buffer, steps):
    """
    Populates the buffer passed in using the given policy. Note! The
    agent will reset the environment when the time ends. This is handled
    behind the scenes.

    """    
    for _ in range(steps):
        time_step = env.current_time_step()
        action_step = policy.action(time_step)
        next_time_step = env.step(action_step.action)
        traj = trajectory.from_transition(time_step, action_step,
                                          next_time_step)
          
        # Add trajectory to the replay buffer
        buffer.add_batch(traj)        

# It is common to have one environment to train on and one environment
# to evaluate metrics on - this way training and metrics gathering
# can be conducted independently
num_actions = sixwinters.SixWinters().action_space.n
train_env = tf_py_environment.TFPyEnvironment(suite_gym.wrap_env(
    sixwinters.SixWinters(), discount = 0.95))
eval_env = tf_py_environment.TFPyEnvironment(suite_gym.wrap_env(
    sixwinters.SixWinters(), discount = 0.95))

# A very simple two layer fully connected neural network
fc_layer_params = [16, 8]

# This creates the neural network
q_net = QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params = fc_layer_params)

train_step = tf.Variable(0)

optimizer = tf.keras.optimizers.RMSprop(lr=2.5e-4, rho=0.95,
                                        momentum=0.0, epsilon=0.00001,
                                        centered=True)

epsilon_fn = tf.keras.optimizers.schedules.PolynomialDecay(
    initial_learning_rate = 1.0,
    decay_steps = 10000,
    end_learning_rate = 0.01)

# Does target_update_period even do anything if there isn't a target network?
agent = DqnAgent(train_env.time_step_spec(),
                 train_env.action_spec(),
                 q_network=q_net,
                 optimizer=optimizer,
                 target_update_period=2000,
                 td_errors_loss_fn=tf.keras.losses.Huber(reduction="none"),
                 gamma=0.99,
                 train_step_counter=train_step)

agent.initialize()

# Optimize by wrapping some of the code in a graph using TF function
agent.train = common.function(agent.train)

# Reset the train step
agent.train_step_counter.assign(0)

# This populates the buffer with a bunch of random moves as a starting 
# point for training. Hopefully some of these purely random games result
# in scores!
random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=10000)

# Initial size of random moves for buffer
initial_collect_steps = 200
collect_data(train_env, random_policy, replay_buffer, initial_collect_steps)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, 
    sample_batch_size=50, 
    num_steps=2).prefetch(3)
iterator = iter(dataset)

num_training_iterations = 750
collect_steps_per_iteration = 1
eval_interval = 10
metrics_eval_episodes = 10

rewards = []
turns = []
strategies = []
actions = []
losses = []

for _ in range(num_training_iterations):

    # Collect a few steps using collect_policy and save to the replay buffer.
    collect_data(train_env, agent.collect_policy, replay_buffer, 
                  collect_steps_per_iteration)
    
    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience).loss
    
    step = agent.train_step_counter.numpy()
    
    if step % eval_interval == 0:
        print(step, train_loss.numpy())
        game_metrics = compute_metrics(eval_env, agent.policy,
                                        num_actions, metrics_eval_episodes)
        
        rewards.append(game_metrics["reward"])
        turns.append(game_metrics["turns"])
        strategies.append(game_metrics["strategies"])
        actions.append(game_metrics["actions"])
        losses.append(train_loss.numpy())

# Plot metrics
fig, ax = plt.subplots(4, gridspec_kw = {'height_ratios': [2, 1, 1, 1]})
fig.tight_layout()

iterations = range(eval_interval, num_training_iterations + eval_interval,
                    eval_interval)

act_hist = np.array(actions).transpose()

ax[0].pcolormesh(act_hist)

action_labels = sixwinters.SixWinters().get_action_meanings()
ax[0].set_yticks(np.arange(len(action_labels)) + 0.5)
ax[0].set_yticklabels(action_labels)
ax[0].set_xticklabels([])

ax[1].plot(iterations, rewards)
ax[1].set_ylabel('Score', rotation=0, labelpad=20)
ax[1].set_ylim(bottom=0)

ax[2].plot(iterations, turns)
ax[2].set_ylabel('Number of Turns', rotation=0, labelpad=50)
ax[2].set_ylim(bottom=1)

ax[3].plot(iterations, losses)
ax[3].set_ylabel('Training Loss', rotation=0, labelpad=40)

plt.xlabel('Number of Training Iterations')