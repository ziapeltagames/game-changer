# game-changer

Reinforcement learning engine for Six Winters strategy tuning. Eventually, the goal is to use reinforcment learning to search through the design space of the game, ensuring there are a number of viable paths to victory.

This repository uses the Open AI Gym interface to track the Six Winters game state. The two main elements of this environment are the action_space (what the AI can choose to do) and observation_space (what the AI can see).

# Running the Game

```
python qlearning.py
```

# Simplified Rules

The first version of the game is very simple. Two characters move between four locations. Each location has a resource type and may hold a number of dice of this type. There are five resource pools, each containing a number of dice, of the following types: mana, timber, ore, luxury, and food.

On their turn, characters may move to any of these four locations, or take dice up to a certain value from the pool to the location card. There are two achievments in play at any given time. Each achievement has a resource type and value, and is fulfilled when there are resource dice of the same type on locations that sum to this value.

## action_space

The first discrete value moves character 1 to one of the four locations (indexed as 0-4). The second moves character 2.

```
spaces.Tuple((spaces.Discrete(4), 
              spaces.Discrete(4)))
```

## observation_space

The observation space is more complex. It consists of encodings for the following:

* Location 1-4:
   * Resource Type, Dice X 5
* Resource Pools 1-5:
   * Resource Type, Dice X 5
* Achievement 1-2:
   * Achievement Type, Resource Type, Total
