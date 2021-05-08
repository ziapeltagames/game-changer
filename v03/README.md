# Observable State

* 5 resource pools containing 3 six sided dice each
   * Each pool has a different types of resource: mana, timber, ore, luxury, and food
* 4 locations
   * Each location has a resource type
   * Each location can hold up to 3 dice of the listed type
* 2 achievements
   * Each achievement has a resource type and a number from 1-12
* 2 characters

## observation_space

The observable state is encoded for the model as a list of 68 integers.

* 5 resource pools, each of a different type, with up to 5 dice
   * Encoded as 6 integers
   * Empty dice slots are encoded with 0
   * [<Resource.ENUM>, die.value, die.value, die.value, die.value, die.value] X 5
* 2 achievements
   * Encoded as 3 integers
   * All achievements are for getting a total number of resources
   * [<AchievementType.ENUM>, <Resource.ENUM>, sum] X 2
* 4 Locations, each of a resource type
   * Encoded as 8 integers
   * Up to 2 characters may be at a location, represented by 1
   * [<Resource.ENUM>,  die.value, die.value, die.value, die.value, die.value, <Character.ID>, <Character.ID>] X 4

## Enumerations

These encodings are used in the observation_space.

```
class Resource(Enum):
    MANA = 0
    TIMBER = 1
    ORE = 2
    LUXURY = 3
    FOOD = 4

class AchievementType(Enum):
    SUM = 1
    SET = 2
    DISTINCT = 3    
    OBSTACLE = 4
```

# Rules

The goal is to collect four achievement cards before the time runs out. Time is fixed, and runs out after **10 turns**. Two achievements are visible at any given time.

This is done by moving the characters to different locations. After moving, a character automatically moves a die from the related resource pool to the location.

Each achievement has a resource type and value, and is fulfilled when there are resource dice of the same type on locations that sum to this value.

## Turn

* Refill dice pools
* Take action
   * Move one character
* Move resources from pool to locations where characters are
* Check to see if achievement completed
* Check if Timers == 10

## action_space

The action_space is one integer from 0-8.

* 0-3: Move the first character (Keel - ID 1) to one of the 4 locations
* 4-7: Move the second character (Thea - ID 2) to one of the 4 locations

# Notes

This is kind of a wonky version of the game. Can only move one character at a time, and resources are brought from pools to locations automatically and without luck. Normally doing that is an action, and there is chance involved.