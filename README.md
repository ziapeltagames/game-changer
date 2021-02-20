# game-changer

Reinforcement learning engine for [_Six Winters_](https://github.com/ziapeltagames/six-winters/blob/master/docs/RULES.md) boardgame strategy tuning. The goal is to use reinforcment learning to search through the design space of the game, gaining insight into questions like:

* Are there different viable paths to victory?
* How likely is success for each path?
* How complex is the decision space?

This repository uses the Open AI Gym interface to track the _Six Winters_ game state. The two main elements of this environment are the action_space (what the AI can choose to do) and observation_space (what the AI can see). These are both encoded as discrete sequences of integers.

## Directory Structure

Each directory contains one version of the game, with its own simplified rules. The most simplified versions of the game will have lower directory numbers. As more complexity is added to the game, more sophisticated reinforcement learning approaches may be needed to handle it.

The basic Open AI Gym interface is the same for all versions of the game. Each directory has a README that details the observation_space and action_space for that version of the game.

## Running the Game

Each directory has a sixwinters.py file, which implements the SixWinters Open AI Gym environment interface. It's possible to play the games manually by making an instance of this class, passing in actions manually via the step(action_space) function. The current state can be rendered as well using render(). The following can be run from the version directory, via the python interpreter.

```
>>>python

from sixwinters import SixWinters
env = SixWinters()

env.reset()
env.render() # Displays a text version of the game state

env.step(4) # Take an action in the game, the specific valid actions depend on the action_space for the particular version of the game.
env.render()

env.step(3)
env.render()

...
```

## Training the AI

The AI can be trained by running:

```
python qlearning.py
```

The approaches all use some form of Deep Q Learning powered by neural networks as the policy engine.