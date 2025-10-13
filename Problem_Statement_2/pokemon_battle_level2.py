import random
from dataclasses import dataclass, field
from typing import List, Tuple, Optional

random.seed(12345)  # deterministic for demo runs

@dataclass
class Pokemon:
    name: str
    max_hp: int
    attack: int
    defense: int
    speed: int
    moves: List[Tuple[str, int]]  # list of (move_name, power)
    hp: int = field(init=False)
    
    def __post_init__(self):
        self.hp = self.max_hp
    
    def is_fainted(self):
        return self.hp <= 0
    
    def choose_move(self, choice):
        if choice == "auto" or choice is None:
            non_zero = [(i,p) for i,(_,p) in enumerate(self.moves) if p>0]
            if non_zero:
                best = max(non_zero, key=lambda x: (x[1], -x[0]))
                return best[0]
            return random.randrange(len(self.moves))
        if not isinstance(choice, int):
            raise ValueError("move choice must be int index or 'auto'")
        return max(0, min(choice, len(self.moves)-1))


class Battle:
    def __init__(self, p1: Pokemon, p2: Pokemon, crit_chance: float = 0.10):
        self.p1 = p1
        self.p2 = p2
        self.crit_chance = crit_chance
        self.turn_count = 0
        self.crit_hits = 0
    
    def _log(self, msg=""):
        print(msg)
    
    def _damage(self, attacker: Pokemon, defender: Pokemon, move_power: int) -> int:
        base = int((attacker.attack * move_power) / defender.defense)
        is_crit = random.random() < self.crit_chance
        damage = base * (2 if is_crit else 1)
        damage = max(1, damage)
        return damage, is_crit
    
    def start_battle(self, manual_choices: Optional[List[Tuple[Optional[int], Optional[int]]]] = None):
        self._log("=== POKÉMON BATTLE BEGINS! ===")
        self._log(f"{self.p1.name} (HP: {self.p1.hp}/{self.p1.max_hp}) VS {self.p2.name} (HP: {self.p2.hp}/{self.p2.max_hp})\n")
        
        choice_index = 0
        while not self.p1.is_fainted() and not self.p2.is_fainted():
            self.turn_count += 1
            if self.p1.speed > self.p2.speed:
                first, second = self.p1, self.p2
                tie_note = ""
            elif self.p2.speed > self.p1.speed:
                first, second = self.p2, self.p1
                tie_note = ""
            else:
                first, second = random.choice([(self.p1, self.p2), (self.p2, self.p1)])
                tie_note = "Speed tie! "
            
            if first is self.p1:
                self._log(f"Turn {self.turn_count}: {tie_note}{self.p1.name} goes first! (Speed: {self.p1.speed} vs {self.p2.speed})")
            else:
                self._log(f"Turn {self.turn_count}: {tie_note}{self.p2.name} goes first! (Speed: {self.p2.speed} vs {self.p1.speed})")
            
            p1_choice = p2_choice = "auto"
            if manual_choices and choice_index < len(manual_choices):
                p1_choice_raw, p2_choice_raw = manual_choices[choice_index]
                p1_choice = p1_choice_raw if p1_choice_raw is not None else "auto"
                p2_choice = p2_choice_raw if p2_choice_raw is not None else "auto"
            choice_index += 1
            
            for attacker, defender, choice in [(first, second, p1_choice if first is self.p1 else p2_choice),
                                               (second, first, p2_choice if second is self.p2 else p1_choice)]:
                if attacker.is_fainted() or defender.is_fainted():
                    continue
                move_idx = attacker.choose_move(choice)
                move_name, power = attacker.moves[move_idx]
                self._log(f"{attacker.name} used {move_name}!")
                if power <= 0:
                    self._log("It had no effect!")
                    continue
                dmg, was_crit = self._damage(attacker, defender, power)
                if was_crit:
                    self._log("Critical Hit!")
                    self.crit_hits += 1
                defender.hp -= dmg
                if defender.hp < 0:
                    defender.hp = 0
                self._log(f"{defender.name} took {dmg} damage!")
                self._log(f"{defender.name} HP: {defender.hp}/{defender.max_hp}\n")
                if defender.is_fainted():
                    self._log(f"{defender.name} fainted!")
                    self._log(f"🏆 {attacker.name} wins the battle!\n")
                    self._log("Battle Summary:")
                    self._log(f"- Winner: {attacker.name}")
                    self._log(f"- Turns: {self.turn_count}")
                    self._log(f"- Critical Hits: {self.crit_hits}")
                    return

# Example usage (optional demo)
if __name__ == "__main__":
    pikachu = Pokemon("Pikachu", 100, 55, 40, 90, 
                     [("Thunder Shock", 40), ("Quick Attack", 30), ("Agility", 0), ("Thunder", 70)])
    charmander = Pokemon("Charmander", 90, 52, 43, 65,
                        [("Ember", 35), ("Scratch", 25), ("Growl", 0), ("Flamethrower", 60)])
    manual_choices = [(0, 0), (None, 0), (3, None)]
    battle = Battle(pikachu, charmander)
    battle.start_battle(manual_choices)
