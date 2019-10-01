import random

def user_input(prompt):
    user_input = input(prompt)
    return user_input

class Ability:
    def __init__(self, name, max_damage):
        self.name = name
        self.max_damage = max_damage

    def attack(self):
        self.attack_strength = random.randint(0, int(self.max_damage))
        return self.attack_strength

class Weapon(Ability):
    def attack(self):
        self.attack_strength = random.randint(int(self.max_damage)//2, int(self.max_damage))
        return self.attack_strength

class Armor:
    def __init__(self, name, max_block):
        self.name = name
        self.max_block = max_block

    def block(self):
        self.block_strength = random.randint(0, int(self.max_block))
        return self.block_strength

class Hero:
    def __init__(self, name, starting_health=100, abilities = list(), armors = list()):
        self.name = name
        self.starting_health = starting_health
        self.current_health = starting_health
        self.abilities = list()
        self.armors = list()
        self.deaths = 0
        self.kills = 0

    def add_ability(self, ability):
        self.abilities.append(ability)

    def add_weapon(self, weapon):
        self.abilities.append(weapon)

    def attack(self):
        return sum(ability.attack() for ability in self.abilities)

    def add_armor(self, armor):
        self.armors.append(armor)

    def defend(self):
        return sum(armor.block() for armor in self.armors)

    def take_damage(self, damage):
        self.current_health = self.current_health - (damage - self.defend())
        if self.current_health > 100:
            self.current_health = 100
        else:
            return self.current_health

    def is_alive(self):
        if self.current_health > 0:
            return True
        else:
            return False

    def add_death(self, num_deaths):
        self.num_deaths = num_deaths
        self.deaths = self.deaths + num_deaths

    def add_kill(self, num_kills):
        self.num_kills = num_kills
        self.kills = self.kills + num_kills

    def fight(self, opponent):
        if self.abilities == [] and opponent.abilities == []:
            print("Draw!")
        else:
            fighting = True
            while fighting:
                self.attack()
                opponent.defend()
                opponent.take_damage(self.attack())
                opponent.is_alive()
                if opponent.is_alive() == False:
                    opponent.add_death(1)
                    self.add_kill(1)
                    print(self.name + " won!")
                    break
                opponent.attack()
                self.defend()
                self.take_damage(opponent.attack())
                self.is_alive()
                if self.is_alive() == False:
                    self.add_death(1)
                    opponent.add_kill(1)
                    print(opponent.name + " won!")
                    break

class Team:
    def __init__(self, name, heroes = list()):
        self.name = name
        self.heroes = list()

    def add_hero(self, hero):
        self.hero = hero
        self.heroes.append(hero)

    def remove_hero(self, name):
        self.name = name
        for name in self.heroes:
            self.heroes.remove(name)
        if name not in self.heroes:
            return 0

    def view_all_heroes(self):
        index = 0
        for hero in self.heroes:
            print(hero.name)
            index += 1

    def attack(self, other_team):
        self.other_team = other_team
        fighting = True
        while fighting:
            self.living_heroes = [hero for hero in self.heroes if hero.is_alive() == True]
            other_team.living_heroes = [hero for hero in other_team.heroes if hero.is_alive() == True]
            if self.living_heroes and other_team.living_heroes != []:
                hero = random.choice(self.living_heroes)
                opponent = random.choice(other_team.living_heroes)
                hero.fight(opponent)
            if self.living_heroes == []:
                return other_team.name
                break
            if other_team.living_heroes == []:
                return self.name
                break

    def revive_heroes(self, health=100):
        self.health = health
        for hero in self.heroes:
            hero.current_health = health

    def stats(self):
        print("""----
        Team """ + self.name)
        #ave kill/death ratio
        ave_kills = sum(hero.kills for hero in self.heroes)//len(self.heroes)
        ave_deaths = sum(hero.deaths for hero in self.heroes)//len(self.heroes)
        print("Team kill/death ratio: " + str(ave_kills) + "/" + str(ave_deaths))
        for hero in self.heroes:
            if hero.current_health > 0:
                print(hero.name + " (alive) " + " - " + str(hero.kills) + " kills, " + str(hero.deaths) + " deaths, current health of " + str(hero.current_health))
            else:
                print(hero.name + " (dead)" + " - " + str(hero.kills) + " kills, " + str(hero.deaths) + " deaths, current health of " + str(hero.current_health))

class Arena:
    def __init__(self):
        team_one_name = user_input("Name team one: ")
        self.team_one_name = team_one_name
        team_two_name = user_input("Name team two: ")
        self.team_two_name = team_two_name
        self.team_one = Team(self.team_one_name)
        self.team_two = Team(self.team_two_name)
        print("You've created team one, " + self.team_one.name + " and team two, " + self.team_two.name)

    def create_ability(self):
        ability = user_input("Choose ability name: ")
        max_damage = user_input("Choose " + ability + " max damage: ")
        ability = Ability(ability, max_damage)
        print(str(ability.name) + " created with a max damage of " + ability.max_damage)
        return ability

    def create_weapon(self):
        weapon = user_input("Choose weapon name: ")
        max_damage = user_input("Choose " + weapon + " max damage: ")
        weapon = Weapon(weapon, max_damage)
        print(str(weapon.name) + " created with a max damage of " + weapon.max_damage)
        return weapon

    def create_armor(self):
        armor = user_input("Choose armor name: ")
        max_block = user_input("Choose " + armor + " max block strength: ")
        armor = Armor(armor, max_block)
        print(str(armor.name) + " created with a max block strength of " + armor.max_block)
        return armor

    def create_hero(self):
        new_hero = user_input("Choose hero name: ")
        new_hero = Hero(new_hero)
        self.new_hero = new_hero
        add_ability = user_input("Give " + new_hero.name + " new ability? Y/N >")
        while add_ability.lower() == "y":
            ability = self.create_ability()
            new_hero.add_ability(ability)
            add_ability = user_input("Give " + new_hero.name + " new ability? Y/N >")
        add_weapon = user_input("Give " + new_hero.name + " new weapons? Y/N >")
        while add_weapon.lower() == "y":
            weapon = self.create_weapon()
            new_hero.add_weapon(weapon)
            add_weapon = user_input("Give " + new_hero.name + " new weapons? Y/N >")
        add_armor = user_input("Give " + new_hero.name + " new armor? Y/N >")
        while add_armor.lower() == "y":
            armor = self.create_armor()
            new_hero.add_armor(armor)
            add_armor = user_input("Give " + new_hero.name + " new armor? Y/N >")
        print("You've created " + new_hero.name)
        if new_hero.abilities != []:
            print("Abilities/Weapons:")
            index = 0
            for ability in new_hero.abilities:
                print(ability.name)
                index += 1
        else:
            print("No Abilities")
        if new_hero.armors != []:
            print("Armors:")
            index = 0
            for armor in new_hero.armors:
                print(armor.name)
                index += 1
        else:
            print("No Armors")
        return new_hero

    def build_team_one(self):
        num_heroes = int(user_input("How many heroes on " + self.team_one.name + "? "))
        self.num_heroes = num_heroes
        for _ in range(num_heroes):
            new_hero = self.create_hero()
            self.team_one.add_hero(new_hero)
        return self.team_one

    def build_team_two(self):
        num_heroes = user_input("How many heroes on " + self.team_two.name + "? ")
        self.num_heroes = num_heroes
        for _ in range(int(num_heroes)):
            new_hero = self.create_hero()
            self.team_two.add_hero(new_hero)
        return self.team_two

    def team_battle(self):
        self.winning_team = self.team_one.attack(self.team_two)

    def show_stats(self):
        print("""----
        Team """ + self.winning_team + """ won!
        """)
        self.team_one.stats()
        self.team_two.stats()
        # including each team's average kill/death ratio.
        # Required Stats:
        #     Show both teams average kill/death ratio.
        #     Show surviving heroes


if __name__ == "__main__":
    game_is_running = True

    arena = Arena()

    arena.build_team_one()
    arena.build_team_two()

    while game_is_running:

        arena.team_battle()
        arena.show_stats()
        play_again = input("Battle teams again? Y/N ")

        if play_again.lower() == "n":
            game_is_running = False
        else:
            arena.team_one.revive_heroes()
            arena.team_two.revive_heroes()


#Tests

# ability = Ability("Debugging Ability", 50)
# ability2 = Ability("Debugging Ability 2", 50)
# # print(ability.name)
# # print(ability.attack())
# # print(ability2.name)
# # print(ability2.attack())
# armor = Armor("Debugging Armor", 10)
# armor2 = Armor("Debugging Armor 2", 10)
# # print(armor.name)
# # print(armor.block())
# # print(armor2.name)
# # print(armor2.block())
# hero = Hero("Debugging Hero")
# hero2 = Hero("Debugging Hero 2")
# # print(hero.starting_health)
# # print(hero2.name)
# # print(hero2.starting_health)
# # print(hero.name)
# hero.add_ability(ability)
# hero2.add_ability(ability2)
# # print(hero2.abilities)
# # print(hero.abilities)
# hero.add_armor(armor)
# hero2.add_armor(armor2)
# # print(hero.armors)
# # print(hero.current_health)
# # print(hero2.armors)
# # print(hero2.current_health)
# # print(hero2.attack())
# # print(hero.attack())
# # print(hero2.defend())
# # # print(hero2.current_health)
# # hero2.take_damage(hero.attack())
# # print(hero2.current_health)
# # print(hero2.is_alive())
# # print(hero.current_health)
# # print(hero.is_alive())
# hero.fight(hero2)

# hero1 = Hero("Wonder Woman")
# hero2 = Hero("Dumbledore")
# hero3 = Hero("Test Hero 1")
# hero4 = Hero("Test Hero 2")
# ability1 = Ability("Super Speed", 300)
# ability2 = Ability("Super Eyes", 130)
# ability3 = Ability("Wizard Wand", 80)
# ability4 = Ability("Wizard Beard", 20)
# armor1 = Armor("Petronum", 350)
# armor2 = Armor("Tortilla Chips", 50)
# armor3 = Armor("Frog", 100)
# hero1.add_ability(ability1)
# hero2.add_ability(ability2)
# hero2.add_ability(ability4)
# hero3.add_ability(ability3)
# hero4.add_ability(ability4)
# hero2.add_armor(armor1)
# hero2.add_armor(armor3)
# hero3.add_armor(armor2)
# team1 = Team("Test Team 1")
# team2 = Team("Test Team 2")
# team1.add_hero(hero1)
# team1.add_hero(hero2)
# team2.add_hero(hero3)
# team2.add_hero(hero4)
# team1.attack(team2)
# team1.stats()
# team2.stats()
# team1.revive_heroes()
# team2.revive_heroes()
# team1.stats()
# team2.stats()

# arena = Arena()
# arena.build_team_one()
# arena.build_team_two()
# arena.team_battle()
# arena.show_stats()
