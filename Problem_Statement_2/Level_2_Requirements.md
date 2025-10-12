# Level 2: Battle System & Combat Logic

## Problem Statement
Implement the core battle mechanics that make fights strategic and exciting. Create a damage calculation system with turn-based combat, critical hits, and proper turn order determination.

## Requirements
- Turn order determined by Speed stats (faster Pokémon goes first)
- Enhanced damage calculation: `damage = (attacker_attack * move_power) / defender_defense`
- Critical hits occur randomly (10% chance for 2x damage)
- Complete turn-based battle loop until one Pokémon faints
- Battle class to manage the entire combat system

## Input Format
```
Battle initialization:
- pokemon1: Pokemon object
- pokemon2: Pokemon object

Turn execution:
- current_pokemon: Pokemon object
- target_pokemon: Pokemon object
- move_choice: integer (0-3) or "auto" for random selection
```

## Output Format
```
Battle start announcement
Turn-by-turn combat log
Critical hit notifications
HP updates after each attack
Battle end result with winner
```

## Example 1: Complete Battle with Critical Hit

### Input:
```python
# Create Pokemon
pikachu = Pokemon("Pikachu", 100, 55, 40, 90, 
                 [("Thunder Shock", 40), ("Quick Attack", 30), ("Agility", 0), ("Thunder", 70)])

charmander = Pokemon("Charmander", 90, 52, 43, 65,
                    [("Ember", 35), ("Scratch", 25), ("Growl", 0), ("Flamethrower", 60)])

# Start battle
battle = Battle(pikachu, charmander)
battle.start_battle()

# Manual turn choices (for demonstration)
# Turn 1: Pikachu uses Thunder Shock (move 0)
# Turn 2: Charmander uses Ember (move 0)
# Turn 3: Pikachu uses Thunder (move 3) - Critical Hit!
# Continue until one faints...
```

### Expected Output:
```
=== POKÉMON BATTLE BEGINS! ===
Pikachu (HP: 100/100) VS Charmander (HP: 90/90)

Turn 1: Pikachu goes first! (Speed: 90 vs 65)
Pikachu used Thunder Shock!
Charmander took 51 damage!
Charmander HP: 39/90

Turn 2: Charmander strikes back!
Charmander used Ember!
Pikachu took 45 damage!
Pikachu HP: 55/100

Turn 3: Pikachu goes first!
Pikachu used Thunder!
Critical Hit!
Charmander took 178 damage!
Charmander HP: 0/90

Charmander fainted!
🏆 Pikachu wins the battle!

Battle Summary:
- Winner: Pikachu
- Turns: 3
- Critical Hits: 1
```

## Example 2: Close Battle with Speed Tie

### Input:
```python
# Create Pokemon with same speed
squirtle = Pokemon("Squirtle", 85, 48, 65, 70,
                  [("Water Gun", 35), ("Tackle", 25), ("Withdraw", 0), ("Bubble Beam", 50)])

bulbasaur = Pokemon("Bulbasaur", 88, 49, 49, 70,
                   [("Vine Whip", 35), ("Tackle", 25), ("Growl", 0), ("Razor Leaf", 45)])

battle = Battle(squirtle, bulbasaur)
battle.start_battle()
```

### Expected Output:
```
=== POKÉMON BATTLE BEGINS! ===
Squirtle (HP: 85/85) VS Bulbasaur (HP: 88/88)

Turn 1: Speed tie! Squirtle goes first! (Speed: 70 vs 70)
Squirtle used Water Gun!
Bulbasaur took 34 damage!
Bulbasaur HP: 54/88

Turn 2: Bulbasaur strikes back!
Bulbasaur used Vine Whip!
Squirtle took 26 damage!
Squirtle HP: 59/85

Turn 3: Bulbasaur goes first!
Bulbasaur used Razor Leaf!
Squirtle took 30 damage!
Squirtle HP: 29/85

Turn 4: Squirtle strikes back!
Squirtle used Bubble Beam!
Bulbasaur took 49 damage!
Bulbasaur HP: 5/88

Turn 5: Bulbasaur goes first!
Bulbasaur used Vine Whip!
Squirtle took 26 damage!
Squirtle HP: 3/85

Turn 6: Squirtle strikes back!
Squirtle used Water Gun!
Bulbasaur took 34 damage!
Bulbasaur HP: 0/88

Bulbasaur fainted!
🏆 Squirtle wins the battle!

Battle Summary:
- Winner: Squirtle
- Turns: 6
- Critical Hits: 0
```

## Enhanced Damage Calculation
```
base_damage = (attacker_attack * move_power) / defender_defense
critical_multiplier = 2.0 if critical_hit else 1.0
final_damage = base_damage * critical_multiplier
final_damage = max(1, final_damage)  // Minimum 1 damage
```

## Turn Order Logic
```
if pokemon1.speed > pokemon2.speed:
    first = pokemon1, second = pokemon2
elif pokemon2.speed > pokemon1.speed:
    first = pokemon2, second = pokemon1
else:
    # Speed tie - random selection
    first, second = random.choice([(pokemon1, pokemon2), (pokemon2, pokemon1)])
```

## Critical Hit Calculation
```
critical_chance = 0.10  // 10% chance
is_critical = random.random() < critical_chance
```