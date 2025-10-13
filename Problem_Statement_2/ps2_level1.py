class Pokemon:
    def __init__(self, name, hp, attack, defense, speed, moves):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.attack_stat = attack
        self.defense_stat = defense
        self.speed_stat = speed
        self.moves = moves  # list of tuples (move_name, power)

    def display_stats(self):
        move_list = ", ".join([f"{m[0]} ({m[1]})" for m in self.moves])
        return (f"{self.name} - HP: {self.current_hp}/{self.max_hp}, "
                f"Attack: {self.attack_stat}, Defense: {self.defense_stat}, Speed: {self.speed_stat}\n"
                f"Moves: {move_list}\n")

    def attack(self, other, move_index):
        move_name, move_power = self.moves[move_index]
        print(f"{self.name} used {move_name}!")

        # If move has 0 power, it’s a non-damaging move (like Growl, Agility)
        if move_power == 0:
            print(f"But it had no effect!\n")
            return

        # Damage formula (simple version)
        damage = max(1, (self.attack_stat * move_power) // (other.defense_stat + 1))
        other.take_damage(damage)
        print(f"{other.name} took {damage} damage!\n")

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp <= 0
