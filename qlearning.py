# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 22:58:43 2021

@author: phill
"""

import sixwinters
import numpy as np

def indices(env_tuple):
    return env_tuple[0], env_tuple[1], env_tuple[2]

# Return both action probabilities for this state
def qactions(qtable, cstate):
    sa, sb, sc = indices(cstate)
    return qtable[sa, sb, sc, :]

# Return the single entry for this state and action
def qaction(qtable, cstate, caction):
    return qactions(qtable, cstate)[caction]

# Run through one game, returning number of turns, updates the Q
# table using standard Q learning algorithm
def play_game(qt, env, lr, y, training = True, logging = False):
    if logging:
        print("(Stage, Current Timers, Total Timers, Current Reward)")
        print("[Bank Progress / Draw] --> Action (0 = Bank, 1 = Draw) Reward")        

    # Reset the game state
    s = env.reset()
    turns = 0
    reward = 0
    done = False
    
    while done == False:
        turns = turns + 1
        if training:
            act = np.argmax(qactions(qt, s) + (np.random.randn(env.action_space.n)))
        else:
            act = np.argmax(qactions(qt, s))
        if logging:
            print(s, qactions(qt, s),"-->",act,reward) 
        s1, reward, done, _ = env.step(act)
        if training:
            
            #Update Q table with new knowledge
            sa, sb, sc = indices(s)
            qt[sa, sb, sc, act] = qaction(qt, s, act) + lr*(reward + y*np.max(qactions(qt, s1)) - qaction(qt, s, act))
        
        s = s1
        
    if logging:
        print("Turns ", turns, "Reward ", reward)
            
    return turns, reward, qt

# Train a simple Q learning algorithm to play Six Winters
def train_qlearn():
    
    env = sixwinters.SixWinters()
    
    # Initialize Q table with all zeros
    Q = np.zeros([env.observation_space.n,
                  env.action_space.n])
    
    return
    
    # lr is the learning rate, the speed at which the Q table is updated
    lr = .00001
    
    # y is the amount to consider future rewards, the higher it is, the more
    # the future rewards are weighed against current rewards
    y = .9
        
    # Number of episodes to conduct training, is there a way to check for
    # convergence?
    num_episodes = 10
    
    # Play a game, returning the updated Q table, along with the number
    # of turns the game lasted, and the total reward
    for i in range(num_episodes):
        turns, r, Q = play_game(Q, env, lr, y, training = True)
    
    # Calculate a batch score after training
    rList = []
    turnList = []
    for i in range(100000):
        turns, r, Q = play_game(Q, env, lr, y, training = False)
        turnList.append(turns)
        rList.append(r)
    
    avg_r = np.average(rList)
    avg_t = np.average(turnList)

    print('Reward ', avg_r,' Turns ', avg_t)

if __name__ ==  "__main__":
    train_qlearn()