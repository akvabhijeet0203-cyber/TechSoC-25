# Level 3: Advanced Battle Features

## Problem Statement
Create an intelligent battle system with computer-controlled opponents, status effects, battle statistics tracking, and tournament mode for multiple Pokémon battles.

## Requirements
- **Smart Computer Player:** AI chooses moves based on effectiveness and remaining HP
- **Status Effects:** Poison, paralysis, or sleep that affect multiple turns
- **Battle Statistics:** Track wins, losses, and battle history
- **Tournament Mode:** Multiple Pokémon face off in elimination rounds
- **Advanced Battle Mechanics:** Status effect interactions and strategic AI

## Input Format
```
Tournament setup:
- participants: list of Pokemon objects (must be power of 2: 4, 8, 16, etc.)
- tournament_name: string

AI Battle:
- player_pokemon: Pokemon object
- computer_pokemon: Pokemon object
- difficulty: string ("easy", "medium", "hard")

Status effects:
- effect_type: string ("poison", "paralysis", "sleep")
- duration: integer (turns remaining)
```

## Output Format
```
Tournament bracket display
Round-by-round results
AI decision explanations
Status effect notifications
Comprehensive battle statistics
Tournament winner announcement
```

## Example 1: AI Battle with Status Effects

### Input:
```python
# Create Pokemon with status-inducing moves
venomoth = Pokemon("Venomoth", 95, 65, 60, 90,
                  [("Poison Powder", 0, "poison"), ("Psychic", 55), ("Sleep Powder", 0, "sleep"), ("Bug Buzz", 50)])

alakazam = Pokemon("Alakazam", 85, 90, 45, 120,
                  [("Psychic", 55), ("Thunder Wave", 0, "paralysis"), ("Teleport", 0), ("Psybeam", 45)])

# Start AI battle (computer controls Alakazam)
ai_battle = AIBattle(venomoth, alakazam, difficulty="hard")
ai_battle.start_battle()
```

### Expected Output:
```
=== AI POKÉMON BATTLE BEGINS! ===
Venomoth (HP: 95/95) VS Alakazam (HP: 85/85) [COMPUTER]

Turn 1: Alakazam goes first! (Speed: 120 vs 90)
🤖 AI Analysis: Enemy has higher HP, using status move for advantage
Alakazam used Thunder Wave!
Venomoth is now paralyzed! (3 turns remaining)

Turn 2: Venomoth is paralyzed and cannot move!
Paralysis duration: 2 turns remaining

Turn 3: Alakazam strikes!
🤖 AI Analysis: Enemy paralyzed, time for damage
Alakazam used Psychic!
Venomoth took 90 damage!
Venomoth HP: 5/95

Turn 4: Venomoth breaks free from paralysis!
Venomoth used Poison Powder!
Alakazam is now poisoned! (4 turns remaining)

Turn 5: Alakazam goes first!
🤖 AI Analysis: Low HP enemy, finish with strongest move
Alakazam used Psychic!
Venomoth took 90 damage!
Venomoth HP: 0/95

Alakazam takes 10 poison damage!
Alakazam HP: 75/85

Venomoth fainted!
🏆 Alakazam (COMPUTER) wins the battle!

Battle Summary:
- Winner: Alakazam (AI)
- Turns: 5
- Status Effects Used: 2
- AI Difficulty: Hard
- Critical Hits: 0
```

## Example 2: 4-Pokémon Tournament

### Input:
```python
# Create tournament participants
participants = [
    Pokemon("Charizard", 120, 84, 78, 100, [("Flamethrower", 60), ("Dragon Claw", 50), ("Fire Blast", 80), ("Slash", 35)]),
    Pokemon("Blastoise", 125, 83, 100, 78, [("Hydro Pump", 80), ("Ice Beam", 55), ("Surf", 65), ("Bite", 40)]),
    Pokemon("Venusaur", 115, 82, 83, 80, [("Solar Beam", 75), ("Vine Whip", 35), ("Petal Dance", 70), ("Sleep Powder", 0, "sleep")]),
    Pokemon("Pikachu", 100, 55, 40, 90, [("Thunder", 70), ("Quick Attack", 30), ("Thunder Wave", 0, "paralysis"), ("Agility", 0)])
]

tournament = Tournament(participants, "Kanto Championship")
tournament.start_tournament()
```

### Expected Output:
```
🏆 KANTO CHAMPIONSHIP TOURNAMENT 🏆
Participants: 4 Pokémon

=== TOURNAMENT BRACKET ===
Semifinal 1: Charizard vs Blastoise
Semifinal 2: Venusaur vs Pikachu

=== SEMIFINAL 1 ===
Charizard (HP: 120/120) VS Blastoise (HP: 125/125)

Turn 1: Charizard goes first! (Speed: 100 vs 78)
Charizard used Flamethrower!
Blastoise took 64 damage!
Blastoise HP: 61/125

Turn 2: Blastoise strikes back!
Blastoise used Hydro Pump!
Critical Hit!
Charizard took 168 damage!
Charizard HP: 0/120

Charizard fainted!
Blastoise advances to the finals!

=== SEMIFINAL 2 ===
Venusaur (HP: 115/115) VS Pikachu (HP: 100/100)

Turn 1: Pikachu goes first! (Speed: 90 vs 80)
Pikachu used Thunder Wave!
Venusaur is now paralyzed! (3 turns remaining)

Turn 2: Venusaur is paralyzed and cannot move!

Turn 3: Pikachu strikes!
Pikachu used Thunder!
Venusaur took 51 damage!
Venusaur HP: 64/115

Turn 4: Venusaur breaks free from paralysis!
Venusaur used Solar Beam!
Pikachu took 74 damage!
Pikachu HP: 26/100

Turn 5: Pikachu goes first!
Pikachu used Thunder!
Critical Hit!
Venusaur took 102 damage!
Venusaur HP: 0/115

Venusaur fainted!
Pikachu advances to the finals!

=== CHAMPIONSHIP FINAL ===
Blastoise (HP: 61/125) VS Pikachu (HP: 26/100)

Turn 1: Pikachu goes first! (Speed: 90 vs 78)
Pikachu used Thunder!
Blastoise took 56 damage!
Blastoise HP: 5/125

Turn 2: Blastoise strikes back!
Blastoise used Surf!
Pikachu took 65 damage!
Pikachu HP: 0/100

Pikachu fainted!
🏆 BLASTOISE WINS THE KANTO CHAMPIONSHIP! 🏆

=== TOURNAMENT STATISTICS ===
Champion: Blastoise
Total Battles: 3
Total Turns: 11
Critical Hits: 2
Status Effects: 1

Final Standings:
1st: Blastoise
2nd: Pikachu  
3rd: Charizard & Venusaur (tied)
```

## AI Decision Logic
```
def choose_move(self, opponent):
    if self.hp < 30% and has_healing_move():
        return healing_move
    elif opponent.hp > 70% and has_status_move():
        return status_move  
    elif opponent.hp < 25%:
        return strongest_move
    else:
        return most_effective_move
```

## Status Effects System
```
Poison: Deals 10% max HP damage each turn for 4 turns
Paralysis: 50% chance to skip turn for 3 turns  
Sleep: Cannot move for 2-4 turns (random duration)
```

## Tournament Structure
```
- Must have 2^n participants (4, 8, 16, etc.)
- Single elimination bracket
- Winners advance, losers are eliminated
- Final champion crowned
- Complete statistics tracking
```