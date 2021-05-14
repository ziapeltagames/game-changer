# -*- coding: utf-8 -*-
"""
Created on Sat May  8 12:24:58 2021

@author: phill
"""

import sixwinters

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

def compute_metrics(environment, policy, num_episodes=10):

  total_return = 0.0
  total_steps = 0.0
  
  for _ in range(num_episodes):

    time_step = environment.reset()
    episode_return = 0.0
    episode_length = 0.0

    while not time_step.is_last():
      action_step = policy.action(time_step)
      time_step = environment.step(action_step.action)
      episode_return += time_step.reward
      episode_length += 1.0
    total_return += episode_return
    total_steps += episode_length

  avg_return = total_return / num_episodes
  avg_steps = total_steps / num_episodes

  return avg_return.numpy()[0], avg_steps

def collect_step(environment, policy, buffer):
  time_step = environment.current_time_step()
  action_step = policy.action(time_step)
  next_time_step = environment.step(action_step.action)
  traj = trajectory.from_transition(time_step, action_step, next_time_step)

  # Add trajectory to the replay buffer
  buffer.add_batch(traj)

def collect_data(env, policy, buffer, steps):
  for _ in range(steps):
    collect_step(env, policy, buffer)
    
train_env = tf_py_environment.TFPyEnvironment(suite_gym.wrap_env(
    sixwinters.SixWinters(), discount = 0.95))
eval_env = tf_py_environment.TFPyEnvironment(suite_gym.wrap_env(
    sixwinters.SixWinters(), discount = 0.95))

fc_layer_params = [16, 8]

q_net = QNetwork(
    train_env.observation_spec(),
    train_env.action_spec(),
    fc_layer_params = fc_layer_params)

train_step = tf.Variable(0)
update_period = 4
optimizer = tf.keras.optimizers.RMSprop(lr=2.5e-4, rho=0.95,
                                        momentum=0.0, epsilon=0.00001,
                                        centered=True)

epsilon_fn = tf.keras.optimizers.schedules.PolynomialDecay(
    initial_learning_rate = 1.0,
    decay_steps = 10000,
    end_learning_rate = 0.01)

agent = DqnAgent(train_env.time_step_spec(),
                 train_env.action_spec(),
                 q_network=q_net,
                 optimizer=optimizer,
                 target_update_period=2000,
                 td_errors_loss_fn=tf.keras.losses.Huber(reduction="none"),
                 gamma=0.99,
                 train_step_counter=train_step)

agent.initialize()



# (Optional) Optimize by wrapping some of the code in a graph using TF function.
agent.train = common.function(agent.train)

# Reset the train step
agent.train_step_counter.assign(0)

# Evaluate the agent's policy once before training.
num_eval_episodes = 10
avg_return, avg_steps = compute_metrics(eval_env, agent.policy, 
                                        num_eval_episodes)
returns = [avg_return]
steps = [avg_steps]

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(),
                                                train_env.action_spec())

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=10000)

initial_collect_steps = 200
collect_data(train_env, random_policy, replay_buffer, initial_collect_steps)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, 
    sample_batch_size=50, 
    num_steps=2).prefetch(3)
iterator = iter(dataset)

num_iterations = 1000
collect_steps_per_iteration = 1
log_interval = 10
eval_interval = 5

for _ in range(num_iterations):

  # Collect a few steps using collect_policy and save to the replay buffer.
  collect_data(train_env, agent.collect_policy, replay_buffer, 
                collect_steps_per_iteration)

  # Sample a batch of data from the buffer and update the agent's network.
  experience, unused_info = next(iterator)
  train_loss = agent.train(experience).loss

  step = agent.train_step_counter.numpy()

  if step % log_interval == 0:
    print('step = {0}: loss = {1}'.format(step, train_loss))

  if step % eval_interval == 0:
    avg_return, avg_steps = compute_metrics(eval_env, agent.policy, 
                                            num_eval_episodes)
    print('step = {0}: Avg Return = {1}, Avg Steps = {2}'.format(step, 
                                                                 avg_return, 
                                                                 avg_steps))
    returns.append(avg_return)
    steps.append(avg_steps)
    
iterations = range(0, num_iterations + 1, eval_interval)
plt.plot(iterations, returns, label='Avg Score')
plt.plot(iterations, steps, label='Game Length')
plt.legend()
plt.xlabel('Number of Training Games')