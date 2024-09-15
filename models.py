# models.py

class Character:
    def __init__(self, name, health, stamina, energy):
        self.name = name
        self.health = health
        self.stamina = stamina
        self.energy = energy
        self.skills = []

    def add_skill(self, skill):
        self.skills.append(skill)

    def use_skill(self, skill_name):
        skill = next((s for s in self.skills if s.name == skill_name), None)
        if skill and self.energy >= skill.energy_cost and self.stamina >= skill.stamina_cost:
            self.energy -= skill.energy_cost
            self.stamina -= skill.stamina_cost
            return skill
        return None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            return f"{self.name} вырублен!"
        return f"{self.name} получил {damage} урона!"


class Skill:
    def __init__(self, name, damage, energy_cost, stamina_cost):
        self.name = name
        self.damage = damage
        self.energy_cost = energy_cost
        self.stamina_cost = stamina_cost


class Battle:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def exchange_turn(self, player1_skill, player2_skill):
        p1_action = self.player1.use_skill(player1_skill)
        p2_action = self.player2.use_skill(player2_skill)

        result_p2 = self.player2.take_damage(p1_action.damage) if p1_action else f"{self.player1.name} не смог использовать {player1_skill}"
        result_p1 = self.player1.take_damage(p2_action.damage) if p2_action else f"{self.player2.name} не смог использовать {player2_skill}"

        return result_p1, result_p2

    def is_battle_over(self):
        if self.player1.health == 0:
            return f"{self.player2.name} победил!"
        elif self.player2.health == 0:
            return f"{self.player1.name} победил!"
        return None
