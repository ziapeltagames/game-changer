# Observable State

The observation_space is encoded for the model as a list of 61 integers.

* 5 Resource Pools
   * Encoded as 6 integers
   * May hold up to 5 resource dice   
   * Empty dice slots are encoded with 0
   * The first value is the resource pool type
   * [<Resource.ENUM>, die.value, die.value, die.value, die.value, die.value] X 5
* 1 Achievement
   * Encoded as 3 integers
   * All achievements are for getting a total number of resource dice onto a location
   * [<AchievementType.ENUM>, <Resource.ENUM>, sum] X 1
* 4 Locations, each of a resource type
   * Encoded as 7 integers
   * A character may be at a location, represented by 0 or 1
   * [<Resource.ENUM>, die.value, die.value, die.value, die.value, die.value, <Character.ID>] X 4

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

This is done by moving the character to different locations. After moving, a character automatically moves a die from the related resource pool to the location.

Each achievement has a resource type and value, and is fulfilled when there are resource dice of the same type on locations that sum to this value.

## Turn

* Refill dice pools
* Take action
   * Move one character
* Move resources from pool to locations where characters are
* Check to see if achievement completed
* Check if Timers == 10

## action_space

The action_space is one integer from 0-4.

* 0-3: Move the character (Keel - ID 1) to one of the 4 locations

# Scaling Back Options

- Remove resource pool representation (30)