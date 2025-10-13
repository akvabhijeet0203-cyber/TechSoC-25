"""
Advanced Pokémon Battle System
- Pokemon class with moves (damage + optional status effects)
- Status effects: poison, paralysis, sleep
- Turn-based battle loop with critical hits
- AIBattle with difficulty levels and move-choosing logic
- Tournament single-elimination (2^n participants)
- Battle statistics tracking and printed outputs

Usage examples are included at the bottom of this file.
"""

import random
import math
from copy import deepcopy
from typing import List, Tuple, Optional, Dict

# -------------------- Helpers & Constants --------------------
CRITICAL_CHANCE = 0.10
CRITICAL_MULT = 2.0

STATUS_POISON = "poison"
STATUS_PARALYSIS = "paralysis"
STATUS_SLEEP = "sleep"

# Poison deals fixed percent of max HP each turn
POISON_PERCENT = 0.10
POISON_DURATION = 4
PARALYSIS_DURATION = 3
SLEEP_MIN = 2
SLEEP_MAX = 4

# -------------------- Pokemon --------------------
class Pokemon:
    def __init__(self, name: str, max_hp: int, attack: int, defense: int, speed: int, moves: List[Tuple]):
        """moves: list of tuples. Each tuple can be one of:
           (name, power) or (name, power, effect) where effect in {"poison","paralysis","sleep"}
           power==0 means a purely status/utility move
        """
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.moves = moves
        self.statuses: Dict[str, Dict] = {}  # effect -> {duration: int}
        self.alive = True

    def is_fainted(self):
        return self.hp <= 0

    def apply_status(self, effect: str, duration: Optional[int] = None):
        if effect == STATUS_POISON:
            self.statuses[STATUS_POISON] = {'duration': duration if duration is not None else POISON_DURATION}
        elif effect == STATUS_PARALYSIS:
            self.statuses[STATUS_PARALYSIS] = {'duration': duration if duration is not None else PARALYSIS_DURATION}
        elif effect == STATUS_SLEEP:
            self.statuses[STATUS_SLEEP] = {'duration': duration if duration is not None else random.randint(SLEEP_MIN, SLEEP_MAX)}

    def clear_status(self, effect: str):
        if effect in self.statuses:
            del self.statuses[effect]

    def take_damage(self, dmg: int):
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def end_of_turn(self):
        # Handle poison damage
        events = []
        if STATUS_POISON in self.statuses:
            pct = POISON_PERCENT
            dmg = math.ceil(self.max_hp * pct)
            self.take_damage(dmg)
            events.append(f"{self.name} takes {dmg} poison damage!\n{self.name} HP: {self.hp}/{self.max_hp}")
            self.statuses[STATUS_POISON]['duration'] -= 1
            if self.statuses[STATUS_POISON]['duration'] <= 0:
                self.clear_status(STATUS_POISON)
                events.append(f"{self.name} is no longer poisoned!")
        # Decrease other durations without immediate effect
        for st in [STATUS_PARALYSIS, STATUS_SLEEP]:
            if st in self.statuses:
                self.statuses[st]['duration'] -= 1
                if self.statuses[st]['duration'] <= 0:
                    self.clear_status(st)
                    events.append(f"{self.name} is no longer {st}ed!")
        return events

    def status_summary(self):
        parts = []
        for k, v in self.statuses.items():
            parts.append(f"{k} ({v['duration']} turns)")
        return ", ".join(parts) if parts else "None"

    def copy_for_battle(self):
        return deepcopy(self)

# -------------------- Damage calculation --------------------

def calculate_damage(attacker: Pokemon, defender: Pokemon, move_power: int):
    # Base damage formula
    if move_power <= 0:
        return 0
    base = (attacker.attack * move_power) / max(1, defender.defense)
    # Critical
    crit = 1
    if random.random() < CRITICAL_CHANCE:
        crit = CRITICAL_MULT
    dmg = math.floor(base * crit)
    return max(1, dmg), crit > 1

# -------------------- Battle --------------------
class Battle:
    def __init__(self, p1: Pokemon, p2: Pokemon, verbose: bool = True):
        self.p1 = p1.copy_for_battle()
        self.p2 = p2.copy_for_battle()
        self.turn = 0
        self.verbose = verbose
        self.log: List[str] = []
        self.stats = {
            'turns': 0,
            'status_used': 0,
            'critical_hits': 0,
        }

    def logf(self, s: str):
        self.log.append(s)
        if self.verbose:
            print(s)

    def apply_move(self, user: Pokemon, target: Pokemon, move: Tuple):
        name = move[0]
        power = move[1] if len(move) > 1 else 0
        effect = move[2] if len(move) > 2 else None

        if power <= 0 and effect is None:
            # purely non-effect, do nothing
            self.logf(f"{user.name} used {name}. (No effect)")
            return

        # Status-only move
        if power <= 0 and effect:
            # Apply status
            if effect not in target.statuses:
                target.apply_status(effect)
                self.stats['status_used'] += 1
                self.logf(f"{user.name} used {name}!")
                self.logf(f"{target.name} is now {effect}! ({target.statuses[effect]['duration']} turns remaining)")
            else:
                self.logf(f"{user.name} used {name}, but {target.name} already has {effect}.")
            return

        # Damage move
        dmg, was_crit = calculate_damage(user, target, power)
        target.take_damage(dmg)
        self.logf(f"{user.name} used {name}!")
        if was_crit:
            self.stats['critical_hits'] += 1
            self.logf("Critical Hit!")
        self.logf(f"{target.name} took {dmg} damage!\n{target.name} HP: {target.hp}/{target.max_hp}")

        # Some damage moves may also carry a status effect (optional)
        if effect and effect not in target.statuses and target.alive:
            target.apply_status(effect)
            self.stats['status_used'] += 1
            self.logf(f"{target.name} is now {effect}! ({target.statuses[effect]['duration']} turns remaining)")

    def can_act(self, pokemon: Pokemon):
        # Check sleep
        if STATUS_SLEEP in pokemon.statuses:
            self.logf(f"{pokemon.name} is asleep and cannot move! (Sleep turns left: {pokemon.statuses[STATUS_SLEEP]['duration']})")
            return False
        # Check paralysis
        if STATUS_PARALYSIS in pokemon.statuses:
            if random.random() < 0.5:
                self.logf(f"{pokemon.name} is paralyzed and cannot move! (Paralysis turns left: {pokemon.statuses[STATUS_PARALYSIS]['duration']})")
                return False
        return True

    def run_turn(self, mover: Pokemon, other: Pokemon, mover_choice: Tuple):
        if mover.is_fainted() or other.is_fainted():
            return
        if not self.can_act(mover):
            return
        self.apply_move(mover, other, mover_choice)

    def auto_choose_move(self, user: Pokemon, opponent: Pokemon):
        # Default naive choice: pick move with highest expected damage; consider status moves
        # Return move tuple
        # For non-AI battles, this can be used as a fallback random choice
        best = None
        best_score = -1
        for mv in user.moves:
            name = mv[0]
            power = mv[1] if len(mv) > 1 else 0
            effect = mv[2] if len(mv) > 2 else None
            score = 0
            if power > 0:
                est_dmg, _ = calculate_damage(user, opponent, power)
                score += est_dmg
            if effect:
                # Score status moves by how much they could change the fight
                score += 10
                if opponent.hp / opponent.max_hp > 0.7:
                    score += 5
            # Slight randomness
            score *= random.uniform(0.9, 1.1)
            if score > best_score:
                best_score = score
                best = mv
        return best if best else random.choice(user.moves)

    def start_battle(self, ai_controller: Optional[Dict] = None):
        # ai_controller: {'which': 'p1' or 'p2', 'difficulty': 'easy'/'medium'/'hard'}
        self.logf("=== BATTLE BEGINS! ===")
        self.logf(f"{self.p1.name} (HP: {self.p1.hp}/{self.p1.max_hp}) VS {self.p2.name} (HP: {self.p2.hp}/{self.p2.max_hp})")
        # Announce statuses
        if ai_controller:
            if ai_controller.get('which') == 'p1':
                self.logf(f"{self.p1.name} is controlled by COMPUTER")
            else:
                self.logf(f"{self.p2.name} is controlled by COMPUTER")

        while self.p1.alive and self.p2.alive:
            self.turn += 1
            self.stats['turns'] = self.turn
            # Determine order
            first, second = (self.p1, self.p2) if self.p1.speed >= self.p2.speed else (self.p2, self.p1)
            self.logf(f"\nTurn {self.turn}: {first.name} goes first! (Speed: {first.speed} vs {second.speed})")

            # Decide moves
            # If AI is controlling one side, use its choice strategy
            choice_first = None
            choice_second = None
            # simple default choices
            if ai_controller and ai_controller.get('which'):
                which = ai_controller['which']
                difficulty = ai_controller.get('difficulty', 'medium')
                # map Pokemon instances to p1/p2
                if which == 'p1':
                    if first is self.p1:
                        choice_first = self.ai_choose_move(self.p1, self.p2, difficulty)
                    else:
                        choice_second = self.ai_choose_move(self.p1, self.p2, difficulty)
                else:
                    if first is self.p2:
                        choice_first = self.ai_choose_move(self.p2, self.p1, difficulty)
                    else:
                        choice_second = self.ai_choose_move(self.p2, self.p1, difficulty)

            # Fill remaining choices with auto_choose_move
            if choice_first is None:
                choice_first = self.auto_choose_move(first, second)
            if choice_second is None:
                choice_second = self.auto_choose_move(second, first)

            # Execute
            self.run_turn(first, second, choice_first)
            if second.alive:
                self.run_turn(second, first, choice_second)

            # End-of-turn effects
            e1 = self.p1.end_of_turn()
            e2 = self.p2.end_of_turn()
            for ev in e1 + e2:
                self.logf(ev)

            # Check faint
            if self.p1.is_fainted():
                self.logf(f"{self.p1.name} fainted!")
                winner = self.p2
                break
            if self.p2.is_fainted():
                self.logf(f"{self.p2.name} fainted!")
                winner = self.p1
                break

        # Determine winner
        winner = self.p1 if self.p1.alive else self.p2
        self.logf(f"\n🏆 {winner.name} wins the battle! 🏆")
        # Summary
        self.logf("\nBattle Summary:")
        self.logf(f"- Winner: {winner.name}")
        self.logf(f"- Turns: {self.stats['turns']}")
        self.logf(f"- Status Effects Used: {self.stats['status_used']}")
        self.logf(f"- Critical Hits: {self.stats['critical_hits']}")
        return winner.name, self.stats

    def ai_choose_move(self, user: Pokemon, opponent: Pokemon, difficulty: str = 'medium'):
        # Explainable AI decision-making printed to logs
        # difficulty:
        # easy: random with bias to damaging moves
        # medium: mix of status/damage using heuristics
        # hard: strategic: status if opponent high HP, finish if low HP, consider self HP

        # Quick helpers
        def has_healing(p):
            # This demo doesn't have healing moves, but put placeholder
            return False

        # Evaluate moves
        if difficulty == 'easy':
            # 70% choose damaging move randomly, 30% pick random
            damaging = [m for m in user.moves if (len(m) > 1 and m[1] > 0)]
            status_moves = [m for m in user.moves if len(m) > 2 and m[2] in (STATUS_POISON, STATUS_PARALYSIS, STATUS_SLEEP)]
            if damaging and random.random() < 0.7:
                choice = random.choice(damaging)
            else:
                choice = random.choice(user.moves)
            self.logf(f"🤖 AI Analysis: (easy) choosing move")
            return choice

        if difficulty == 'medium':
            # Use some heuristics
            damaging = sorted([m for m in user.moves if (len(m) > 1 and m[1] > 0)], key=lambda x: x[1], reverse=True)
            status_moves = [m for m in user.moves if len(m) > 2 and m[2] in (STATUS_POISON, STATUS_PARALYSIS, STATUS_SLEEP)]
            if opponent.hp / opponent.max_hp > 0.7 and status_moves:
                self.logf("🤖 AI Analysis: Opponent high HP, using status move")
                return random.choice(status_moves)
            if opponent.hp / opponent.max_hp < 0.25 and damaging:
                self.logf("🤖 AI Analysis: Opponent low HP, going for highest damage")
                return damaging[0]
            # otherwise pick medium-high damaging move
            self.logf("🤖 AI Analysis: Balanced choice")
            return damaging[0] if damaging else random.choice(user.moves)

        # hard
        if difficulty == 'hard':
            damaging = sorted([m for m in user.moves if (len(m) > 1 and m[1] > 0)], key=lambda x: x[1], reverse=True)
            status_moves = [m for m in user.moves if len(m) > 2 and m[2] in (STATUS_POISON, STATUS_PARALYSIS, STATUS_SLEEP)]
            # If opponent high HP and we have status, use it
            if opponent.hp / opponent.max_hp > 0.6 and status_moves:
                self.logf("🤖 AI Analysis: Enemy has higher HP, using status move for advantage")
                return random.choice(status_moves)
            # If opponent paralyzed/sleeping, hit with damage
            if STATUS_PARALYSIS in opponent.statuses or STATUS_SLEEP in opponent.statuses:
                self.logf("🤖 AI Analysis: Enemy impaired, time for damage")
                return damaging[0] if damaging else random.choice(user.moves)
            # If opponent low HP, finish with strongest
            if opponent.hp / opponent.max_hp < 0.25 and damaging:
                self.logf("🤖 AI Analysis: Low HP enemy, finish with strongest move")
                return damaging[0]
            # else pick effective damage
            self.logf("🤖 AI Analysis: Hard mode, selecting most effective move")
            # pick damaging move with highest expected damage estimate
            best = None
            best_est = -1
            for mv in damaging:
                est, _ = calculate_damage(user, opponent, mv[1])
                if est > best_est:
                    best_est = est
                    best = mv
            return best if best else random.choice(user.moves)

# -------------------- Tournament --------------------
class Tournament:
    def __init__(self, participants: List[Pokemon], tournament_name: str, verbose: bool = True):
        if (len(participants) & (len(participants) - 1)) != 0 or len(participants) == 0:
            raise ValueError("Number of participants must be a power of two (4,8,16,...)")
        self.name = tournament_name
        self.original = participants
        self.bracket = [p.copy_for_battle() for p in participants]
        self.verbose = verbose
        self.stats = {
            'total_battles': 0,
            'total_turns': 0,
            'critical_hits': 0,
            'status_effects': 0,
        }
        self.history: List[str] = []

    def run_match(self, a: Pokemon, b: Pokemon):
        battle = Battle(a, b, verbose=self.verbose)
        winner_name, bstats = battle.start_battle()
        # update tournament stats
        self.stats['total_battles'] += 1
        self.stats['total_turns'] += bstats.get('turns', 0)
        self.stats['critical_hits'] += bstats.get('critical_hits', 0)
        self.stats['status_effects'] += bstats.get('status_used', 0)
        self.history.append(f"{a.name} vs {b.name} -> Winner: {winner_name} (Turns: {bstats.get('turns',0)})")
        # return winner Pokemon object with remaining HP etc.
        return a if a.alive else b

    def start_tournament(self):
        print(f"🏆 {self.name.upper()} TOURNAMENT 🏆")
        print(f"Participants: {len(self.bracket)} Pokémon\n")
        round_num = 1
        participants = self.bracket
        while len(participants) > 1:
            print(f"=== ROUND {round_num} ===")
            next_round = []
            for i in range(0, len(participants), 2):
                a = participants[i]
                b = participants[i+1]
                print(f"Match: {a.name} vs {b.name}")
                winner = self.run_match(a, b)
                print(f"{winner.name} advances to next round!\n")
                # Winner proceeds with its current HP and statuses preserved
                next_round.append(winner)
            participants = next_round
            round_num += 1
        champion = participants[0]
        print(f"🏆 {champion.name.upper()} WINS THE {self.name.upper()}! 🏆\n")
        print("=== TOURNAMENT STATISTICS ===")
        print(f"Champion: {champion.name}")
        print(f"Total Battles: {self.stats['total_battles']}")
        print(f"Total Turns: {self.stats['total_turns']}")
        print(f"Critical Hits: {self.stats['critical_hits']}")
        print(f"Status Effects: {self.stats['status_effects']}\n")
        print("Final Standings:")
        # Simple standings: champion, runner-up, others tied
        print(f"1st: {champion.name}")
        # runner-up can be inferred from history last match
        if self.history:
            last = self.history[-1]
            # parse last => "X vs Y -> Winner: Z"
            parts = last.split('->')
            if len(parts) >= 2:
                winner_part = parts[1].strip()
                runner_up = None
                # determine who lost in final by name
                if winner_part.startswith(champion.name):
                    # unfortunate—this case shouldn't happen normally
                    runner_up = 'Unknown'
                else:
                    runner_up = winner_part.replace('Winner:','').strip()
                print(f"2nd: {runner_up}")
        print("(Other participants eliminated in earlier rounds are tied for 3rd...)")
        return champion.name

# -------------------- Example Usage --------------------
if __name__ == '__main__':
    # Example 1: AI Battle with Status Effects
    venomoth = Pokemon("Venomoth", 95, 65, 60, 90,
                      [("Poison Powder", 0, STATUS_POISON), ("Psychic", 55), ("Sleep Powder", 0, STATUS_SLEEP), ("Bug Buzz", 50)])

    alakazam = Pokemon("Alakazam", 85, 90, 45, 120,
                      [("Psychic", 55), ("Thunder Wave", 0, STATUS_PARALYSIS), ("Teleport", 0), ("Psybeam", 45)])

    ai_battle = Battle(venomoth, alakazam, verbose=True)
    # let the AI control alakazam (p2) as 'hard'
    ai_battle.start_battle(ai_controller={'which': 'p2', 'difficulty': 'hard'})

    # Example 2: 4-Pokémon Tournament
    participants = [
        Pokemon("Charizard", 120, 84, 78, 100, [("Flamethrower", 60), ("Dragon Claw", 50), ("Fire Blast", 80), ("Slash", 35)]),
        Pokemon("Blastoise", 125, 83, 100, 78, [("Hydro Pump", 80), ("Ice Beam", 55), ("Surf", 65), ("Bite", 40)]),
        Pokemon("Venusaur", 115, 82, 83, 80, [("Solar Beam", 75), ("Vine Whip", 35), ("Petal Dance", 70), ("Sleep Powder", 0, STATUS_SLEEP)]),
        Pokemon("Pikachu", 100, 55, 40, 90, [("Thunder", 70), ("Quick Attack", 30), ("Thunder Wave", 0, STATUS_PARALYSIS), ("Agility", 0)])
    ]

    tournament = Tournament(participants, "Kanto Championship", verbose=True)
    tournament.start_tournament()
