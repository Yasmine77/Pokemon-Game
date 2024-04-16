from enum import Enum
from typing import List, Optional
import random

class MenuChoice(Enum):
    """
    Enumeration representing menu choices.
    """
    CHOOSE_MAIN_POKEMON = "1"
    INITIATE_FIGHT = "2"
    QUIT = "3"

class PokemonType(Enum):
    """
    Enumeration representing Pokemon types.
    """
    FIRE = "Fire"
    GRASS = "Grass"
    WATER = "Water"
    NORMAL = "Normal"
    ELECTRIC = "Electric"

class Pokemon:
    """
    Class representing a Pokemon.

    Attributes:
        name (str): The name of the Pokemon.
        type_ (PokemonType): The type of the Pokemon.
        max_health (int): The maximum health points of the Pokemon.
        current_health (int): The current health points of the Pokemon.
        attack_power (int): The attack power of the Pokemon.
    """
    def __init__(self, name: str, type_: PokemonType, max_health: int, attack_power: int):
        self.name = name
        self.type = type_
        self.max_health = max_health
        self.current_health = max_health
        self.attack_power = attack_power

    def attack(self, enemy: 'Pokemon'):
        """
        Attack the enemy Pokemon.

        Args:
            enemy (Pokemon): The enemy Pokemon to attack.
        """
        damage = self.calculate_damage(enemy)
        enemy.take_damage(damage)
        print(f"{self.name} attacks {enemy.name} and deals {damage} damage.")


    def calculate_damage(self, enemy: 'Pokemon') -> int:
        """
        Calculate the damage dealt to the enemy Pokemon.

        Args:
            enemy (Pokemon): The enemy Pokemon.

        Returns:
            int: The calculated damage.
        """
        effectiveness = {
            PokemonType.GRASS: 2,
            PokemonType.WATER: 0.5,
            PokemonType.FIRE: 0.5,
            PokemonType.NORMAL: 1,
            PokemonType.ELECTRIC: 2,
        }
        damage = random.randint(1, self.attack_power)
        if enemy.type in effectiveness:
            damage *= effectiveness[enemy.type]
        return int(damage)


    def is_alive(self) -> bool:
        """
        Check if the Pokemon is alive.

        Returns:
            bool: True if the Pokemon is alive, False otherwise.
        """
        return self.current_health > 0


    def display_stats(self):
        """
        Display the current health of the Pokemon.
        """
        print(f"{self.name} Health: {self.current_health}/{self.max_health}")


    def take_damage(self, damage: int):
        """
        Reduce the current health of the Pokemon by the specified damage.

        Args:
            damage (int): The amount of damage to take.
        """
        self.current_health = max(0, self.current_health - damage)

class Trainer:
    """
    Class representing a Pokemon Trainer.

    Attributes:
        name (str): The name of the Trainer.
        pokemons (List[Pokemon]): The list of Pokemons owned by the Trainer.
        active_pokemon (Optional[Pokemon]): The currently active Pokemon of the Trainer.
    """
    def __init__(self, name: str, pokemons: List[Pokemon]):
        self.name = name
        self.pokemons = pokemons
        self.active_pokemon = None


    def switch_pokemon(self, pokemon: Pokemon):
        """
        Switch the active Pokemon of the Trainer.

        Args:
            pokemon (Pokemon): The Pokemon to switch to.
        """
        if pokemon in self.pokemons:
            self.active_pokemon = pokemon
            print(f"{self.name} switches to {self.active_pokemon.name}.")
        else:
            print("Invalid Pokemon.")

class Menu:
    """
    Class representing the game menu.

    Methods:
        display_main_menu(): Display the main menu options.
        get_main_menu_choice(): Get the choice from the main menu.
        display_endgame_menu(): Display the endgame menu options.
    """
    @staticmethod
    def display_main_menu() -> None:
        """Display the main menu options."""
        print("\nMain Menu:")
        print("1. Choose Main Pokemon")
        print("2. Initiate Fight")
        print("3. Quit")

    @staticmethod
    def get_main_menu_choice() -> str:
        """Get the choice from the main menu."""
        while True:
            choice = input("Enter the number of your choice: ")
            if choice in [choices.value for choices in MenuChoice]:
                return choice
            else:
                print("Invalid choice. Please choose again.")

    @staticmethod
    def display_endgame_menu() -> str:
        """Display the endgame menu options."""
        print("\nEnd Game Menu:")
        print("1. Restart")
        print("2. Quit")
        while True:
            choice = input("Enter your choice: ")
            if choice in ["1", "2"]:
                return choice
            else:
                print("Invalid choice. Please choose again.")

class PokemonGame:
    """
    Class representing the Pokemon game.

    Attributes:
        pokemons (List[Pokemon]): The list of all Pokemons in the game.
        trainers (List[Trainer]): The list of all Trainers in the game.
    """
    def __init__(self):
        self.pokemons: List[Pokemon] = []
        self.trainers: List[Trainer] = []

    def add_pokemon(self, pokemon: Pokemon):
        """
        Add a Pokemon to the game.
        """
        self.pokemons.append(pokemon)

    def add_trainer(self, trainer: Trainer):
        """
        Add a Trainer to the game.
        """
        self.trainers.append(trainer)

    def run_game(self):
        """
        Run the main game loop.
        """
        menu = Menu()
        running = True
        while running:
            menu.display_main_menu()
            choice = menu.get_main_menu_choice()
            match choice:
                case MenuChoice.CHOOSE_MAIN_POKEMON.value:
                    self.choose_main_pokemon(self.trainers[0])
                case MenuChoice.INITIATE_FIGHT.value:
                    self.initiate_fight(self.trainers[0])
                case MenuChoice.QUIT.value:
                    print("Exiting game...")
                    running = False

    def choose_main_pokemon(self, trainer: Trainer):
        """
        Choose the main Pokemon for the Trainer.
        """
        self.choose_pokemon(trainer, is_main_pokemon=True)

    def initiate_fight(self, trainer: Trainer):
        """
        Initiate a fight between the Trainer's main Pokemon and an opponent.
        """
        if trainer.active_pokemon is None:
            print("You need to choose your main Pokemon first.")
            return
        enemy_pokemon = self.choose_enemy_pokemon(trainer)
        if enemy_pokemon:
            print("Initiating fight...")
            print(f"{trainer.name}'s main Pokemon ({trainer.active_pokemon.name}) is battling {enemy_pokemon.name}.")
            while trainer.active_pokemon.is_alive() and enemy_pokemon.is_alive():
                self.start_battle(trainer.active_pokemon, enemy_pokemon)
                self.start_battle(enemy_pokemon, trainer.active_pokemon)
                trainer.active_pokemon.display_stats()
                enemy_pokemon.display_stats()

                if not trainer.active_pokemon.is_alive():
                    print(f"{trainer.active_pokemon.name} fainted!")
                    self.end_battle(enemy_pokemon, trainer.active_pokemon)
                    return
                elif not enemy_pokemon.is_alive():
                    print(f"{enemy_pokemon.name} fainted!")
                    self.end_battle(trainer.active_pokemon, enemy_pokemon)
                    return
                else:
                    print("Do you want to switch your Pokemon? (yes/no):")
                    switch_choice = input().lower()
                    if switch_choice == "yes":
                        self.switch_pokemon_during_battle(trainer)
                    elif switch_choice == "no" or switch_choice == "":
                        pass
                    else:
                        print("Invalid choice. Please choose 'yes' or 'no'.")

            self.end_battle(trainer.active_pokemon, enemy_pokemon)

    def start_battle(self, pokemon1: Pokemon, pokemon2: Pokemon):
        """
        Start a battle between two Pokemons.
        """
        damage = pokemon1.calculate_damage(pokemon2)
        pokemon2.take_damage(damage)
        print(f"{pokemon1.name} attacks {pokemon2.name} and deals {damage} damage.")

    def end_battle(self, player_pokemon: Pokemon, enemy_pokemon: Pokemon):
        """
        End the battle and display the result.
        """
        print("Battle is over \U0001F480")
        if player_pokemon.is_alive():
            print(f"{player_pokemon.name} wins!")
        else:
            print(f"{enemy_pokemon.name} wins!")
        endgame_choice = Menu.display_endgame_menu()
        if endgame_choice == "1":
            self.restart_game()
        elif endgame_choice == "2":
            print("Exiting game...")
            return
        else:
            print("No opponent to fight.")

    def switch_pokemon_during_battle(self, trainer: Trainer):
        """
        Switch the active Pokemon during a battle.
        """
        self.choose_pokemon(trainer)

    def choose_pokemon(self, trainer: Trainer, is_main_pokemon: bool = False):
        """
        Choose a Pokemon for the Trainer.

        Args:
            trainer (Trainer): The Trainer choosing a Pokemon.
            is_main_pokemon (bool): Indicates whether the choice is for the main Pokemon or during battle.
        """
        action = "choose" if is_main_pokemon else "switch to"
        print(f"{trainer.name}, {action} your {'main ' if is_main_pokemon else 'active '}Pokemon:")
        for i, pokemon_info in enumerate(self.list_pokemons(trainer), start=1):
            print(f"{i}. {pokemon_info}")
        while True:
            try:
                choice = int(input("Enter the number of your choice: ")) - 1
                if 0 <= choice < len(trainer.pokemons):
                    if is_main_pokemon:
                        trainer.active_pokemon = trainer.pokemons[choice]
                        print(f"{trainer.name} chose {trainer.active_pokemon.name} as the main Pokemon.")
                    else:
                        trainer.active_pokemon = trainer.pokemons[choice]
                        print(f"{trainer.name} switches to {trainer.active_pokemon.name}.")
                    break
                else:
                    print("Invalid Pokemon choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def list_pokemons(self, trainer: Trainer) -> List[str]:
        """
        List all Pokemons owned by the Trainer.
        """
        return [f"{pokemon.name} (Type: {pokemon.type.value}, Health: {pokemon.current_health}/{pokemon.max_health})"
                for pokemon in trainer.pokemons]

    def choose_enemy_pokemon(self, trainer: Trainer) -> Optional[Pokemon]:
        """
        Chooses a random enemy Pokemon for the Trainer to battle.

        Args:
            trainer (Trainer): The Trainer choosing an enemy Pokemon.

        Returns:
            Optional[Pokemon]: The chosen enemy Pokemon, or None if no suitable
            enemy Pokemon is available.
        """
        if trainer.active_pokemon:
            main_pokemon_type = trainer.active_pokemon.type
            available_enemy_pokemons = [pokemon for pokemon in self.pokemons
                                        if pokemon.type != main_pokemon_type and pokemon not in trainer.pokemons]
            if available_enemy_pokemons:
                enemy_pokemon = random.choice(available_enemy_pokemons)
                print(f"Opponent chose {enemy_pokemon.name} as their Pokémon.")
                return enemy_pokemon
            else:
                return print("No available enemy Pokémon.")
        else:
            return None

    def restart_game(self):
        """
        Restart the game.
        """
        self.enemy_pokemon = None
        self.trainers[0].active_pokemon = None
        for pokemon in self.pokemons:
            pokemon.current_health = pokemon.max_health

if __name__ == "__main__":
    
    # Create some Pokemon and a Trainer
    pokemon1 = Pokemon("Charmander", PokemonType.FIRE, max_health=50, attack_power=10)
    pokemon2 = Pokemon("Bulbasaur", PokemonType.GRASS, max_health=60, attack_power=8)
    pokemon3 = Pokemon("Squirtle", PokemonType.WATER, max_health=55, attack_power=9)
    pokemon4 = Pokemon("Pikachu", PokemonType.ELECTRIC, max_health=45, attack_power=12)
    pokemon5 = Pokemon("Rattata", PokemonType.NORMAL, max_health=40, attack_power=7)

    trainer1 = Trainer("trainer1", [pokemon1, pokemon2, pokemon3])

    # Create the game and add Pokemons and Trainer
    game = PokemonGame()
    game.add_pokemon(pokemon1)
    game.add_pokemon(pokemon2)
    game.add_pokemon(pokemon3)
    game.add_pokemon(pokemon4)
    game.add_pokemon(pokemon5)
    game.add_trainer(trainer1)

    # Run the game
    game.run_game()
