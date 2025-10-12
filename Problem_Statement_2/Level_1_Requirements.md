# Level 1: Create Your First Pokémon

## Introduction to the Pokémon Battle Simulator

This challenge involves building a Pokémon battle simulator. You will start by creating the fundamental building block of the simulator: the `Pokemon` class.

A Pokémon battle is a turn-based encounter between two Pokémon. The outcome of the battle depends on the Pokémon's stats and the moves they use.

- **Stats**: Each Pokémon has HP (Health Points), Attack, Defense, and Speed.
- **Moves**: Each Pokémon has a set of four moves with varying power levels.
- **Battle Logic**: The speed of a Pokémon determines who attacks first. The damage dealt by an attack is calculated based on the attacker's Attack stat, the move's power, and the defender's Defense stat.

## Problem Statement
Design and implement a `Pokemon` class that represents a battle-ready creature with all essential attributes and basic functionality. This will be the foundation upon which all future battle mechanics will be built.

## Requirements
- **Attributes:** Name, HP (Health Points), Attack, Defense, Speed
- **Moveset:** Array of 4 moves with different power levels
- **Core Methods:** Attack another Pokémon, take damage, check if fainted
- **Constructor:** Initialize Pokémon with custom stats

## Input Format
```
Pokemon creation:
- name: string
- hp: integer (1-200)
- attack: integer (1-100)
- defense: integer (1-100)
- speed: integer (1-100)
- moves: array of 4 move names with power levels

Attack action:
- attacker: Pokemon object
- defender: Pokemon object
- move_index: integer (0-3)
```

## Output Format
```
Pokemon status display
Attack result messages
Fainted status check
```

## Example 1: Basic Pokemon Creation and Attack

### Input:
```python
# Create Pikachu
pikachu = Pokemon("Pikachu", 100, 55, 40, 90, 
                 [("Thunder Shock", 40), ("Quick Attack", 30), ("Agility", 0), ("Thunder", 70)])

# Create Charmander
charmander = Pokemon("Charmander", 90, 52, 43, 65,
                    [("Ember", 35), ("Scratch", 25), ("Growl", 0), ("Flamethrower", 60)])

# Display initial stats
print(pikachu.display_stats())
print(charmander.display_stats())

# Pikachu attacks Charmander with Thunder Shock
pikachu.attack(charmander, 0)
print(charmander.display_stats())

# Check if Charmander fainted
print(f"Charmander fainted: {charmander.is_fainted()}")
```

### Expected Output:
```
Pikachu - HP: 100/100, Attack: 55, Defense: 40, Speed: 90
Moves: Thunder Shock (40), Quick Attack (30), Agility (0), Thunder (70)

Charmander - HP: 90/90, Attack: 52, Defense: 43, Speed: 65
Moves: Ember (35), Scratch (25), Growl (0), Flamethrower (60)

Pikachu used Thunder Shock!
Charmander took 51 damage!

Charmander - HP: 39/90, Attack: 52, Defense: 43, Speed: 65
Moves: Ember (35), Scratch (25), Growl (0), Flamethrower (60)

Charmander fainted: False
```

## Example 2: Pokemon Fainting

### Input:
```python
# Create weak Magikarp
magikarp = Pokemon("Magikarp", 30, 10, 55, 80,
                  [("Splash", 0), ("Tackle", 20), ("Flail", 15), ("Bounce", 25)])

# Create strong Gyarados
gyarados = Pokemon("Gyarados", 150, 85, 79, 81,
                  [("Hydro Pump", 80), ("Bite", 45), ("Dragon Rage", 50), ("Hyper Beam", 90)])

print(magikarp.display_stats())
print(gyarados.display_stats())

# Gyarados attacks with Hydro Pump
gyarados.attack(magikarp, 0)
print(magikarp.display_stats())
print(f"Magikarp fainted: {magikarp.is_fainted()}")
```

### Expected Output:
```
Magikarp - HP: 30/30, Attack: 10, Defense: 55, Speed: 80
Moves: Splash (0), Tackle (20), Flail (15), Bounce (25)

Gyarados - HP: 150/150, Attack: 85, Defense: 79, Speed: 81
Moves: Hydro Pump (80), Bite (45), Dragon Rage (50), Hyper Beam (90)

Gyarados used Hydro Pump!
Magikarp took 123 damage!

Magikarp - HP: 0/30, Attack: 10, Defense: 55, Speed: 80
Moves: Splash (0), Tackle (20), Flail (15), Bounce (25)

Magikarp fainted: True
```

```